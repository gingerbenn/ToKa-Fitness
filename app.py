from flask import Flask
from datetime import timedelta, datetime

app = Flask(__name__)


app.secret_key = 'Livi'

app.permanent_session_lifetime = timedelta(hours=1)
import routes

if __name__ == '__main__':
    app.run(debug=True)