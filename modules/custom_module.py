from models.interfaces.imodule import IModule


class CustomModule(IModule):
    def __init__(self, params: dict):
        pass

    async def execute(self) -> dict:
        pass

    async def verify(self) -> bool:
        pass