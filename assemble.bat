@echo off
setlocal
cd /d "%~dp0"
copy /b source-bundle\part-00.bin+source-bundle\part-01.bin+source-bundle\part-02.bin+source-bundle\part-03.bin+source-bundle\part-04.bin retrowave-player.tar.xz >nul
if errorlevel 1 (
  echo Failed to join source bundle parts.
  exit /b 1
)
tar -xJf retrowave-player.tar.xz
if errorlevel 1 (
  echo Failed to extract source bundle. Use Windows 10/11 tar or install 7-Zip.
  exit /b 1
)
py -3 "%~dp0apply-project-overlay.py" "%~dp0retrowave-player"
if errorlevel 1 exit /b 1
echo.
echo Project extracted and supplied GLSL overlay applied to .\retrowave-player
