@echo off
REM =============================================================================
REM HYDRA-UMC / URTC Ecosystem - starter-kit.bat
REM Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
REM GPL-3.0 - see LICENSE.md
REM
REM Windows counterpart to starter-kit.sh - same 13 core repos, same
REM idempotent "skip what's already here, never pull/reset" behavior. See
REM starter-kit.sh's own header comment for the full reasoning.
REM
REM Usage:
REM   starter-kit.bat [destination-directory]   (default: current directory)
REM =============================================================================
setlocal enabledelayedexpansion

set "DEST=%~1"
if "%DEST%"=="" set "DEST=."
if not exist "%DEST%" mkdir "%DEST%"
cd /d "%DEST%"

set REPOS=HYDRA-UMC HYDRA-UMC-SERVER HYDRA-UMC-STUDIO HYDRA-UMC-SUITE HYDRA-UMC-DSI HYDRA-UMC-ANDROID-CONTROL HYDRA-UMC-IOS-CONTROL HYDRA-UMC-EDITOR-URDF URTC URTC-FLASHER URTC-TESTER URTC-WEB-STUDIO HYDRA-UMC-UPDATER

echo ============================================================
echo  HYDRA-UMC / URTC Starter Kit
echo  Cloning the 13 core repositories into: %CD%
echo ============================================================

set /a cloned=0
set /a skipped=0
set /a failed=0

for %%R in (%REPOS%) do (
    if exist "%%R" (
        echo SKIP  %%R ^(already exists here - untouched^)
        set /a skipped+=1
    ) else (
        echo CLONE %%R ...
        git clone --quiet "https://github.com/JuanenRac/%%R.git" "%%R"
        if errorlevel 1 (
            echo FAIL  %%R - see git's own error above
            set /a failed+=1
        ) else (
            set /a cloned+=1
        )
    )
)

echo ============================================================
echo  Done: !cloned! cloned, !skipped! already present, !failed! failed
echo ============================================================
echo.
echo Next step: HYDRA-UMC-UPDATER (one of the 13 repos just cloned above)
echo can check versions, install/update any of the other projects one
echo at a time, and build each project via its own build.sh/.bat - see
echo HYDRA-UMC-UPDATER\README.md. This script's only job was step one:
echo getting the source onto disk.

if !failed! GTR 0 exit /b 1
