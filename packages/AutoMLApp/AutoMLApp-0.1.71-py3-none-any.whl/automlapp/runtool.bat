@echo off
REM Fetch the directory containing the Streamlit application
FOR /F "tokens=*" %%i IN ('python -m automlapp.fetchdir') DO SET APP_DIR=%%i

REM Navigate to the directory
cd %APP_DIR%

REM Run the Streamlit application
streamlit run app.py

pause
