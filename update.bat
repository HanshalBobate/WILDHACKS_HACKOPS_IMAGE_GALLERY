@echo off
title WildID — Dynamic Gallery & Blog Synchronizer
echo ===================================================================
echo   WildID -- Dynamic Synchronization Engine
echo   Scanning images/ and blog.txt for new or altered assets...
echo ===================================================================
echo.
python "%~dp0sync.py"
echo.
echo ===================================================================
echo   Synchronization complete! Refresh your browser to view updates.
echo ===================================================================
pause
