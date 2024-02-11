#!/bin/bash
source /home/AlgoPage/.venv/bin/activate
cd /home/AlgoPage
echo "Starting ReflexPage"
screen -AmdS reflexpage reflex run --env prod
echo "ReflexPage started!"
while true; do
    sleep 1
done
