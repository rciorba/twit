#!/bin/sh
if [ ! -d ./src/ ]; then
    git clone ../ ./src/ --depth=1
fi

DESCRIPTION=$(cd ./src/; git pull origin > /dev/null; git show HEAD -s --oneline)
echo "building for $DESCRIPTION"
docker build -t twit .


