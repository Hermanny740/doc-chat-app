@echo off
REM setup_windows.bat - Installiert alle Abhängigkeiten für Windows und erstellt benötigte Ordner

REM 1. Virtuelle Umgebung erstellen
python -m venv venv

REM 2. Virtuelle Umgebung aktivieren
call venv\Scripts\activate.bat

REM 3. pip updaten
python -m pip install --upgrade pip

REM 4. Anforderungen installieren
pip install -r requirements.txt

REM 5. Benötigte Ordner erstellen
if not exist data mkdir data
if not exist data\faiss_index mkdir data\faiss_index

echo.
echo ✅ Alle Pakete installiert und benötigte Ordner erstellt!
echo Um die App zu starten, aktiviere die virtuelle Umgebung:
echo call venv\Scripts\activate.bat
echo und dann:
echo streamlit run app.py
pause