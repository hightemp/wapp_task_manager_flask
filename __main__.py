
# -*- coding: utf-8 -*-
import sys
import main
from gunicorn.app.wsgiapp import run
sys.argv.append('main:app')
sys.exit(run())

# from main import run

# run()