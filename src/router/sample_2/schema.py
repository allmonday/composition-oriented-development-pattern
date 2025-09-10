from typing import List
from pydantic_resolve import Loader

import src.services.user.loader as ul

import src.services.user.schema as us
import src.services.team.schema as tms
class Sample2TeamDetail(tms.Team):
    senior_members: list[us.User] = []
    def resolve_senior_members(self, loader=Loader(ul.UserByLevelLoader)):
        return loader.load(self.id)

def copy_class(name, Kls):
    return type(name, Kls.__bases__, dict(Kls.__dict__))

SeniorMemberLoader = copy_class('SeniorMemberLoader', ul.UserByLevelLoader)
JuniorMemberLoader = copy_class('JuniorMemberLoader', ul.UserByLevelLoader)


class Sample2TeamDetailMultipleLevel(tms.Team):
    senior_members: list[us.User] = []
    def resolve_senior_members(self, loader=Loader(SeniorMemberLoader)):
        return loader.load(self.id)

    junior_members: list[us.User] = []
    def resolve_junior_members(self, loader=Loader(JuniorMemberLoader)):
        return loader.load(self.id)
    
    senior_junior: List[us.User] = []
    async def resolve_senior_junior(self, 
                                    loader_j=Loader(JuniorMemberLoader),
                                    loader_s=Loader(SeniorMemberLoader)
                                    ):
        return await loader_j.load(self.id) + await loader_s.load(self.id)
