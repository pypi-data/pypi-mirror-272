from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from plextraktsync.factory import logging
from plextraktsync.trakt.TraktUserListCollection import TraktUserListCollection

if TYPE_CHECKING:
    from plextraktsync.config.SyncConfig import SyncConfig
    from plextraktsync.plan.Walker import Walker
    from plextraktsync.plex.PlexApi import PlexApi
    from plextraktsync.trakt.TraktApi import TraktApi


class Sync:
    logger = logging.getLogger(__name__)

    def __init__(self, config: SyncConfig, plex: PlexApi, trakt: TraktApi):
        self.config = config
        self.plex = plex
        self.trakt = trakt
        self.walker = None

    @cached_property
    def trakt_lists(self):
        return TraktUserListCollection()

    async def sync(self, walker: Walker, dry_run=False):
        self.walker = walker
        is_partial = walker.is_partial

        from plextraktsync.sync.plugin import SyncPluginManager
        pm = SyncPluginManager()
        pm.register_plugins(self)

        pm.hook.init(sync=self, pm=pm, is_partial=is_partial, dry_run=dry_run)

        if self.config.need_library_walk:
            for movie in walker.find_movies():
                await pm.ahook.walk_movie(movie=movie, dry_run=dry_run)

            for episode in walker.find_episodes():
                await pm.ahook.walk_episode(episode=episode, dry_run=dry_run)

        await pm.ahook.fini(walker=walker, dry_run=dry_run)
