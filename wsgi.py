# wsgi.py

import sys
sys.path.insert(0, '/var/www/python/fmapp')

activate_this = '/var/www/python/fmapp/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from app import application

if __name__ == "__main__":
  application.run()
