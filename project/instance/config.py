import os

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
	SERVER_NAME='127.0.0.1:5000'
	HOST='127.0.0.1'
	PORT=5000

class ProductionConfig(Config):
	ENV='production'
	DEBUG=False
	TESTING=False
	SQLALCHEMY_DATABASE_URI='sqllite:///'+ os.path.join(basedir, 'db/fpa.db')
	SESSION_COOKIE_NAME='fpa_session_cookie'

class DevelopmentConfig(Config):
	ENV='development'
	DEBUG=True
	TESTING=True
	SQLALCHEMY_DATABASE_URI='sqllite:///'+ os.path.join(basedir, 'db/fpa_dev.db')
	SESSION_COOKIE_NAME='fpa_dev_session_cookie'
	# SERVER_NAME='192.168.1.16:5000'

class TestingConfig(Config):
	DEBUG=True
	TESTING=True
	SQLALCHEMY_DATABASE_URI='sqllite:///'+ os.path.join(basedir, 'db/fpa_test.db')
	SESSION_COOKIE_NAME='fpa_test_session_cookie'


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}

current_config = 'development'
