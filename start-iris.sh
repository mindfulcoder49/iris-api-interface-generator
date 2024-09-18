#!/bin/sh
# start iris
/iris-main "$@" &

# wait for iris to be ready
/usr/irissys/dev/Cloud/ICM/waitISC.sh
