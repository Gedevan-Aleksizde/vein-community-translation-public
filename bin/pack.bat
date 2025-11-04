@ECHO OFF

SET BINDIR=%~dp0
CALL "%BINDIR%\settings.bat"

SET RELEASEDIR=%BINDIR%..\releases

CD "%BINDIR%..\rawassets"

SET ROOTDIR=%CD%

ECHO working dir=%CD%

FOR /D %%m IN (..\rawassets\content\*) DO (
  ECHO ----- packing %%~nm language files... ------
  TYPE nul > tmp\pack-%%~nm.txt
  ECHO "%ROOTDIR%\content\%%~nm\Game.locres" "../../../Vein/Content/Localization/Game/en/Game.locres" >> "%ROOTDIR%\tmp\pack-%%~nm.txt"
  ECHO "%ROOTDIR%\content\%%~nm\Game2.locres" "../../../Vein/Content/Localization/Game/%%~nm/Game.locres" >> "%ROOTDIR%\tmp\pack-%%~nm.txt"
  "%UNREALBIN64%\UnrealPak.exe" -create="%ROOTDIR%\tmp\pack-%%~nm.txt" "%RELEASEDIR%\Vein\Content\Paks\~zzzVein-%%~nm.pak"

)

pause >nul