from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from template import html
from fastapi.responses import HTMLResponse
from routers import chat

app = FastAPI()

app.include_router(chat.router)

origins = [
    "http://localhost",
    "http://localhost:8000"
]

app.add_middleware(
   CORSMiddleware,
   allow_origins=origins,
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"]
)


@app.get("/")
async def get():
    return HTMLResponse(html)