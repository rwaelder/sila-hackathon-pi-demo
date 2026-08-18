import dataclasses
import collections.abc
from importlib.metadata import version

from unitelabs.cdk import Connector, ConnectorBaseConfig, SiLAServerConfig

from .features.si7021 import TemperatureHumiditySensor

__version__ = version("unitelabs-pi-4-weather-station")


@dataclasses.dataclass
class Pi4WeatherStationConfig(ConnectorBaseConfig):
    """Configuration for the Pi 4 Weather Station."""

    sila_server: SiLAServerConfig = dataclasses.field(
        default_factory=lambda: SiLAServerConfig(
            name="Pi 4 Weather Station",
            type="Example",
            description=(
                """
                A connector for the Pi 4 Weather Station built with the UniteLabs CDK.
                """
            ),
            version=str(__version__),
            vendor_url="https://unitelabs.io/",
        )
    )


async def create_app(config: Pi4WeatherStationConfig) -> collections.abc.AsyncGenerator[Connector, None]:
    """Create the connector application."""

    app = Connector(config)
    app.register(TemperatureHumiditySensor())
    yield app
