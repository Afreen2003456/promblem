@echo off
echo ✈️ Airline Analytics Dashboard - GitHub Deployment Script
echo ============================================================
echo.

:: Check if Git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git is not installed or not in PATH
    echo Please install Git from https://git-scm.com/
    pause
    exit /b 1
)

:: Get user input
echo 📝 Please provide the following information:
echo.
set /p GITHUB_USERNAME="Enter your GitHub username: "
set /p REPO_NAME="Enter repository name (default: airline-analytics-dashboard): "
if "%REPO_NAME%"=="" set REPO_NAME=airline-analytics-dashboard

echo.
echo 🔧 Configuration:
echo GitHub Username: %GITHUB_USERNAME%
echo Repository Name: %REPO_NAME%
echo.

set /p CONFIRM="Is this correct? (y/n): "
if /i not "%CONFIRM%"=="y" (
    echo ❌ Deployment cancelled
    pause
    exit /b 1
)

:: Create deployment directory
echo.
echo 📁 Creating deployment directory...
if exist "%REPO_NAME%" (
    echo Directory %REPO_NAME% already exists. Removing...
    rmdir /s /q "%REPO_NAME%"
)
mkdir "%REPO_NAME%"
cd "%REPO_NAME%"

:: Initialize Git repository
echo.
echo 🔄 Initializing Git repository...
git init
git branch -M main

:: Copy dashboard files
echo.
echo 📋 Copying dashboard files...

:: Copy frontend files
copy "..\frontend\index.html" "index.html" >nul
copy "..\frontend\styles.css" "styles.css" >nul
copy "..\frontend\app.js" "app.js" >nul

:: Create README.md
echo.
echo 📄 Creating README.md...
(
echo # ✈️ Airline Analytics Dashboard
echo.
echo ^> Real-time insights into airline booking trends, popular routes, and market demand
echo.
echo ## 🌟 Features
echo.
echo - **Interactive Data Visualization** - Charts and graphs for trends analysis
echo - **Real-time Flight Search** - Search and filter flights by route and price
echo - **Market Insights** - AI-powered analysis of airline data
echo - **Responsive Design** - Works on desktop and mobile devices
echo - **Export Functionality** - Download data in CSV format
echo.
echo ## 🎯 Live Demo
echo.
echo 🔗 **[View Live Dashboard](https://%GITHUB_USERNAME%.github.io/%REPO_NAME%/)**
echo.
echo ## 🛠️ Technologies Used
echo.
echo - **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
echo - **Charts:** Chart.js for data visualization
echo - **Backend:** Python FastAPI (for local development^)
echo - **Deployment:** GitHub Pages
echo.
echo ## 📈 Key Metrics
echo.
echo - **300+** Sample flights analyzed
echo - **16** Major airports covered
echo - **8** Airlines included
echo - **10** Popular routes tracked
echo.
echo ## 🚀 Quick Start
echo.
echo 1. Visit the [live dashboard](https://%GITHUB_USERNAME%.github.io/%REPO_NAME%/^)
echo 2. Use the filter options to search for flights
echo 3. View interactive charts and analytics
echo 4. Export data for further analysis
echo.
echo ## 🔧 Local Development
echo.
echo ```bash
echo # Clone the repository
echo git clone https://github.com/%GITHUB_USERNAME%/%REPO_NAME%.git
echo.
echo # Navigate to project directory
echo cd %REPO_NAME%
echo.
echo # Open in your browser
echo open index.html
echo ```
echo.
echo ## 📄 License
echo.
echo This project is licensed under the MIT License.
echo.
echo ## 🙏 Acknowledgments
echo.
echo - Flight data powered by aviation APIs
echo - Charts created with Chart.js
echo - UI built with Bootstrap 5
) > README.md

:: Update app.js for GitHub Pages deployment
echo.
echo 🔧 Updating app.js for GitHub Pages deployment...
(
echo // Airline Analytics Dashboard - JavaScript (GitHub Pages Version^)
echo const API_BASE_URL = ''; // Use sample data for GitHub Pages
echo const USE_SAMPLE_DATA = true;
echo.
) > temp_app.js
type "..\frontend\app.js" >> temp_app.js
move temp_app.js app.js >nul

:: Add files to Git
echo.
echo 📦 Adding files to Git...
git add .
git commit -m "🚀 Deploy Airline Analytics Dashboard to GitHub Pages"

:: Add remote origin
echo.
echo 🔗 Adding remote origin...
git remote add origin https://github.com/%GITHUB_USERNAME%/%REPO_NAME%.git

:: Push to GitHub
echo.
echo 🚀 Pushing to GitHub...
echo.
echo ⚠️  IMPORTANT: You need to create the repository on GitHub first!
echo.
echo 1. Go to https://github.com/new
echo 2. Create a repository named: %REPO_NAME%
echo 3. Make it PUBLIC (required for GitHub Pages^)
echo 4. Do NOT initialize with README (we already have one^)
echo 5. Click "Create repository"
echo.
echo After creating the repository, press any key to continue...
pause

echo.
echo 🔄 Pushing files to GitHub...
git push -u origin main

if %errorlevel% neq 0 (
    echo.
    echo ❌ Failed to push to GitHub
    echo Please check:
    echo - Repository exists and is public
    echo - You have push access to the repository
    echo - Your GitHub credentials are correct
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Successfully deployed to GitHub!
echo.
echo 🌐 Setting up GitHub Pages...
echo.
echo Manual steps to enable GitHub Pages:
echo 1. Go to https://github.com/%GITHUB_USERNAME%/%REPO_NAME%
echo 2. Click "Settings" tab
echo 3. Scroll down to "Pages" section
echo 4. Under "Source" select "Deploy from a branch"
echo 5. Select branch: "main"
echo 6. Select folder: "/ (root^)"
echo 7. Click "Save"
echo.
echo 🎉 Your dashboard will be available at:
echo https://%GITHUB_USERNAME%.github.io/%REPO_NAME%/
echo.
echo ⏱️  GitHub Pages deployment usually takes 5-10 minutes
echo.

:: Open GitHub repository in browser
echo 🌐 Opening GitHub repository in browser...
start https://github.com/%GITHUB_USERNAME%/%REPO_NAME%

:: Clean up
cd ..
echo.
echo 🧹 Cleaning up...
echo Deployment files are in: %REPO_NAME%
echo.
echo 📊 Deployment Summary:
echo - Repository: %GITHUB_USERNAME%/%REPO_NAME%
echo - Files deployed: index.html, styles.css, app.js, README.md
echo - GitHub Pages URL: https://%GITHUB_USERNAME%.github.io/%REPO_NAME%/
echo.
echo 🎯 Next Steps:
echo 1. Enable GitHub Pages in repository settings
echo 2. Wait 5-10 minutes for deployment
echo 3. Visit your live dashboard!
echo.
echo ✨ Happy coding!
pause 