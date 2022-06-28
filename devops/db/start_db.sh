#!/usr/bin/env bash

if [ "$1" ]; then
    VIRTUALENV_PATH=${1}
    source ${VIRTUALENV_PATH}/bin/activate
fi

FILE_DIR="$(dirname $0)"
cd $FILE_DIR
export DJANGO_READ_DOT_ENV_FILE=True

docker-compose up -d
python3 ../../manage.py migrate