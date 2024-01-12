import os 
from dotenv import load_dotenv
from utils.constants import PINECONE_ENV
import pinecone
from pinecone.core.client.configuration import Configuration as OpenApiConfiguration
load_dotenv()

class PineconeOperations:

    def __init__(self) -> None:
        self.pinecone_api_key = os.getenv("SANIC_PINECONE_KEY")
        self.pinecone_environment = PINECONE_ENV
        self.pinecone_openapi_config = OpenApiConfiguration.get_default_copy()
        self.pinecone_openapi_config.verify_ssl = False
        pinecone.init(
            api_key=self.pinecone_api_key,
            environment=self.pinecone_environment,
            openapi_config=self.pinecone_openapi_config,
        )

    def get_index(self, index_name: str):
        return pinecone.Index(index_name)