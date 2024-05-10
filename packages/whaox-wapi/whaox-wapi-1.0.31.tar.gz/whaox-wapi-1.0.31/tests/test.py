from dataclasses import dataclass
from typing import Optional, List

from wapi import Route, GET


@dataclass
class MemberDTO:
    id: int
    guild_id: int
    user_id: int
    name: str
    gender: str
    birthdate: str
    about: str
    lover: Optional[int]
    exp: int
    lvl: int
    up_exp: int
    wallet: int


@dataclass
class MetaResponse:
    message: str
    timestamp: str


@dataclass
class FetchMembersFromGuildRequest:
    meta: MetaResponse
    data: List[MemberDTO]


@Route("http://127.0.0.1:8080/guilds/{guild_id}/members")
class MembersService:

    @GET("/", FetchMembersFromGuildRequest, auto=True)
    def fetch_all_from_guild(
        self,
        *,
        guild_id: int,
        page: int = 1,
        size: int = 10,
        all: bool = False
    ) -> FetchMembersFromGuildRequest: pass

m = MembersService().fetch_all_from_guild(guild_id=1056553604246413313)

print(m)