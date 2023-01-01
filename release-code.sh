#!/bin/bash

CFILE=wapp_task_manager_flask
timestamp=$(date +%s)
VERSION=$(echo `cat VERSION`.$timestamp)

git add .
git commit -am "`date` update"
git tag $VERSION
git push

if [ "$?" != "0" ]; then
    echo "====================================================="
    echo "ERROR"
    echo
    exit 1
fi

echo "[!] " gh release create $VERSION -t $VERSION -n '""' --target main
gh release create $VERSION -t $VERSION -n "" --target main

cd ..
python3 -m zipapp $CFILE -p "/usr/bin/env python3"
echo $PWD/$CFILE.pyz
cd $CFILE
gh release upload $VERSION ../$CFILE.pyz --clobber