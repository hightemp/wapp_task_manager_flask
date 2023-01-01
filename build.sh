#!/bin/bash

CFILE=wapp_task_manager_flask

cd ..
rm -f ./wapp_task_manager_flask.database.db
python3 -m zipapp -c -p "/usr/bin/env python3" $CFILE
echo $PWD/$CFILE.pyz

./$CFILE.pyz --bind 0.0.0.0:5014
