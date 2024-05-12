from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.chat_result import ChatResult


T = TypeVar("T", bound="PaginatedChatResultList")


@_attrs_define
class PaginatedChatResultList:
    """
    Attributes:
        page_size (Union[Unset, int]): The number of items per page Example: 40.
        pages_total (Union[Unset, int]): The total number of pages Example: 1.
        items_total (Union[Unset, int]): The total number of items Example: 1.
        next_page (Union[Unset, int]): The next page number Example: 2.
        previous_page (Union[Unset, int]): The previous page number Example: 1.
        first_page (Union[Unset, int]): The first page number Example: 1.
        results (Union[Unset, List['ChatResult']]):
    """

    page_size: Union[Unset, int] = UNSET
    pages_total: Union[Unset, int] = UNSET
    items_total: Union[Unset, int] = UNSET
    next_page: Union[Unset, int] = UNSET
    previous_page: Union[Unset, int] = UNSET
    first_page: Union[Unset, int] = UNSET
    results: Union[Unset, List["ChatResult"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        page_size = self.page_size

        pages_total = self.pages_total

        items_total = self.items_total

        next_page = self.next_page

        previous_page = self.previous_page

        first_page = self.first_page

        results: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.results, Unset):
            results = []
            for results_item_data in self.results:
                results_item = results_item_data.to_dict()
                results.append(results_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if page_size is not UNSET:
            field_dict["page_size"] = page_size
        if pages_total is not UNSET:
            field_dict["pages_total"] = pages_total
        if items_total is not UNSET:
            field_dict["items_total"] = items_total
        if next_page is not UNSET:
            field_dict["next_page"] = next_page
        if previous_page is not UNSET:
            field_dict["previous_page"] = previous_page
        if first_page is not UNSET:
            field_dict["first_page"] = first_page
        if results is not UNSET:
            field_dict["results"] = results

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.chat_result import ChatResult

        d = src_dict.copy()
        page_size = d.pop("page_size", UNSET)

        pages_total = d.pop("pages_total", UNSET)

        items_total = d.pop("items_total", UNSET)

        next_page = d.pop("next_page", UNSET)

        previous_page = d.pop("previous_page", UNSET)

        first_page = d.pop("first_page", UNSET)

        results = []
        _results = d.pop("results", UNSET)
        for results_item_data in _results or []:
            results_item = ChatResult.from_dict(results_item_data)

            results.append(results_item)

        paginated_chat_result_list = cls(
            page_size=page_size,
            pages_total=pages_total,
            items_total=items_total,
            next_page=next_page,
            previous_page=previous_page,
            first_page=first_page,
            results=results,
        )

        paginated_chat_result_list.additional_properties = d
        return paginated_chat_result_list

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
