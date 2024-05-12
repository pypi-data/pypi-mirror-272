import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserProfile")


@_attrs_define
class UserProfile:
    """
    Attributes:
        first_name (str):
        second_name (str):
        last_updated (datetime.datetime):
        is_online (bool):  Default: False.
        uuid (str):
        reqires_contact_password (bool):  Default: False.
        public (Union[Unset, bool]):
        description_title (Union[Unset, str]):
        description (Union[Unset, str]):
        image (Union[None, Unset, str]):
        is_bot (Union[Unset, bool]):
    """

    first_name: str
    second_name: str
    last_updated: datetime.datetime
    uuid: str
    is_online: bool = False
    reqires_contact_password: bool = False
    public: Union[Unset, bool] = UNSET
    description_title: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    image: Union[None, Unset, str] = UNSET
    is_bot: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        first_name = self.first_name

        second_name = self.second_name

        last_updated = self.last_updated.isoformat()

        is_online = self.is_online

        uuid = self.uuid

        reqires_contact_password = self.reqires_contact_password

        public = self.public

        description_title = self.description_title

        description = self.description

        image: Union[None, Unset, str]
        if isinstance(self.image, Unset):
            image = UNSET
        else:
            image = self.image

        is_bot = self.is_bot

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "first_name": first_name,
                "second_name": second_name,
                "last_updated": last_updated,
                "is_online": is_online,
                "uuid": uuid,
                "reqires_contact_password": reqires_contact_password,
            }
        )
        if public is not UNSET:
            field_dict["public"] = public
        if description_title is not UNSET:
            field_dict["description_title"] = description_title
        if description is not UNSET:
            field_dict["description"] = description
        if image is not UNSET:
            field_dict["image"] = image
        if is_bot is not UNSET:
            field_dict["is_bot"] = is_bot

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        first_name = d.pop("first_name")

        second_name = d.pop("second_name")

        last_updated = isoparse(d.pop("last_updated"))

        is_online = d.pop("is_online")

        uuid = d.pop("uuid")

        reqires_contact_password = d.pop("reqires_contact_password")

        public = d.pop("public", UNSET)

        description_title = d.pop("description_title", UNSET)

        description = d.pop("description", UNSET)

        def _parse_image(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        image = _parse_image(d.pop("image", UNSET))

        is_bot = d.pop("is_bot", UNSET)

        user_profile = cls(
            first_name=first_name,
            second_name=second_name,
            last_updated=last_updated,
            is_online=is_online,
            uuid=uuid,
            reqires_contact_password=reqires_contact_password,
            public=public,
            description_title=description_title,
            description=description,
            image=image,
            is_bot=is_bot,
        )

        user_profile.additional_properties = d
        return user_profile

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
