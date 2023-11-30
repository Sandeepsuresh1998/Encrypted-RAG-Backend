from sanic import Blueprint
from sanic.response import json
from utils.constants import APP_NAME
from sanic import Sanic

from llama_index.embeddings import OpenAIEmbedding
from llama_index import VectorStoreIndex, SimpleDirectoryReader

bp = Blueprint("embeddings", url_prefix="/v1/embeddings")

@bp.get("/create")
async def create(request):

   embeddings_model = OpenAIEmbedding()

#    documents = SimpleDirectoryReader("src/data").load_data()
#    index = VectorStoreIndex.from_documents(documents)
   app = Sanic.get_app(APP_NAME)
   journal_index = app.ctx.journal_index
   journal_index.upsert(
    vectors=[
       {'id': "vec1", "values":[0.1, 0.2, 0.3, 0.4], "metadata": {'genre': 'drama'}},
       {'id': "vec2", "values":[0.2, 0.3, 0.4, 0.5], "metadata": {'genre': 'action'}},
    ],
   )
   return json({"hello": "world"})