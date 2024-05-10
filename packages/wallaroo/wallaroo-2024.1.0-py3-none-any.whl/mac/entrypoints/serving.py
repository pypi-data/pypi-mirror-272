"""This module features entrypoints for serving a PythonStep using a Service."""

import logging
from pathlib import Path
from typing import Callable, Dict

from pydata_util.nats import NATSMessage

from mac.config.python_step import (
    AutoInferenceConfig,
    CustomStepConfig,
)
from mac.config.service import ServerConfig, ServiceConfig
from mac.config.service.creation import ServiceConfigFactory
from mac.inference.creation import InferenceBuilder
from mac.io.custom_step_loaders import load_custom_inference, load_custom_step
from mac.service.creation import ServiceFactory
from mac.types import (
    PythonStep,
    SupportedFrameworks,
    SupportedServices,
)

logger = logging.getLogger(__name__)

CUSTOM_STEP_LOADERS: Dict[
    SupportedFrameworks, Callable[[CustomStepConfig], PythonStep]
] = {
    SupportedFrameworks.CUSTOM: load_custom_inference,
    SupportedFrameworks.PYTHON: load_custom_step,
}


def create_auto_inference_config(
    nats_message: NATSMessage,
) -> AutoInferenceConfig:
    """Creates an AutoInferenceConfig from a given NATSMessage.

    :param nats_message: A NATSMessage instance.

    :raises pydantic.ValidationError: If AutoInferenceConfig is invalid,
    then a ValidationError is raised.

    :return: An AutoInferenceConfig instance.
    """
    return AutoInferenceConfig(
        framework=nats_message.model_framework, model_path=nats_message.model_file_name
    )


def create_custom_step_config(nats_message: NATSMessage) -> CustomStepConfig:
    """Creates an CustomStepConfig from a given NATSMessage.

    :param nats_message: A NATSMessage instance.

    :raises pydantic.ValidationError: If CustomStepConfig is invalid,
    then a ValidationError is raised.

    :return: An CustomStepConfig instance.
    """
    return CustomStepConfig(
        framework=nats_message.model_framework,
        model_path=nats_message.model_file_name,
        modules_to_include=set([Path("*.py")]),
    )


def serve_auto_inference_from_nats_message(
    nats_message: NATSMessage,
    inference_builder: InferenceBuilder,
    inference_config_creator: Callable[
        [NATSMessage], AutoInferenceConfig
    ] = create_auto_inference_config,
    service_type: SupportedServices = SupportedServices.FLIGHT,
    host: str = "0.0.0.0",
    port: int = 8080,
) -> None:
    """Entrypoint for serving a PythonStep associated with an auto
    Inference from a given NATSMessage.

    :param nats_message: A NATSMessage instance.
    :param inference_builder: An InferenceBuilder instance.
    :param service_type: The Service to be used for serving the auto Inference.
    :param host: The service host.
    :param port: The service port.

    Example of the config file:

    {
            "id": "uuid",
            "metadata": {
                "name": "model_name",
                "visibility": "string",
                "workspace_id": 1234,
                "conversion": {
                    "python_version": "3.8",
                    "framework": "keras",
                    "requirements": [],
                },
                "file_info": {
                    "version": "uuid",
                    "sha": "0000000000000000...",
                    "file_name": "model_file.h5"
                }
            }
        }
    """
    logger.info(
        f"Serving auto Inference with `{service_type.value}` from `NATSMessage`..."
    )

    auto_inference_config = inference_config_creator(nats_message)
    auto_inference = inference_builder.create(auto_inference_config)
    service_config = ServiceConfigFactory().create(
        service_type.value,
        python_step=auto_inference_config,
        server=ServerConfig(host=host, port=port),
    )

    serve_python_step(
        service_config=service_config,
        python_step=auto_inference.predict,
    )

    logger.info("Serving successful.")


def serve_custom_step_from_nats_message(
    nats_message: NATSMessage,
    service_type: SupportedServices = SupportedServices.FLIGHT,
    host: str = "0.0.0.0",
    port: int = 8080,
) -> None:
    """Entrypoint for serving a custom PythonStep (i.e. a custom Inference or
    a pre/post-processing step) from a given NATSMessage.

    :param nats_message: A NATSMessage instance.
    :param service_type: The Service to be used for serving the auto Inference.
    :param host: The service host.
    :param port: The service port.
    """
    logger.info(
        f"Serving custom PythonStep with {service_type.value} from `NATSMessage`..."
    )

    custom_step_config = create_custom_step_config(nats_message=nats_message)
    service_config = ServiceConfigFactory().create(
        service_type.value,
        python_step=custom_step_config,
        server=ServerConfig(host=host, port=port),
    )
    python_step = _get_custom_step_loader(nats_message.model_framework)(
        custom_step_config
    )

    serve_python_step(
        service_config=service_config,
        python_step=python_step,
    )

    logger.info("Serving successful.")


def serve_python_step(
    service_config: ServiceConfig,
    python_step: PythonStep,
) -> None:
    """Serve a PythonStep given a ServiceConfig.

    :param service_config: An ServiceConfig instance.
    :param python_step: A PythonStep instance.
    """
    service = ServiceFactory().create(
        service_config.service_type.value,
        config=service_config,
        python_step=python_step,
    )
    service.serve()


def _get_custom_step_loader(
    framework: SupportedFrameworks,
) -> Callable[[CustomStepConfig], PythonStep]:
    """Returns the custom PythonStep loader for the given framework.

    :param framework: The framework to get the custom PythonStep loader for.

    :raises ValueError: If the framework is not supported.

    :return: The custom step loader for the given framework.
    """
    try:
        return CUSTOM_STEP_LOADERS[framework]
    except KeyError:
        raise ValueError(f"Unsupported framework: {framework}")
