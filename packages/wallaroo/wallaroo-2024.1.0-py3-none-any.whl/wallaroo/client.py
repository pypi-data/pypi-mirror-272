import base64
from http import HTTPStatus
import json
import math
import os
import pathlib
import posixpath
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from itertools import chain, repeat
from typing import Any, Dict, List, NewType, Optional, Tuple, Union, cast
from urllib.parse import quote_plus

import dateutil
import gql
import httpx  # type: ignore
import numpy as np
import pandas as pd
import pyarrow as pa  # type: ignore
import requests
from gql.transport.requests import RequestsHTTPTransport
from requests_toolbelt import MultipartEncoder
from wallaroo.assays_v2 import AssayResultsList, AssayV2, AssayV2List, Summarizer
from wallaroo.model_registry import ModelRegistriesList, ModelRegistry

from wallaroo.model import Model, ModelList
from wallaroo.unwrap import unwrap
from wallaroo.wallaroo_ml_ops_api_client.models.data_origin import DataOrigin
from wallaroo.assays_v2 import SummaryBaseline, Targeting
from wallaroo.wallaroo_ml_ops_api_client.models.data_path import DataPath
from wallaroo.wallaroo_ml_ops_api_client.models.interval_unit import IntervalUnit
from wallaroo.wallaroo_ml_ops_api_client.models.run_frequency_type_0 import (
    RunFrequencyType0,
)
from wallaroo.wallaroo_ml_ops_api_client.models.run_frequency_type_1 import (
    RunFrequencyType1,
)

from . import auth
from .assay import Assay, AssayAnalysis, AssayAnalysisList, Assays
from .assay_config import (
    AssayBuilder,
    AssayConfig,
    UnivariateContinousSummarizerConfig,
    CalculatedBaseline as V1CalculatedBaseline,
    FixedBaseline as V1FixedBaseline,
    StaticBaseline as V1StaticBaseline,
    ensure_tz,
)
from .checks import require_dns_compliance
from .datasizeunit import DataSizeUnit
from .deployment import Deployment
from .engine_config import Acceleration, Architecture, InvalidAccelerationError
from .framework import Framework
from .inference_decode import inference_logs_to_dataframe, nested_df_to_flattened_df
from .logs import LogEntries, LogEntry
from .model_version import ModelVersion, ModelVersionList
from .model_config import ModelConfig
from .object import (
    EntityNotFoundError,
    ModelConversionError,
    ModelConversionTimeoutError,
    ModelUploadError,
)
from .orchestration import Orchestration
from .pipeline import Pipeline, Pipelines
from .pipeline_config import PipelineConfig
from .pipeline_version import PipelineVersion, PipelineVersionList
from .tag import Tag, Tags
from .task import Task
from .user import User
from .utils import (
    create_new_file,
    is_arrow_enabled,
    is_models_enabled,
    write_to_file,
    is_assays_v2_enabled,
)
from .version import _user_agent
from .visibility import _Visibility
from .wallaroo_ml_ops_api_client.api.assay import (
    assays_create,
    assays_get_assay_results,
    assays_list,
    assays_set_active,
)
from .wallaroo_ml_ops_api_client.api.model import models_list
from .wallaroo_ml_ops_api_client.api.pipelines import pipelines_create
from .wallaroo_ml_ops_api_client.api.workspace import workspaces_list
from .wallaroo_ml_ops_api_client.client import (
    AuthenticatedClient as MLOpsClient,
)
from .wallaroo_ml_ops_api_client.models import (
    assays_get_assay_results_body,
    models_list_body,
    pipelines_create_body,
    pipelines_create_body_definition_type_0,
    workspaces_list_body,
    AssaysSetActiveBody,
    AssaysSetActiveResponse200,
)
from .wallaroo_ml_ops_api_client.models.assays_create_body import (
    AssaysCreateBody,
)
from .wallaroo_ml_ops_api_client.models.assays_create_response_200 import (
    AssaysCreateResponse200,
)
from .wallaroo_ml_ops_api_client.models.assays_get_assay_results_response_200_item import (
    AssaysGetAssayResultsResponse200Item,
)
from .wallaroo_ml_ops_api_client.models.assays_list_body import AssaysListBody
from .wallaroo_ml_ops_api_client.models.models_list_response_200 import (
    ModelsListResponse200,
)
from .wallaroo_ml_ops_api_client.models.pipelines_create_response_200 import (
    PipelinesCreateResponse200,
)
from .wallaroo_ml_ops_api_client.models.workspaces_list_response_200 import (
    WorkspacesListResponse200,
)
from .wallaroo_ml_ops_api_client.types import UNSET
from .workspace import Workspace, Workspaces
from .connection import Connection, ConnectionList
from .wallaroo_ml_ops_api_client.api.pipelines.remove_edge import (
    RemoveEdgeBody,
    sync_detailed as removeEdgeSync,
)
from .wallaroo_ml_ops_api_client.api.assays.schedule import (
    sync_detailed as sync,
    ScheduleBody,
)
from .wallaroo_ml_ops_api_client.models.scheduling import Scheduling
from .wallaroo_ml_ops_api_client.models.rolling_window import RollingWindow
from .wallaroo_ml_ops_api_client.models.baseline_type_0 import (
    BaselineType0 as V2SummaryBaseline,
)
from .wallaroo_ml_ops_api_client.models.baseline_type_1 import (
    BaselineType1 as V2StaticBaseline,
)
from .wallaroo_ml_ops_api_client.models.summarizer_type_0 import (
    SummarizerType0,
)
from .wallaroo_ml_ops_api_client.models.univariate_continuous import (
    UnivariateContinuous,
)
from .wallaroo_ml_ops_api_client.models.aggregation import Aggregation
from .wallaroo_ml_ops_api_client.models.bin_mode_type_0 import BinModeType0
from .wallaroo_ml_ops_api_client.models.bin_mode_type_1 import BinModeType1
from .wallaroo_ml_ops_api_client.models.metric import Metric
from .wallaroo_ml_ops_api_client.models.data_path import DataPath
from .wallaroo_ml_ops_api_client.models.run_frequency_type_1 import (
    RunFrequencyType1 as MLOpsSimpleRunFrequency,
)
from .wallaroo_ml_ops_api_client.models.pg_interval import PGInterval
from .wallaroo_ml_ops_api_client.models.window_width_duration import (
    WindowWidthDuration,
)
from .wallaroo_ml_ops_api_client.models.data_origin import DataOrigin


Datetime = NewType("Datetime", datetime)

WALLAROO_SDK_AUTH_TYPE = "WALLAROO_SDK_AUTH_TYPE"
WALLAROO_SDK_AUTH_ENDPOINT = "WALLAROO_SDK_AUTH_ENDPOINT"
WALLAROO_URL = "WALLAROO_URL"
WALLAROO_AUTH_URL = "WALLAROO_AUTH_URL"

ARROW_CONTENT_TYPE = "application/vnd.apache.arrow.file"
JSON_CONTENT_TYPE = "application/json"
OCTET_STREAM_CONTENT_TYPE = "application/octet-stream"

UPLOAD_MODEL_STREAM_SUPPORTED_FLAVORS = [
    Framework.ONNX,
    Framework.TENSORFLOW,
]
DEFAULT_MODEL_CONVERSION_TIMEOUT = 60 * 10  # 10 minutes
DEFAULT_MODEL_CONVERSION_PYTHON_VERSION = "3.8"

DEFAULT_RECORDS_LIMIT = 100
DEFAULT_RECORDS_BY_TIME_LIMIT = 1_000_000
DEFAULT_MAX_DATA_SIZE = 100  # type: float
DEFAULT_MAX_DATA_UNIT = DataSizeUnit.MiB


class Client(object):
    """Client handle to a Wallaroo platform instance.

    Objects of this class serve as the entrypoint to Wallaroo platform
    functionality.
    """

    @staticmethod
    def get_urls(
        auth_type: Optional[str] = None,
        api_endpoint: Optional[str] = None,
        auth_endpoint: Optional[str] = None,
    ) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """Method to calculate the auth values specified as defaults,
        as params or in ENV vars.
        Made static to be testable without reaching out to SSO, etc."""

        # If this is set, we are running in a pipeline orchestration deployment, meaning: we
        # override auth type because no other auth type provided in user code will work. Also, this
        # lets the user write a plain notebook and that does wallaroo.Client(auth_type=WHATEVER)
        # and upload it as an orchestration, and we will handle it silently.

        if os.getenv("WALLAROO_TASK_ID"):
            auth_type = "orch"

        elif auth_type is None:
            auth_type = os.environ.get(WALLAROO_SDK_AUTH_TYPE, None)

        if auth_endpoint is None or len(auth_endpoint.strip()) == 0:
            auth_endpoint = os.environ.get(WALLAROO_AUTH_URL, None) or os.environ.get(
                WALLAROO_SDK_AUTH_ENDPOINT, None
            )
        if api_endpoint is None or len(api_endpoint.strip()) == 0:
            api_endpoint = os.environ.get(WALLAROO_URL, None)

        if any(x is None for x in [auth_type, api_endpoint, auth_endpoint]):
            raise ValueError(
                f"auth_type, auth_endpoint, and api_endpoint must be provided or set in environment as \n"
                f"`WALLAROO_SDK_AUTH_TYPE`, `WALLAROO_AUTH_URL`, and `WALLAROO_URL` respectively.\n"
            )
        return auth_type, api_endpoint, auth_endpoint

    def __init__(
        self,
        api_endpoint: Optional[str] = None,
        auth_endpoint: Optional[str] = None,
        request_timeout: Optional[int] = None,
        auth_type: Optional[str] = None,
        gql_client: Optional[gql.Client] = None,
        interactive: Optional[bool] = None,
        time_format: str = "%Y-%d-%b %H:%M:%S",
    ):
        """Create a Client handle.

        :param Optional[str] api_endpoint: Host/port of the platform API endpoint. If not provided, the value of the `WALLAROO_URL` environment variable will be used.
        :param Optional[str] auth_endpoint: Host/port of the platform Keycloak instance. If not provided, the value of the `WALLAROO_AUTH_URL` environment variable will be used.
        :param Optional[int] request_timeout: Max timeout of web requests, in seconds
        :param Optional[str] auth_type: Authentication type to use. Can be one of: "none",
            "sso", "user_password".
        :param Optional[bool] interactive: If provided and True, some calls will print additional human information, or won't when False. If not provided, interactive defaults to True if running inside Jupyter and False otherwise.
        :param str time_format: Preferred `strftime` format string for displaying timestamps in a human context.
        """

        auth_type, api_endpoint, auth_endpoint = Client.get_urls(
            auth_type, api_endpoint, auth_endpoint
        )
        # no way these are none at this point, just making mypy happy
        assert auth_type is not None
        assert auth_endpoint is not None
        assert api_endpoint is not None

        self.auth = auth.create(auth_endpoint, auth_type)

        if request_timeout is None:
            request_timeout = int(os.getenv("WALLAROO_REQUEST_TIMEOUT", 45))

        if gql_client:
            self._gql_client = gql_client
        else:
            gql_transport = RequestsHTTPTransport(
                url=posixpath.join(api_endpoint, "v1/graphql"),
                auth=self.auth,
                timeout=request_timeout,
            )
            self._gql_client = gql.Client(
                transport=gql_transport, fetch_schema_from_transport=True
            )

        self.api_endpoint = api_endpoint

        self.auth_endpoint = auth_endpoint

        self.timeout = request_timeout

        self._setup_mlops_client()

        self._current_workspace: Optional[Workspace] = None

        # TODO: debate the names of these things
        self._default_ws_name: Optional[str] = None

        user_email = self.auth.user_email()
        if user_email is not None:
            self._default_ws_name = user_email + "_ws"

        if interactive is not None:
            self._interactive = interactive
        elif (
            "JUPYTER_SVC_SERVICE_HOST" in os.environ or "JUPYTERHUB_HOST" in os.environ
        ):
            self._interactive = True
        else:
            self._interactive = False

        self._time_format = time_format

        self._in_task = "WALLAROO_TASK_ID" in os.environ
        self._task_args_filename = "/home/jovyan/arguments.json"

    def _get_rest_api(self, path: str, params: dict):
        headers = {
            "authorization": self.auth._bearer_token_str(),
            "user-agent": _user_agent,
        }

        url = f"{self.api_endpoint}/{path}"

        return requests.get(url, headers=headers, params=params)

    def _post_rest_api(self, path: str, body: dict):
        headers = {
            "authorization": self.auth._bearer_token_str(),
            "user-agent": _user_agent,
        }

        url = f"{self.api_endpoint}/{path}"
        return requests.post(url, headers=headers, json=body)

    def list_tags(self) -> Tags:
        """List all tags on the platform.

        :return: A list of all tags on the platform.
        :rtype: List[Tag]
        """
        res = self._gql_client.execute(
            gql.gql(
                """
            query ListTags {
              tag(order_by: {id: desc}) {
                id
                tag
                model_tags {
                  model {
                    id
                    model_id
                    models_pk_id
                    model_version

                  }
                }
                pipeline_tags {
                  pipeline {
                    id
                    pipeline_id
                    pipeline_versions {
                        id
                        version
                    }
                  }
                }
              }
            }


            """
            )
        )
        return Tags([Tag(client=self, data={"id": p["id"]}) for p in res["tag"]])

    def list_models(self) -> ModelList:
        """List all models on the platform.

        :return: A list of all models on the platform.
        :rtype: List[ModelVersion]
        """
        id = self.get_current_workspace().id()
        res = models_list.sync(
            client=self.mlops(),
            body=models_list_body.ModelsListBody(id),
        )

        if res is None:
            raise Exception("Failed to list models")

        if not isinstance(res, ModelsListResponse200):
            raise Exception(res.msg)

        return ModelList([Model(client=self, data=v.to_dict()) for v in res.models])

    def list_deployments(self) -> List[Deployment]:
        """List all deployments (active or not) on the platform.

        :return: A list of all deployments on the platform.
        :rtype: List[Deployment]
        """
        res = self._gql_client.execute(
            gql.gql(
                """
            query ListDeployments {
              deployment {
                id
                deploy_id
                deployed
                deployment_model_configs {
                  model_config {
                    id
                  }
                }
              }
            }
            """
            )
        )
        return [Deployment(client=self, data=d) for d in res["deployment"]]

    """
        # Removed until we figure out what pipeline ownership means
        #
        # def search_my_pipelines(
        #     self,
        #     search_term: Optional[str] = None,
        #     deployed: Optional[bool] = None,
        #     created_start: Optional["Datetime"] = None,
        #     created_end: Optional["Datetime"] = None,
        #     updated_start: Optional["Datetime"] = None,
        #     updated_end: Optional["Datetime"] = None,
        # ) -> List[Pipeline]:
        #     user_id = self.auth.user_id()
        #     return Pipelines(
        #         self._search_pipelines(
        #             search_term,
        #             deployed,
        #             user_id,
        #             created_start,
        #             created_end,
        #             updated_start,
        #             updated_end,
        #         )
        #     )
    """

    def search_pipelines(
        self,
        search_term: Optional[str] = None,
        deployed: Optional[bool] = None,
        created_start: Optional["Datetime"] = None,
        created_end: Optional["Datetime"] = None,
        updated_start: Optional["Datetime"] = None,
        updated_end: Optional["Datetime"] = None,
    ) -> PipelineVersionList:
        """Search for pipelines. All parameters are optional, in which case the result is the same as
        `list_pipelines()`. All times are strings to be parsed by `datetime.isoformat`. Example:

             myclient.search_pipelines(created_end='2022-04-19 13:17:59+00:00', search_term="foo")

        :param str search_term: Will be matched against tags and model names. Example: "footag123".
        :param bool deployed: Pipeline was deployed or not
        :param str created_start: Pipeline was created at or after this time
        :param str created_end: Pipeline was created at or before this time
        :param str updated_start: Pipeline was updated at or before this time
        :param str updated_end: Pipeline was updated at or before this time

        :return: A list of pipeline versions matching the search criteria.
        :rtype: List[PipelineVersion]
        """
        return PipelineVersionList(
            self._search_pipeline_versions(
                search_term,
                deployed,
                None,
                created_start,
                created_end,
                updated_start,
                updated_end,
            )
        )

    def search_pipeline_versions(
        self,
        search_term: Optional[str] = None,
        deployed: Optional[bool] = None,
        created_start: Optional["Datetime"] = None,
        created_end: Optional["Datetime"] = None,
        updated_start: Optional["Datetime"] = None,
        updated_end: Optional["Datetime"] = None,
    ) -> PipelineVersionList:
        """Search for pipeline versions. All parameters are optional. All times are strings to be parsed by
        `datetime.isoformat`.
        Example:
            >>> myclient.search_pipeline_versions(created_end='2022-04-19 13:17:59+00:00', search_term="foo")

        :param str search_term: Will be matched against tags and model names. Example: "footag123".
        :param bool deployed: Pipeline was deployed or not
        :param str created_start: Pipeline was created at or after this time
        :param str created_end: Pipeline was created at or before this time
        :param str updated_start: Pipeline was updated at or before this time
        :param str updated_end: Pipeline was updated at or before this time

        :return: A list of pipeline versions matching the search criteria.
        :rtype: List[PipelineVersion]
        """
        return PipelineVersionList(
            self._search_pipeline_versions(
                search_term,
                deployed,
                None,
                created_start,
                created_end,
                updated_start,
                updated_end,
            )
        )

    def _search_pipeline_versions(
        self,
        search_term: Optional[str] = None,
        deployed: Optional[bool] = None,
        user_id: Optional[str] = None,
        created_start: Optional["Datetime"] = None,
        created_end: Optional["Datetime"] = None,
        updated_start: Optional["Datetime"] = None,
        updated_end: Optional["Datetime"] = None,
    ) -> List[PipelineVersion]:
        (query, params) = self._generate_search_pipeline_query(
            search_term=search_term,
            deployed=deployed,
            user_id=user_id,
            created_start=created_start,
            created_end=created_end,
            updated_start=updated_start,
            updated_end=updated_end,
        )
        q = gql.gql(query)
        data = self._gql_client.execute(q, variable_values=params)
        pipelines = []
        if data["search_pipelines"]:
            for p in data["search_pipelines"]:
                pipelines.append(PipelineVersion(self, p))
        return pipelines

    def _generate_search_pipeline_query(
        self,
        search_term: Optional[str] = None,
        deployed: Optional[bool] = None,
        user_id: Optional[str] = None,
        created_start: Optional["Datetime"] = None,
        created_end: Optional["Datetime"] = None,
        updated_start: Optional["Datetime"] = None,
        updated_end: Optional["Datetime"] = None,
    ):
        filters = []
        query_params = []
        params: Dict[str, Any] = {}
        search = ""
        if search_term:
            search = search_term
        params["search_term"] = search
        query_params.append("$search_term: String!")

        if user_id:
            filters.append("owner_id: {_eq: $user_id}")
            params["user_id"] = user_id
            query_params.append("$user_id: String!")

        if deployed is not None:
            filters.append("pipeline: {deployment: {deployed: {_eq: $deployed}}}")
            params["deployed"] = deployed
            query_params.append("$deployed: Boolean")

        self._generate_time_range_graphql(
            "created_at",
            start=created_start,
            end=created_end,
            filters=filters,
            query_params=query_params,
            params=params,
        )
        self._generate_time_range_graphql(
            "updated_at",
            start=updated_start,
            end=updated_end,
            filters=filters,
            query_params=query_params,
            params=params,
        )

        where_clause_str = self._generate_where_clause_str(filters)
        query_param_str = self._generate_query_param_str(query_params)
        query = f"""
            query GetPipelines({query_param_str}) {{
                search_pipelines(args: {{search: $search_term}}, distinct_on: id{where_clause_str}, order_by: {{id: desc}}) {{
                    id
                    created_at
                    pipeline_pk_id
                    updated_at
                    version
                    pipeline {{
                        id
                        pipeline_id
                        pipeline_tags {{
                            id
                            tag {{
                                id
                                tag
                            }}
                        }}
                    }}
                }}
            }}
        """
        return (query, params)

    def _generate_where_clause_str(self, filters: List[str]) -> str:
        where_clause_str = ""
        filters_len = len(filters)
        if filters_len > 0:
            if filters_len > 1:
                where_clause_str = f""", where: {{_and: {{ {", ".join(filters)} }}}}"""
            else:
                where_clause_str = f", where: {{{filters[0]}}}"
        return where_clause_str

    def _generate_query_param_str(self, query_params: List[str]):
        return ", ".join(query_params)

    def _generate_time_range_graphql(
        self,
        field: str,
        start: Optional["Datetime"],
        end: Optional["Datetime"],
        filters: List[str],
        query_params: List[str],
        params: Dict[str, Any],
    ):
        if start and not end:
            filters.append(f"{field}: {{_gte: $start_{field}}}")
            params[f"start_{field}"] = start
            query_params.append(f"$start_{field}: timestamptz!")
        elif end and not start:
            filters.append(f"{field}: {{_lte: $end_{field}}}")
            params[f"end_{field}"] = end
            query_params.append(f"$end_{field}: timestamptz!")
        elif start and end:
            filters.append(f"{field}: {{_gte: $start_{field}, _lte: $end_{field}}}")
            params[f"start_{field}"] = start
            params[f"end_{field}"] = start
            query_params.append(f"$start_{field}: timestamptz!")
            query_params.append(f"$end_{field}: timestamptz!")

    # TODO: Misleading name, this is actually searching for all model versions.
    # Future work will redo the query to give models instead of versions.
    def search_my_models(
        self,
        search_term: Optional[str] = None,
        uploaded_time_start: Optional["Datetime"] = None,
        uploaded_time_end: Optional["Datetime"] = None,
    ) -> ModelVersionList:
        """Search models owned by you.
            Example:
                >>> client.search_my_models(search_term="my_model")
        :param search_term: Searches the following metadata: names, shas, versions, file names, and tags
        :param uploaded_time_start: Inclusive time of upload
        :param uploaded_time_end: Inclusive time of upload
        :return: ModelVersionList
        """
        user_id = self.auth.user_id()
        return ModelVersionList(
            self._search_model_versions(
                search_term=search_term,
                user_id=user_id,
                start=uploaded_time_start,
                end=uploaded_time_end,
            )
        )

    def search_my_model_versions(
        self,
        search_term: Optional[str] = None,
        uploaded_time_start: Optional["Datetime"] = None,
        uploaded_time_end: Optional["Datetime"] = None,
    ) -> ModelVersionList:
        """Search model versions owned by you.
            Example:
                >>> client.search_my_model_versions(search_term="my_model")
        :param search_term: Searches the following metadata: names, shas, versions, file names, and tags
        :param uploaded_time_start: Inclusive time of upload
        :param uploaded_time_end: Inclusive time of upload
        :return: ModelVersionList
        """
        user_id = self.auth.user_id()
        return ModelVersionList(
            self._search_model_versions(
                search_term=search_term,
                user_id=user_id,
                start=uploaded_time_start,
                end=uploaded_time_end,
            )
        )

    # TODO: Misleading name, this is actually searching for all model versions.
    # Future work will redo the query to give models instead of versions.
    def search_models(
        self,
        search_term: Optional[str] = None,
        uploaded_time_start: Optional["Datetime"] = None,
        uploaded_time_end: Optional["Datetime"] = None,
    ) -> ModelVersionList:
        """Search all models you have access to.
        :param search_term: Searches the following metadata: names, shas, versions, file names, and tags
        :param uploaded_time_start: Inclusive time of upload
        :param uploaded_time_end: Inclusive time of upload
        :return: ModelVersionList
        """
        return ModelVersionList(
            self._search_model_versions(
                search_term=search_term,
                start=uploaded_time_start,
                end=uploaded_time_end,
            )
        )

    def search_model_versions(
        self,
        search_term: Optional[str] = None,
        uploaded_time_start: Optional["Datetime"] = None,
        uploaded_time_end: Optional["Datetime"] = None,
    ) -> ModelVersionList:
        """Search all model versions you have access to.
            Example:
                >>> client.search_model_versions(search_term="my_model")
        :param search_term: Searches the following metadata: names, shas, versions, file names, and tags
        :param uploaded_time_start: Inclusive time of upload
        :param uploaded_time_end: Inclusive time of upload
        :return: ModelVersionList
        """
        return ModelVersionList(
            self._search_model_versions(
                search_term=search_term,
                start=uploaded_time_start,
                end=uploaded_time_end,
            )
        )

    def _search_model_versions(
        self, search_term=None, user_id=None, start=None, end=None
    ) -> List[ModelVersion]:
        (query, params) = self._generate_model_query(
            search_term=search_term,
            user_id=user_id,
            start=start,
            end=end,
        )

        q = gql.gql(query)

        data = self._gql_client.execute(q, variable_values=params)
        models = []
        if data["search_models"]:
            for m in data["search_models"]:
                models.append(ModelVersion(self, m))
        return models

    def _generate_model_query(
        self,
        search_term=None,
        user_id=None,
        start=None,
        end=None,
    ):
        filters = []
        query_params = []
        params = {}
        search = ""
        if search_term:
            search = search_term
        params["search_term"] = search
        query_params.append("$search_term: String!")
        if user_id:
            filters.append("owner_id: {_eq: $user_id}")
            params["user_id"] = user_id
            query_params.append("$user_id: String!")

        self._generate_time_range_graphql(
            "created_at",
            start=start,
            end=end,
            filters=filters,
            params=params,
            query_params=query_params,
        )

        where_clause_str = self._generate_where_clause_str(filters)
        query_param_str = self._generate_query_param_str(query_params)
        query = f"""
            query GetModels({query_param_str}) {{
              search_models(args: {{search: $search_term}}{where_clause_str}, order_by: {{created_at: desc}}) {{
                id
              }}
            }}
        """
        return (query, params)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Find a user by email"""
        assert email is not None
        escaped_email = quote_plus(email)
        url = (
            f"{self.auth_endpoint}/auth/admin/realms/master/users?email={escaped_email}"
        )
        headers = {
            "Content-Type": "application/json",
            "Authorization": self.auth._bearer_token_str(),
            "User-Agent": _user_agent,
        }
        resp = requests.get(url, headers=headers, data={})
        jresp = resp.json()
        return None if jresp == [] else User(client=self, data=jresp[0])

    def deactivate_user(self, email: str) -> None:
        """Deactivates an existing user of the platform

        Deactivated users cannot log into the platform.
        Deactivated users do not count towards the number of allotted user seats from the license.

        The Models and Pipelines owned by the deactivated user are not removed from the platform.

        :param str email: The email address of the user to deactivate.

        :return: None
        :rtype: None
        """

        if self.auth.user_email() == email:
            raise Exception("A user may not deactive themselves.")

        user = self.get_user_by_email(email)

        if user is None:
            raise EntityNotFoundError("User", {"email": email})

        if user.username() == "admin":
            raise Exception("Admin user may not be deactivated.")

        url = f"{self.auth_endpoint}/auth/admin/realms/master/users/{user._id}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": self.auth._bearer_token_str(),
            "User-Agent": _user_agent,
        }

        # Get the current full user representation to return in the mutation due to keycloak bug
        get_user_response = requests.get(url, headers=headers, data={})

        cur_user_rep = get_user_response.json()
        cur_user_rep["enabled"] = False

        resp = requests.put(url, headers=headers, json=cur_user_rep)

        if resp.status_code != 204:
            raise EntityNotFoundError("User", {"email": email})
        return None

    def activate_user(self, email: str) -> None:
        """Activates an existing user of the platform that had been previously deactivated.

        Activated users can log into the platform.

        :param str email: The email address of the user to activate.

        :return: None
        :rtype: None
        """
        user = self.get_user_by_email(email)

        if user is None:
            raise EntityNotFoundError("User", {"email": email})

        url = f"{self.auth_endpoint}/auth/admin/realms/master/users/{user._id}"

        headers = {
            "Content-Type": "application/json",
            "Authorization": self.auth._bearer_token_str(),
            "User-Agent": _user_agent,
        }

        # Get the current full user representation to return in the mutation due to keycloak bug
        get_user_response = requests.get(url, headers=headers, data={})

        cur_user_rep = get_user_response.json()
        cur_user_rep["enabled"] = True

        resp = requests.put(url, headers=headers, json=cur_user_rep)

        if resp.status_code != 204:
            raise EntityNotFoundError("User", {"email": email})
        return None

    def _get_user_by_id(self, id: str) -> Optional[User]:
        assert id is not None
        url = f"{self.auth_endpoint}/auth/admin/realms/master/users/{id}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": self.auth._bearer_token_str(),
            "User-Agent": _user_agent,
        }
        resp = requests.get(url, headers=headers, data={})
        jresp = resp.json()
        return None if jresp == [] else User(client=self, data=jresp)

    def list_users(self) -> List[User]:
        """List of all Users on the platform

        :return: A list of all Users on the platform.
        :rtype: List[User]
        """
        resp = User.list_users(
            auth=self.auth,
            api_endpoint=self.api_endpoint,
            auth_endpoint=self.auth_endpoint,
        )
        return [User(client=self, data=u) for u in resp]

    def upload_model(
        self,
        name: str,
        path: Union[str, pathlib.Path],
        framework: Optional[Framework] = None,
        input_schema: Optional[pa.Schema] = None,
        output_schema: Optional[pa.Schema] = None,
        convert_wait: Optional[bool] = True,
        arch: Optional[Architecture] = None,
        accel: Optional[Acceleration] = None,
    ) -> ModelVersion:
        """Upload a model defined by a file as a new model variant.

        :param name: str The name of the model of which this is a variant.
            Names must be ASCII alpha-numeric characters or dash (-) only.
        :param path: Union[str, pathlib.Path] Path of the model file to upload.
        :param framework: Optional[Framework] Supported model frameworks.
            Use models from Framework Enum. Example: Framework.PYTORCH, Framework.TENSORFLOW
        :param input_schema: Optional pa.Schema Input schema, required for flavors other than ONNX, Tensorflow, and Python
        :param output_schema: Optional pa.Schema Output schema, required for flavors other than ONNX, Tensorflow, and Python
        :param convert_wait: Optional bool Defaults to True. Specifies if method should return when conversion is over or not.
        :return: The created Model.
        :rtype: ModelVersion
        """
        require_dns_compliance(name)

        if accel is not None:
            arch = arch or Architecture.default()
            if not accel.is_applicable(arch):
                raise InvalidAccelerationError(accel, arch)

        payload = {
            "name": name,
            "visibility": _Visibility.PRIVATE,
            "workspace_id": self.get_current_workspace().id(),
        }

        if isinstance(path, str):
            path = pathlib.Path(path)

        with path.open("rb") as f:
            if not is_models_enabled():
                return self._upload_model_stream(path.name, payload, f)

            if not isinstance(framework, Framework):
                raise ValueError(
                    "framework must be a Framework Enum. Example: Framework.PYTORCH, Framework.TENSORFLOW"
                )

            payload["conversion"] = {
                "arch": arch or Architecture.default(),
                "accel": accel or Acceleration.default(),
                "framework": framework.value,
                "python_version": DEFAULT_MODEL_CONVERSION_PYTHON_VERSION,
                "requirements": [],
            }

            if framework in UPLOAD_MODEL_STREAM_SUPPORTED_FLAVORS:
                return self._upload_model_via_models_service(
                    payload, (path.name, f), False
                )

            if input_schema is None:
                raise Exception("parameter 'input_schema' required for this framework")
            if output_schema is None:
                raise Exception("parameter 'output_schema' required for this framework")

            payload["input_schema"] = base64.b64encode(
                bytes(input_schema.serialize())
            ).decode("utf8")
            payload["output_schema"] = base64.b64encode(
                bytes(output_schema.serialize())
            ).decode("utf8")
            return self._upload_model_via_models_service(
                payload, (path.name, f), True, convert_wait
            )

    def _upload_model_stream(
        self, filename: str, data: Dict[str, Any], file: Any
    ) -> ModelVersion:
        endpoint = posixpath.join(self.api_endpoint, "v1/api/models/upload_stream")
        payload = {"filename": filename, **data}
        headers = {"User-Agent": _user_agent}

        res = requests.post(
            endpoint, auth=self.auth, params=payload, data=file, headers=headers
        )
        if res.status_code != 200:
            raise ModelUploadError(res.text)

        res_dict = json.loads(res.text)
        return ModelVersion(
            self, data=res_dict["insert_models"]["returning"][0]["models"][0]
        )

    def _upload_model_via_models_service(
        self,
        data: Dict[str, Any],
        file_info: Optional[Tuple[str, Any]],
        convert: Optional[bool] = True,
        convert_wait: Optional[bool] = True,
    ) -> ModelVersion:
        """
        Upload and (possibly) convert a model defined by a file as a new model variant. If convert_wait
        is True, the method will wait for about 10min for the conversion to finish before returning.
        If convert_wait is False, the method will return immediately.
        """
        files: Dict[str, Tuple[Optional[str], Any, str]] = {
            "metadata": (None, json.dumps(data), JSON_CONTENT_TYPE),
        }
        # we must have either file information or we're not trying to convert
        assert file_info is not None or convert is False
        if file_info is not None:
            filename = file_info[0]
            file = file_info[1]
            files["file"] = (filename, file, OCTET_STREAM_CONTENT_TYPE)

        multipart_files = MultipartEncoder(fields=files)

        headers = {"User-Agent": _user_agent}
        headers["Content-Type"] = multipart_files.content_type

        route = "upload_and_convert" if convert else "upload"
        endpoint = posixpath.join(self.api_endpoint, f"v1/api/models/{route}")

        try:
            self.auth._force_reload()
            res = requests.post(
                endpoint, auth=self.auth, data=multipart_files, headers=headers
            )
            res.raise_for_status()
        except requests.exceptions.RequestException as request_err:
            raise request_err
        try:
            res_dict = json.loads(res.text)
        except (json.JSONDecodeError, ValueError) as json_err:
            raise ValueError("Decoding response from model upload failed") from json_err

        model = ModelVersion(
            self, data=res_dict["insert_models"]["returning"][0]["models"][0]
        )
        if convert is not True or convert_wait is not True:
            return self._get_configured_model_version(model)
        else:
            return self._wait_for_model(model)

    def _wait_for_model(self, model_version: ModelVersion) -> ModelVersion:
        from .wallaroo_ml_ops_api_client.models.model_status import ModelStatus
        from .model_status import model_status_to_string, is_attempting_load

        poll_interval = 5
        expire_time = datetime.now() + timedelta(
            seconds=DEFAULT_MODEL_CONVERSION_TIMEOUT
        )
        print(
            f"Waiting for model loading - this will take up to {DEFAULT_MODEL_CONVERSION_TIMEOUT/60}min."
        )
        last_status = None
        while datetime.now() < expire_time:
            model_version = self._get_configured_model_version(model_version)
            status = model_version.status()

            if last_status != status:
                if last_status is not None:
                    # report success / failure for attempting to convert / package
                    if is_attempting_load(last_status):
                        print(
                            "successful"
                            if status == ModelStatus.READY
                            else "incompatible"
                        )
                    # new status needs to start on a new line
                    print()

                if status == ModelStatus.READY:
                    print("Ready")
                    return model_version
                elif status == ModelStatus.ERROR:
                    print("ERROR!")
                    raise ModelConversionError(
                        f"An error occured during model conversion."
                    )

                print(f"Model is {model_status_to_string(status)}", end="")

            # marching dots
            print(".", end="", flush=True)
            last_status = status
            time.sleep(poll_interval)
        else:
            raise ModelConversionTimeoutError(
                f"Model conversion timed out after {DEFAULT_MODEL_CONVERSION_TIMEOUT/60}min."
            )

    def _get_configured_model_version(
        self, model_version: ModelVersion
    ) -> ModelVersion:
        headers = {"User-Agent": _user_agent}
        endpoint = posixpath.join(self.api_endpoint, "v1/api/models/get_version_by_id")
        params = {"model_version_id": model_version.id()}
        try:
            get_model_version_response = requests.post(
                endpoint, auth=self.auth, json=params, headers=headers
            )
            get_model_version_response.raise_for_status()
        except requests.exceptions.RequestException as request_err:
            raise request_err
        try:
            get_model_version_response_dict = json.loads(
                get_model_version_response.text
            )
        except (json.JSONDecodeError, ValueError) as json_err:
            raise ValueError(
                "Decoding response from models/get_version_by_id failed"
            ) from json_err

        model_version = ModelVersion(
            self,
            data=get_model_version_response_dict["model_version"]["model_version"],
        )
        model_version._config = ModelConfig(
            self,
            get_model_version_response_dict["model_version"]["config"],
        )
        return model_version

    def register_model_image(self, name: str, image: str) -> ModelVersion:
        """Registers an MLFlow model as a new model.

        :param str model_name: The name of the model of which this is a variant.
            Names must be ASCII alpha-numeric characters or dash (-) only.
        :param str image: Image name of the MLFlow model to register.
        :return: The created Model.
        :rtype: ModelVersion
        """

        require_dns_compliance(name)
        data = {
            "image_path": image,
            "name": name,
            "visibility": _Visibility.PRIVATE,
            "workspace_id": self.get_current_workspace().id(),
            "conversion": {
                "framework": "mlflow",
                "python_version": DEFAULT_MODEL_CONVERSION_PYTHON_VERSION,
                "requirements": [],
            },
        }
        return self._upload_model_via_models_service(data, None, False)

    def get_model(self, name: str, version: Optional[str] = None):
        """
        Retrieves a model by name and optionally version from the current workspace.
        :param name: The name of the model.
        :param version: The version of the model. If not provided, the latest version is returned.
        :return ModelVersion: The requested model.
        Raises:
            Exception: If the model with the given name does not exist.
            Exception: If the model with the given version does not exist.
        """
        model = next(
            iter(
                [p for p in self.get_current_workspace().models() if p.name() == name]
            ),
            None,
        )
        if model is None:
            raise Exception(f"Error: A model with the name {name} does not exist.")
        if version is not None:
            model_version = next(
                iter([mv for mv in model.versions() if mv.version() == version]), None
            )
            if model_version is not None:
                return model_version
            else:
                raise Exception(
                    f"Error: A model with the version {version} not found in this workspace."
                )
        return model.versions()[-1]

    def model_by_name(self, model_class: str, model_name: str) -> ModelVersion:
        """Fetch a Model by name.

        :param str model_class: Name of the model class.
        :param str model_name: Name of the variant within the specified model class.
        :return: The Model with the corresponding model and variant name.
        :rtype: ModelVersion
        """
        res = self._gql_client.execute(
            gql.gql(
                """
                query ModelByName($model_id: String!, $model_version: String!) {
                  model(where: {_and: [{model_id: {_eq: $model_id}}, {model_version: {_eq: $model_version}}]}) {
                    id
                    model_id
                    model_version
                  }
                }
                """
            ),
            variable_values={
                "model_id": model_class,
                "model_version": model_name,
            },
        )
        if not res["model"]:
            raise EntityNotFoundError(
                "ModelVersion", {"model_class": model_class, "model_name": model_name}
            )
        return ModelVersion(client=self, data={"id": res["model"][0]["id"]})

    def model_version_by_name(self, model_class: str, model_name: str) -> ModelVersion:
        """Fetch a Model version by name.

        :param str model_class: Name of the model class.
        :param str model_name: Name of the variant within the specified model class.
        :return: The Model with the corresponding model and variant name.
        :rtype: ModelVersion
        """
        res = self._gql_client.execute(
            gql.gql(
                """
                query ModelByName($model_id: String!, $model_version: String!) {
                  model(where: {_and: [{model_id: {_eq: $model_id}}, {model_version: {_eq: $model_version}}]}) {
                    id
                    model_id
                    model_version
                  }
                }
                """
            ),
            variable_values={
                "model_id": model_class,
                "model_version": model_name,
            },
        )
        if not res["model"]:
            raise EntityNotFoundError(
                "ModelVersion", {"model_class": model_class, "model_name": model_name}
            )
        return ModelVersion(client=self, data={"id": res["model"][0]["id"]})

    def deployment_by_name(self, deployment_name: str) -> Deployment:
        """Fetch a Deployment by name.

        :param str deployment_name: Name of the deployment.
        :return: The Deployment with the corresponding name.
        :rtype: Deployment
        """
        res = self._gql_client.execute(
            gql.gql(
                """
                query DeploymentByName($deployment_name: String!) {
                  deployment(where: {deploy_id: {_eq: $deployment_name}}) {
                    id
                  }
                }
                """
            ),
            variable_values={
                "deployment_name": deployment_name,
            },
        )
        if not res["deployment"]:
            raise EntityNotFoundError(
                "Deployment", {"deployment_name": deployment_name}
            )
        return Deployment(client=self, data={"id": res["deployment"][0]["id"]})

    def pipelines_by_name(self, pipeline_name: str) -> List[Pipeline]:
        """Fetch Pipelines by name.

        :param str pipeline_name: Name of the pipeline.
        :return: The Pipeline with the corresponding name.
        :rtype: Pipeline
        """
        res = self._gql_client.execute(
            gql.gql(
                """
                query PipelineByName($pipeline_name: String!) {
                  pipeline(where: {pipeline_id: {_eq: $pipeline_name}}, order_by: {created_at: desc}) {
                    id
                  }
                }
                """
            ),
            variable_values={
                "pipeline_name": pipeline_name,
            },
        )
        assert "pipeline" in res
        length = len(res["pipeline"])
        if length < 1:
            raise EntityNotFoundError("Pipeline", {"pipeline_name": pipeline_name})
        return [Pipeline(client=self, data={"id": p["id"]}) for p in res["pipeline"]]

    def list_pipelines(self) -> List[Pipeline]:
        """List all pipelines on the platform.

        :return: A list of all pipelines on the platform.
        :rtype: List[Pipeline]
        """
        res = self._gql_client.execute(
            gql.gql(
                """
            query ListPipelines {
              pipeline(order_by: {id: desc}) {
                id
                pipeline_tags {
                  tag {
                    id
                    tag
                  }
                }
              }
            }
            """
            )
        )
        return Pipelines([Pipeline(client=self, data=d) for d in res["pipeline"]])

    def get_pipeline(self, name: str, version: Optional[str] = None) -> Pipeline:
        """
        Retrieves a pipeline by name and optional version from the current workspace.
        :param name: The name of the pipeline to retrieve.
        :param version: The version of the pipeline to retrieve. Defaults to None.
        :return: Pipeline: The requested pipeline.
        Raises:
            Exception: If the pipeline with the given name is not found in the workspace.
            Exception: If the pipeline with the given version is not found in the workspace.
        """
        pipeline = next(
            iter(
                [
                    p
                    for p in self.get_current_workspace().pipelines()
                    if p.name() == name
                ]
            ),
            None,
        )
        if pipeline is None:
            raise Exception(f"Pipeline {name} not found in this workspace.")
        if version is not None:
            pipeline_version = next(
                iter([pv for pv in pipeline.versions() if pv.name() == version]), None
            )
            if pipeline_version is not None:
                pipeline._pipeline_version_to_deploy = pipeline_version
                return pipeline
            else:
                raise Exception(
                    f"Pipeline version {version} not found in this workspace."
                )
        return pipeline

    def build_pipeline(self, pipeline_name: str) -> "Pipeline":
        """Starts building a pipeline with the given `pipeline_name`,
        returning a :py:PipelineConfigBuilder:

        When completed, the pipeline can be uploaded with `.upload()`

        :param pipeline_name string: Name of the pipeline, must be composed of ASCII
          alpha-numeric characters plus dash (-).
        """

        require_dns_compliance(pipeline_name)

        _Visibility.PRIVATE

        # TODO: Needs to handle visibility?
        data = pipelines_create.sync(
            client=self.mlops(),
            body=pipelines_create_body.PipelinesCreateBody(
                pipeline_name,
                self.get_current_workspace().id(),
                pipelines_create_body_definition_type_0.PipelinesCreateBodyDefinitionType0.from_dict(
                    {}
                ),
            ),
        )

        if data is None:
            raise Exception("Failed to create pipeline")

        if not isinstance(data, PipelinesCreateResponse200):
            raise Exception(data.msg)

        return Pipeline(client=self, data={"id": data.pipeline_pk_id})

    def _upload_pipeline_variant(
        self,
        name: str,
        config: PipelineConfig,
    ) -> Pipeline:
        """Creates a new PipelineVariant with the specified configuration.

        :param str name: Name of the Pipeline. Must be unique across all Pipelines.
        :param config PipelineConfig: Pipeline configuration.
        """
        definition = config.to_json()
        _Visibility.PRIVATE

        data = pipelines_create.sync(
            client=self.mlops(),
            body=pipelines_create_body.PipelinesCreateBody(
                name,
                self.get_current_workspace().id(),
                pipelines_create_body_definition_type_0.PipelinesCreateBodyDefinitionType0.from_dict(
                    definition
                ),
            ),
        )

        if data is None:
            # TODO: Generalize
            raise Exception("Failed to create pipeline")

        if not isinstance(data, PipelinesCreateResponse200):
            raise Exception(data.msg) if "msg" in data else Exception(data)

        pipeline_data = data.to_dict()
        pipeline_data["id"] = data.pipeline_pk_id

        return Pipeline(
            client=self,
            data=pipeline_data,
        )

    def create_value_split_experiment(
        self,
        name: str,
        meta_key: str,
        default_model: ModelConfig,
        challenger_models: List[Tuple[Any, ModelConfig]],
    ) -> Pipeline:
        """Creates a new PipelineVariant of a "value-split experiment" type.
        :param str name: Name of the Pipeline
        :param meta_key str: Inference input key on which to redirect inputs to
            experiment models.
        :param default_model ModelConfig: Model to send inferences by default.
        :param challenger_models List[Tuple[Any, ModelConfig]]: A list of
            meta_key values -> Models to send inferences. If the inference data
            referred to by meta_key is equal to one of the keys in this tuple,
            that inference is redirected to the corresponding model instead of
            the default model.
        """
        args = [meta_key, default_model.model_version().name()]
        for v, m in challenger_models:
            args.append(v)
            args.append(m.model_version().name())
        step = {
            "id": "metavalue_split",
            "operation": "map",
            "args": args,
        }
        definition = {"id": name, "steps": [step]}
        # TODO: This seems like a one-to-one replace, find appropriate test.
        data = self._gql_client.execute(
            gql.gql(
                """
            mutation CreatePipeline(
                $pipeline_id: String,
                $version: String,
                $definition: jsonb,
                $workspace_id: bigint
            ) {
                insert_pipeline(
                    objects: {
                    pipeline_versions: {
                        data: { definition: $definition }
                    }
                    pipeline_id: $pipeline_id
                    }
                ) {
                    returning {
                        id
                    }
                }
            }
            """
            ),
            variable_values={
                "pipeline_id": name,
                "definition": definition,
                "workspace_id": self.get_current_workspace().id(),
            },
        )
        return Pipeline(
            client=self,
            data=data["insert_pipeline"]["returning"][0],
        )

    @staticmethod
    def cleanup_arrow_data_for_display(arrow_data: pa.Table) -> pa.Table:
        """
        Cleans up the inference result and log data from engine / plateau for display (ux) purposes.
        """
        columns = []
        table_schema = []
        for column_name in arrow_data.column_names:
            column_data = arrow_data[column_name]
            column_schema = arrow_data.schema.field(column_name)
            if "time" == column_name:
                time_df = arrow_data["time"].to_pandas().copy()
                time_df = pd.to_datetime(time_df, unit="ms")
                column_data = pa.array(time_df)
                column_schema = pa.field("time", pa.timestamp("ms"))
            if "check_failures" == column_name:
                check_failures_df = arrow_data["check_failures"].to_pandas()
                column_data = pa.array(check_failures_df.apply(len))
                column_schema = pa.field("check_failures", pa.int8())
            columns.append(column_data)
            table_schema.append(column_schema)
        new_schema = pa.schema(table_schema)
        return pa.Table.from_arrays(columns, schema=new_schema)

    @staticmethod
    def _build_headers_and_params(
        limit: Optional[int] = None,
        start_datetime: Optional[datetime] = None,
        end_datetime: Optional[datetime] = None,
        dataset: Optional[List[str]] = None,
        dataset_exclude: Optional[List[str]] = None,
        dataset_separator: Optional[str] = None,
    ) -> Tuple[Dict[str, str], Dict[str, Any]]:
        headers = {"User-Agent": _user_agent}
        params = dict()
        if is_arrow_enabled():
            headers.update({"Accept": ARROW_CONTENT_TYPE})
            if start_datetime is None and end_datetime is None:
                # type: ignore
                params["page_size"] = (
                    limit if limit is not None else DEFAULT_RECORDS_LIMIT
                )
                params["order"] = "desc"  # type: ignore
            elif start_datetime is not None and end_datetime is not None:
                if limit is not None:
                    params["page_size"] = limit  # type: ignore
                start_str = start_datetime.astimezone(tz=timezone.utc).isoformat()
                params["time.start"] = start_str  # type: ignore
                end_str = end_datetime.astimezone(tz=timezone.utc).isoformat()
                params["time.end"] = end_str  # type: ignore
            else:
                raise Exception(
                    "Please provide both start datetime and end datetime together."
                )
            params["dataset[]"] = dataset or ["*"]  # type: ignore
            if dataset_exclude is not None:
                params["dataset.exclude[]"] = dataset_exclude  # type: ignore
            params["dataset.separator"] = dataset_separator or "."  # type: ignore
        else:
            # type: ignore
            params["limit"] = limit if limit is not None else DEFAULT_RECORDS_LIMIT
            headers.update({"Accept": JSON_CONTENT_TYPE})
        return headers, params

    def _get_next_records(
        self,
        params: Optional[Dict[str, Any]],
        iterator: Optional[Dict[str, Any]],
        headers: Optional[Dict[str, Any]],
        base: str,
    ) -> requests.Response:
        try:
            resp = requests.post(
                base + "/records",
                params=params,
                json=iterator,
                auth=self.auth,
                headers=headers,
            )
            resp.raise_for_status()
        except requests.exceptions.HTTPError as http_error:
            raise requests.exceptions.HTTPError(http_error, resp.text)
        return resp

    def _extract_logs_from_response(
        self, resp: requests.Response
    ) -> Tuple[pa.Table, Dict[str, Any], str]:
        with pa.ipc.open_file(resp.content) as reader:
            entries = reader.read_all()
            metadata_dict = reader.schema.metadata
            metadata = (
                json.loads(metadata_dict[b"status"])
                if metadata_dict is not None
                else None
            )
            status = metadata["status"] if metadata is not None else None
            if entries.num_rows > 0:
                clean_entries = self.cleanup_arrow_data_for_display(entries)
                iterator = metadata["next"] if "next" in metadata else None
                return clean_entries, iterator, status
            else:
                iterator = None
                return entries, iterator, status

    @staticmethod
    def _slice_log_results_if_exceeds_limit(
        logs_table: pa.Table, rows_written: int, limit: Optional[int] = None
    ) -> Tuple[pa.Table, int, bool]:
        if limit is not None and rows_written >= limit:
            return (
                logs_table.slice(0, limit - (rows_written - logs_table.num_rows)),
                limit,
                True,
            )
        return logs_table, rows_written, False

    @staticmethod
    def _should_stop_log_collection(
        status: str,
        data_size_exceeded: bool,
        rows_written: int,
        end_time: str,
        data_size: float,
        data_unit: DataSizeUnit,
        is_sliced: bool,
        chronological_order: str,
    ) -> bool:
        if data_size_exceeded:
            sys.stderr.write(
                f"Warning: Pipeline log data size limit of {data_size} {data_unit.value} exceeded."
                f" {rows_written} {chronological_order} records exported successfully, {chronological_order}"
                f" record seen was at {end_time}. Set a different limit using data_size_limit for more data."
                f" Please request additional files separately.\n\n"
            )
            return True
        if status == "RecordLimited":
            sys.stderr.write(
                f"Warning: There are more logs available."
                f" Please set a larger limit to export more data.\n\n"
            )
            return True
        if status == "All":
            return True
        if is_sliced:
            return True

        return False

    def _process_logs(
        self, logs_table: pa.Table, rows_written: int, limit: Optional[int]
    ) -> Tuple[pa.Table, int, bool, str]:
        rows_written += logs_table.num_rows
        (
            logs_table,
            total_rows_written,
            is_sliced,
        ) = self._slice_log_results_if_exceeds_limit(logs_table, rows_written, limit)
        end_time = (
            logs_table.column("time")[-1].as_py() if logs_table.num_rows > 0 else None
        )
        return logs_table, total_rows_written, is_sliced, end_time

    @staticmethod
    def _validate_file_size_input(data_size_limit: str) -> Tuple[float, DataSizeUnit]:
        pattern = r"^(\d+(\.\d+)?)\s*([KMGT]iB)$"
        match = re.match(pattern, data_size_limit, re.IGNORECASE)

        if not match:
            raise ValueError(
                "Invalid data size format. Please use the format: <number><unit> (e.g. 1.5MiB or 1 GiB)"
            )

        size = float(match.group(1))
        unit = DataSizeUnit.from_string(match.group(3).strip())

        if size <= 0:
            raise ValueError("File size must be positive.")

        return size, unit

    def _export_logs(
        self,
        base: str,
        params: Dict[str, Any],
        headers: Dict[str, str],
        directory: str,
        file_prefix: str,
        data_size_limit: Optional[str] = None,
        limit: Optional[int] = None,
        arrow: Optional[bool] = False,
    ) -> None:
        iterator = {}  # type: Dict[str, Any]

        chronological_order = (
            "oldest" if "time.start" and "time.end" in params else "newest"
        )
        data_size, data_unit = (
            self._validate_file_size_input(data_size_limit)
            if data_size_limit
            else (DEFAULT_MAX_DATA_SIZE, DEFAULT_MAX_DATA_UNIT)
        )
        data_size_limit_in_bytes = data_unit.calculate_bytes(data_size)

        rows_written = 0
        writer = None
        file_num = 0
        schema = None
        schema_changed = False
        columns_dropped = False
        end_time = None
        previous_end_time = None
        data_size_exceeded = False
        total_arrow_data_size = 0
        total_pandas_data_size = 0
        dropped_columns = []
        while iterator is not None:
            response = self._get_next_records(params, iterator, headers, base)
            logs_table, iterator, status = self._extract_logs_from_response(response)
            if logs_table.num_rows == 0:
                break
            if "metadata.dropped" in logs_table.column_names:
                flattened_metadata = logs_table["metadata.dropped"].flatten()
                if len(flattened_metadata[0][0]) > 0:
                    columns_dropped = True
                    dropped_columns = flattened_metadata[0][0]
            if "metadata" not in params["dataset[]"]:
                metadata_columns_to_drop = []
                for column_name in logs_table.column_names:
                    if column_name.startswith("metadata."):
                        metadata_columns_to_drop.append(column_name)
                logs_table = logs_table.drop(metadata_columns_to_drop)
            if schema is not None and schema != logs_table.schema:
                schema_changed = True
                writer.close()
                writer = None
            if writer is None:
                schema = logs_table.schema
                file_num += 1
                writer = create_new_file(
                    directory, file_num, file_prefix, schema, arrow
                )

            if end_time is None:
                previous_end_time = logs_table.column("time")[-1].as_py()

            sliced_table, rows_written, is_sliced, sliced_end_time = self._process_logs(
                logs_table, rows_written, limit
            )

            end_time = (
                sliced_end_time if sliced_end_time is not None else previous_end_time
            )
            for record_batch in sliced_table.to_batches():
                if arrow:
                    total_arrow_data_size += record_batch.nbytes
                    write_to_file(record_batch, writer)
                    if total_arrow_data_size > data_size_limit_in_bytes:
                        data_size_exceeded = True
                        break
                else:
                    json_str = record_batch.to_pandas().to_json(
                        orient="records", lines=True
                    )
                    total_pandas_data_size += sys.getsizeof(json_str)
                    write_to_file(json_str, writer)
                    if total_pandas_data_size > data_size_limit_in_bytes:
                        data_size_exceeded = True
                        break

            if self._should_stop_log_collection(
                status,
                data_size_exceeded,
                rows_written,
                end_time,
                data_size,
                data_unit,
                is_sliced,
                chronological_order,
            ):
                writer.close()
                break
        if schema_changed:
            sys.stderr.write(
                f"Note: The logs with different schemas are "
                f"written to separate files in the provided directory."
            )
        if columns_dropped:
            sys.stderr.write(
                f"Warning: The inference log is above the allowable limit and the following columns may have"
                f" been suppressed for various rows in the logs: {dropped_columns}."
                f" To review the dropped columns for an individual inference’s suppressed data,"
                f' include dataset=["metadata"] in the log request.'
                f"\n"
            )
        return None

    def get_logs(
        self,
        topic: str,
        limit: Optional[int] = None,
        start_datetime: Optional[datetime] = None,
        end_datetime: Optional[datetime] = None,
        dataset: Optional[List[str]] = None,
        dataset_exclude: Optional[List[str]] = None,
        dataset_separator: Optional[str] = None,
        directory: Optional[str] = None,
        file_prefix: Optional[str] = None,
        data_size_limit: Optional[str] = None,
        arrow: Optional[bool] = False,
    ) -> Tuple[Union[pa.Table, pd.DataFrame, LogEntries, None], Optional[str]]:
        """
        Get logs for the given topic.
        :param topic: str The topic to get logs for.
        :param limit: Optional[int] The maximum number of logs to return.
        :param start_datetime: Optional[datetime] The start time to get logs for.
        :param end_datetime: Optional[datetime] The end time to get logs for.
         :param dataset: Optional[List[str]] By default this is set to ["*"] which returns,
            ["time", "in", "out", "anomaly"]. Other available options - ["metadata"]
        :param dataset_exclude: Optional[List[str]] If set, allows user to exclude parts of dataset.
        :param dataset_separator: Optional[Union[Sequence[str], str]] If set to ".", return dataset will be flattened.
        :param directory: Optional[str] If set, logs will be exported to a file in the given directory.
        :param file_prefix: Optional[str] Prefix to name the exported file. Required if directory is set.
        :param data_size_limit: Optional[str] The maximum size of the exported data in MB.
            Size includes all files within the provided directory. By default, the data_size_limit will be set to 100MB.
        :param arrow: Optional[bool] If set to True, return logs as an Arrow Table. Else, returns Pandas DataFrame.
        :return: Tuple[Union[pa.Table, pd.DataFrame, LogEntries], str] The logs and status.
        """
        base = self.api_endpoint + f"/v1/logs/topic/" + topic

        headers, params = self._build_headers_and_params(
            limit=limit,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            dataset=dataset,
            dataset_exclude=dataset_exclude,
            dataset_separator=dataset_separator,
        )
        if file_prefix is not None and directory is not None:
            self._export_logs(
                base=base,
                directory=directory,
                file_prefix=file_prefix,
                data_size_limit=data_size_limit,
                params=params,
                headers=headers,
                limit=limit,
                arrow=arrow,
            )
            return None, None
        if is_arrow_enabled():
            response = self._get_next_records(
                params=params, iterator={}, headers=headers, base=base
            )
            entries, _, status = self._extract_logs_from_response(response)
            return entries if arrow else entries.to_pandas(), status
        else:
            if limit is None:
                limit = DEFAULT_RECORDS_LIMIT
            response_parts = requests.get(base, auth=self.auth)
            partitions = response_parts.json()["partitions"]

            iterator = {
                k: max(0, span["end"] - math.floor(limit / len(partitions)))
                for k, span in partitions.items()
            }
            response = self._get_next_records(
                params=params, iterator=iterator, headers=headers, base=base
            )
            response_json = response.json()
            return (
                LogEntries([LogEntry(json.loads(l)) for l in response_json["records"]]),
                response_json.get("status", "None"),
            )

    def security_logs(self, limit: int) -> List[dict]:
        """This function is not available in this release"""
        raise RuntimeError("security_log() is not available in this release.")

    def get_raw_logs(
        self,
        topic: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        limit: int = 100_000,
        parse: bool = False,
        dataset: Optional[List[str]] = None,
        dataset_exclude: Optional[List[str]] = None,
        dataset_separator: Optional[str] = None,
        verbose: bool = False,
    ) -> Union[List[Dict[str, Any]], pd.DataFrame]:
        """Gets logs from Plateau for a particular time window without attempting
        to convert them to Inference LogEntries. Logs can be returned as strings
        or the json parsed into lists and dicts.
        :param topic str: The name of the topic to query
        :param start Optional[datetime]: The start of the time window
        :param end Optional[datetime]: The end of the time window
        :param limit int: The number of records to retrieve. Note retrieving many
            records may be a performance bottleneck.
        :param parse bool: Wether to attempt to parse the string as a json object.
        :param verbose bool: Prints out info to help diagnose issues.
        """

        assert limit <= 1_000_000

        base = self.api_endpoint + f"/v1/logs/topic/" + topic
        headers = {"User-Agent": _user_agent}
        resp = requests.get(base, auth=self.auth, headers=headers)
        if resp.status_code != 200:
            raise EntityNotFoundError(
                f"Could not get partitions {resp.text}", {"url": base}
            )
        data = resp.json()
        partitions = data["partitions"]

        if verbose:
            print(f"Got partitions {partitions}")

        params: Dict[str, Any] = {"page_size": limit}
        if start is not None:
            start_str = start.astimezone(tz=timezone.utc).isoformat()
            params["time.start"] = start_str
        if end is not None:
            end_str = end.astimezone(tz=timezone.utc).isoformat()
            params["time.end"] = end_str

        if len(partitions) == 0:
            next: Optional[Dict[str, int]] = None
        else:
            sizes = [
                sz + excess
                for sz, excess in zip(
                    repeat(limit // len(partitions), len(partitions)),
                    chain(repeat(1, limit % len(partitions)), repeat(0)),
                )
            ]

            next = {
                k: max(0, span["end"] - sz)
                for (k, span), sz in zip(partitions.items(), sizes)
            }

        if is_arrow_enabled():
            headers.update({"Accept": ARROW_CONTENT_TYPE})
            params["dataset[]"] = dataset or ["*"]
            if dataset_exclude is not None:
                params["dataset.exclude[]"] = dataset_exclude
            if dataset_separator is not None:
                params["dataset.separator"] = dataset_separator  # type: ignore
        else:
            headers.update({"Accept": JSON_CONTENT_TYPE})

        if verbose:
            print("Using params: ", params)
            print("Using iterators: ", next)

        records = []
        while next is not None:
            resp = requests.post(
                base + "/records",
                params=params,
                json=next,
                auth=self.auth,
                headers=headers,
            )
            if resp.status_code != 200:
                raise EntityNotFoundError(
                    f"Could not get records {resp.text}",
                    {"url": base, "params": str(params), "iterator": str(next)},
                )

            if verbose:
                print("response: ", resp)

            if is_arrow_enabled():
                with pa.ipc.open_file(resp.content) as reader:
                    entries_df = reader.read_pandas()
                    if len(entries_df) > 0:
                        records.append(entries_df)
                        next = json.loads(reader.schema.metadata[b"status"])["next"]
                    else:
                        next = None
            else:
                result = resp.json()
                result_records = result["records"]
                if len(result_records) > 0:
                    records.extend(result_records)
                    next = result["next"]
                else:
                    next = None

        if is_arrow_enabled():
            return pd.concat(records) if len(records) > 0 else pd.DataFrame()
        if parse:
            return [json.loads(r) for r in records]
        return records

    def get_raw_pipeline_inference_logs(
        self,
        topic: str,
        start: datetime,
        end: datetime,
        model_name: Optional[str] = None,
        limit: int = 100_000,
        verbose: bool = False,
    ) -> List[Union[Dict[str, Any], pd.DataFrame]]:
        """Gets logs from Plateau for a particular time window and filters them for
        the model specified.
        :param pipeline_name str: The name/pipeline_id of the pipeline to query
        :param topic str: The name of the topic to query
        :param start Optional[datetime]: The start of the time window
        :param end Optional[datetime]: The end of the time window
        :param model_id: The name of the specific model to filter if any
        :param limit int: The number of records to retrieve. Note retrieving many
            records may be a performance bottleneck.
        :param verbose bool: Prints out info to help diagnose issues.
        """
        logs = self.get_raw_logs(
            topic,
            start=start,
            end=end,
            limit=limit,
            parse=True,
            verbose=verbose,
        )

        if verbose:
            print(f"Got {len(logs)} initial logs")

        if len(logs) == 0:
            return logs

        if model_name:
            if isinstance(logs, pd.DataFrame):
                logs = logs[
                    logs["metadata"].map(
                        lambda md: json.loads(md["last_model"])["model_name"]
                    )
                    == model_name
                ]
            else:
                logs = [l for l in logs if l["model_name"] == model_name]

        # inference results are a unix timestamp in millis - filter by that
        start_ts = int(start.timestamp() * 1000)
        end_ts = int(end.timestamp() * 1000)

        if isinstance(logs, pd.DataFrame):
            logs = logs[(start_ts <= logs["time"]) & (logs["time"] < end_ts)]
        else:
            logs = [l for l in logs if start_ts <= l["time"] < end_ts]

        return logs

    def get_pipeline_inference_dataframe(
        self,
        topic: str,
        start: datetime,
        end: datetime,
        model_name: Optional[str] = None,
        limit: int = 100_000,
        verbose=False,
    ) -> pd.DataFrame:
        logs = self.get_raw_pipeline_inference_logs(
            topic, start, end, model_name, limit, verbose
        )
        if isinstance(logs, pd.DataFrame):
            return nested_df_to_flattened_df(logs)

        return inference_logs_to_dataframe(logs)

    def get_assay_results(
        self,
        assay_id: Union[str, int],
        start: datetime,
        end: datetime,
    ) -> AssayAnalysisList:
        """Gets the assay results for a particular time window, parses them, and returns an
        List of AssayAnalysis.
        :param assay_id: int The id of the assay we are looking for.
        :param start: datetime The start of the time window. If timezone info not set, uses UTC timezone by default.
        :param end: datetime The end of the time window. If timezone info not set, uses UTC timezone by default.
        """

        # We don't need the assays v2 flag here. Leaving it out ensures compatibility if it's not enabled.
        if isinstance(assay_id, str):
            return AssayV2(self, id=assay_id).results(start=start, end=end)

        res = assays_get_assay_results.sync(
            client=self.mlops(),
            body=assays_get_assay_results_body.AssaysGetAssayResultsBody(
                assay_id, ensure_tz(start), ensure_tz(end)
            ),
        )

        if res is None:
            raise Exception("Failed to list models")

        if not isinstance(res, List):
            raise Exception(res.msg)

        if len(res) != 0 and not isinstance(
            res[0], AssaysGetAssayResultsResponse200Item
        ):
            raise Exception("invalid response")
        return AssayAnalysisList(
            [AssayAnalysis(client=self, raw=v.to_dict()) for v in res]
        )

    def build_assay(
        self,
        *,
        assay_name: str,
        pipeline: Pipeline,
        iopath: str,
        model_name: Optional[str] = None,
        baseline_start: Optional[datetime] = None,
        baseline_end: Optional[datetime] = None,
        baseline_data: Optional[np.ndarray] = None,
    ) -> AssayBuilder:
        """Creates an AssayBuilder that can be used to configure and create
        Assays.
        :param assay_name: str Human friendly name for the assay
        :param pipeline: Pipeline The pipeline this assay will work on
        :param iopath: str The path to the input or output of the model that this assay will monitor.
        :param model_name: Optional[str] The name of the model to use for the assay.
        :param baseline_start: Optional[datetime] The start time for the inferences to
            use as the baseline
        :param baseline_end: Optional[datetime] The end time of the baseline window.
        the baseline. Windows start immediately after the baseline window and
        are run at regular intervals continuously until the assay is deactivated
        or deleted.
        :param baseline_data: Optional[np.ndarray] Use this to load existing baseline data at assay creation time.
        """
        assay_builder = AssayBuilder(
            client=self,
            name=assay_name,
            pipeline_id=pipeline.id(),
            pipeline_name=pipeline.name(),
            model_name=model_name,
            iopath=iopath,
            baseline_start=baseline_start,
            baseline_end=baseline_end,
            baseline_data=baseline_data,
        )

        return assay_builder

    def upload_assay(self, config: AssayConfig) -> int:
        """Creates an assay in the database.
        :param config AssayConfig: The configuration for the assay to create.
        :return assay_id: The identifier for the assay that was created.
        :rtype int
        """

        if is_assays_v2_enabled():
            return self._schedule_assay_v2_from_v1(config).id

        data = assays_create.sync(
            client=self.mlops(),
            body=AssaysCreateBody.from_dict(
                {
                    **json.loads(config.to_json()),
                    "created_at": datetime.now(timezone.utc).isoformat(),
                }
            ),
        )

        if data is None:
            raise Exception("Failed to create assay")

        if not isinstance(data, AssaysCreateResponse200):
            raise Exception(data)

        return data.assay_id

    def list_assays(self) -> List[Assay]:
        """List all assays on the platform.

        :return: A list of all assays on the platform.
        :rtype: List[Assay]
        """
        if is_assays_v2_enabled():
            return self._list_assays_v2()

        res = assays_list.sync(client=self.mlops(), body=AssaysListBody(UNSET))

        if res is None:
            raise Exception("Failed to get assays")

        if not isinstance(res, List):
            raise Exception(res.msg)

        return Assays([Assay(client=self, data=v.to_dict()) for v in res])

    def get_assay_info(self, assay_id: Union[int, str]) -> pd.DataFrame:
        """Get information about a specific assay.

        :param assay_id: int The identifier for the assay to retrieve.
        :return: The assay with the given identifier
        :rtype: Assay
        """
        if isinstance(assay_id, str):
            return AssayV2(self, id=assay_id)
        return Assay.get_assay_info(client=self, assay_id=assay_id)

    def set_assay_active(self, assay_id: Union[int, str], active: bool) -> None:
        """Sets the state of an assay to active or inactive.
        :param assay_id: int The id of the assay to set the active state of.
        :param active: bool The active state to set the assay to. Default is True.
        """
        if isinstance(assay_id, str):
            return AssayV2(self, assay_id).set_active(active)

        res = assays_set_active.sync(
            client=self.mlops(),
            body=AssaysSetActiveBody(assay_id, active),
        )

        if res is None:
            raise Exception("Failed to set assay active")

        if not isinstance(res, AssaysSetActiveResponse200):
            raise Exception(res.msg)

    def _list_assays_v2(self):
        from .wallaroo_ml_ops_api_client.api.assays.get import sync, GetBody
        from .wallaroo_ml_ops_api_client.models.filter_on_active import FilterOnActive

        ret = sync(client=self.mlops(), body=GetBody(FilterOnActive.ALL))
        return AssayV2List([AssayV2(client=self, id=x.id) for x in ret])

    def _schedule_assay_v2_from_v1(
        self,
        config: AssayConfig,
    ):
        name = config.name
        config_summarizer = cast(UnivariateContinousSummarizerConfig, config.summarizer)

        # Baseline
        parsed_path = unwrap(config.window.path).split()
        prefix = "in" if parsed_path[0] == "input" else "out"

        iopath = f"{prefix}.{parsed_path[1]}.{parsed_path[2]}"
        baseline = cast(Union[None, SummaryBaseline, V2StaticBaseline], None)
        # TODO: if baseline.start is specified, send to assays v2 instead of using computed.
        baseline_start_at = cast(Optional[datetime], None)
        baseline_end_at = cast(Optional[datetime], None)

        if isinstance(config.baseline, V1CalculatedBaseline) or isinstance(
            config.baseline, V1FixedBaseline
        ):
            start = cast(
                str, config.baseline.calculated["fixed_window"].get("start_at")
            )
            baseline_start_at = dateutil.parser.parse(start)
            end = cast(str, config.baseline.calculated["fixed_window"].get("end_at"))
            baseline_end_at = dateutil.parser.parse(end)
        elif isinstance(config.baseline, V1StaticBaseline):
            start = cast(str, config.baseline.static.get("start"))
            baseline_start_at = dateutil.parser.parse(start)
            end = cast(str, config.baseline.static.get("end"))
            baseline_end_at = dateutil.parser.parse(end)
            baseline = SummaryBaseline.from_v1_summary(
                config.baseline, config_summarizer, iopath
            )

        if baseline is None:
            raise Exception("Failed to parse Baseline from v1 config")

        # Scheduling
        # if interval is None, legacy behavior is to be the same as width.
        interval = (
            config.window.interval if config.window.interval else config.window.width
        )

        first_run = (
            config.window.start
            if config.window.start
            else (baseline_end_at if baseline_end_at else datetime.now(timezone.utc))
        )

        run_frequency = cast(Optional[PGInterval], None)
        [count, unit] = interval.split()
        if unit == "minutes" or unit == "minute":
            run_frequency = PGInterval(quantity=int(count), unit=IntervalUnit.MINUTE)
        elif unit == "hours" or unit == "hour":
            run_frequency = PGInterval(quantity=int(count), unit=IntervalUnit.HOUR)
        elif unit == "days" or unit == "day":
            run_frequency = PGInterval(quantity=int(count), unit=IntervalUnit.DAY)
        elif unit == "weeks" or unit == "week":
            run_frequency = PGInterval(quantity=int(count), unit=IntervalUnit.WEEK)

        if run_frequency is None:
            raise Exception(
                "Failed to parse the run frequency for this assay.", interval
            )

        sched = Scheduling(
            first_run=first_run,
            run_frequency=RunFrequencyType1(simple_run_frequency=run_frequency),
            end=config.run_until,
        )

        # Targeting
        targeting = Targeting._from_v1_config(config)

        # Window - Convert width to seconds
        dur = None
        [count, unit] = config.window.width.split()
        if unit == "minutes" or unit == "minute":
            dur = int(count) * 60
        elif unit == "hours" or unit == "hour":
            dur = int(count) * 60 * 60
        elif unit == "days" or unit == "day":
            dur = int(count) * 60 * 60 * 24
        elif unit == "weeks" or unit == "week":
            dur = int(count) * 60 * 60 * 24 * 7

        window = RollingWindow(width=WindowWidthDuration(seconds=unwrap(dur)))

        # Summarizer
        summarizer = Summarizer.from_v1_summarizer(config_summarizer)

        ret = sync(
            client=self.mlops(),
            body=ScheduleBody(
                name=name,
                baseline=baseline,
                scheduling=sched,
                summarizer=summarizer,
                targeting=targeting,
                window=window,
            ),
        )

        if ret.parsed is None:
            raise Exception("Failed to create V2 assay from a V1 config.", ret)

        return AssayV2(client=self, id=ret.parsed)

    def create_tag(self, tag_text: str) -> Tag:
        """Create a new tag with the given text."""
        assert tag_text is not None
        return Tag._create_tag(client=self, tag_text=tag_text)

    def create_workspace(self, workspace_name: str) -> Workspace:
        """Create a new workspace with the current user as its first owner.

        :param str workspace_name: Name of the workspace, must be composed of ASCII
           alpha-numeric characters plus dash (-)"""
        assert workspace_name is not None
        require_dns_compliance(workspace_name)
        return Workspace._create_workspace(client=self, name=workspace_name)

    def list_workspaces(self) -> List[Workspace]:
        """List all workspaces on the platform which this user has permission see.

        :return: A list of all workspaces on the platform.
        :rtype: List[Workspace]
        """
        return Workspace.list_workspaces(self)

    def get_workspace(
        self, name: str, create_if_not_exist: Optional[bool] = False
    ) -> Optional[Workspace]:
        """
        Get a workspace by name. If the workspace does not exist, create it.
        :param name: The name of the workspace to get.
        :param create_if_not_exist: If set to True, create a new workspace if workspace by given name doesn't already exist.
            Set to False by default.
        :return: The workspace with the given name.
        """
        return Workspace.get_workspace(
            client=self, name=name, create_if_not_exist=create_if_not_exist
        )

    def set_current_workspace(self, workspace: Workspace) -> Workspace:
        """Any calls involving pipelines or models will use the given workspace from then on."""
        assert workspace is not None
        if not isinstance(workspace, Workspace):
            raise TypeError("Workspace type was expected")

        self._current_workspace = workspace
        return cast("Workspace", self._current_workspace)

    def get_current_workspace(self) -> Workspace:
        """Return the current workspace.  See also `set_current_workspace`."""
        if self._current_workspace is None:
            # Is there a default? Use that or make one.
            default_ws = Workspace._get_user_default_workspace(self)
            if default_ws is not None:
                self._current_workspace = default_ws
            else:
                self._current_workspace = Workspace._create_user_default_workspace(self)

        return cast("Workspace", self._current_workspace)

    def invite_user(self, email, password=None):
        return User.invite_user(
            email, password, self.auth, self.api_endpoint, self.auth_endpoint
        )

    def get_topic_name(self, pipeline_pk_id: int) -> str:
        return self._post_rest_api(
            "v1/api/plateau/get_topic_name",
            {
                "pipeline_pk_id": pipeline_pk_id,
            },
        ).json()["topic_name"]

    def shim_token(self, token_data: auth.TokenData):
        fetcher = auth._RawTokenFetcher(token_data)
        self.auth = auth._PlatformAuth(fetcher)

    def list_orchestrations(self):
        """List all Orchestrations in the current workspace.

        :return: A List containing all Orchestrations in the current workspace.
        """
        return Orchestration.list_orchestrations(self)

    def upload_orchestration(
        self,
        bytes_buffer: Optional[bytes] = None,
        path: Optional[str] = None,
        name: Optional[str] = None,
        file_name: Optional[str] = None,
    ):
        """Upload a file to be packaged and used as an Orchestration.

        The uploaded artifact must be a ZIP file which contains:

        * User code. If `main.py` exists, then that will be used as the task entrypoint. Otherwise,
          the first `main.py` found in any subdirectory will be used as the entrypoint.
        * Optional: A standard Python `requirements.txt` for any dependencies to be provided in the
          task environment. The Wallaroo SDK will already be present and should not be mentioned.
          Multiple `requirements.txt` files are not allowed.
        * Optional: Any other artifacts desired for runtime, including data or code.

        :param Optional[str] path: The path to the file on your filesystem that will be uploaded as an Orchestration.
        :param Optional[bytes] bytes_buffer: The raw bytes to upload to be used Orchestration. Cannot be used with the `path` param.
        :param Optional[str] name: An optional descriptive name for this Orchestration.
        :param Optional[str] file_name: An optional filename to describe your Orchestration when using the bytes_buffer param. Ignored when `path` is used.
        :return: The Orchestration that was uploaded.
        :raises OrchestrationUploadFailed If a server-side error prevented the upload from succeeding.

        """
        return Orchestration.upload(
            self, bytes_buffer=bytes_buffer, path=path, name=name, file_name=file_name
        )

    def list_tasks(self, killed: bool = False):
        """List all Tasks in the current Workspace.

        :return: A List containing Task objects."""
        return Task.list_tasks(self, self.get_current_workspace().id(), killed=killed)

    def get_task_by_id(self, task_id: str):
        """Retrieve a Task by its ID.

        :param str task_id: The ID of the Task to retrieve.
        :return: A Task object."""
        return Task.get_task_by_id(self, task_id)

    def in_task(self) -> bool:
        """Determines if this code is inside an orchestration task.

        :return: True if running in a task."""
        return self._in_task

    def task_args(self) -> Dict[Any, Any]:
        """When running inside a task (see `in_task()`), obtain arguments passed to the task.

        :return: Dict of the arguments"""
        with open(self._task_args_filename, "rb") as fp:
            return json.load(fp)

    def list_connections(self) -> ConnectionList:
        """List all Connections defined in the platform.
        :return: List of Connections in the whole platform.
        """
        return Connection.list_connections(self)

    def get_connection(self, name=str) -> Connection:
        """Retrieves a Connection by its name.
        :return: Connection to an external data source.
        """
        return Connection.get_connection(self, name=name)

    def create_connection(
        self, name=str, connection_type=str, details=Dict[str, Any]
    ) -> Connection:
        """Creates a Connection with the given name, type, and type-specific details.
        :return: Connection to an external data source.
        """
        return Connection.create_connection(
            self, name=name, connection_type=connection_type, details=details
        )

    def create_model_registry(
        self, name: str, token: str, url: str, workspace_id: Optional[int] = None
    ) -> ModelRegistry:
        """Create a Model Registry connection in this workspace that can be reused across workspaces.

        :param: name str A descriptive name for this registry
        :param: token str A Bearer token necessary for accessing this Registry.
        :param: url str The root URL for this registry. It should NOT include `/api/2.0/mlflow` as part of it.
        :param: workspace_id int The ID of the workspace to attach this registry to, i.e. `client.get_current_workspace().id()`.
        :return: A ModelRegistry object.
        """
        from .wallaroo_ml_ops_api_client.api.model.create_registry import (
            sync_detailed as sync,
            CreateRegistryWithoutWorkspaceRequest,
        )

        ret = sync(
            client=self.mlops(),
            body=CreateRegistryWithoutWorkspaceRequest(
                name=name,
                token=token,
                url=url,
                workspace_id=workspace_id,
            ),
        )

        if ret.parsed is None:
            raise Exception("Failed to create Model Registry connection.", ret.content)

        return ModelRegistry(client=self, data={"id": ret.parsed.id})

    def list_model_registries(self, workspace_id: Optional[int] = None):
        from .wallaroo_ml_ops_api_client.api.model.list_registries import sync
        from .wallaroo_ml_ops_api_client.models.list_registries_request import (
            ListRegistriesRequest,
        )

        workspace_id = (
            workspace_id
            if workspace_id is not None
            else self.get_current_workspace()._id
        )
        ret = sync(
            client=self.mlops(),
            body=ListRegistriesRequest(workspace_id=workspace_id),
        )

        if ret is None:
            raise Exception("Failed to list all Model Registries")

        return ModelRegistriesList([ModelRegistry(self, d.to_dict()) for d in ret])

    def get_email_by_id(self, id: str):
        return User.get_email_by_id(client=self, id=id)

    def remove_edge(
        self,
        name: str,
    ):
        """Remove an edge to a published pipeline.

        :param str name: The name of the edge that will be removed. This is not limited to this pipeline.
        """

        res = removeEdgeSync(
            client=self.mlops(),
            body=RemoveEdgeBody(
                name=name,
                # pipeline_publish_id=self.id,
            ),
        )
        if res.status_code != HTTPStatus.OK:
            raise Exception("Failed to remove edge to published pipeline.", res.content)

    def _post_rest_api_json(self, uri: str, body: dict):
        result = self._post_rest_api(uri, body)
        if result.status_code == 200:
            return result.json()
        else:
            raise Exception(f"{result.status_code}: {result.text}")

    def _setup_mlops_client(self) -> "MLOpsClient":
        headers = {
            "user-agent": _user_agent,
        }
        self._mlops = MLOpsClient(
            base_url=self.api_endpoint,
            token=self.auth._access_token().token,
            headers=headers,
        ).with_timeout(httpx.Timeout(60, connect=5.0))
        return self._mlops

    def mlops(self) -> "MLOpsClient":
        return self._setup_mlops_client()
