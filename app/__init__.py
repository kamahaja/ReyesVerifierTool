from flask import Flask

app = Flask(__name__)
app.secret_key = "super secret key"

from app import routes #also known in the python documentation as the views