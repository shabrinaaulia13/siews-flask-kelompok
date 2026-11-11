# Menguji aplikasi tanpa menjalankan server, memakai test client Flask
import re
from app import app

klien = app.test_client()

def judul(html):  # ambil isi <h1> sebagai ringkasan halaman
    return re.search(r"<h1>(.*?)</h1>", html, re.S).group(1).strip()

URL_UJI = [
    "/",
    "/mahasiswa?prodi=ti",
    "/mahasiswa/A11.2023.00002",
    "/mahasiswa/X99",
    "/api/mahasiswa/A13.2023.00005",
]

for url in URL_UJI:
    r = klien.get(url)
    isi = r.get_json()["nama"] if r.is_json else judul(r.get_data(as_text=True))
    print(f"GET  {url:<31} -> {r.status_code}  {isi}")

r = klien.post("/cari", data={"nim": "A12.2023.00003"})
print(f"POST /cari                       -> {r.status_code}  Location: {r.headers['Location']}")

# Autoescaping Jinja mencegah XSS
from flask import render_template_string
with app.app_context():
    print("Autoescape:", render_template_string("{{ x }}", x="<script>alert(1)</script>"))