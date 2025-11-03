@ECHO OFF

SET BINDIR=%~dp0
CALL "%BINDIR%\settings.bat"

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

