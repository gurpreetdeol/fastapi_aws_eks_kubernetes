from typing import List, Optional
from fastapi import HTTPException, status
from . import models


async def new_user_register(request, database) -> models.User:
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=request.password
    )
    database.add(new_user)
    database.commit()
    database.refresh(new_user)
    return new_user


async def all_users(database) -> List[models.User]:
    users = database.query(models.User).all()
    return users


async def get_user_by_id(user_id: int, database) -> Optional[models.User]:
    user_info = database.query(models.User).get(user_id)
    if not user_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} is not found")
    return user_info


async def delete_user_by_id(user_id: int, database):
    database.query(models.User).filter(models.User.id == user_id).delete(synchronize_session=False)
    database.commit()
