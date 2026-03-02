@echo off
echo ========================================
echo   D&D Character Sheet - Build Script
echo ========================================
echo.

REM Verifica se PyInstaller está instalado
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller nao encontrado. Instalando...
    pip install pyinstaller
    echo.
)

echo Criando executavel...
echo.

REM Executa PyInstaller
pyinstaller --name="DnD Character Sheet" --onefile --windowed --add-data="data;data" --optimize=2 --clean main.py

echo.
echo ========================================
echo   Build concluido!
echo ========================================
echo.
echo O executavel esta em: dist\DnD Character Sheet.exe
echo.
pause
