#!/bin/bash

# pipx installs
python -m pip install --user pipx
python -m pipx ensurepath
python -m pipx install "nautc==1.1.0"

# pip installs
python -m pip install -U "discord.py==1.7.3"
python -m pip install "asyncpraw==7.6.1"
python -m pip install "nautc==1.1.0"

python ./swablu.py
