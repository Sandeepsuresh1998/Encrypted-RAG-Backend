from sanic import Sanic
from sanic.worker.loader import AppLoader
from utils.constants import APP_NAME
import os
from dotenv import load_dotenv
from embeddings.routes import bp as embeddings_bp
from queries.routes import bp as queries_bp
from k8s_routes import bp as k8s_bp
from utils.rag import RAGOperations

load_dotenv()

def create_app():
    app = Sanic(APP_NAME)
    pinecone_key = os.getenv("PINECONE_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    rag_ops = RAGOperations(
        pinecone_key=pinecone_key,
    )
    app.config.update({
        "OPENAI_API_KEY": OPENAI_API_KEY,
        "RAG_OPS": rag_ops,
    })

    app.blueprint(embeddings_bp)
    app.blueprint(queries_bp)
    app.blueprint(k8s_bp)
    return app


def run_app():
    loader = AppLoader(factory=create_app)
    app = loader.load()
    app.prepare(
        host="0.0.0.0",
        port=8000,
        debug=True,
        access_log=True,
        auto_reload=True,
    )

    try:
        Sanic.serve(primary=app, app_loader=loader)
    except Exception as e:
        pass


if __name__ == "__main__":
    run_app()