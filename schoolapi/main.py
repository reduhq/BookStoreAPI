from fastapi import FastAPI

app = FastAPI()

@app.get(path="/users")
def get_user():
    return {"username": "reduhq"}