from sanic import Sanic
from sanic.response import text
from sanic.worker.loader import AppLoader
from utils.constants import APP_NAME
from dotenv import load_dotenv
import os
from embeddings.routes import bp as embeddings_bp

import pinecone

load_dotenv()

def create_app():
    app = Sanic(APP_NAME)

    app.blueprint(embeddings_bp)
    return app


def run_app():
    loader = AppLoader(factory=create_app)
    app = loader.load()
    app.prepare(
        host="0.0.0.0",
        port=8000,
        debug=True,
        access_log=True,
    )

    pinecone.init(
        api_key=os.getenv("PINECONE_API_KEY"),
        environment="gcp-starter",
    )

    journal_index = pinecone.Index("journal_index")

    app.ctx.journal_index = journal_index




    try:
        Sanic.serve(primary=app, app_loader=loader)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    run_app()