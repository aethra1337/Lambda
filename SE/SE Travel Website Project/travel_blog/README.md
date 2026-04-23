# Wanderlust — Seyahat Blog Sitesi

## Kurulum

```bash
pip install -r requirements.txt
python app.py
```

Tarayıcıda aç: http://localhost:5000

## Proje Yapısı

```
travel_blog/
├── app.py                  # Flask uygulaması, route'lar, veri
├── requirements.txt
├── templates/
│   ├── base.html           # Ortak layout (nav, footer)
│   ├── index.html          # Anasayfa (hero, yazılar, galeri)
│   ├── gallery.html        # Tam galeri sayfası
│   └── post.html           # Blog yazısı detay sayfası
└── static/
    ├── css/
    │   └── main.css        # Tüm stiller (Clean & Modern tema)
    └── js/
        └── main.js         # Cursor, animasyonlar, lightbox, filtre
```

## Özellikler

- Custom cursor (masaüstü)
- Scroll reveal animasyonları
- Hover efektleri (kart, görsel zoom, ok dönüşü)
- Infinite marquee şerit
- Kategori filtre sistemi (JS + CSS geçiş)
- Galeri lightbox (klavye + tıklama navigasyonu)
- Hero parallax efekti
- Responsive tasarım (mobil hamburger menü)
- Flask API endpoint: GET /api/posts?category=Asya
