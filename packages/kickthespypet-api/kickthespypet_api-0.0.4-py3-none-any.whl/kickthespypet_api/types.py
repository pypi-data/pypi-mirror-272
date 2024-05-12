import dataclasses
import typing


@dataclasses.dataclass
class GetBotAPIResponse:
    """
    API response for both `byInv` and `getBot`
    """
    id: str
    username: str
    avatarURL: typing.Optional[str] = None
