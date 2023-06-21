import httpx
from prefect import flow, task, get_run_logger
from prefect.tasks import task_input_hash
from prefect.artifacts import create_markdown_artifact


@task(retries=2, persist_result=True, cache_key_fn=task_input_hash)
def fetch_temperature(lat: float, lon: float):
    base_url = "https://api.open-meteo.com/v1/forecast/"
    weather = httpx.get(
        base_url,
        params=dict(latitude=lat, longitude=lon, hourly="temperature_2m"),
    )
    most_recent_temp = float(weather.json()["hourly"]["temperature_2m"][0])
    return most_recent_temp


@task(retries=2, persist_result=True)
def fetch_windspeed(lat: float, lon: float):
    base_url = "https://api.open-meteo.com/v1/forecast/"
    weather = httpx.get(
        base_url,
        params=dict(latitude=lat, longitude=lon, hourly="windspeed_10m"),
    )
    most_recent_temp = float(weather.json()["hourly"]["windspeed_10m"][0])
    return most_recent_temp


@task(log_prints=True)
def print_weather_report(temperature: float, windspeed: float):
    logger = get_run_logger()
    logger.info(f"The current temperature is {temperature} and the windspeed is {windspeed}")


@flow
def get_weather_with_artifacts(lat: float=38.9, lon: float=-77.0):
    temp = fetch_temperature(lat, lon)
    wind = fetch_windspeed(lat, lon)
    print_weather_report(temp, wind)

    create_markdown_artifact(key="report", markdown=
        f"""# Values

        Temp: {temp}
        Wind: {wind}
        """
    )

    return {
        "temp": temp,
        "wind": wind
    }


if __name__ == "__main__":
    get_weather_with_artifacts(38.9, -77.0)