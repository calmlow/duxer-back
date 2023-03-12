# Database admin endpoints etc.
import os

from fastapi import APIRouter
from calmlogging import get_logger
from db import DATABASE_FILE

log = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/admin",
    tags=["admin"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}}
)


@router.get("/resetdb")
async def reset_database():
    """ Development aid to reset the database. get_db_connection instance will try to set it up again. """
    log.warn("Will reset the database")
    os.remove(DATABASE_FILE)

    return {"status": "done. This is only to aid development. You need to restart the server also."}
