@ECHO OFF
SETLOCAL

@REM Change current directory to script location so relative paths work
CD /D "%~dp0"
ECHO Current directory is: %CD%


@REM Check for virtual environment directory
IF NOT EXIST "venv" (
  ECHO Virtual environment not found. Please create it first using:
  ECHO   python -m venv venv
  EXIT /B 1
)

@REM Activate the virtual environment (use CALL so control returns here)
CALL "venv\Scripts\activate.bat" || EXIT /B 1

ECHO Installing dependencies from requirements.txt...
python -m pip install -r "requirements.txt" || EXIT /B 1

ECHO Launching application...
python "main.py" || EXIT /B 1

ENDLOCAL
EXIT /B 0