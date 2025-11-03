@ECHO off

SET VER=0.022.5
SET UNREALBIN64=C:\Program Files\Epic Games\UE_5.4\Engine\Binaries\Win64
SET BINDIR=%~dp0

REM 1. place font files in rawassets\content\<lang> folder
REM 2. edit pack-<lang>-font.txt 
REM edit into your language name

SET lang=jp 

CD "%BINDIR%\..\rawassets"
SET WORKDIR=%cd%
SET RELEASEDIR=%BINDIR%..\releases
ECHO working dir=%WORKDIR%

"%UNREALBIN64%\UnrealPak.exe" -create="%WORKDIR%\pack-%lang%-font.txt" "%RELEASEDIR%\Vein\Content\Paks\~zzzVein-%lang%-font.pak" 
REM "%UNREALBIN64%\UnrealPak.exe" -create="%WORKDIR%\pack-%lang%-font-full.txt" "%RELEASEDIR%\Vein\Content\Paks\~zzzVein-%lang%-font-full.pak" 

pause >nul