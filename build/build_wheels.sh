#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ ! -d $DIR/wheelhouse ]; then
  mkdir $DIR/wheelhouse
fi

cp $DIR/src/REQUIREMENTS $DIR/wheelhouse/

docker run -v $DIR/wheelhouse/:/wheelhouse:rw wheeler pip wheel -r /wheelhouse/REQUIREMENTS --log /wheelhouse/log
