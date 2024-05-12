"""Contains all the data models used in inputs/outputs"""

from .augmented_bot_user import AugmentedBotUser
from .chat import Chat
from .chat_creation_response import ChatCreationResponse
from .chat_delete_result import ChatDeleteResult
from .chat_result import ChatResult
from .chat_settings import ChatSettings
from .get_chat_by_title_request import GetChatByTitleRequest
from .login_info import LoginInfo
from .message import Message
from .paginated_chat_result_list import PaginatedChatResultList
from .paginated_message_list import PaginatedMessageList
from .paginated_user_profile_list import PaginatedUserProfileList
from .patched_user_profile import PatchedUserProfile
from .person import Person
from .register_bot import RegisterBot
from .register_response_success import RegisterResponseSuccess
from .send_message import SendMessage
from .set_chat_title_request import SetChatTitleRequest
from .user_profile import UserProfile
from .user_self import UserSelf

__all__ = (
    "AugmentedBotUser",
    "Chat",
    "ChatCreationResponse",
    "ChatDeleteResult",
    "ChatResult",
    "ChatSettings",
    "GetChatByTitleRequest",
    "LoginInfo",
    "Message",
    "PaginatedChatResultList",
    "PaginatedMessageList",
    "PaginatedUserProfileList",
    "PatchedUserProfile",
    "Person",
    "RegisterBot",
    "RegisterResponseSuccess",
    "SendMessage",
    "SetChatTitleRequest",
    "UserProfile",
    "UserSelf",
)
