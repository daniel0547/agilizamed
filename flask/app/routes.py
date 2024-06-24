from app.settings import *
from app.api import api

app.register_blueprint(api, url_prefix='/api')
