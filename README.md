# Setup Environment 
c:\Users\galaxy\AppData\Local\Programs\Python\Python312\python.exe -m venv venv

# go to project dirctory
cd /path/to/destination/your_project_directory

# create Environment 
python -m venv venv

# Enable powershell Sript
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# Activate Environment
PS D:\code\youtubeDownloader> venv\Scripts\activate

# --------------- package installation ---------------
python install -r requirements.txt

# --------------- or Manually installation ---------------
# Install Flask
pip install Flask

# install pytube 
pip install pytube
