from flask import Flask, render_template, request, redirect, flash
from helpers import get_weather, calculate_nutrition

app = Flask(__name__)
app.secret_key = "lari_maraton_2026_hydropace_super_rahasia" 

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        sport_type = request.form.get("sport_type")
        duration = request.form.get("duration")
        weight = request.form.get("weight")
        city = request.form.get("city")

        if not sport_type or not duration or not weight or not city:
            flash("Semua kolom harus diisi!")
            return redirect("/")

        # Panggil API Cuaca lewat helpers
        weather = get_weather(city)
        if not weather:
            flash("Kota tidak ditemukan atau masalah jaringan API. Coba kota lain!")
            return redirect("/")

        # Hitung nutrisi
        results = calculate_nutrition(
            sport_type=sport_type,
            duration_min=float(duration),
            weight_kg=float(weight),
            temp_c=weather["temp"],
            humidity=weather["humidity"]
        )

        return render_template("result.html", weather=weather, results=results, sport=sport_type, duration=duration)

    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)