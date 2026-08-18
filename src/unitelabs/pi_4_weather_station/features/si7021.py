import asyncio
import adafruit_si7021
import board
import typing

from unitelabs.cdk import sila

class TemperatureHumiditySensor(sila.Feature):
	"""Read temperature and humidity values"""

	def __init__(self):
		super().__init__(
			originator='ares',
			category='weather',
			version='0.1',
			maturity_level='Draft',
		)

		self.sensor = adafruit_si7021.SI7021( board.I2C() )

	@sila.UnobservableProperty()
	async def get_temperature(self) -> typing.Annotated[float, sila.constraints.Unit(label='°C', offset=273.15,
		components=[sila.constraints.UnitComponent(unit=sila.constraints.SIUnit.KELVIN,)])]:

		"""Get the current temperature reading in °C"""

		return self.sensor.temperature

	@sila.ObservableProperty(name='Temperature Stream')
	async def subscribe_temperature(self, interval: float = 1,) -> sila.Stream[float]:
		"""Stream the current temperature reading in °C"""

		while True:
			yield self.sensor.temperature
			await asyncio.sleep(interval)


	@sila.UnobservableProperty()
	async def get_relative_humidity(self) -> typing.Annotated[float, sila.constraints.Unit(label='%',
		components=[sila.constraints.UnitComponent(unit=sila.constraints.SIUnit.DIMENSIONLESS,)])]:
		"""Get the current relative humidity reading in %"""

		return self.sensor.relative_humidity

	@sila.ObservableProperty(name='Relative Humidity Stream')
	async def subscribe_relative_humidity(self, interval: float = 1, ) -> sila.Stream[float]:
		"""Subscribe to the current relative humidity reading in %"""

		while True:
			yield self.sensor.relative_humidity
			await asyncio.sleep(interval)
