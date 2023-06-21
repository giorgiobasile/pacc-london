import httpx
from prefect import flow, task


@task
def fetch_temperature(lat: float, lon: float):
    base_url = "https://api.open-meteo.com/v1/forecast/"
    weather = httpx.get(
        base_url,
        params=dict(latitude=lat, longitude=lon, hourly="temperature_2m"),
    )
    most_recent_temp = float(weather.json()["hourly"]["temperature_2m"][0])
    return most_recent_temp


@task
def fetch_windspeed(lat: float, lon: float):
    base_url = "https://api.open-meteo.com/v1/forecast/"
    weather = httpx.get(
        base_url,
        params=dict(latitude=lat, longitude=lon, hourly="windspeed_10m"),
    )
    most_recent_temp = float(weather.json()["hourly"]["windspeed_10m"][0])
    return most_recent_temp


@task
def save_weather(weather_var: float, filename: str):
    with open(f"{filename}.csv", "w+") as w:
        w.write(str(weather_var))
    return f"Successfully wrote {filename}"


@flow
def pipeline(lat: float, lon: float):
    temp = fetch_temperature(lat, lon)
    wind = fetch_windspeed(lat, lon)
    temp_result = save_weather(temp, "temperature")
    wind_result = save_weather(wind, "windspeed")
    return {
        "temp": temp_result,
        "wind": wind_result
    }


if __name__ == "__main__":
    pipeline(38.9, -77.0)