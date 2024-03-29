from common.database.postgres.pool import postgres_db_pool
from common.models import Chat, Assistant
from typing import Dict
from common.database_ops.utils import update_object
from .get import get_chat


async def update_chat(assistant: Assistant, chat: Chat, update_dict: Dict):
    # 1. pop from redis
    await chat.pop_redis()

    # 2. Update chat in database
    async with postgres_db_pool.get_db_connection() as conn:
        await update_object(
            conn,
            update_dict=update_dict,
            update_time=True,
            table_name="chat",
            equal_filters={"assistant_id": chat.assistant_id, "chat_id": chat.chat_id},
        )

    # 3. Get updated chat
    chat = await get_chat(assistant, chat.chat_id)

    return chat
