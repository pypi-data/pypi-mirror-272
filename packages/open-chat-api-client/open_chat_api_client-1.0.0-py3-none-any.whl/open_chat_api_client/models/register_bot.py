from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RegisterBot")


@_attrs_define
class RegisterBot:
    """
    Attributes:
        username (str):
        password (str):
        password_confirm (str):
        first_name (Union[Unset, str]):  Default: 'Bot'.
        second_name (Union[Unset, str]):  Default: 'Bot'.
        public (Union[Unset, bool]):  Default: False.
        description (Union[Unset, str]):  Default: "Hello there I'm a bot".
        description_title (Union[Unset, str]):  Default: 'About the bot:'.
        reveal_secret (Union[Unset, str]):  Default: 'password'.
        contact_password (Union[None, Unset, str]):  Default: 'password'.
    """

    username: str
    password: str
    password_confirm: str
    first_name: Union[Unset, str] = "Bot"
    second_name: Union[Unset, str] = "Bot"
    public: Union[Unset, bool] = False
    description: Union[Unset, str] = "Hello there I'm a bot"
    description_title: Union[Unset, str] = "About the bot:"
    reveal_secret: Union[Unset, str] = "password"
    contact_password: Union[None, Unset, str] = "password"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        username = self.username

        password = self.password

        password_confirm = self.password_confirm

        first_name = self.first_name

        second_name = self.second_name

        public = self.public

        description = self.description

        description_title = self.description_title

        reveal_secret = self.reveal_secret

        contact_password: Union[None, Unset, str]
        if isinstance(self.contact_password, Unset):
            contact_password = UNSET
        else:
            contact_password = self.contact_password

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "username": username,
                "password": password,
                "password_confirm": password_confirm,
            }
        )
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if second_name is not UNSET:
            field_dict["second_name"] = second_name
        if public is not UNSET:
            field_dict["public"] = public
        if description is not UNSET:
            field_dict["description"] = description
        if description_title is not UNSET:
            field_dict["description_title"] = description_title
        if reveal_secret is not UNSET:
            field_dict["reveal_secret"] = reveal_secret
        if contact_password is not UNSET:
            field_dict["contact_password"] = contact_password

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        username = d.pop("username")

        password = d.pop("password")

        password_confirm = d.pop("password_confirm")

        first_name = d.pop("first_name", UNSET)

        second_name = d.pop("second_name", UNSET)

        public = d.pop("public", UNSET)

        description = d.pop("description", UNSET)

        description_title = d.pop("description_title", UNSET)

        reveal_secret = d.pop("reveal_secret", UNSET)

        def _parse_contact_password(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        contact_password = _parse_contact_password(d.pop("contact_password", UNSET))

        register_bot = cls(
            username=username,
            password=password,
            password_confirm=password_confirm,
            first_name=first_name,
            second_name=second_name,
            public=public,
            description=description,
            description_title=description_title,
            reveal_secret=reveal_secret,
            contact_password=contact_password,
        )

        register_bot.additional_properties = d
        return register_bot

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
