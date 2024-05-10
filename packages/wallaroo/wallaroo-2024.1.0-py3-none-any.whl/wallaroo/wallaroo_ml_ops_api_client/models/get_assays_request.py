from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.filter_on_active import FilterOnActive
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetAssaysRequest")


@_attrs_define
class GetAssaysRequest:
    """
    Attributes:
        active (FilterOnActive):
        pipeline_name (Union[None, Unset, str]):
    """

    active: FilterOnActive
    pipeline_name: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        active = self.active.value

        pipeline_name: Union[None, Unset, str]
        if isinstance(self.pipeline_name, Unset):
            pipeline_name = UNSET
        else:
            pipeline_name = self.pipeline_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "active": active,
            }
        )
        if pipeline_name is not UNSET:
            field_dict["pipeline_name"] = pipeline_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        active = FilterOnActive(d.pop("active"))

        def _parse_pipeline_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        pipeline_name = _parse_pipeline_name(d.pop("pipeline_name", UNSET))

        get_assays_request = cls(
            active=active,
            pipeline_name=pipeline_name,
        )

        get_assays_request.additional_properties = d
        return get_assays_request

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
