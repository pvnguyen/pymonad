#!/bin/bash

# add/replace if variable is non empty
# $1 = variable to replace/remove
# $2 = new value to set
function update_conf() {
    local query
    if [ "$1" == "" ]; then return 0; fi

    # First remove existing configuration info
    if [ -e /code/task_config.py ]; then
        if [ "$2" != "" ]; then
            query="$1"
	        mv /code/task_config.py /code/task_config.py.old
            grep -v "^$query" /code/task_config.py.old > /code/task_config.py
            rm /code/task_config.py.old
	    fi
    fi

    # Then, update config info
    if [ "$2" != "" ]; then
        echo "$1=\"$2\"" >> /code/task_config.py
    fi
}

# Set configuration information 
update_conf   "RABBITMQ_URL" "$RABBITMQ_URL"

# Start task
cd /code
python task.py
