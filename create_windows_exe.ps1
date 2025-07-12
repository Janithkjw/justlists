Write-Host "============================================" -ForegroundColor Green
Write-Host "Workshop Inventory Management - Windows Executable Builder" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""

Write-Host "Installing required packages..." -ForegroundColor Yellow
python -m pip install --upgrade pip
pip install Flask==2.3.3 Flask-SQLAlchemy==3.0.5 Werkzeug==2.3.7 openpyxl==3.1.2 Pillow==10.0.1 python-dotenv==1.0.0 pyinstaller

Write-Host ""
Write-Host "Building Windows executable..." -ForegroundColor Yellow
pyinstaller --onefile --windowed --name "Workshop_Inventory_Management" --icon=static/favicon.ico --add-data "templates;templates" --add-data "static;static" --hidden-import=openpyxl --hidden-import=PIL --hidden-import=sqlite3 launcher.py

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "Build complete!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host "Your Windows executable is located in the 'dist' folder" -ForegroundColor Cyan
Write-Host "File: Workshop_Inventory_Management.exe" -ForegroundColor Cyan
Write-Host ""
Write-Host "Double-click the .exe file to run the application" -ForegroundColor White
Write-Host "Default login: admin / admin123" -ForegroundColor White
Write-Host "============================================" -ForegroundColor Green
Read-Host "Press Enter to exit"