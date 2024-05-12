import dataclasses
import typing

Unknown = str | typing.Any | None

@dataclasses.dataclass
class GetBotAPIResponse:
    """
    API response for both `byInv` and `getBot`
    """

    avatar: str
    "Avatar ID"

    discriminator: int
    "Bot's discriminator"

    flags: int
    "Undocumented"

    global_name: str
    "Global bot's username (Not server specific)"

    id: int
    "Bot's Snowflake ID"

    public_flags: int
    "Undocumented"

    username: str
    "Bot's username"

    avatar_url: typing.Optional[str] = None
    "Full avatar URL"

    accent_color: Unknown = None
    "Undocumented"

    avatar_decoration_data: Unknown = None
    "Undocumented"

    banner: typing.Optional[str] = None
    "Full banner URL"

    banner_color: Unknown = None
    "Undocumented"

    clan: Unknown = None
    "Undocumented"
