from models.interfaces.imodule import IModule
from models.params.zora_mint_params import ZoraMintParams


class ZoraMint(IModule[ZoraMintParams]):

    async def execute(self) -> dict:
        return {}


    async def verify(self) -> bool:
        return True