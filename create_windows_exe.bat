@echo off
echo ============================================
echo Workshop Inventory Management - Windows Executable Builder
echo ============================================
echo.

echo Installing required packages...
python -m pip install --upgrade pip
pip install Flask==2.3.3 Flask-SQLAlchemy==3.0.5 Werkzeug==2.3.7 openpyxl==3.1.2 Pillow==10.0.1 python-dotenv==1.0.0 pyinstaller

echo.
echo Building Windows executable...
pyinstaller --onefile --windowed --name "Workshop_Inventory_Management" --icon=static/favicon.ico --add-data "templates;templates" --add-data "static;static" --hidden-import=openpyxl --hidden-import=PIL --hidden-import=sqlite3 launcher.py

echo.
echo ============================================
echo Build complete!
echo ============================================
echo Your Windows executable is located in the 'dist' folder
echo File: Workshop_Inventory_Management.exe
echo.
echo Double-click the .exe file to run the application
echo Default login: admin / admin123
echo ============================================
pause