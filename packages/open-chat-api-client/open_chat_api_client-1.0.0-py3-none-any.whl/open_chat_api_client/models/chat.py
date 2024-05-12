import datetime
from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="Chat")


@_attrs_define
class Chat:
    """
    Attributes:
        uuid (str):
        u1 (str):
        u2 (str):
        created (datetime.datetime):
    """

    uuid: str
    u1: str
    u2: str
    created: datetime.datetime
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        uuid = self.uuid

        u1 = self.u1

        u2 = self.u2

        created = self.created.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "u1": u1,
                "u2": u2,
                "created": created,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        uuid = d.pop("uuid")

        u1 = d.pop("u1")

        u2 = d.pop("u2")

        created = isoparse(d.pop("created"))

        chat = cls(
            uuid=uuid,
            u1=u1,
            u2=u2,
            created=created,
        )

        chat.additional_properties = d
        return chat

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
