import logging
from utils.constants import APP_NAME
from sanic import Sanic
from sanic import Blueprint
from sanic_ext import validate
from queries.types import QueryGenerate
from llama_index.vector_stores import PineconeVectorStore
from llama_index import VectorStoreIndex, ServiceContext
from sanic import json
from sanic_ext import cors
from utils.rag import DecryptionNodePostProcessor
from pinecone.core.client.configuration import Configuration as OpenApiConfiguration
import os
from utils.constants import PINECONE_ENV
import pinecone 

logger = logging.getLogger(__name__)

bp = Blueprint("queries")

@bp.get("/v1/queries/get")
@cors(origin="*")
@validate(query=QueryGenerate)
def create(request, query: QueryGenerate):
   try:
      logger.info("Received query prompt: %s", query.prompt)
      sanic_app = Sanic.get_app(APP_NAME)
      rag_ops = sanic_app.config.RAG_OPS

      pinecone_openapi_config = OpenApiConfiguration.get_default_copy()
      pinecone.init(
         api_key=os.getenv("PINECONE_API_KEY"),
         environment=PINECONE_ENV,
         openapi_config=pinecone_openapi_config
      )
      logger.info(os.getenv("PINECONE_API_KEY"))
      logger.info(os.getenv("OPENAI_API_KEY"))
      pinecone_index = pinecone.Index("journal")

      vector_store = PineconeVectorStore(
         pinecone_index=pinecone_index,
         api_key=os.getenv("PINECONE_API_KEY"),
         environment=PINECONE_ENV
      )
      logger.info("Created vector store")
      index = VectorStoreIndex.from_vector_store(
         vector_store,
         ServiceContext.from_defaults()
      )
   except Exception as e:
      logger.error("Error creating index: %s", e)
      return json(
         {
            "response": "Error creating index",
            "success": "false",
         }
      )
   # query_engine = index.as_query_engine(
   #    node_postprocessors=[
   #       DecryptionNodePostProcessor(),
   #    ]
   # )
   # logger.info("Created query engine")
   # query_response = query_engine.query(query.prompt)
   # return json(
   #    {
   #       "response": query_response.response,
   #       "success": "true",
   #    }
   # )

   return json(
      {
         "response": "This is a test response",
      }
   )
