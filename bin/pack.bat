@ECHO OFF

SET VER=0.022.5
SET UNREALBIN64=C:\Program Files\Epic Games\UE_5.4\Engine\Binaries\Win64
SET BINDIR=%~dp0

SET RELEASEDIR=%BINDIR%..\releases

CD "%BINDIR%..\rawassets"

SET ROOTDIR=%CD%

ECHO working dir=%var%

FOR /D %%m IN (..\rawassets\content\*) DO (
  ECHO ----- packing %%~nm language files... ------
  TYPE nul > tmp\pack-%%~nm.txt
  ECHO "%ROOTDIR%\content\%%~nm\Game.locres" "../../../Vein/Content/Localization/Game/en/Game.locres" >> "%ROOTDIR%\tmp\pack-%%~nm.txt"
  ECHO "%ROOTDIR%\content\%%~nm\Game2.locres" "../../../Vein/Content/Localization/Game/%%~nm/Game.locres" >> "%ROOTDIR%\tmp\pack-%%~nm.txt"
  "%UNREALBIN64%\UnrealPak.exe" -create="%ROOTDIR%\tmp\pack-%%~nm.txt" "%RELEASEDIR%\Vein\Content\Paks\~zzzVein-%%~nm.pak"

)

pause >nul