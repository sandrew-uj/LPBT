from fastapi import FastAPI
from typing_extensions import List, Type

from Models import Token
from Models.token import TokenDB, TokenModel

app_token = FastAPI(
    title="backend_token"
)


# Endpoint to add a token
@app_token.post("/add_token")
async def add_token(token: Token) -> int:
    return await token.add_token()


# Endpoint to get used ports
@app_token.get("/get_used_ports")
async def get_used_ports() -> List[int]:
    return await TokenDB.get_ports()


# Endpoint to get used ports
@app_token.get("/get_all_tokens")
async def get_all_tokens() -> List[Token]:
    return await TokenDB.get_all_tokens()


# Endpoint to get modules
@app_token.get("/get_modules/{token}")
async def get_modules(token: str) -> Type[TokenModel] | None:
    return await TokenDB.get_token(token=token)


@app_token.post("/get_bot")
async def get_bot(bot: Token):
    return await TokenDB.get_token(token=bot.token)
