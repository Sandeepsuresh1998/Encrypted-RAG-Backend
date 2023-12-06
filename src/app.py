from sanic import Sanic
from sanic.response import text
from sanic.worker.loader import AppLoader
from utils.constants import APP_NAME
from dotenv import load_dotenv
import os
from embeddings.routes import bp as embeddings_bp
from k8s_routes import bp as k8s_bp

load_dotenv()

def create_app():
    app = Sanic(APP_NAME)
    app.config.update({
        "SANIC_PINECONE_KEY": os.getenv("SANIC_PINECONE_KEY"),
        "SANIC_OPENAI_KEY": os.getenv("SANIC_OPENAI_KEY"),
    })

    app.blueprint(embeddings_bp)
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
        print(e)


if __name__ == "__main__":
    run_app()