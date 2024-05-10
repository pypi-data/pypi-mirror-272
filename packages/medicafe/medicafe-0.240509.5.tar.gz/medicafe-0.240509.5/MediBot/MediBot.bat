@echo off
setlocal enabledelayedexpansion

:: Define paths
set "source_folder=C:\MEDIANSI\MediCare"
set "target_folder=C:\MEDIANSI\MediCare\CSV"
set "config_file=F:\Medibot\json\config.json"
set "python_script=C:\Python34\Lib\site-packages\MediBot\update_json.py"
set "python_script2=C:\Python34\Lib\site-packages\MediBot\Medibot.py"
set "medicafe_package=medicafe"
set "upgrade_medicafe=F:\Medibot\update_medicafe.py"
set "temp_file=F:\Medibot\last_update_timestamp.txt"
set "firefox_path=C:\Program Files\Mozilla Firefox\firefox.exe"
set "package_version="
set PYTHONWARNINGS=ignore

:: Check if the medicafe package is installed
echo Checking installed MediCafe package version...
python -c "import pkg_resources" > nul 2>&1
if %errorlevel% neq 0 (
    echo Medicafe package is not installed.
) else (
    echo Medicafe package is installed.
    for /f "tokens=2 delims==" %%a in ('python -c "import pkg_resources; print(pkg_resources.get_distribution('medicafe').version)"') do set package_version=%%a
)

:: Check for internet connectivity
ping -n 1 google.com > nul 2>&1
set "internet_available=%ERRORLEVEL%"

:: Common pre-menu setup
echo Setting up the environment...
if not exist "%config_file%" (
    echo Configuration file missing.
    goto end_script
)
if exist "C:\Python34\Lib\site-packages\MediBot\upgrade_medicafe.py" (
    move "C:\Python34\Lib\site-packages\MediBot\upgrade_medicafe.py" "F:\Medibot\upgrade_medicafe.py" /y
)

:: Main menu
:main_menu
cls
echo v!package_version!
echo ---------------------------------------------
echo         .//*  Welcome to MediCafe  *\\. 
echo ---------------------------------------------
echo.
echo Please select an option:
if "!internet_available!"=="0" (
    echo 1. Check for MediCafe Package Updates
    echo 2. Download Email de Carol
    echo 3. MediLink Claims
)
echo 4. Run MediBot
echo 5. Exit
echo.
set /p choice=Enter your choice:  

if "%choice%"=="5" goto end_script
if "%choice%"=="4" goto medibot_flow
if "%choice%"=="3" goto medilink_flow
if "%choice%"=="2" goto download_emails
if "%choice%"=="1" goto check_updates

:: Medicafe Update
:check_updates
if "!internet_available!" neq "0" (
    echo No internet connection available.
    goto main_menu
)
echo Checking for MediCafe package updates. Please wait...
start cmd /c py "%upgrade_medicafe%" > upgrade_log.txt 2>&1 && (
    echo %DATE% %TIME% Upgrade initiated. >> "%temp_file%"
    echo Exiting batch to complete the upgrade.
) || (
    echo %DATE% %TIME% Update failed. Check logs. >> upgrade_log.txt
)
exit /b

:: Download Carol's Emails
:download_emails
if "!internet_available!" neq "0" (
    echo No internet connection available.
    goto main_menu
)
echo Downloading emails...
py "../MediLink/MediLink_Gmail.py" "%firefox_path%"
if errorlevel 1 (
    echo Failed to download emails.
) else (
    call :process_csvs
)
goto main_menu

:: Run MediBot Flow
:medibot_flow
call :process_csvs
py "%python_script2%" "%config_file%"
if errorlevel 1 echo Failed to run MediBot.
goto main_menu

:: Continue to MediLink
:medilink_flow
if "!internet_available!" neq "0" (
    echo No internet connection available.
    goto main_menu
)
call :process_csvs
py "C:\Python34\Lib\site-packages\MediLink\MediLink.py"
if errorlevel 1 echo MediLink failed to execute.
goto main_menu

:: Process CSV Files
:process_csvs
for /f "tokens=1-5 delims=/: " %%a in ('echo %time%') do (
    set "hour=%%a"
    set "minute=%%b"
    set "second=%%c"
)
set "timestamp=%DATE:~-4%%DATE:~3,2%%DATE:~0,2%_%hour%%minute%"
set "latest_csv="
for /f "delims=" %%a in ('dir /b /a-d /o-d "%source_folder%\*.csv" 2^>nul') do (
    set "latest_csv=%%a"
    goto process_found_csv
)
echo No new CSV files found.
goto :eof

:process_found_csv
move "%source_folder%\!latest_csv!" "%target_folder%\SX_CSV_!timestamp!.csv"
set "new_csv_path=%target_folder%\SX_CSV_!timestamp!.csv"
py "%python_script%" "%config_file%" "!new_csv_path!"
goto :eof

:: Exit Script
:end_script
echo Exiting MediCafe.
pause
exit /b