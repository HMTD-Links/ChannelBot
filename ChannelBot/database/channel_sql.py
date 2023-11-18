from sqlalchemy import Column, String, Boolean, BigInteger
from ChannelBot.database import BASE, SESSION


class Channel(BASE):
    __tablename__ = "channels"
    __table_args__ = {'extend_existing': True}
    channel_id = Column(BigInteger, primary_key=True)
    admin_id = Column(BigInteger)
    buttons = Column(String, nullable=True)

    def __init__(self, channel_id, admin_id, caption=None, buttons=None, edit_mode=None, position=None, webpage_preview=False, sticker_id=None):
        self.channel_id = channel_id
        self.admin_id = admin_id
        self.buttons = buttons

Channel.__table__.create(checkfirst=True)


async def num_channels():
    try:
        return SESSION.query(Channel).count()
    finally:
        SESSION.close()


async def add_channel(channel_id, user_id):
    q = SESSION.query(Channel).get(channel_id)
    if not q:
        SESSION.add(Channel(channel_id, user_id))
        SESSION.commit()
    else:
        SESSION.close()


async def remove_channel(channel_id):
    q = SESSION.query(Channel).get(channel_id)
    if q:
        SESSION.delete(q)
        SESSION.commit()
    else:
        SESSION.close()


async def get_channel_info(channel_id):
    q = SESSION.query(Channel).get(channel_id)
    if q:
        info = {
            'admin_id': q.admin_id,
            'buttons': q.buttons
        }
        SESSION.close()
        return True, info
    else:
        SESSION.close()
        return False, {}

async def set_buttons(channel_id, buttons):
    q = SESSION.query(Channel).get(channel_id)
    if q:
        q.buttons = buttons
        SESSION.commit()
        return True
    else:
        SESSION.close()
        return False


async def get_buttons(channel_id):
    q = SESSION.query(Channel).get(channel_id)
    if q and q.buttons:
        buttons = q.buttons
        SESSION.close()
        return buttons
    else:
        SESSION.close()
        return None
