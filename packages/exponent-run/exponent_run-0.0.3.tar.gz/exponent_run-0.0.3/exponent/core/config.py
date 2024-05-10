import json
import os
from functools import lru_cache
from importlib.metadata import Distribution

from pydantic_settings import BaseSettings, SettingsConfigDict

# If the package is editable, we want to use:
# base_url = localhost:3000
# base_api_url = localhost:8000


def is_editable_install() -> bool:
    if os.getenv("ENVIRONMENT") == "test":
        # We should explicitly set these variables
        # in test when needed
        return False

    try:
        direct_url = Distribution.from_name("exponent-run").read_text("direct_url.json")
        if not direct_url:
            return False
        pkg_is_editable = (
            json.loads(direct_url).get("dir_info", {}).get("editable", False)
        )
        return bool(pkg_is_editable)
    except Exception as e:
        print(e)
        return False


class Settings(BaseSettings):
    base_url: str = "https://exponent.run"
    base_api_url: str = "https://api.exponent.run"
    api_key: str | None = None

    model_config = SettingsConfigDict(
        env_prefix="EXPONENT_",
        env_file=os.path.expanduser("~/.exponent"),
        case_sensitive=False,
    )


@lru_cache(maxsize=1)
def get_settings(use_prod: bool = False) -> Settings:
    if is_editable_install() and not use_prod:
        return Settings(
            base_url="http://localhost:3000", base_api_url="http://localhost:8000"
        )

    return Settings()
