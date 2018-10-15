#!/bin/bash

mkdir bin
cp client.py ./bin
cp helper.py ./bin
cp log.py ./bin
cd ./aioconsole
python3 ./setup.py install
cd ../
cp run.sh ./bin