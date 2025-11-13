@echo off
echo ========================================
echo Crypto Streaming Pipeline - Demarrage
echo ========================================
echo.

echo [1/4] Verification de Docker...
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Docker n'est pas lance.
    pause
    exit /b 1
)
echo [OK] Docker pret!

echo [2/4] Verification de Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Python n'est pas installe.
    pause
    exit /b 1
)
echo [OK] Python detecte

echo [3/4] Creation environnement virtuel...
if not exist "venv" (
    python -m venv venv
)
call venv\Scripts\activate.bat
pip install -q -r requirements.txt
echo [OK] Dependances installees

echo [4/4] Demarrage services Docker...
docker-compose up -d

echo.
echo ========================================
echo Infrastructure demarree !
echo ========================================
echo.
echo Interfaces Web:
echo   - Kafka UI:    http://localhost:8080
echo   - Grafana:     http://localhost:3000
echo   - Prometheus:  http://localhost:9090
echo   - ClickHouse:  http://localhost:8123
echo.
pause
