#!/bin/bash
cp ../*.txt .
cp ../*.py .
pip3 install -r requirements.txt -t ./
rm -f lambdas.zip && zip -r lambdas.zip ./ -x '*.zip'
cp lambdas.zip ../
find . \! -name 'package.sh' -delete