@echo off
echo Gerando Executavel...

:: Substitua 'meu_projeto.py' pelo nome exato que voce encontrou no Passo 1
pyinstaller --noconsole --onefile --add-data "maxi.png;." --add-data "ultra.png;." --add-data "icone.ico;." --icon="icone.ico" app.py

echo.
echo Processo concluido! Verifique a pasta 'dist'.
pause