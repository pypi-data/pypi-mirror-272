import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserSelf")


@_attrs_define
class UserSelf:
    """
    Attributes:
        id (int):
        uuid (str):
        username (str): Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.
        email (Union[Unset, str]):
        is_staff (Union[Unset, bool]): Designates whether the user can log into this admin site.
        is_superuser (Union[Unset, bool]): Designates that this user has all permissions without explicitly assigning
            them.
        date_joined (Union[Unset, datetime.datetime]):
        last_login (Union[None, Unset, datetime.datetime]):
        automated (Union[Unset, bool]):
    """

    id: int
    uuid: str
    username: str
    email: Union[Unset, str] = UNSET
    is_staff: Union[Unset, bool] = UNSET
    is_superuser: Union[Unset, bool] = UNSET
    date_joined: Union[Unset, datetime.datetime] = UNSET
    last_login: Union[None, Unset, datetime.datetime] = UNSET
    automated: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        uuid = self.uuid

        username = self.username

        email = self.email

        is_staff = self.is_staff

        is_superuser = self.is_superuser

        date_joined: Union[Unset, str] = UNSET
        if not isinstance(self.date_joined, Unset):
            date_joined = self.date_joined.isoformat()

        last_login: Union[None, Unset, str]
        if isinstance(self.last_login, Unset):
            last_login = UNSET
        elif isinstance(self.last_login, datetime.datetime):
            last_login = self.last_login.isoformat()
        else:
            last_login = self.last_login

        automated = self.automated

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "uuid": uuid,
                "username": username,
            }
        )
        if email is not UNSET:
            field_dict["email"] = email
        if is_staff is not UNSET:
            field_dict["is_staff"] = is_staff
        if is_superuser is not UNSET:
            field_dict["is_superuser"] = is_superuser
        if date_joined is not UNSET:
            field_dict["date_joined"] = date_joined
        if last_login is not UNSET:
            field_dict["last_login"] = last_login
        if automated is not UNSET:
            field_dict["automated"] = automated

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        uuid = d.pop("uuid")

        username = d.pop("username")

        email = d.pop("email", UNSET)

        is_staff = d.pop("is_staff", UNSET)

        is_superuser = d.pop("is_superuser", UNSET)

        _date_joined = d.pop("date_joined", UNSET)
        date_joined: Union[Unset, datetime.datetime]
        if isinstance(_date_joined, Unset):
            date_joined = UNSET
        else:
            date_joined = isoparse(_date_joined)

        def _parse_last_login(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_login_type_0 = isoparse(data)

                return last_login_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        last_login = _parse_last_login(d.pop("last_login", UNSET))

        automated = d.pop("automated", UNSET)

        user_self = cls(
            id=id,
            uuid=uuid,
            username=username,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            date_joined=date_joined,
            last_login=last_login,
            automated=automated,
        )

        user_self.additional_properties = d
        return user_self

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
