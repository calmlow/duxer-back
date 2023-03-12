from fastapi import FastAPI
from configureapp import configure
from calmlogging import get_logger
from features import users
from features import admin

log = get_logger(__file__)

app = FastAPI(debug=True)
configure(app)
app.include_router(users.router)
app.include_router(admin.router)


@app.get("/check")
async def check():
    """Simple health check endpoint. Right now testing the logging """
    test = "test"
    log.warning("Warn from the /check endpoint {}:{}", test, test)
    log.error("Error from the /check endpoint")
    log.info("Info logg from the /check endpoint")
    log.debug("Debug from the /check endpoint")
    log.critical("critical from the /check endpoint")
    return {"success": True}


@app.get("/")
async def root():
    return {"root": "/"}
