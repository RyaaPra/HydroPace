import requests

# API Key OpenWeather milikmu
API_KEY = "d802ae59fa0f22a40f6c7e808a5a321c"

def get_weather(city_name):
    """Mengambil data suhu (Celsius) dan kelembapan dari OpenWeather API"""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()
        
        weather_data = {
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "city": data["name"]
        }
        return weather_data
    except Exception as e:
        print(f"Error mengambil data cuaca: {e}")
        return None

def calculate_nutrition(sport_type, duration_min, weight_kg, temp_c, humidity):
    """Logika Kustom: Menghitung hidrasi, sodium, dan karbohidrat"""
    if sport_type.lower() == "lari":
        carb_per_hour = 60  
        base_sweat_rate = 0.8  
    else:  # sepeda
        carb_per_hour = 45
        base_sweat_rate = 0.6

    # Faktor pengali beban berdasarkan cuaca (Heat Index Impact)
    weather_factor = 1.0
    if temp_c > 30:
        weather_factor += 0.3
    if humidity > 70:
        weather_factor += 0.2

    total_hours = duration_min / 60
    
    # Kalkulasi dasar ilmiah olahraga
    total_carbs = carb_per_hour * total_hours
    total_fluid = base_sweat_rate * total_hours * weather_factor * (weight_kg / 70)
    total_sodium = total_fluid * 500 if temp_c > 28 else total_fluid * 300

    # Konversi praktis barang bawaan atlet
    gel_needed = round(total_carbs / 30)
    bottles_needed = round(total_fluid / 0.6, 1)

    return {
        "carbs_g": round(total_carbs),
        "fluid_l": round(total_fluid, 2),
        "sodium_mg": round(total_sodium),
        "practical_gel": gel_needed if gel_needed > 0 else 1,
        "practical_bottle": bottles_needed if bottles_needed > 0 else 0.5
    }