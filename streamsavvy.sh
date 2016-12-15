#!/bin/bash


WORKING_DIR=/path/to/your/project
ACTIVATE_PATH=/path/to/your/virtualenv/bin/activate
cd ${WORKING_DIR}
source ${ACTIVATE_PATH}
exec $@
