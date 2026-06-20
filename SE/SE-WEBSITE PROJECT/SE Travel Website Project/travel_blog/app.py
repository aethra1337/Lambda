import math
import os
from uuid import uuid4

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "dev-admin-secret-key"
UPLOAD_FOLDER = os.path.join(app.static_folder, "uploads")
ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

posts = [
    {
        "id": 1,
        "title": "Tokyo'nun Sessiz Sabahları",
        "location": "Tokyo, Japonya",
        "country": "JP",
        "country_name": "Japonya",
        "lat": 35.6762,
        "lng": 139.6503,
        "date": "Mart 2024",
        "category": "Asya",
        "read_time": "5 dk",
        "excerpt": "Shibuya Crossing'in milyonlarca insanın geçtiği o ikonik kavşağında, gün doğmadan önce tek başıma durdum. Şehir henüz uyanmamıştı.",
        "cover": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=800&q=80",
        "featured": True
    },
    {
        "id": 2,
        "title": "Santorini'de Altın Saat",
        "location": "Santorini, Yunanistan",
        "country": "GR",
        "country_name": "Yunanistan",
        "lat": 36.3932,
        "lng": 25.4615,
        "date": "Temmuz 2024",
        "category": "Avrupa",
        "read_time": "4 dk",
        "excerpt": "Oia'nın beyaz badanalı evleri arasında kaybolurken, Ege Denizi'nin mavisinin bu kadar gerçek olabileceğine inanamıyordum.",
        "cover": "https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?w=800&q=80",
        "featured": False
    },
    {
        "id": 3,
        "title": "Fas'ın Renk Cümbüşü",
        "location": "Marrakech, Fas",
        "country": "MA",
        "country_name": "Fas",
        "lat": 31.6295,
        "lng": -7.9811,
        "date": "Kasım 2023",
        "category": "Afrika",
        "read_time": "6 dk",
        "excerpt": "Medina'nın labirent sokaklarında her köşe başında yeni bir koku, yeni bir renk, yeni bir ses. Burada zaman farklı akar.",
        "cover": "https://images.unsplash.com/photo-1489493887464-892be6d1daae?w=800&q=80",
        "featured": False
    },
    {
        "id": 4,
        "title": "İzlanda'nın Kuzey Işıkları",
        "location": "Reykjavik, İzlanda",
        "country": "IS",
        "country_name": "İzlanda",
        "lat": 64.1466,
        "lng": -21.9426,
        "date": "Ocak 2024",
        "category": "Avrupa",
        "read_time": "7 dk",
        "excerpt": "Gece yarısı çadırın fermuarını açtığımda gökyüzü yeşil ve mor ışıklarla dans ediyordu. Hiçbir fotoğraf o anı tam anlatamaz.",
        "cover": "https://images.unsplash.com/photo-1531366936337-7c912a4589a7?w=800&q=80",
        "featured": False
    },
    {
        "id": 5,
        "title": "Bali'nin Pirinç Terasları",
        "location": "Ubud, Endonezya",
        "country": "ID",
        "country_name": "Endonezya",
        "lat": -8.5069,
        "lng": 115.2625,
        "date": "Şubat 2024",
        "category": "Asya",
        "read_time": "5 dk",
        "excerpt": "Tegallalang'ın yemyeşil pirinç teraslarında sabah sisini izlerken, dünyanın en güzel geometrisinin doğanın kendisi olduğunu anladım.",
        "cover": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=800&q=80",
        "featured": False
    },
    {
        "id": 6,
        "title": "Patagonia'nın Sonsuzluğu",
        "location": "Torres del Paine, Şili",
        "country": "CL",
        "country_name": "Şili",
        "lat": -50.9423,
        "lng": -73.4068,
        "date": "Aralık 2023",
        "category": "Amerika",
        "read_time": "8 dk",
        "excerpt": "Torres del Paine'nin granit kuleleri bulutların arasından çıktığında, dünyanın ucunda olmanın ne demek olduğunu gerçekten hissettim.",
        "cover": "https://images.unsplash.com/photo-1501854140801-50d01698950b?w=800&q=80",
        "featured": False
    }
]

gallery_photos = [
    {"src": "https://images.unsplash.com/photo-1480796927426-f609979314bd?w=600&q=80", "caption": "Tokyo, Japonya", "size": "tall"},
    {"src": "https://images.unsplash.com/photo-1523906834658-6e24ef2386f9?w=600&q=80", "caption": "Venedik, İtalya", "size": "wide"},
    {"src": "https://images.unsplash.com/photo-1518548419970-58e3b4079ab2?w=600&q=80", "caption": "Santorini, Yunanistan", "size": "normal"},
    {"src": "https://images.unsplash.com/photo-1552733407-5d5c46c3bb3b?w=600&q=80", "caption": "Bali, Endonezya", "size": "normal"},
    {"src": "https://images.unsplash.com/photo-1526392060635-9d6019884377?w=600&q=80", "caption": "Marrakech, Fas", "size": "wide"},
    {"src": "https://images.unsplash.com/photo-1548013146-72479768bada?w=600&q=80", "caption": "Hindistan", "size": "normal"},
    {"src": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600&q=80", "caption": "İsviçre Alpleri", "size": "tall"},
    {"src": "https://images.unsplash.com/photo-1493246507139-91e8fad9978e?w=600&q=80", "caption": "Patagonia, Şili", "size": "normal"},
    {"src": "https://images.unsplash.com/photo-1518623489648-a173ef7824f3?w=600&q=80", "caption": "Norveç Fiyordları", "size": "normal"},
]

@app.route("/")
def index():
    featured = next((p for p in posts if p["featured"]), posts[0])
    recent = posts[:6]
    globe_points = [
        {
            "id": p["id"],
            "title": p["title"],
            "location": p["location"],
            "country": p["country_name"],
            "lat": p["lat"],
            "lng": p["lng"],
            "date": p["date"],
        }
        for p in posts
    ]
    return render_template(
        "index.html",
        featured=featured,
        posts=recent,
        gallery=gallery_photos,
        globe_points=globe_points,
    )

@app.route("/gallery")
def gallery():
    return render_template("gallery.html", gallery=gallery_photos)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/post/<int:post_id>")
def post(post_id):
    p = next((p for p in posts if p["id"] == post_id), None)
    if not p:
        return "Post not found", 404
    return render_template("post.html", post=p)

@app.route("/api/posts")
def api_posts():
    category = request.args.get("category", "")
    filtered = posts if not category else [p for p in posts if p["category"] == category]
    return jsonify(filtered)


def is_admin_logged_in():
    return session.get("is_admin", False)


def is_allowed_image(filename):
    if "." not in filename:
        return False
    extension = filename.rsplit(".", 1)[1].lower()
    return extension in ALLOWED_IMAGE_EXTENSIONS


def calculate_read_time(text):
    word_count = len(text.split())
    minutes = max(1, math.ceil(word_count / 200))
    return f"{minutes} dk"


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if is_admin_logged_in():
        return redirect(url_for("admin_panel"))

    error = ""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if username == "admin" and password == "12345":
            session["is_admin"] = True
            return redirect(url_for("admin_panel"))

        error = "Kullanici adi veya sifre hatali."

    return render_template("admin_login.html", error=error)


@app.route("/admin/logout")
def admin_logout():
    session.pop("is_admin", None)
    return redirect(url_for("admin_login"))


@app.route("/admin/panel", methods=["GET", "POST"])
def admin_panel():
    if not is_admin_logged_in():
        return redirect(url_for("admin_login"))

    error = ""
    success = ""

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        location = request.form.get("location", "").strip()
        country_name = request.form.get("country_name", "").strip()
        country = request.form.get("country", "").strip().upper()
        date = request.form.get("date", "").strip()
        category = request.form.get("category", "").strip()
        excerpt = request.form.get("excerpt", "").strip()
        lat_raw = request.form.get("lat", "").strip()
        lng_raw = request.form.get("lng", "").strip()
        cover_file = request.files.get("cover_file")

        if not all([title, location, country_name, country, date, category, excerpt, lat_raw, lng_raw]):
            error = "Lutfen tum alanlari doldur."
        elif not cover_file or not cover_file.filename:
            error = "Lutfen bir kapak gorseli yukle."
        elif not is_allowed_image(cover_file.filename):
            error = "Gecersiz dosya tipi. PNG, JPG, JPEG, WEBP veya GIF kullan."
        else:
            try:
                lat = float(lat_raw)
                lng = float(lng_raw)
            except ValueError:
                error = "Enlem ve boylam sayi olmali."
            else:
                safe_name = secure_filename(cover_file.filename)
                file_ext = safe_name.rsplit(".", 1)[1].lower()
                final_filename = f"{uuid4().hex}.{file_ext}"
                save_path = os.path.join(UPLOAD_FOLDER, final_filename)
                cover_file.save(save_path)
                cover_url = url_for("static", filename=f"uploads/{final_filename}")
                read_time = calculate_read_time(excerpt)
                next_id = max((p["id"] for p in posts), default=0) + 1
                new_post = {
                    "id": next_id,
                    "title": title,
                    "location": location,
                    "country": country[:2] if country else "",
                    "country_name": country_name,
                    "lat": lat,
                    "lng": lng,
                    "date": date,
                    "category": category,
                    "read_time": read_time,
                    "excerpt": excerpt,
                    "cover": cover_url,
                    "featured": False,
                }
                posts.insert(0, new_post)
                success = "Yeni seyahat basariyla eklendi."

    return render_template("admin_panel.html", posts=posts, error=error, success=success)

if __name__ == "__main__":
    app.run(debug=True)
