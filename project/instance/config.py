import os
from datetime import timedelta

#
# SECRETS
#
#

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG=False
    TESTING=False
    SECRET_KEY='6cf362b3053c446996275f13cfafa193'
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    PROTOCOL='HTTP://'
    SERVER_NAME='127.0.0.1:5000'
    USE_SESSION_FOR_NEXT=True
    REMEMBER_COOKIE_DURATION=timedelta(seconds=20)
    CRYPTO_KEY=b'jj0jmmv7t-63PN818_B-Wjm3jm6zXRVS7q9W7SSRYyY='
    LOG_FILE='project/instance/fpa.log'

class ProductionConfig(Config):
    ENV='production'
    DEBUG=False
    TESTING=False
    SQLALCHEMY_DATABASE_URI='mysql://fmapp:fmapp@localhost/fmapp'
    SESSION_COOKIE_NAME='fpa_session_cookie'
    VERSION="v1.0 PROD"

class DevelopmentConfig(Config):
    ENV='development'
    DEBUG=True
    TESTING=True
    SQLALCHEMY_DATABASE_URI='mysql://fmapp:fmapp@localhost/fmapp'
    SESSION_COOKIE_NAME='fpa_dev_session_cookie'
    SERVER_NAME='192.168.1.16:5000'
    HOST='192.168.1.16'
    PORT=5000
    VERSION="v0.1 BETA"

class TestingConfig(Config):
    DEBUG=True
    TESTING=True
    SQLALCHEMY_DATABASE_URI='sqlite:///'+ os.path.join(basedir, 'db/fpa_test.db')
    SESSION_COOKIE_NAME='fpa_test_session_cookie'


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}

current_config = 'development'
