#!/bin/sh
while true
do
		git pull
        python3 xmppexchange.py
        sleep 1
done
