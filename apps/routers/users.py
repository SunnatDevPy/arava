from fastapi import APIRouter

from apps.models import User

user_router = APIRouter(prefix='/users', tags=['User'])


@user_router.get("/profile", name='user_profile')
async def user_profile(user_id: int):
    user = await User.get(user_id)
    return user
