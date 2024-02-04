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

bp = Blueprint("queries")

@bp.get("/v1/queries/get")
@cors(origin="*")
@validate(query=QueryGenerate)
async def create(request, query: QueryGenerate):
   # print("Received query prompt: ", query.prompt)
   # app = Sanic.get_app(APP_NAME)
   # rag_ops = app.config.RAG_OPS
   # pinecone_index = rag_ops.get_index("journal")
   # vector_store = PineconeVectorStore(
   #    pinecone_index=pinecone_index,
   # )
   # index = VectorStoreIndex.from_vector_store(vector_store)
   # # retriever = index.as_retriever()
   # # nodes = retriever.retrieve(query.prompt)
   # # for node in nodes:
   # #    print(node.text)
   # #    text = rag_ops.decrypt_text(node.text)

   # query_engine = index.as_query_engine(
   #    node_postprocessors=[
   #       DecryptionNodePostProcessor(),
   #    ]
   # )
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
   