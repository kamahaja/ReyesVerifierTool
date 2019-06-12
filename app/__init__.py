from flask import Flask

app = Flask(__name__)

from app import routes #also known in the python documentation as the views