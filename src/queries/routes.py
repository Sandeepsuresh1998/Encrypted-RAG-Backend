from utils.constants import APP_NAME
from sanic import Sanic
from sanic import Blueprint
from sanic_ext import validate
from queries.types import QueryGenerate
from llama_index.vector_stores import PineconeVectorStore
from llama_index import VectorStoreIndex
from sanic import json
from sanic_ext import cors
from utils.rag import DecryptionNodePostProcessor
from pinecone.core.client.configuration import Configuration as OpenApiConfiguration
import os
from utils.constants import PINECONE_ENV
import pinecone 

bp = Blueprint("queries")

@bp.get("/v1/queries/get")
@cors(origin="*")
@validate(query=QueryGenerate)
async def create(request, query: QueryGenerate):
   print("Received query prompt: ", query.prompt)
   sanic_app = Sanic.get_app(APP_NAME)
   rag_ops = sanic_app.config.RAG_OPS

   pinecone_openapi_config = OpenApiConfiguration.get_default_copy()
   pinecone.init(
      api_key=os.getenv("PINECONE_API_KEY"),
      environment=PINECONE_ENV,
      openapi_config=pinecone_openapi_config
   )
   print(os.getenv("PINECONE_API_KEY"))
   pinecone_index = pinecone.Index("journal")

   vector_store = PineconeVectorStore(
      pinecone_index=pinecone_index,
      api_key=os.getenv("PINECONE_API_KEY"),
      environment=PINECONE_ENV
   )
   index = VectorStoreIndex.from_vector_store(vector_store)
   retriever = index.as_retriever()
   nodes = await retriever.retrieve(query.prompt)
   print("Retrieved nodes")
   for node in nodes:
      print(node.text)
      text = rag_ops.decrypt_text(node.text)


   query_engine = index.as_query_engine(
      node_postprocessors=[
         DecryptionNodePostProcessor(),
      ]
   )
   query_response = await query_engine.query(query.prompt)
   return json(
      {
         "response": query_response.response,
         "success": "true",
      }
   )

   return json(
      {
         "response": "This is a test response",
      }
   )
   