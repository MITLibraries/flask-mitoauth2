# -*- coding: utf-8 -*-
import os
import hashlib

from flask import (session, Blueprint, current_app, url_for, request,
                   redirect)
from werkzeug.security import safe_str_cmp
import jwt


oauthlib_client = 'oauthlib.client'
oauth2 = Blueprint('oauth2', __name__)


class MITOAuth2(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        url_prefix = app.config.get('OAUTH2_PREFIX')
        app.register_blueprint(oauth2, url_prefix=url_prefix)


@oauth2.route('/login/<remote>')
def login(remote):
    client = _get_client(remote)
    redirect = request.args.get('redirect')
    session['rfp_token'] = hashlib.sha1(os.urandom(64)).hexdigest()
    state = _create_state(session['rfp_token'],
                          current_app.config['SECRET_KEY'], redirect)
    callback = url_for('oauth2.authorized', remote=remote, _external=True)
    return client.authorize(callback=callback, state=state)


@oauth2.route('/login/<remote>/authorized')
def authorized(remote):
    state = request.args.get('state')
    valid_state = _validate_state(state, current_app.config['SECRET_KEY'])
    if not valid_state:
        raise Exception("Invalid authorization request")
    session.pop('rfp_token')
    client = _get_client(remote)
    tokens = client.authorized_response()
    # TODO: validate ID token and scopes
    session['%s_id_token' % remote] = tokens['id_token']
    user = client.get('userinfo', token=(tokens['access_token'], ''))
    session['%s_user_info' % remote] = user.data
    if 'redirect' in valid_state:
        return redirect(valid_state['redirect'])
    else:
        'Authorized'


@oauth2.route('/logout')
def logout():
    session.pop('mit_id_token', None)
    redirect = request.args.get('redirect')
    if redirect:
        return redirect(redirect)
    else:
        return 'Logged out'


def _create_state(rfp, secret, redirect=None):
    state = {'rfp': rfp}
    if redirect is not None:
        state['redirect'] = redirect
    return jwt.encode(state, secret)


def _validate_state(state, secret):
    msg = jwt.decode(state, secret)
    if safe_str_cmp(msg['rfp'], session['rfp_token']):
        return msg


def _get_client(remote):
    oauth = current_app.extensions.get(oauthlib_client)
    if remote not in oauth.remote_apps:
        raise Exception('Unregistered client')
    return oauth.remote_apps[remote]
