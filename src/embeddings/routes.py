from sanic import Blueprint
from sanic.response import json
from utils.constants import APP_NAME
from sanic import Sanic
from sanic_ext import validate
from embeddings.types import EmbeddingCreate
from sanic_ext import cors

bp = Blueprint("embeddings")


@bp.post("/v1/embeddings/create")
@cors(origin="*")
@validate(json=EmbeddingCreate)
async def create(request, body: EmbeddingCreate):

   ## TODO: There will need to be an auth decorator incorporated with Auth0 here

   # Create the embeddings for the loaded text
   text_input = body.text
   sanic_app = Sanic.get_app(APP_NAME)
   rag_ops = sanic_app.config.RAG_OPS

   embeddings_vector = rag_ops.create_embedding(
      text_input=text_input,
      openai_key=sanic_app.config.SANIC_OPENAI_KEY,
   )

   # Upsert the embeddings into Pinecone
   user_id = body.user_id
   rag_ops.upsert_embedding(
      user_id=user_id,
      embeddings_vector=embeddings_vector,
      text_input=text_input,
   )
   
   return json({
      "success": "true",
   })

# @bp.post("v1/embeddings/clear")
# async def clear(request):
#    ## TODO: This is really only for testing purposes and should be removed in production
#    sanic_app = Sanic.get_app(APP_NAME)

#    # Create connection to pinecone
#    openapi_config = OpenApiConfiguration.get_default_copy()
#    openapi_config.verify_ssl = False


#    pinecone.init(
#       api_key=sanic_app.config.SANIC_PINECONE_KEY,
#       environment="gcp-starter",
#       openapi_config=openapi_config,
#    )
   
#    # Retrieve the index
#    journal_index = pinecone.Index("journal")

#    journal_index.delete(
#       ids=["kljsndfkjn-skdjbnfs"],
#    )

#    return json(
#       {"success": "true"}
#    )