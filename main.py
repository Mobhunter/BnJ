from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.staticfiles import StaticFiles
from BNJ.wsgi import application
from account_api.main import app as account_api_app
from messaging_api.main import app as messaging_api_app
from pathlib import Path
from dependencies import DjangoUserMiddleware

current_file = Path(__file__)
current_file_dir = current_file.parent
project_root = current_file_dir
project_root_absolute = project_root.resolve()
static_root_absolute = project_root_absolute / "static"  # or wherever the static folder actually is
media_root_absolute = project_root_absolute / "media"

app = FastAPI()
app.add_middleware(DjangoUserMiddleware)
app.mount("/static",
    StaticFiles(
         directory=static_root_absolute
    ),
    name="static",
)
app.mount("/media",
    StaticFiles(
         directory=media_root_absolute
    ),
    name="media",
)
app.mount("/api/account", account_api_app)
app.mount("/api/messaging", messaging_api_app)
app.mount("/", WSGIMiddleware(application))