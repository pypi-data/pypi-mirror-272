from readyapi import ReadyAPI

app = ReadyAPI()


@app.get("/")
def app_root():
    return {"message": "single file app"}
