import yfinance as yf
from datetime import datetime
import locale

# Format tanggal lokal (Indonesia)
try:
    locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')
except:
    locale.setlocale(locale.LC_TIME, '')

# Saham LQ45 + nama singkat
SAHAM_LQ45 = {
    "ACES": "Ace Hardware", "ADMR": "Adaro Minerals", "ADRO": "Adaro Energy", "AKRA": "AKR Corporindo",
    "AMMN": "Amman Mineral", "AMRT": "Alfamart", "ANTM": "Aneka Tambang", "ARTO": "Bank Jago",
    "ASII": "Astra International", "BBCA": "Bank Central Asia", "BBNI": "Bank Negara Indonesia",
    "BBRI": "Bank Rakyat Indonesia", "BBTN": "Bank Tabungan Negara", "BMRI": "Bank Mandiri",
    "BRIS": "BRI Syariah", "BRPT": "Barito Pacific", "CPIN": "Charoen Pokphand", "CTRA": "Ciputra Development",
    "ESSA": "Surya Esa Perkasa", "EXCL": "XL Axiata", "GOTO": "GoTo Gojek Tokopedia",
    "ICBP": "Indofood CBP", "INCO": "Vale Indonesia", "INDF": "Indofood Sukses Makmur",
    "INKP": "Indah Kiat Pulp", "ISAT": "Indosat Ooredoo Hutchison", "ITMG": "Indo Tambangraya",
    "JPFA": "Japfa Comfeed", "JSMR": "Jasa Marga", "KLBF": "Kalbe Farma", "MAPA": "Map Aktif",
    "MAPI": "Mitra Adiperkasa", "MBMA": "Merdeka Battery", "MDKA": "Merdeka Copper Gold",
    "MEDC": "Medco Energi", "PGAS": "Perusahaan Gas Negara", "PGEO": "Pertamina Geothermal",
    "PTBA": "Bukit Asam", "SIDO": "Sido Muncul", "SMGR": "Semen Indonesia",
    "SMRA": "Summarecon", "TLKM": "Telkom Indonesia", "TOWR": "Sarana Menara Nusantara",
    "UNTR": "United Tractors", "UNVR": "Unilever Indonesia"
}

def fetch_price(symbol):
    try:
        data = yf.download(symbol + ".JK", period="2d", interval="1d", progress=False, auto_adjust=False).dropna()
        if len(data) < 2: return None
        harga = round(data["Close"].iloc[-1].item())
        harga_kemarin = round(data["Close"].iloc[-2].item())
        perubahan = ((harga - harga_kemarin) / harga_kemarin) * 100
        return harga, round(perubahan, 2)
    except:
        return None

def fetch_ihsg():
    try:
        data = yf.download("^JKSE", period="2d", interval="1d", progress=False, auto_adjust=False).dropna()
        if len(data) < 2: return None
        harga = round(data["Close"].iloc[-1].item())
        kemarin = round(data["Close"].iloc[-2].item())
        perubahan = ((harga - kemarin) / kemarin) * 100
        return harga, round(perubahan, 2)
    except:
        return None

# Tanggal
tanggal = datetime.now().strftime("%A, %d %B %Y")
tanggal = tanggal.replace('Sunday', 'Minggu').replace('Monday', 'Senin').replace('Tuesday', 'Selasa')\
    .replace('Wednesday', 'Rabu').replace('Thursday', 'Kamis').replace('Friday', 'Jumat')\
    .replace('Saturday', 'Sabtu')

# IHSG box
ihsg_data = fetch_ihsg()
if ihsg_data:
    arah = "naik" if ihsg_data[1] >= 0 else "turun"
    warna = "naik" if ihsg_data[1] >= 0 else "turun"
    ihsg_html = f"""
    <h2>IHSG Hari Ini</h2>
    <div class="ihsg-box {warna}">{ihsg_data[0]:,} ({ihsg_data[1]:+.2f}%)</div>
    """.replace(",", ".")
else:
    ihsg_html = ""

# Saham rows
rows = ""
data_dict = {}
for kode, nama in SAHAM_LQ45.items():
    result = fetch_price(kode)
    if result:
        harga, perubahan = result
        warna = "naik" if perubahan >= 0 else "turun"
        harga_str = f"Rp{harga:,}".replace(",", ".")
        perubahan_str = f'<td class="{warna}">{perubahan:+.2f}%</td>'
        rows += f"<tr><td>{kode}</td><td>{nama}</td><td>{harga_str}</td>{perubahan_str}</tr>\n"
        data_dict[kode] = nama

# HTML output
html = f"""<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <title>Harga Saham Hari Ini – {tanggal}</title>
  <meta name="description" content="Harga saham LQ45 dan IHSG hari ini, termasuk BBCA, BBRI, TLKM, dan lainnya. Update otomatis setiap 30 menit.">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {{ font-family: Arial, sans-serif; padding: 20px; }}
    h1, h2 {{ color: #333; }}
    .ihsg-box {{ font-size: 1.4em; font-weight: bold; margin-bottom: 20px; }}
    .naik {{ color: green; }}
    .turun {{ color: red; }}
    input {{ width: 100%; padding: 8px; margin-bottom: 15px; }}
    table {{ border-collapse: collapse; width: 100%; display: none; }}
    th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
    th {{ background-color: #f4f4f4; }}
    tr.hide {{ display: none; }}
    @media(max-width:600px) {{
      table, thead, tbody, th, td, tr {{ display: block; }}
      th {{ position: absolute; top: -9999px; left: -9999px; }}
      td {{ border: none; position: relative; padding-left: 50%; }}
      td::before {{
        position: absolute; top: 8px; left: 8px; width: 45%; white-space: nowrap;
        font-weight: bold;
      }}
      td:nth-of-type(1)::before {{ content: "Kode"; }}
      td:nth-of-type(2)::before {{ content: "Perusahaan"; }}
      td:nth-of-type(3)::before {{ content: "Harga"; }}
      td:nth-of-type(4)::before {{ content: "Perubahan"; }}
    }}
  </style>
</head>
<body>
  <h1>Saham Hari Ini</h1>
  <p>Harga Saham Hari Ini – {tanggal}</p>
  {ihsg_html}
  <input type="text" id="cari" placeholder="Cari saham BBRI, Telkom, Unilever...">
  <div id="hasil"></div>
  <table id="tabel">
    <thead>
      <tr><th>Kode</th><th>Perusahaan</th><th>Harga</th><th>Perubahan</th></tr>
    </thead>
    <tbody>
      {rows}
    </tbody>
  </table>
<script>
const input = document.getElementById('cari');
const tabel = document.getElementById('tabel');
const tbody = tabel.getElementsByTagName('tbody')[0];
const hasil = document.getElementById('hasil');
const data = {str(data_dict)};

tabel.style.display = 'none';

input.addEventListener('input', function () {{
  const filter = this.value.toLowerCase();
  const rows = tbody.getElementsByTagName('tr');
  let ketemu = false;

  if (filter.length > 0) {{
    tabel.style.display = 'table';
  }} else {{
    tabel.style.display = 'none';
    hasil.innerHTML = '';
    return;
  }}

  for (let i = 0; i < rows.length; i++) {{
    const kode = rows[i].cells[0].textContent.toLowerCase();
    const nama = rows[i].cells[1].textContent.toLowerCase();
    if (kode.includes(filter) || nama.includes(filter)) {{
      rows[i].style.display = '';
      if (!ketemu && filter.length >= 2) {{
        hasil.innerHTML = "<h2>Saham " + kode.toUpperCase() + " Hari Ini</h2>";
        ketemu = true;
      }}
    }} else {{
      rows[i].style.display = 'none';
    }}
  }}

  if (!ketemu) {{
    hasil.innerHTML = '';
  }}
}});
</script>
</body>
</html>
"""

with open("saham_lq45.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ sukses: saham_lq45.html dibuat.")
