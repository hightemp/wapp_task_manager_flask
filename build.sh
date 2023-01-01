#!/bin/bash

CFILE=wapp_task_manager_flask

cd ..
python3 -m zipapp $CFILE -p "/usr/bin/env python3"
echo $PWD/$CFILE.pyz

./$CFILE.pyz --bind 0.0.0.0:5014
