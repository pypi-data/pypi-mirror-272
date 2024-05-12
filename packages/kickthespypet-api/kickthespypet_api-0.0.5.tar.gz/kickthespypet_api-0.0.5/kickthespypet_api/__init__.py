import logging
import typing

import aiohttp
import orjson
import requests
import yarl

from .types import GetBotAPIResponse


def convert_values_to_api_response(json: dict) -> GetBotAPIResponse:
    logger = logging.getLogger("kickthespypet_api.convert_values_to_api_response")
    logger.debug("JSON response: %s", json)
    return GetBotAPIResponse(
        avatar=json.get("avatar", ""),
        discriminator=int(json.get("discriminator", "")),
        flags=int(json.get("flags", "")),
        global_name=json.get("global_name", ""),
        id=int(json.get("id", "")),
        public_flags=int(json.get("public_flags", "")),
        username=json.get("username", ""),
        avatar_url=json.get("avatarURL"),
        accent_color=json.get("accent_color"),
        avatar_decoration_data=json.get("avatar_decoration_data"),
        banner=json.get("banner"),
        banner_color=json.get("banner_color"),
        clan=json.get("clan"),
    )


def convert_values_to_ints(
    lists: list[str], validate: bool
) -> typing.Sequence[int | str]:
    converted = []
    for id in lists:
        try:
            converted.append(int(id))
        except ValueError:
            if not validate:
                converted.append(id)
    return converted


class KickTheSpyPetAPI:
    """
    API Wrapper for kickthespy.pet
    """

    BASE_URL = yarl.URL("https://kickthespy.pet")
    LOGGER = logging.getLogger("kickthespypet_api.KickTheSpyPetAPI")

    def __init__(self, client: typing.Optional[requests.Session] = None) -> None:
        if not client:
            self.LOGGER.warn("No client supplied, creating one")
            client = requests.Session()
        self.client = client
        self.client.headers["client"] = "github.com/timelessnesses/kickthespypet_api"

    def get_bot_by_server_id(
        self, id: typing.Union[int, str]
    ) -> typing.Optional[GetBotAPIResponse]:
        """Get bot account ID in server by server's ID

        Keyword arguments:
        id -- A server ID as number, string or `discord.Guild` object
        Return: API data. Raise if API returns status code anything than 200 and 404 for `None`
        """

        response = self.client.get(
            str(self.BASE_URL / "getBot"),
            params={"id": id},
        )
        self.LOGGER.debug("Got response from getBot")
        if response.status_code == 404:  # not found
            self.LOGGER.debug("Returned Not Found from API")
            return None
        response.raise_for_status()
        return convert_values_to_api_response(response.json())

    def get_bot_by_server_invite(self, code: str) -> typing.Optional[GetBotAPIResponse]:
        """Get bot account ID in server by server's invite code

        Keyword arguments:
        code -- A server invite code as string or `discord.Invite` object
        Return: API data. Raise if API returns status code anything than 200 and 404 for `None`
        """
        response = self.client.get(
            str(self.BASE_URL / "byInv"),
            params={"code": code},
        )
        self.LOGGER.debug("Got response from byInv")
        if response.status_code == 404:  # not found. again
            self.LOGGER.debug("Returned Not Found from API")
            return None
        response.raise_for_status()
        return convert_values_to_api_response(response.json())

    @typing.overload
    def get_bot_user_ids_int(
        self, use_orjson: bool, validate_user_ids: typing.Literal[False]
    ) -> typing.Sequence[int | str]: ...

    @typing.overload
    def get_bot_user_ids_int(
        self, use_orjson: bool, validate_user_ids: typing.Literal[True]
    ) -> typing.Sequence[int]: ...

    def get_bot_user_ids_int(
        self, use_orjson=False, validate_user_ids=False
    ) -> typing.Sequence[int | str]:
        """Get a list of bots as user ID

        Keyword arguments:
        use_orjson -- Uses orjson for faster JSON loading
        validate_user_ids -- Verify if user IDs in list is actually a number
        Return: Returns a list of user ID in number
        """

        response = self.client.get(str(self.BASE_URL / "ids"))
        self.LOGGER.debug("Got response from ids")
        response.raise_for_status()
        if use_orjson:
            self.LOGGER.debug("Converting to JSON using orjson")
            r: list[str] = orjson.loads(response.text)
        else:
            self.LOGGER.debug("Converting to JSON using json")
            r = response.json()
        return convert_values_to_ints(r, validate_user_ids)

    def __enter__(self):
        self.LOGGER.info("Entered context.")
        return self

    def __exit__(self, *_):
        self.LOGGER.info("Exitted context. Cleaning up.")
        self.client.close()
        self.LOGGER.info("Successfully cleaned up.")

    def close(self):
        """Close connections gracefully. Call this function when you are done doing API calls"""
        self.client.close()
        self.LOGGER.info("Closed session.")


class AsyncKickTheSpyPetAPI:
    """
    Asynchronous API Wrapper for kickthespy.pet
    """

    BASE_URL = yarl.URL("https://kickthespy.pet")
    LOGGER = logging.getLogger("kickthespypet_api.AsyncKickTheSpyPetAPI")

    def __init__(self, client: typing.Optional[aiohttp.ClientSession] = None) -> None:
        if not client:
            self.LOGGER.warn("No client supplied, creating one")
            client = aiohttp.ClientSession(
                self.BASE_URL,
                headers={"client": "github.com/timelessnesses/kickthespypet_api"},
            )
        self.client = client

    async def get_bot_by_server_id(
        self, id: typing.Union[int, str]
    ) -> typing.Optional[GetBotAPIResponse]:
        """Get bot account ID in server by server's ID

        Keyword arguments:
        id -- A server ID as number, string or `discord.Guild` object
        Return: API data. Raise if API returns status code anything than 200 and 404 for `None`
        """

        async with self.client.get(
            "/getBot",
            params={"id": id},
        ) as resp:
            self.LOGGER.debug("Got response from getBot")
            if resp.status == 404:  # not found
                return None
            resp.raise_for_status()
            return convert_values_to_api_response(await resp.json())

    async def get_bot_by_server_invite(
        self, code: str
    ) -> typing.Optional[GetBotAPIResponse]:
        """Get bot account ID in server by server's invite code

        Keyword arguments:
        code -- A server invite code as string or `discord.Invite` object
        Return: API data. Raise if API returns status code anything than 200 and 404 for `None`
        """
        async with self.client.get(
            "/byInv",
            params={"code": code},
        ) as resp:
            self.LOGGER.debug("Got response from getBot")
            if resp.status == 404:  # not found. again
                return None
            resp.raise_for_status()
            return convert_values_to_api_response(await resp.json())

    @typing.overload
    async def get_bot_user_ids_int(
        self, use_orjson: bool, validate_user_ids: typing.Literal[False]
    ) -> typing.Sequence[int | str]: ...

    @typing.overload
    async def get_bot_user_ids_int(
        self, use_orjson: bool, validate_user_ids: typing.Literal[True]
    ) -> typing.Sequence[int]: ...

    async def get_bot_user_ids_int(
        self, use_orjson=False, validate_user_ids=False
    ) -> typing.Sequence[int | str]:
        """Get a list of bots as user ID

        Keyword arguments:
        use_orjson -- Uses orjson for faster JSON loading
        validate_user_ids -- Verify if user IDs in list is actually a number
        Return: Returns a list of user ID in number
        """

        async with self.client.get("/ids") as resp:
            self.LOGGER.debug("Got response from ids")
            resp.raise_for_status()
            if use_orjson:
                self.LOGGER.debug("Converting to JSON using orjson")
                r: list[str] = orjson.loads(await resp.text())
            else:
                self.LOGGER.debug("Converting to JSON using json")
                r = await resp.json()
            return convert_values_to_ints(r, validate_user_ids)

    async def close(self):
        """Close connections gracefully. Call this function when you are done doing API calls"""
        await self.client.close()
        self.LOGGER.info("Closed session.")

    async def __aenter__(self):
        self.LOGGER.info("Entered context.")
        return self

    async def __aexit__(self, *_):
        self.LOGGER.info("Exitted context. Cleaning up.")
        await self.client.close()
        self.LOGGER.info("Successfully cleaned up.")
