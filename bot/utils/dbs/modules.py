import json
import os

import requests

import config


class ModulesDB:
    @staticmethod
    async def add_bot(bot):

        res = requests.post(f"{config.BACKEND_URL}/add_token", json=new_token)
        return res

    @staticmethod
    async def get_used_ports():
        res = requests.get(f"{config.BACKEND_URL}/get_used_ports")
        return res
