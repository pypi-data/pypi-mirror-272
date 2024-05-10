from typing import Any
import traceback

from ..itl import Itl
from ..clusters import BaseController, PendingOperation


class ResourceController:
    def __init__(
        self,
        itl: Itl,
        cluster: str,
        group: str,
        version: str,
        kind: str,
        fiber: str = "resource",
    ):
        self.itl: Itl = itl
        self.cluster = cluster
        self.group = group
        self.version = version
        self.kind = kind
        self.fiber = fiber
        self._started = False

    def start(self, key=None):
        if self._started:
            return
        self._started = True

        self.itl.controller(
            self.cluster, self.group, self.version, self.kind, fiber=self.fiber, key=key
        )(self.controller)

    async def controller(self, pending: BaseController):
        async for op in pending:
            message = await op.message()
            if message != None:
                try:
                    await self.post_resource(op)
                    await op.accept()
                except Exception as e:
                    await op.reject()
                    print(
                        f"Failed to post resource {self.kind}/{message['metadata']['name']}: {e}"
                    )
                    traceback.print_exc()
                    print("(Still running)")
                continue

            new_config = await op.new_config()
            if new_config == None:
                # Delete the resource
                try:
                    await self.delete_resource(op)
                    await op.accept(delete=True)
                except Exception as e:
                    await op.reject()
                    print(f"Failed to delete resource {self.kind}/{pending.name}: {e}")
                    traceback.print_exc()
                    print("(Still running)")
                continue

            old_config = await op.old_config()

            try:
                if old_config == None:
                    new_config = await self.create_resource(op)
                else:
                    new_config = await self.update_resource(op)

                await op.accept(new_config)

            except Exception as e:
                await op.reject()
                print(f"Failed to load resource {self.kind}/{pending.name}: {e}")
                traceback.print_exc()
                print("(Still running)")
            continue

    async def create_resource(self, op: PendingOperation):
        raise ValueError("create_resource not implemented")

    async def update_resource(self, op: PendingOperation):
        return await self.create_resource(op)

    async def post_resource(self, op: PendingOperation):
        pass

    async def delete_resource(self, op: PendingOperation):
        pass
