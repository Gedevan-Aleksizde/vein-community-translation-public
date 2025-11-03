@ECHO OFF

SET VER=0.022.5
SET STORAGEDIR=D:\User\Documents\Unreal Projects\VEIN-l10n
SET BINDIR=%~dp0

CD "%STORAGEDIR%\text\to-locres\"
SET dirloop=%CD%

ECHO %dirloop%

FOR /D %%f IN ( "%dirloop%\*" ) DO (
  echo %%f / %%~nf
  MKDIR "%dirloop%\%%~nf\"
  COPY "%STORAGEDIR%\text\original-locres\%VER%\en\Game.locres" "%dirloop%\%%~nf\"
  COPY /Y "%STORAGEDIR%\text\original-locres\%VER%\%%~nf\Game.locres" "%dirloop%\%%~nf\"
  "%BINDIR%\UE4localizationsTool.exe" -import "%%f\game.locres.txt"
  COPY /Y "%dirloop%\%%~nf\Game.locres" "%BINDIR%\..\rawassets\content\%%~nf\Game.locres"
  COPY /Y "%dirloop%\%%~nf\Game.locres" "%BINDIR%\..\rawassets\content\%%~nf\Game2.locres"
)

