from utils.constants import PINECONE_ENV
import pinecone
import base64
from openai import OpenAI
from pinecone.core.client.configuration import Configuration as OpenApiConfiguration
from utils.constants import ENCRYPTION_KEY, SALT
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from llama_index import QueryBundle
from llama_index.schema import NodeWithScore
from typing import Optional, List


def _get_cipher_suite():
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=100000,
        backend=default_backend()
    )

    key = base64.urlsafe_b64encode(kdf.derive(ENCRYPTION_KEY))
    # Encryption generation
    cipher_suite = Fernet(key)
    return cipher_suite

class RAGOperations:

    def __init__(self, pinecone_key) -> None:
        self.pinecone_api_key = pinecone_key
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

    
    async def create_embedding(self, text_input: str, openai_key: str):
        # Create openai connection
        openai = OpenAI(
            api_key=openai_key
        )
        # Generate the embedding with OpenAI
        embeddings_vector = await openai.embeddings.create(
           input=[text_input], 
           model="text-embedding-ada-002",
        ).data[0].embedding

        return embeddings_vector
    
    def upsert_embedding(self, user_id: str, embeddings_vector: list, text_input: str, is_encrypted=True):
        journal_index = self.get_index("journal")
        cipher_suite = _get_cipher_suite()

        # # Encrypt the text input
        if is_encrypted:
            text_input = cipher_suite.encrypt(text_input.encode("utf-8"))
            text_input = text_input.decode("utf-8")

        journal_index.upsert(
            vectors=[
                {
                    'id': user_id, 
                    "values": embeddings_vector, 
                    "metadata": {
                        'user_id': user_id,
                        'text': text_input,
                    }
                },
            ],
        )



class DecryptionNodePostProcessor:
    def __init__(self):
        pass

    def _decrypt_text(self, text: str):
        cipher_suite = _get_cipher_suite()
        text_input = cipher_suite.decrypt(text.encode("utf-8"))
        return text_input.decode("utf-8")

    def postprocess_nodes(
        self, 
        nodes: List[NodeWithScore], 
        query_bundle: Optional[QueryBundle] = None,
    ):
        # Takes nodes and decrypts the text
        for n in nodes:
            n.node.text = self._decrypt_text(n.node.text)
        return nodes