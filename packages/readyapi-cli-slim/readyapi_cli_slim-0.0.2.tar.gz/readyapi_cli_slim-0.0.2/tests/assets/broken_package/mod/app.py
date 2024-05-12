from readyapi import ReadyAPI

from ..utils import get_message

app = ReadyAPI()


@app.get("/")
def app_root():
    return {"message": get_message()}
