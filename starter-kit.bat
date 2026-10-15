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
REM Second argument = which set to clone (see starter-kit.sh): core (the 13
REM repos below, default), hydra-umc, urtc, armor or all - the last four are
REM discovered live (every public JuanenRac repository carrying that
REM ecosystem's manifest) with PowerShell, which every supported Windows has.
REM
REM Usage:
REM   starter-kit.bat [destination-directory] [core|hydra-umc|urtc|armor|all]
REM =============================================================================
setlocal enabledelayedexpansion

set "DEST=%~1"
if "%DEST%"=="" set "DEST=."
set "SET=%~2"
if "%SET%"=="" set "SET=core"
set "MANIFESTS="
if /i "%SET%"=="hydra-umc" set "MANIFESTS=hydra-umc.project.json"
if /i "%SET%"=="urtc" set "MANIFESTS=urtc.project.json"
if /i "%SET%"=="armor" set "MANIFESTS=armor.project.json"
if /i "%SET%"=="all" set "MANIFESTS=hydra-umc.project.json,urtc.project.json,armor.project.json"
if /i not "%SET%"=="core" if "%MANIFESTS%"=="" (
    echo Unknown set '%SET%' - use core, hydra-umc, urtc, armor or all
    exit /b 2
)
if not exist "%DEST%" mkdir "%DEST%"
cd /d "%DEST%"

set REPOS=HYDRA-UMC HYDRA-UMC-SERVER HYDRA-UMC-STUDIO HYDRA-UMC-SUITE HYDRA-UMC-DSI HYDRA-UMC-ANDROID-CONTROL HYDRA-UMC-IOS-CONTROL HYDRA-UMC-EDITOR-URDF URTC URTC-FLASHER URTC-TESTER URTC-WEB-STUDIO HYDRA-UMC-UPDATER

if not "%MANIFESTS%"=="" (
    set "REPOS="
    for /f "usebackq delims=" %%N in (`powershell -NoProfile -ExecutionPolicy Bypass -Command "$ErrorActionPreference='Stop'; $h=@{'User-Agent'='starter-kit'}; if($env:GITHUB_TOKEN){$h.Authorization='Bearer '+$env:GITHUB_TOKEN}; $p=1; $repos=@(); do { $page=Invoke-RestMethod -Headers $h ('https://api.github.com/users/JuanenRac/repos?type=owner&per_page=100&page='+$p); $repos+=$page; $p++ } while ($page.Count -eq 100); foreach($r in $repos){ foreach($m in '%MANIFESTS%'.Split(',')){ try { Invoke-WebRequest -UseBasicParsing -Method Head -Headers @{'User-Agent'='starter-kit'} ('https://raw.githubusercontent.com/JuanenRac/'+$r.name+'/'+$r.default_branch+'/'+$m) | Out-Null; $r.name } catch {} } }"`) do set "REPOS=!REPOS! %%N"
    if "!REPOS!"=="" (
        echo No repositories found for set '%SET%' - network, rate limit, or nothing to clone.
        exit /b 1
    )
)

echo ============================================================
echo  HYDRA-UMC / URTC / A.R.M.O.R. Starter Kit - set: %SET%
echo  Cloning into: %CD%
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
echo Next step: each ecosystem's own updater (HYDRA-UMC-UPDATER,
echo URTC-UPDATER, ARMOR-UPDATER - or ELECTRO-HOBBY-3D-UPDATER for all
echo three^) can check versions, install/update any other project one at a
echo time, and build each project via its own build.sh/.bat. This script's
echo only job was step one: getting the source onto disk.

if !failed! GTR 0 exit /b 1
