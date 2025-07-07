import yfinance as yf
import pandas as pd
from datetime import datetime

SAHAM_LIST = [
    "ACES", "ADMR", "ADRO", "AKRA", "AMMN", "AMRT", "ANTM", "ARTO",
    "ASII", "BBCA", "BBNI", "BBRI", "BBTN", "BMRI", "BRIS", "BRPT",
    "CPIN", "CTRA", "ESSA", "EXCL", "GOTO", "ICBP", "INCO", "INDF",
    "INKP", "ISAT", "ITMG", "JPFA", "JSMR", "KLBF", "MAPA", "MAPI",
    "MBMA", "MDKA", "MEDC", "PGAS", "PGEO", "PTBA", "SIDO", "SMGR",
    "SMRA", "TLKM", "TOWR", "UNTR", "UNVR"
]

HARI_INDONESIA = {
    "Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu",
    "Thursday": "Kamis", "Friday": "Jumat", "Saturday": "Sabtu", "Sunday": "Minggu"
}

def fetch_data(symbol):
    try:
        df = yf.download(symbol + ".JK", period="2d", interval="1d", progress=False, auto_adjust=False).dropna()
        if len(df) < 2: return None
        harga_today = df["Close"].iloc[-1].item()
        harga_yesterday = df["Close"].iloc[-2].item()
        change = ((harga_today - harga_yesterday) / harga_yesterday) * 100
        return {"harga": f"Rp{round(harga_today):,}".replace(",", "."), "change": f"{change:+.2f}%"}
    except: return None

def fetch_ihsg():
    try:
        df = yf.download("^JKSE", period="2d", interval="1d", progress=False, auto_adjust=False).dropna()
        if len(df) < 2: return None
        harga_today = df["Close"].iloc[-1].item()
        harga_yesterday = df["Close"].iloc[-2].item()
        change = ((harga_today - harga_yesterday) / harga_yesterday) * 100
        return {"harga": f"{round(harga_today):,}".replace(",", "."), "change": f"{change:+.2f}%"}
    except: return None

data_saham = {}
for kode in SAHAM_LIST:
    hasil = fetch_data(kode)
    if hasil:
        data_saham[kode] = hasil
    else:
        data_saham[kode] = {"harga": "N/A", "change": "Gagal ambil data"}

now = datetime.now()
judul_hari = f"{HARI_INDONESIA[now.strftime('%A')]}, {now.strftime('%d %B %Y')}"
ihsg = fetch_ihsg()
if ihsg:
    arah = "naik" if "-" not in ihsg["change"] else "turun"
    ihsg_html = f"<div class='ihsg-box {arah}'><strong>IHSG:</strong> {ihsg['harga']} <span>({ihsg['change']})</span></div>"
else:
    ihsg_html = "<div class='ihsg-box gagal'><strong>IHSG:</strong> <span>Data tidak tersedia</span></div>"

html = f"""<!DOCTYPE html>
<html lang="id"><head><meta charset="UTF-8">
<style>
body {{ font-family: sans-serif; font-size: 14px; }}
#sahamWidget {{ border: 1px solid #ccc; padding: 10px; border-radius: 6px; }}
select {{ width: 100%; margin-bottom: 10px; }}
.naik {{ color: green; }} .turun {{ color: red; }} .gagal {{ color: gray; font-style: italic; }}
.ihsg-box {{ padding: 8px; margin-bottom: 10px; border-radius: 5px; color: white; }}
.ihsg-box.naik {{ background-color: #4CAF50; }}
.ihsg-box.turun {{ background-color: #f44336; }}
.ihsg-box.gagal {{ background-color: #999; }}
</style></head><body>
<div id="sahamWidget">
  <h4>Harga Saham Hari Ini – {judul_hari}</h4>
  {ihsg_html}
  <select id="dropdownSaham">
"""

for kode in SAHAM_LIST:
    html += f'    <option value="{kode}">{kode}</option>\n'

html += """  </select>
  <div id="infoHarga"></div>
</div>
<script>
const data = """ + str(data_saham).replace("'", '"') + """;
const infoDiv = document.getElementById("infoHarga");
const dropdown = document.getElementById("dropdownSaham");

function updateInfo() {
  const kode = dropdown.value;
  const item = data[kode];
  let kelas = "naik";
  if (item.change === "Gagal ambil data") {{
    kelas = "gagal";
  }} else if (item.change.startsWith("-")) {{
    kelas = "turun";
  }}
  infoDiv.innerHTML = `<strong>${kode}</strong><br>Harga: ${item.harga}<br><span class='${kelas}'>Perubahan: ${item.change}</span>`;
}
dropdown.addEventListener("change", updateInfo);
window.addEventListener("load", updateInfo);
</script></body></html>"""

with open("saham_lq45.html", "w", encoding="utf-8") as f:
    f.write(html)
print("✅ sukses: saham_lq45.html dibuat.")
