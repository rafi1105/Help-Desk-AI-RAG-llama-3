@echo off
REM Quick Script to Open Latest Visualization Report
REM =================================================

echo.
echo 📊 Finding latest research report...
echo.

for /f "delims=" %%i in ('dir /b /ad /o-d research_reports_* 2^>nul') do (
    set "LATEST=%%i"
    goto :found
)

:notfound
echo ❌ No research reports found!
echo.
echo Please run research analysis first:
echo    .\run_research_analysis.bat
echo    Select Option 4: Run FULL RESEARCH ANALYSIS
echo.
pause
exit /b 1

:found
echo ✅ Found latest report: %LATEST%
echo.

set HTML_FILE=%LATEST%\visualizations\index.html

if exist "%HTML_FILE%" (
    echo 🌐 Opening visualization report in browser...
    echo    Location: %HTML_FILE%
    echo.
    start "" "%HTML_FILE%"
    echo ✅ HTML report opened in your default browser!
) else (
    echo ❌ HTML file not found: %HTML_FILE%
    echo.
    echo The report folder exists but visualizations were not generated.
    echo Please run Option 4 in run_research_analysis.bat again.
)

echo.
echo Press any key to exit...
pause >nul
