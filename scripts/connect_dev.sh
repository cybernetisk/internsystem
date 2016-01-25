#!/bin/bash

ssh -R 0.0.0.0:8000:localhost:8000 -R 0.0.0.0:3000:localhost:3000 django@internt.cyb.no

