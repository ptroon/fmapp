import os
from datetime import timedelta

#
# SECRETS
#
#

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    APP_NAME="secFBA"
    DEBUG=True
    TESTING=False
    SECRET_KEY='6cf362b3053c446996275f13cfafa193'
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    PROTOCOL='HTTP://'
    # SERVER_NAME='myideahub.drayddns.com:8000'
    SERVER_NAME="192.168.1.248:8000"
    USE_SESSION_FOR_NEXT=True
    REMEMBER_COOKIE_DURATION=timedelta(seconds=20)
    CRYPTO_KEY=b'jj0jmmv7t-63PN818_B-Wjm3jm6zXRVS7q9W7SSRYyY='
    LOG_FILE='project/instance/fpa.log'
    COPYRIGHT="&copy; Company_Name 2020 [written in Flask]"
    PAGINATION_SIZE=20

class ProductionConfig(Config):
    ENV='production'
    DEBUG=False
    TESTING=False
    SQLALCHEMY_DATABASE_URI='mysql://fmapp:fmapp@localhost/fmapp'
    SESSION_COOKIE_NAME='fpa_session_cookie'
    VERSION="v1.0 PROD"
    MAIL_SERVER='localhost'
    MAIL_PORT=25
    MAIL_USERNAME=""
    MAIL_PASSWORD=""
    MAIL_DEFAULT_SENDER="secFPA@gmail.com"

class DevelopmentConfig(Config):
    ENV='development'
    DEBUG=True
    TESTING=True
    SQLALCHEMY_DATABASE_URI='mysql://fmapp:fmapp@localhost/fmapp'
    SESSION_COOKIE_NAME='fpa_dev_session_cookie'
    VERSION="v0.1 BETA"
    MAIL_SERVER="smtp.ionos.co.uk"
    MAIL_USE_TLS=True
    MAIL_USE_SSL=False
    MAIL_PORT=587
    MAIL_USERNAME="philiptroon@zebaroo.com"
    MAIL_PASSWORD="Evan2020!!"
    MAIL_DEFAULT_SENDER="secFPA@gmail.com"
    MAIL_SUPPRESS_SEND=False

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
