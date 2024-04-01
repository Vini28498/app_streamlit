import subprocess
import sys

# Use sys.executable para obter o caminho para o executável Python atual e execute o pip
subprocess.run([sys.executable, "-m", "pip", "install", "gspread"])