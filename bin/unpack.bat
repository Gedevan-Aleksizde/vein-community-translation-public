@ECHO OFF

SET VER=0.022.5
SET STORAGEDIR=D:\User\Documents\Unreal Projects\VEIN-l10n
SET BINDIR=%~dp0

MKDIR "%STORAGEDIR%\tmp-pak"
MKDIR "%STORAGEDIR%\text\original-locres\%VER%"
MKDIR "%STORAGEDIR%\text\original-txt\%VER%"


"C:\Program Files\Epic Games\UE_5.4\Engine\Binaries\Win64\UnrealPak.exe" "C:\Program Files (x86)\Steam\steamapps\common\Vein\Vein\Content\Paks\pakchunk0-Windows.pak" -extract "%STORAGEDIR%\tmp-pak"
XCOPY /s /Y "%STORAGEDIR%\tmp-pak\Vein\Content\Vein\Localization\Game" "%STORAGEDIR%\text\original-locres\%VER%\"
CD "%STORAGEDIR%\text\original-locres\%VER%"

SET dirloop=%STORAGEDIR%\text\original-locres\%VER%\*

FOR /D %%f IN ( "%dirloop%" ) DO (
  echo %%f / %%~nf
  "%BINDIR%\UE4localizationsTool.exe" export "%%f\Game.locres"
  MKDIR "%STORAGEDIR%\text\original-txt\%VER%\%%~nf\"
  COPY "%%f\game.locres.txt" "%STORAGEDIR%\text\original-txt\%VER%\%%~nf\"
)

