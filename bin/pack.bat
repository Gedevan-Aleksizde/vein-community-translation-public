SET var=%cd%
SET lang=JP
echo %var%
"C:\Program Files\Epic Games\UE_5.4\Engine\Binaries\Win64\UnrealPak.exe" -create="%var%\..\pak\pack-%lang%.txt" "%var%\..\releases\Vein\Content\Paks\~zzzVein-%lang%.pak" 
"C:\Program Files\Epic Games\UE_5.4\Engine\Binaries\Win64\UnrealPak.exe" -create="%var%\..\pak\pack-%lang%-font.txt" "%var%\..\releases\Vein\Content\Paks\~zzzVein-%lang%-font.pak" 

pause >nul