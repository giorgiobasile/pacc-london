import httpx
from prefect import flow, task


@task
def fetch_cat_fact():
    return httpx.get("https://catfact.ninja/fact?max_length=140").json()["fact"]


@task
def formatting(fact: str):
    return fact.title()


@flow
def pipeline():
    fact = fetch_cat_fact()
    print(formatting(fact))