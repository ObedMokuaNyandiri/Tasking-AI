import pytest

from tests.services_api.inference.text_embedding import text_embedding
from tests.services_api.model.model import create_model
from tests.settings import OPENAI_API_KEY


class TestTextEmbedding:

    text_embedding_model_id = None

    input_list = [
        {
            "input": "hello, nice to meet you"
        },
        {
            "input": [
                "hello, nice to meet you",
                "i'm fine thank you"
            ]
        }
    ]

    @pytest.mark.run(order=31)
    @pytest.mark.asyncio
    @pytest.mark.parametrize("input_data", input_list)
    async def test_text_embedding(self, input_data):

        if self.text_embedding_model_id is None:

            create_text_embedding_model_data = {
                "name": "My Embedding Model",
                "model_schema_id": "openai/text-embedding-ada-002",
                "credentials": {"OPENAI_API_KEY": OPENAI_API_KEY}
            }

            create_text_embedding_model_res = await create_model(create_text_embedding_model_data)
            create_text_embedding_model_res_json = create_text_embedding_model_res.json()
            TestTextEmbedding.text_embedding_model_id = create_text_embedding_model_res_json.get("data").get("model_id")

        input_data.update({"model_id": self.text_embedding_model_id})
        res = await text_embedding(input_data)
        res_json = res.json()
        assert res.status_code == 200
        assert res_json.get("status") == "success"
        for item in res_json.get("data"):
            assert all(isinstance(value, float) for value in item.get("embedding"))
