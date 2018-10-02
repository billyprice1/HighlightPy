from discord.ext.commands import AutoShardedBot
from .edgecases import int_list_or_none
from .loop import loop
import rethinkdb as r
import os


class BaseClient(AutoShardedBot):
    """The client class that HighlightPy is based on."""
    def __init__(self, **kwargs):
        if "shard_count" not in kwargs:
            kwargs['shard_count'] = os.environ.get("SHARD_COUNT")

        if "shard_ids" not in kwargs:
            kwargs['shard_ids'] = int_list_or_none(os.environ.get("SHARD_IDS"))

        super().__init__(**kwargs)
        self.remove_command("help")
        self.rethink_connection = loop.run_until_complete(
            self._get_rethink_connection()
        )
        self.token = os.environ['BOT_TOKEN']

    @staticmethod
    async def _get_rethink_connection():
        """Gets a RethinkDB connection."""
        return await r.connect(
            host=os.environ.get("RETHINK_HOST") or "127.0.0.1",
            port=28015,
            password=os.environ.get("RETHINK_PASS") or ""
        )

    def run(self):
        """Runs with the token in the code."""
        super().run(self.token)


client = BaseClient(loop=loop)
# Defines a initialised version of the base client.
