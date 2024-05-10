import datetime
from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="AssaysGetAssayResultsBody")


@_attrs_define
class AssaysGetAssayResultsBody:
    """Request to return assay results.

    Attributes:
        assay_id (int):
        start (datetime.datetime):
        end (datetime.datetime):
    """

    assay_id: int
    start: datetime.datetime
    end: datetime.datetime
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        assay_id = self.assay_id

        start = self.start.isoformat()

        end = self.end.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "assay_id": assay_id,
                "start": start,
                "end": end,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        assay_id = d.pop("assay_id")

        start = isoparse(d.pop("start"))

        end = isoparse(d.pop("end"))

        assays_get_assay_results_body = cls(
            assay_id=assay_id,
            start=start,
            end=end,
        )

        assays_get_assay_results_body.additional_properties = d
        return assays_get_assay_results_body

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
