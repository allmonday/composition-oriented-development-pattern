from typing import List, Optional
from pydantic2_resolve import LoaderDepend

import src.services.user.loader as ul

import src.services.user.schema as us
import src.services.team.schema as tms


class Sample2TeamDetail(tms.Team):
    senior_members: list[us.User] = []
    def resolve_senior_members(self, loader=LoaderDepend(ul.UserByLevelLoader)):
        return loader.load(self.id)