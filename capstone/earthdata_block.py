from prefect.blocks.core import Block
from pydantic import Field, SecretStr
import earthaccess
import os


class EarthdataCredentials(Block):
    """
    Block used to manage authentication with NASA Earthdata. 
    NASA Earthdata authentication is handled via the `earthaccess` module. Refer to the
    [earthaccess docs](https://nsidc.github.io/earthaccess/)
    for more info about the possible credential configurations.

    Example:
        Load stored Earthdata credentials:
        ```python
        from prefect_eo import EarthdataCredentials

        ed_credentials_block = EarthdataCredentials.load("BLOCK_NAME")
        ```
    """  # noqa E501

    _logo_url = "https://yt3.googleusercontent.com/ytc/AGIKgqPjIUeAw3_hrkHWZgixdwD5jc-hTWweoCA6bJMhUg=s176-c-k-c0x00ffffff-no-rj"  # noqa
    _block_type_name = "NASA EarthData Credentials"
    _documentation_url = "https://nsidc.github.io/earthaccess/"  # noqa

    earthdata_username: str = Field(
        default=...,
        description="A specific Earthdata username.",
        title="Earthdata username",
    )
    earthdata_password: SecretStr = Field(
        default=...,
        description="The Earthdata password of a specific account.",
        title="Earthdata password",
    )

    def auth(self):
        os.environ["EARTHDATA_USERNAME"] = self.earthdata_username
        os.environ["EARTHDATA_PASSWORD"] = self.earthdata_password.get_secret_value()
        return earthaccess.login()

