#!/usr/bin/env bash
CODEBANG_WORKSPACE="/media/devecor/Data/clone/codebang"
IFUTURE_SERVER_WORKSPACE="/media/devecor/Data/clone/future-server/ifuture"

# set title for current window
echo -e "\033]0;codebang\007"

gnome-terminal --tab --title="future-server" \
               -- bash -c "cd $IFUTURE_SERVER_WORKSPACE;\
                           python3 manage.py runserver 9092;\
                           exec bash;"

cd $CODEBANG_WORKSPACE
sudo npm run serve
