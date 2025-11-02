@echo off

SET unrealbin64=C:\Program Files\Epic Games\UE_5.4\Engine\Binaries\Win64

CD ..\rawassets
SET var=%cd%
ECHO working dir=%var%

FOR /D %%m IN (..\rawassets\content\*) DO (
  ECHO ----- packing %%~nm language files... ------
  TYPE nul > tmp\pack-%%~nm.txt
  ECHO "%var%\content\%%~nm\Game.locres" "../../../Vein/Content/Localization/Game/en/Game.locres" >> "..\rawassets\tmp\pack-%%~nm.txt"
  ECHO "%var%\content\%%~nm\Game2.locres" "../../../Vein/Content/Localization/Game/%%~nm/Game.locres" >> "..\rawassets\tmp\pack-%%~nm.txt"

  "%unrealbin64%\UnrealPak.exe" -create="%var%\..\rawassets\tmp\pack-%%~nm.txt" "%var%\..\releases\Vein\Content\Paks\~zzzVein-%%~nm.pak"

  REM "%unrealbin64%\UnrealPak.exe" -create="%var%\..\rawassets\pack-%lang%-font.txt" "%var%\..\releases\Vein\Content\Paks\~zzzVein-%lang%-font.pak" 
  REM "%unrealbin64%\UnrealPak.exe" -create="%var%\..\rawassets\pack-%lang%-font-full.txt" "%var%\..\releases\Vein\Content\Paks\~zzzVein-%lang%-font-full.pak" 

)

pause >nul