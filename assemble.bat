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
  echo Extraction failed. Install 7-Zip or use a recent Windows tar.
  exit /b 1
)
echo.
echo Project extracted to .\retrowave-player
