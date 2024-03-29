from common.database.postgres.pool import postgres_db_pool
from common.models import Assistant
from typing import Dict
from common.database_ops.utils import update_object
from .get import get_assistant


async def update_assistant(assistant: Assistant, update_dict: Dict):
    # 1. pop from redis
    await assistant.pop_redis()

    async with postgres_db_pool.get_db_connection() as conn:
        # 2. Update assistant in database
        await update_object(
            conn,
            update_dict=update_dict,
            update_time=True,
            table_name="assistant",
            equal_filters={"assistant_id": assistant.assistant_id},
        )

    # 3. Get updated assistant
    assistant = await get_assistant(assistant.assistant_id)

    return assistant
