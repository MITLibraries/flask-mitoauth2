# -*- coding: utf-8 -*-
from flask_oauthlib.contrib.apps import RemoteAppFactory


mit = RemoteAppFactory('mit', {
    'base_url': 'https://oidc.mit.edu',
    'access_token_url': '/token',
    'authorize_url': '/authorize',
    'request_token_url': None,
    'request_token_params': {'scope': 'openid,email,profile'},
})
