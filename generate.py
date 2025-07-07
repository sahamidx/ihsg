import yfinance as yf
from datetime import datetime

# Kode saham + nama perusahaan singkat
SAHAM_LQ45 = {
    "ACES": "Ace Hardware",
    "ADMR": "Adaro Minerals",
    "ADRO": "Adaro Energy",
    "AKRA": "AKR Corporindo",
    "AMMN": "Amman Mineral",
    "AMRT": "Alfamart",
    "ANTM": "Aneka Tambang",
    "ARTO": "Bank Jago",
    "ASII": "Astra International",
    "BBCA": "Bank Central Asia",
    "BBNI": "Bank Negara Indonesia",
    "BBRI": "Bank Rakyat Indonesia",
    "BBTN": "Bank Tabungan Negara",
    "BMRI": "Bank Mandiri",
    "BRIS": "BRI Syariah",
    "BRPT": "Barito Pacific",
    "CPIN": "Charoen Pokphand",
    "CTRA": "Ciputra Development",
    "ESSA": "Surya Esa Perkasa",
    "EXCL": "XL Axiata",
    "GOTO": "GoTo Gojek Tokopedia",
    "ICBP": "Indofood CBP",
    "INCO": "Vale Indonesia",
    "INDF": "Indofood Sukses Makmur",
    "INKP": "Indah Kiat Pulp",
    "ISAT": "Indosat Ooredoo Hutchison",
    "ITMG": "Indo Tambangraya",
    "JPFA": "Japfa Comfeed",
    "JSMR": "Jasa Marga",
    "KLBF": "Kalbe Farma",
    "MAPA": "Map Aktif Adiperkasa",
    "MAPI": "Mitra Adiperkasa",
    "MBMA": "Merdeka Battery",
    "MDKA": "Merdeka Copper Gold",
    "MEDC": "Medco Energi",
    "PGAS": "Perusahaan Gas Negara",
    "PGEO": "Pertamina Geothermal",
    "PTBA": "Bukit Asam",
    "SIDO": "Industri Jamu Sido Muncul",
    "SMGR": "Semen Indonesia",
    "SMRA": "Summarecon Agung",
    "TLKM": "Telkom Indonesia",
    "TOWR": "Sarana Menara Nusantara",
    "UNTR": "United Tractors",
    "UNVR": "Unilever Indonesia"
}

def fetch_price(symbol):
    try:
        data = yf.download(symbol + ".JK", period="2d", interval="1d", progress=False, auto_adjust=False).dropna()
        if len(data) < 2: return None
        harga = round(data["Close"].iloc[-1])
        harga_kemarin = round(data["Close"].iloc[-2])
        perubahan = ((harga - harga_kemarin) / harga_kemarin) * 100
        return harga, perubahan
    except:
        return None

def fetch_ihsg():
    try:
        data = yf.download("^JKSE", period="2d", interval="1d", progress=False, auto_adjust=False).dropna()
        if len(data) < 2: return None
        harga = round(data["Close"].iloc[-1])
        kemarin = round(data["Close"].iloc[-2])
        perubahan = ((harga - kemarin) / kemarin) * 100
        return harga, perubahan
    except:
        return None

# Waktu hari ini
today = datetime.now().strftime("%d %B %Y")

# Fetch IHSG
ihsg = fetch_ihsg()
ihsg_html = ""
if ihsg:
    arah = "naik" if ihsg[1] >= 0.0 else "turun"
    ihsg_html = f"<h2>IHSG Hari Ini</h2><p><strong>{ihsg[0]:,}".replace(",", ".") + f"</strong> ({ihsg[1]:+.2f}%)</p>"

# Fetch semua saham
rows = ""
data_dict = {}
for kode, nama in SAHAM_LQ45.items():
    result = fetch_price(kode)
    if result:
        harga, perubahan = result
        harga_str = f"Rp{harga:,}".replace(",", ".")
        perubahan_str = f"{perubahan:+.2f}%"
    else:
        harga_str = "N/A"
        perubahan_str = "N/A"
    rows += f"<tr><td>{kode}</td><td>{nama}</td><td>{harga_str}</td><td>{perubahan_str}</td></tr>\n"
    data_dict[kode] = nama

# HTML Output
html = f"""<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Harga Saham LQ45 dan IHSG Hari Ini</title>
  <meta name="description" content="Lihat harga terbaru saham LQ45 dan IHSG hari ini. Termasuk BBCA, BBRI, TLKM, dan lainnya. Update otomatis setiap 30 menit.">
  <style>
    body {{ font-family: Arial, sans-serif; padding: 20px; }}
    h1, h2 {{ color: #333; }}
    input {{ width: 100%; padding: 8px; margin-bottom: 15px; }}
    table {{ border-collapse: collapse; width: 100%; }}
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
  <h1>Harga Saham Hari Ini (LQ45 dan IHSG)</h1>
  <p>Data per {today}. Halaman ini menampilkan harga terbaru dari saham-saham terlikuid di Indonesia beserta IHSG, diperbarui otomatis setiap 30 menit.</p>
  {ihsg_html}
  <input type="text" id="cari" placeholder="Cari saham BBCA, Telkom, Unilever...">
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
const tabel = document.getElementById('tabel').getElementsByTagName('tbody')[0];
const hasil = document.getElementById('hasil');
const data = {str(data_dict)};

input.addEventListener('keyup', function() {{
  const filter = this.value.toLowerCase();
  const rows = tabel.getElementsByTagName('tr');
  let ketemu = false;
  for (let i = 0; i < rows.length; i++) {{
    const kode = rows[i].cells[0].textContent.toLowerCase();
    const nama = rows[i].cells[1].textContent.toLowerCase();
    if (kode.includes(filter) || nama.includes(filter)) {{
      rows[i].style.display = '';
      if (!ketemu && filter.length >= 2) {{
        hasil.innerHTML = `<h2>Saham ${kode.toUpperCase()} Hari Ini</h2>`;
        ketemu = true;
      }}
    }} else {{
      rows[i].style.display = 'none';
    }}
  }}
  if (!ketemu) hasil.innerHTML = '';
}});
</script>
</body>
</html>
"""

with open("saham_lq45.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ sukses: saham_lq45.html dibuat.")
