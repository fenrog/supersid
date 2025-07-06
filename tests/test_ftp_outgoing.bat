@echo off
REM This test
REM - has to be run as administrator (otherwise taskkill will not work)
REM - assumes python module twisted is installed
REM - expects no other ftp server is running on port 21 of localhost
REM - requires to grant private networks access to the ftp server

set UNITTEST_BATCH=True
if exist incoming rmdir incoming

REM test socket.gaierror as the "UnknownServer" cannot be resolved
set UNITTEST_SERVER_ERROR=True
set UNITTEST_FTP_SERVER=UnknownServer
python test_ftp_outgoing.py || (set UNITTEST_ERROR_LINE=15 & goto fail)

REM test ConnectionRefusedError as the ftp server is not running
set UNITTEST_SERVER_ERROR=True
set UNITTEST_FTP_SERVER=localhost
python test_ftp_outgoing.py || (set UNITTEST_ERROR_LINE=20 & goto fail)

REM test missing "incoming" folder
start "ftpserver" ftpserver.py
set UNITTEST_SERVER_ERROR=True
set UNITTEST_FTP_SERVER=localhost
python test_ftp_outgoing.py || (set UNITTEST_ERROR_LINE=26 & goto fail)
taskkill /fi "WINDOWTITLE eq ftpserver" > nul 2>&1

REM test write permission denied (twistd doesn't allow anonymous write)
if not exist incoming mkdir incoming
start "ftpserver" ftpserver.py
set UNITTEST_SERVER_ERROR=True
set UNITTEST_FTP_SERVER=localhost
python test_ftp_outgoing.py || (set UNITTEST_ERROR_LINE=34 & goto fail)
taskkill /fi "WINDOWTITLE eq ftpserver" > nul 2>&1

REM test login failed due to unknown user
if not exist incoming mkdir incoming
start "ftpserver" ftpserver.py
set UNITTEST_SERVER_ERROR=True
set UNITTEST_FTP_SERVER=localhost
set UNITTEST_FTP_LOGIN=unknown_user
set UNITTEST_FTP_PASSWORD=pass
python test_ftp_outgoing.py || (set UNITTEST_ERROR_LINE=34 & goto fail)
taskkill /fi "WINDOWTITLE eq ftpserver" > nul 2>&1

REM test login failed due to unknown password
if not exist incoming mkdir incoming
start "ftpserver" ftpserver.py
set UNITTEST_SERVER_ERROR=True
set UNITTEST_FTP_SERVER=localhost
set UNITTEST_FTP_LOGIN=user
set UNITTEST_FTP_PASSWORD=unknown_pass
python test_ftp_outgoing.py || (set UNITTEST_ERROR_LINE=34 & goto fail)
taskkill /fi "WINDOWTITLE eq ftpserver" > nul 2>&1

REM test happy day
REM hint: twisted expects the home directory of the 'user' in a file named 'user'
REM thus a link is created from incoming to user\incoming
if exist incoming rmdir incoming
if not exist user mkdir user
if not exist user\incoming mkdir user\incoming
mklink /J incoming user\incoming
start "ftpserver" ftpserver.py
set UNITTEST_SERVER_ERROR=False
set UNITTEST_FTP_SERVER=localhost
set UNITTEST_FTP_LOGIN=user
set UNITTEST_FTP_PASSWORD=pass
python test_ftp_outgoing.py || (set UNITTEST_ERROR_LINE=47 & goto fail)
taskkill /fi "WINDOWTITLE eq ftpserver" > nul 2>&1
rmdir /S /Q incoming

:pass
echo ###########################
echo # all tests passed
echo ###########################
goto end

:fail
echo ###########################
echo # test failed in line %UNITTEST_ERROR_LINE%
echo ###########################
goto end

:end
taskkill /fi "WINDOWTITLE eq ftpserver" > nul 2>&1
if exist incoming rmdir /S /Q incoming
if exist user rmdir /S /Q user
set UNITTEST_BATCH=
set UNITTEST_SERVER_ERROR=
set UNITTEST_FTP_SERVER=
set UNITTEST_FTP_LOGIN=
set UNITTEST_FTP_PASSWORD=