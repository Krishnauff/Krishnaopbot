from sqlalchemy import Column, Integer, String, UnicodeText

from . import BASE, SESSION


class Bot_Users(BASE):
    __tablename__ = "bot_users"
    message_id = Column(Integer, primary_key=True)
    first_name = Column(UnicodeText)
    chat_id = Column(String(14))
    reply_id = Column(Integer)

    def __init__(self, message_id, first_name, chat_id, reply_id):
        self.message_id = message_id
        self.first_name = first_name
        self.chat_id = str(chat_id)
        self.reply_id = reply_id


Bot_Users.__table__.create(checkfirst=True)


def add_user_to_db(
    message_id,
    first_name,
    chat_id,
    reply_id,
):
    user = Bot_Users(message_id, first_name, str(chat_id), reply_id)
    SESSION.add(user)
    SESSION.commit()
    return True


def get_user_id(message_id):
    try:
        _result = SESSION.query(Bot_Users).get(str(message_id))
        if _result:
            return int(_result.chat_id), _result.um_id
        return None, None
    finally:
        SESSION.close()


def get_user_name(message_id):
    try:
        _result = SESSION.query(Bot_Users).get(str(message_id))
        if _result:
            return int(_result.chat_id), _result.first_name
        return None, None
    finally:
        SESSION.close()