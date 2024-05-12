from readyapi import ReadyAPI

first_other = ReadyAPI()


@first_other.get("/")
def first_other_root():
    return {"message": "single file first_other"}


second_other = ReadyAPI()


@second_other.get("/")
def second_other_root():
    return {"message": "single file second_other"}


api = ReadyAPI()


@api.get("/")
def api_root():
    return {"message": "single file api"}


app = ReadyAPI()


@app.get("/")
def app_root():
    return {"message": "single file app"}
