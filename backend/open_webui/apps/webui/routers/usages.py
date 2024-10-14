import logging
from typing import Optional
from open_webui.apps.webui.models.chats import Chats
from open_webui.apps.webui.models.users import (
    Users,
)
from open_webui.apps.webui.models.usages import (
    UsageModel,
    Usages,
)
from open_webui.constants import ERROR_MESSAGES
from open_webui.env import SRC_LOG_LEVELS
from fastapi import APIRouter, Depends, HTTPException, status
from open_webui.utils.utils import get_admin_user

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MODELS"])

router = APIRouter()

############################
# GetUsages
############################


@router.get("/", response_model=list[UsageModel])
async def get_usages(page: Optional[int] = None, user=Depends(get_admin_user)):
    limit = 100
    skip = page * limit
    return Usages.get_usages(skip, limit)


############################
# GetUsagesByUserId
############################


@router.get("/{user_id}", response_model=list[UsageModel])
async def get_user_by_id(
    user_id: str, page: Optional[int] = None, user=Depends(get_admin_user)
):
    # Check if user_id is a shared chat
    # If it is, get the user_id from the chat
    if user_id.startswith("shared-"):
        chat_id = user_id.replace("shared-", "")
        chat = Chats.get_chat_by_id(chat_id)
        if chat:
            user_id = chat.user_id
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ERROR_MESSAGES.USER_NOT_FOUND,
            )

    user = Users.get_user_by_id(user_id)

    if user:
        limit = 100
        skip = page * limit
        return Usages.get_usages_by_user_id(user_id, skip, limit)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.USER_NOT_FOUND,
        )
