# Flask-MITOAuth2

Flask-MITOAuth2 provides authentication for Flask applications using MIT's OAuth2 implementation.

## Installation

```
$ pip install git+https://github.com/MITLibraries/flask-mitoauth2@master#egg=Flask-MITOAuth2
```

## Usage

This extension is primarily a Flask blueprint that provides several views necessary for completing the OAuth2 authentication process. You should make sure you have set `MIT_CONSUMER_KEY` (client ID from the registration process) and `MIT_CONSUMER_SECRET` (client secret from the registration process) in your application configuration. If you have not already set `SECRET_KEY` you will need to do this, as well.

Initialization requires creating a remote app using [https://github.com/lepture/flask-oauthlib] Flask-OAuthlib and then initializing this extension:

```python
from flask import Flask
from flask_oauthlib.client import OAuth
from flask_mitoauth2 import MITOAuth2
from flask_mitoauth2.contrib.apps import mit

app = Flask(__name__)
app.config['MIT_CONSUMER_KEY'] = 'your-client-id'
app.config['MIT_CONSUMER_SECRET'] = 'your-client-secret'
app.config['SECRET_KEY'] = 'app-secret-key'

oauth = OAuth(app)
mit.register_to(oauth)
MITOAuth2(app)
```

This will set up three routes in your application.

`oauth2.login` initiates the login process. The user will be redirected to MIT's OAuth2 service to authenticate and authorize the client. Once the user has completed this step they are redirected to `oauth2.authorized` where user info is fetched. If this is successful, the user info will be stored in `session['mit_user_info']`. If a `redirect` parameter was passed to the `oauth2.login` route in the beginning of the process the authenticated user will be redirected to this url.

`oauth2.logout` will destroy the session. If a `redirect` parameter is passed the user will be redirected to this url.

Typically, you would want to generate links to the login and logout routes. This can be done using Flask's `url_for` utility. The login route requires a `remote` param set to `mit` and optionally a `redirect` param. As an example, you might create a route decorator to authenticate certain resources:

```python
from functools import wraps
from flask import request

def authenticate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'mit_id_token' not in session:
            return redirect(url_for('oauth2.login', remote='mit',
                                    redirect=request.path))
        return f(*args, **kwargs)
    return wrapper


@app.route('/restricted')
@authenticate
def restricted():
    return 'Restricted stuff'
```
