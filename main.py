import requests
import fitz  # PyMuPDF
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# PDF herunterladen
url = "https://www.kba.de/SharedDocs/Downloads/DE/Pressemitteilungen/2025/pm_29_2025_nr1_seg_06_2025.pdf?__blob=publicationFile&v=4"
response = requests.get(url)
with open("kba_juni2025.pdf", "wb") as f:
    f.write(response.content)

# PDF auslesen
doc = fitz.open("kba_juni2025.pdf")
text = "".join(page.get_text() for page in doc)

# Daten extrahieren
pattern = r"(Benzin|Diesel|Elektro|Hybrid|Plug-in-Hybrid|Sonstige)[^\d]*(\d{1,2},\d)\s?%"
matches = re.findall(pattern, text)

# Daten vorbereiten
bezugsmonat = "Juni 2025"
daten = [["Antriebsart", bezugsmonat]] + matches

# Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("KBA Antriebsarten").sheet1
sheet.clear()
sheet.update("A1", daten)
