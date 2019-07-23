from flask import Flask
from flask_ldap import LDAP

app = Flask(__name__)
app.debug = True

app.config['LDAP_HOST'] = 'ldap.example.com'
app.config['LDAP_DOMAIN'] = 'example.com'
app.config['LDAP_AUTH_TEMPLATE'] = 'login.html'
app.config['LDAP_PROFILE_KEY'] = 'employeeID'
# app.config['LDAP_AUTH_VIEW'] = 'login'

ldap = LDAP(app)
app.secret_key = "secret"
app.add_url_rule('/login', 'login', ldap.login, methods=['GET', 'POST'])

@app.route('/')
@ldap.login_required
def index():
    pass

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     pass

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")