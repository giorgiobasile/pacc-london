from prefect import flow, get_run_logger
from earthdata_block import EarthdataCredentials
import earthaccess
from prefect.artifacts import create_link_artifact


@flow
def earthdata_search_flow(
    product_short_name='MCD12Q1',
    product_version="061",
    cloud_hosted=True,
    bounding_box=(-10, 20, 10, 50), 
    temporal=("2000-02", "2023-03"),
    count=100
):
    
    logger = get_run_logger()

    earthdata_block = EarthdataCredentials.load("earthdata-credentials")

    earthdata_block.auth()

    results = earthaccess.search_data(
        short_name=product_short_name,
        version=product_version,
        cloud_hosted=cloud_hosted,
        bounding_box=bounding_box,
        temporal=temporal,
        count=count
    )

    logger.info(f"Found {len(results)} results.")
    if len(results) > 0:
        first_result = results[0]
        first_url = first_result.data_links(access="external")[0]
        logger.info(f"First result: {first_result}")
        create_link_artifact(link=first_url, link_text=first_url)

    return results


if __name__ == "__main__":
    earthdata_search_flow()