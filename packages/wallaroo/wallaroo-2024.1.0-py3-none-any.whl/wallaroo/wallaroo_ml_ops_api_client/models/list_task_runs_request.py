from typing import (
    Any,
    Dict,
    List,
    Type,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.list_task_runs_request_status import ListTaskRunsRequestStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListTaskRunsRequest")


@_attrs_define
class ListTaskRunsRequest:
    """
    Attributes:
        task_id (str):
        limit (Union[None, Unset, int]):
        status (Union[ListTaskRunsRequestStatus, None, Unset]):
    """

    task_id: str
    limit: Union[None, Unset, int] = UNSET
    status: Union[ListTaskRunsRequestStatus, None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        task_id = self.task_id

        limit: Union[None, Unset, int]
        if isinstance(self.limit, Unset):
            limit = UNSET
        else:
            limit = self.limit

        status: Union[None, Unset, str]
        if isinstance(self.status, Unset):
            status = UNSET
        elif isinstance(self.status, ListTaskRunsRequestStatus):
            status = self.status.value
        else:
            status = self.status

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "task_id": task_id,
            }
        )
        if limit is not UNSET:
            field_dict["limit"] = limit
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        task_id = d.pop("task_id")

        def _parse_limit(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        limit = _parse_limit(d.pop("limit", UNSET))

        def _parse_status(
            data: object,
        ) -> Union[ListTaskRunsRequestStatus, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_1 = ListTaskRunsRequestStatus(data)

                return status_type_1
            except:  # noqa: E722
                pass
            return cast(Union[ListTaskRunsRequestStatus, None, Unset], data)

        status = _parse_status(d.pop("status", UNSET))

        list_task_runs_request = cls(
            task_id=task_id,
            limit=limit,
            status=status,
        )

        list_task_runs_request.additional_properties = d
        return list_task_runs_request

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
