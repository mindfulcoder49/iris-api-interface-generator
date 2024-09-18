#!/bin/sh
# Initialize iop
cd /irisdev/app

iop --init

# Load production settings
iop -m /irisdev/app/app/interop/settings.py

# Start production
iop --start Python.Production --detach
