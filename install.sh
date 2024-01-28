#!/bin/bash
python3 -m venv /home/AlgoPage/.venv
source /home/AlgoPage/.venv/bin/activate
pip install --upgrade pip
pip install -r /home/AlgoPage/requirements.txt
cd /home/AlgoPage
reflex init