import httpx
from prefect import flow, task, get_run_logger
from prefect.tasks import task_input_hash
from prefect.artifacts import create_markdown_artifact
from prefect.deployments import run_deployment


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


@task
def fetch_cat_fact():
    return httpx.get("https://catfact.ninja/fact?max_length=140").json()["fact"]


@task
def formatting(fact: str):
    return fact.title()


@flow
def fetch_cat_fact_flow():
    fact = fetch_cat_fact()
    print(formatting(fact))


@flow
def get_weather_with_cat_facts(lat: float=38.9, lon: float=-77.0, fact_subdeploy: bool=False):
    temp = fetch_temperature(lat, lon)
    wind = fetch_windspeed(lat, lon)
    print_weather_report(temp, wind)

    create_markdown_artifact(key="report", markdown=
        f"""# Values

        Temp: {temp}
        Wind: {wind}
        """
    )

    if not fact_subdeploy:
        fact = fetch_cat_fact()
    else:
        fact = run_deployment("fetch_cat_fact_deployment/fetch_cat_fact_flow")

    return {
        "temp": temp,
        "wind": wind,
        "fact": fact
    }


if __name__ == "__main__":
    get_weather_with_cat_facts(38.9, -77.0)