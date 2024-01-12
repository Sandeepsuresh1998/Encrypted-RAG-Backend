from utils.constants import APP_NAME
from sanic import Sanic
from sanic import Blueprint
from sanic_ext import validate
from queries.types import QueryGenerate
from llama_index.vector_stores import PineconeVectorStore
from llama_index import VectorStoreIndex
from sanic import json

bp = Blueprint("queries")

@bp.get("/v1/queries/get")
@validate(query=QueryGenerate)
async def create(request, query: QueryGenerate):
   app = Sanic.get_app(APP_NAME)
   pinecone_ops = app.config.PINECONE
   pinecone_index = pinecone_ops.get_index("journal")
   vector_store = PineconeVectorStore(
      pinecone_index=pinecone_index,
   )
   index = VectorStoreIndex.from_vector_store(vector_store)
   query_engine = index.as_query_engine()
   query_response = query_engine.query(query.prompt)
   print(query_response)
   return json(
      {
         "response": query_response.response,
         "success": "true",
      }
   )
   