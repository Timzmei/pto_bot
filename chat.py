import os
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from message_class import Message_class
from telethon.tl.patched import Message
from user_class import User_class


class Chat:
    load_dotenv()
    
    phone = os.environ.get("PHONE")
    api_id = os.environ.get("API_ID")
    api_hash = os.environ.get("API_BASH") 
    client = TelegramClient(phone, api_id, api_hash)
    client.start()
    
    chats = []
    last_date = None
    size_chats = 200
    groups = []
    all_messages = []
    all_users = []
    offset_id = 0
    limit = 100
    total_messages = 0
    total_count_limit = 0

    @classmethod
    async def get_messages(cls):
        history = await cls.client(GetHistoryRequest(
            peer=-4025991977,
            offset_id=cls.offset_id,
            offset_date=None,
            add_offset=0,
            limit=cls.limit,
            max_id=0,
            min_id=0,
            hash=0
        ))

        messages = await history.messages
        for message in messages:
            if isinstance(message, Message):
                cls.all_messages.append(Message_class(message.id, message.from_id.user_id, message.message))
        return cls.all_messages[::-1]

    @classmethod
    async def get_users(cls):
        all_participants = await cls.client.get_participants(-4025991977)

        for user in all_participants:
            cls.all_users.append(User_class(user.id, user.first_name, user.last_name, user.username, user.phone))
        
        return cls.all_users