:: pipx installs
powershell.exe python.exe -m pip install --user pipx
powershell.exe python.exe -m pipx install "nautc==1.1.0"
powershell.exe python.exe -m pipx ensurepath

:: pip installs
powershell.exe python.exe -m pip install -U "discord.py==1.7.3"
powershell.exe python.exe -m pip install "asyncpraw==7.6.1"
powershell.exe python.exe -m pip install "nautc==1.1.0"

:: PYTHONUTF8=1 environtment variable nessisary for nautc to work on windows
powershell.exe $env:PYTHONUTF8 = '1'; python .\swablu.py
