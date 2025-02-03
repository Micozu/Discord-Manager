@echo off
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt

echo Running mz-dctool.py...
python mz-dctool.py
pause
