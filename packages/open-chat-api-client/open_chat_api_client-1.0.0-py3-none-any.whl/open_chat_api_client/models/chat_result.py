import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.chat_settings import ChatSettings
    from ..models.message import Message
    from ..models.user_profile import UserProfile


T = TypeVar("T", bound="ChatResult")


@_attrs_define
class ChatResult:
    """
    Attributes:
        uuid (str):
        created (datetime.datetime):
        newest_message (Message):
        unread_count (int):
        partner (UserProfile):
        settings (Union[Unset, ChatSettings]):
    """

    uuid: str
    created: datetime.datetime
    newest_message: "Message"
    unread_count: int
    partner: "UserProfile"
    settings: Union[Unset, "ChatSettings"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        uuid = self.uuid

        created = self.created.isoformat()

        newest_message = self.newest_message.to_dict()

        unread_count = self.unread_count

        partner = self.partner.to_dict()

        settings: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.settings, Unset):
            settings = self.settings.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "created": created,
                "newest_message": newest_message,
                "unread_count": unread_count,
                "partner": partner,
            }
        )
        if settings is not UNSET:
            field_dict["settings"] = settings

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.chat_settings import ChatSettings
        from ..models.message import Message
        from ..models.user_profile import UserProfile

        d = src_dict.copy()
        uuid = d.pop("uuid")

        created = isoparse(d.pop("created"))

        newest_message = Message.from_dict(d.pop("newest_message"))

        unread_count = d.pop("unread_count")

        partner = UserProfile.from_dict(d.pop("partner"))

        _settings = d.pop("settings", UNSET)
        settings: Union[Unset, ChatSettings]
        if isinstance(_settings, Unset):
            settings = UNSET
        else:
            settings = ChatSettings.from_dict(_settings)

        chat_result = cls(
            uuid=uuid,
            created=created,
            newest_message=newest_message,
            unread_count=unread_count,
            partner=partner,
            settings=settings,
        )

        chat_result.additional_properties = d
        return chat_result

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
