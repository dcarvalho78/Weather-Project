def get_weather_emoji(data):
    """
    Wählt ein Emoji basierend auf den Wetterbedingungen.
    Erwartet ein Objekt mit:
    - temp_c
    - humidity
    - wind_speed
    - uv_index
    - is_raining
    - is_snowing
    - cloud_cover
    """
    # 🌨️ Schnee
    if data.is_snowing:
        return "🌨️"

    # 🌧️ Regen
    if data.is_raining:
        return "🌧️"

    # 🌫️ Nebel (sehr feucht + wenig Wind)
    if data.humidity >= 95 and data.wind_speed < 1:
        return "🌫️"

    # ☀️ Klar (wenig Wolken, hoher UV)
    if data.cloud_cover is not None and data.cloud_cover < 20:
        return "☀️"

    # ⛅ Wolkig (20–70 % Bewölkung)
    if data.cloud_cover is not None and 20 <= data.cloud_cover <= 70:
        return "⛅"

    # ☁️ Bewölkt (starke Wolken)
    if data.cloud_cover is not None and data.cloud_cover > 70:
        return "☁️"

    # Fallback
    return "❓"
