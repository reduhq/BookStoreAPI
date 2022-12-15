from fastapi import FastAPI

app = FastAPI()

@app.get(path="/")
def get_user():
    return {"username": "Rey Eduardo Halsall Quintero"}