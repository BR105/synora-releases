@echo off
chcp 65001 >nul
REM ============================================================
REM  ABRE ZYNORA POR PRIMERA VEZ EN ESTE EQUIPO.
REM  Solo doble clic: se pedira permiso de administrador una vez.
REM  Hace de CONFIANZA a Zynora, le quita la marca de Internet
REM  (para que NO salga "Windows protegio tu PC") y la abre.
REM  Despues de esto puedes abrir Zynora.exe directamente.
REM ============================================================

REM --- Auto-elevacion: si no es admin, se relanza pidiendo permiso ---
net session >nul 2>&1
if %errorlevel% neq 0 (
  echo  Solicitando permisos de administrador...
  powershell -NoProfile -Command "Start-Process -FilePath '%~f0' -Verb RunAs" >nul 2>&1
  exit /b
)

set "DIR=%~dp0"
set "CER=%~dp0Zynora.cer"
set "EXE=%~dp0Zynora.exe"

if not exist "%EXE%" (
  echo  [!] No se encontro Zynora.exe junto a este script.
  pause
  exit /b 1
)

echo.
echo  Confiando en el certificado de Zynora (raiz + editores)...
if exist "%CER%" (
  certutil -addstore -f Root "%CER%" >nul
  certutil -addstore -f TrustedPublisher "%CER%" >nul
)

echo  Quitando la marca de Internet de la carpeta (evita SmartScreen)...
powershell -NoProfile -Command "Get-ChildItem -LiteralPath '%DIR%' -Recurse -File | Unblock-File" 2>nul

echo  Abriendo Zynora...
REM Lanza Zynora SIN privilegios de admin (via explorer, que corre como el usuario).
explorer.exe "%EXE%"

echo.
echo  ============================================================
echo   LISTO. Zynora deberia estar abriendose.
echo   Si no abrio sola, haz doble clic en Zynora.exe (ya no avisara).
echo.
echo   Si actualizas Zynora a una version nueva y vuelve a avisar,
echo   ejecuta de nuevo este archivo para desbloquear la copia nueva.
echo  ============================================================
echo.
timeout /t 6 >nul
