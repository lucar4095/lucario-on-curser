echo starting
pyinstaller --noconsole --onefile --name "lucario on curser" --icon "icon.ico" "source for run.py"

pyinstaller --noconsole --onefile --name "stop code" --icon "icon.ico" "source for stop.py"

move /Y "dist\lucario on curser.exe" "%~dp0"

move /Y "dist\stop code.exe" "%~dp0"

echo building done
pause