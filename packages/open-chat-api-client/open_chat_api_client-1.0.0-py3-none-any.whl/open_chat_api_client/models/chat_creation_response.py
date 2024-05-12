from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.chat import Chat
    from ..models.message import Message


T = TypeVar("T", bound="ChatCreationResponse")


@_attrs_define
class ChatCreationResponse:
    """
    Attributes:
        chat (Chat):
        message (Message):
    """

    chat: "Chat"
    message: "Message"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        chat = self.chat.to_dict()

        message = self.message.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "chat": chat,
                "message": message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.chat import Chat
        from ..models.message import Message

        d = src_dict.copy()
        chat = Chat.from_dict(d.pop("chat"))

        message = Message.from_dict(d.pop("message"))

        chat_creation_response = cls(
            chat=chat,
            message=message,
        )

        chat_creation_response.additional_properties = d
        return chat_creation_response

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
