from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


class Query(BaseModel):
    parameter1: str | None = None
    parameter2: str | None = None
    parameter3: str | None = None


app = FastAPI()

origins = [
    "http://localhost:5173",
    "localhost:5173",
    'http://127.0.0.1:5173',
]

app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
)


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/so-da/")
def so_da(query: Query):
    print(query)
    return {"message": "Hello from soda"}
