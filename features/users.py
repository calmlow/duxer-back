import uuid

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Union
from calmlogging import get_logger
from db import select, upsert
from time import sleep

log = get_logger(__file__)


router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


class User(BaseModel):
    id: Union[str, None] = None
    name: str
    email: Union[str, None] = None
    is_admin: bool = False


@router.get("/")
async def get_users():
    """Get all users."""
    sleep(1)
    users = select('SELECT * FROM users')
    return {"users": users}


@router.post("/")
async def create_users(user: User):
    """Create a user"""
    query = '''
    INSERT INTO users
        (id, name, email, is_admin)
    VALUES
        (?, ?, ?, ?)
    '''
    id = str(uuid.uuid1())
    log.info("Will try to create following user: %s" % user)
    sleep(2)

    try:
        upsert(query, (id, user.name, user.email, user.is_admin))
    except Exception as e:
        log.error("Couldn't save user! %s: %s" % (e.__class__.__name__, e))
        raise HTTPException(
            status_code=400, detail=f"Couldn't save user! {e.__class__.__name__}: {e}")

    users = select(f"SELECT * FROM users WHERE id = '{id}' LIMIT 1")
    log.info("Successfully created user with id: %s. And sleeping 2 seconds" % id)

    return users[0]


@router.get("/{id}")
async def get_user(id: str):
    """Get a single user."""
    query = "SELECT * FROM users WHERE id = ? LIMIT 1"

    try:
        user = select(query, (str(id),))

        if user:
            return user[0]
        else:
            log.error("User not found!")
            raise HTTPException(
                status_code=404, detail=f"User with id '{id}' not found")
    except Exception as e:
        log.error("Couldn't get user! %s: %s" % (e.__class__.__name__, e))
        raise HTTPException(
            status_code=404, detail=f"User with id '{id}' not found")


@router.put("/{id}")
async def update_user(id: str, user: User):
    """Update a single user."""

    log.debug("Got request: %s" % user)
    log.debug("Updating user with id: %s" % id)
    query = '''UPDATE users
              SET name = ? ,
                  email = ? ,
                  is_admin = ?
              WHERE id = ?'''
    try:
        upsert(query, (user.name, user.email, user.is_admin, id))
        log.info("Successfully updated user with id: %s" % id)
        user.id = id
        return user
    except IndexError:
        raise HTTPException(
            status_code=404, detail=f"User with id '{id}' not found")


@router.delete("/{id}")
async def delete_user(id: str):
    """Delete a single user."""
    log.debug("Deleting a user with id: %s" % id)
    user = select(f"SELECT * FROM users WHERE id = '{id}' LIMIT 1")
    log.debug("Got user before deletion: %s" % user)

    try:
        upsert(f"DELETE FROM users WHERE id = ? LIMIT 1", (id,))
        log.debug("Returning user: %s" % user[0])
        return user[0]
    except IndexError:
        raise HTTPException(
            status_code=400, detail=f"User with id '{id}' could not be deleted.")
