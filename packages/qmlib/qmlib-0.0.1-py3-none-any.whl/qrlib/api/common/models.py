from prisma.models import (
    Channel as ChannelSession,
)


class Channel(ChannelSession):
    pass


Channel.model_rebuild(force=True)
