import json
import os
from typing import List

import requests
from aiogram import Bot
from pydantic import BaseModel

import config


class Token(BaseModel):
    token: str
    port: int
    course_id: int

    def add(self):
        return TokensDB.add_bot(self)


class TokensDB:
    @staticmethod
    def add_bot(token: Token):
        res = requests.post(f"{config.BACKEND_URL}/tblp/tokens/add_token", json=json.dumps(token.__dict__))
        return res

    @staticmethod
    def get_used_ports():
        res = requests.get(f"{config.BACKEND_URL}/tblp/tokens/get_used_ports")
        return res

    @staticmethod
    def get_all_tokens() -> List[Token]:
        res = requests.get(f"{config.BACKEND_URL}/tblp/tokens/get_all_tokens")
        ans = []
        for i in res.json():
            ans.append(Token(**i))
        return ans

    @staticmethod
    def get_modules(bot: Bot):
        token = bot  # don't know how to get token
        res = requests.get(f"{config.BACKEND_URL}/tblp/tokens/get_modules/{token}")
        return res
