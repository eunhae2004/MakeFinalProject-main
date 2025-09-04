from typing import Dict, Any, Optional

from backend.app.services import storage
from backend.app.utils.errors import http_error


def get_me(user_id: str) -> Dict[str, Any]:
    user = storage.get_user_by_id(user_id)
    if not user:
        raise http_error("RESOURCE_NOT_FOUND", "user not found", status=404)
    return _public_user(user)


def patch_me(user_id: str, nickname: Optional[str] = None, avatar_url: Optional[str] = None) -> Dict[str, Any]:
    user = storage.get_user_by_id(user_id)
    if not user:
        raise http_error("RESOURCE_NOT_FOUND", "user not found", status=404)

    updates = {}
    if nickname is not None:
        updates["nickname"] = nickname
    if avatar_url is not None:
        updates["avatar_url"] = avatar_url

    if updates:
        updates["updated_at"] = storage.utcnow_iso()

    updated = storage.update_user(user_id, updates) or user
    return _public_user(updated)


def _public_user(user: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": user["id"],
        "email": user["email"],
        "nickname": user.get("nickname"),
        "avatar_url": user.get("avatar_url"),
        "created_at": user.get("created_at"),
        "updated_at": user.get("updated_at"),
    }
