import typing

import aiohttp
import discord
import orjson
import requests
import yarl

from .types import GetBotAPIResponse


class KickTheSpyPetAPI:
    """
    API Wrapper for kickthespy.pet
    """

    BASE_URL = yarl.URL("https://kickthespy.pet")

    def __init__(self, client: typing.Optional[requests.Session] = None) -> None:
        if not client:
            client = requests.Session()
        self.client = client
        self.client.headers["client"] = "github.com/timelessnesses/kickthespypet_api"

    def get_bot_by_server_id(
        self, id: typing.Union[int, str, discord.Guild]
    ) -> typing.Optional[GetBotAPIResponse]:
        """Get bot account ID in server by server's ID

        Keyword arguments:
        id -- A server ID as number, string or `discord.Guild` object
        Return: API data. Raise if API returns status code anything than 200 and 404 for `None`
        """

        response = self.client.get(
            str(self.BASE_URL / "getBot"),
            params={"id": id if not isinstance(id, discord.Guild) else id.id},
        )
        if response.status_code == 404:  # not found
            return None
        response.raise_for_status()
        return GetBotAPIResponse(**response.json())

    def get_bot_by_server_invite(
        self, code: typing.Union[str, discord.Invite]
    ) -> typing.Optional[GetBotAPIResponse]:
        """Get bot account ID in server by server's invite code

        Keyword arguments:
        code -- A server invite code as string or `discord.Invite` object
        Return: API data. Raise if API returns status code anything than 200 and 404 for `None`
        """
        response = self.client.get(
            str(self.BASE_URL / "byInv"),
            params={"code": code if not isinstance(code, discord.Invite) else code.id},
        )
        if response.status_code == 404:  # not found. again
            return None
        response.raise_for_status()
        return GetBotAPIResponse(**response.json())

    def get_bot_user_ids_int(self, use_orjson=False) -> list[int]:
        """Get a list of bots as user ID

        Keyword arguments:
        use_orjson -- Uses orjson for faster JSON loading
        Return: Returns a list of user ID
        """

        response = self.client.get(str(self.BASE_URL / "ids"))
        response.raise_for_status()
        if use_orjson:
            return orjson.loads(response.text)
        return response.json()


class AsyncKickTheSpyPetAPI:
    """
    Asynchronous API Wrapper for kickthespy.pet
    """

    BASE_URL = yarl.URL("https://kickthespy.pet")

    def __init__(self, client: typing.Optional[aiohttp.ClientSession] = None) -> None:
        if not client:
            client = aiohttp.ClientSession(
                self.BASE_URL,
                headers={"client": "github.com/timelessnesses/kickthespypet_api"},
            )
        self.client = client

    async def get_bot_by_server_id(
        self, id: typing.Union[int, str, discord.Guild]
    ) -> typing.Optional[GetBotAPIResponse]:
        """Get bot account ID in server by server's ID

        Keyword arguments:
        id -- A server ID as number, string or `discord.Guild` object
        Return: API data. Raise if API returns status code anything than 200 and 404 for `None`
        """

        async with self.client as req:
            async with req.get(
                self.BASE_URL / "getBot",
                params={"id": id if not isinstance(id, discord.Guild) else id.id},
            ) as resp:
                if resp.status == 404:  # not found
                    return None
                resp.raise_for_status()
                return GetBotAPIResponse(**await resp.json())

    async def get_bot_by_server_invite(
        self, code: typing.Union[str, discord.Invite]
    ) -> typing.Optional[GetBotAPIResponse]:
        """Get bot account ID in server by server's invite code

        Keyword arguments:
        code -- A server invite code as string or `discord.Invite` object
        Return: API data. Raise if API returns status code anything than 200 and 404 for `None`
        """
        async with self.client as req:
            async with req.get(
                self.BASE_URL / "byInv",
                params={
                    "code": code if not isinstance(code, discord.Invite) else code.id
                },
            ) as resp:
                if resp.status == 404:  # not found. again
                    return None
                resp.raise_for_status()
                return GetBotAPIResponse(**await resp.json())

    async def get_bot_user_ids_int(self, use_orjson=False) -> list[int]:
        """Get a list of bots as user ID

        Keyword arguments:
        use_orjson -- Uses orjson for faster JSON loading
        Return: Returns a list of user ID
        """

        async with self.client as req:
            async with req.get(self.BASE_URL / "ids") as resp:
                resp.raise_for_status()
                if use_orjson:
                    return orjson.loads(await resp.text())
                return await resp.json()
