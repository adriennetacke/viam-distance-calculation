from typing import (Any, ClassVar, Dict, List, Mapping, Optional,
                    Sequence, cast)

from typing_extensions import Self
from viam.components.sensor import *
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import Geometry, ResourceName
from viam.resource.base import ResourceBase
from viam.resource.easy_resource import EasyResource
from viam.resource.types import Model, ModelFamily
from viam.utils import SensorReading, ValueTypes, struct_to_dict
from viam.components.sensor import Sensor
from viam.logging import getLogger

LOGGER = getLogger(__name__)

# Conversion constants
METER_TO_INCH_MULTIPLE = 39.37
METER_TO_CENTIMETER_MULTIPLE = 100

class UltrasonicDistanceCalculation(Sensor, EasyResource):
    # To enable debug-level logging, either run viam-server with the --debug option,
    # or configure your resource/machine to display debug logs.
    MODEL: ClassVar[Model] = Model(
        ModelFamily("atacke", "distance-calculation"), "ultrasonic-distance-calculation"
    )

    @classmethod
    def new(
        cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ) -> Self:
        """This method creates a new instance of this Sensor component.
        The default implementation sets the name from the `config` parameter and then calls `reconfigure`.

        Args:
            config (ComponentConfig): The configuration for this resource
            dependencies (Mapping[ResourceName, ResourceBase]): The dependencies (both implicit and explicit)

        Returns:
            Self: The resource
        """
        return super().new(config, dependencies)

    @classmethod
    def validate_config(cls, config: ComponentConfig) -> Sequence[str]:
        """This method allows you to validate the configuration object received from the machine,
        as well as to return any implicit dependencies based on that `config`.

        Args:
            config (ComponentConfig): The configuration for this resource

        Returns:
            Sequence[str]: A list of implicit dependencies
        """
        attrs = struct_to_dict(config.attributes)
        required_dependencies = ["sensor"]
        implicit_dependencies = []
        
        for component in required_dependencies:
            if component not in attrs or not isinstance(attrs[component], str):
                raise ValueError(f"{component} is required in the configuration and must be a string")
            else:
                implicit_dependencies.append(attrs[component])

        return implicit_dependencies

    def reconfigure(
        self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ):
        """This method allows you to dynamically update your service when it receives a new `config` object.

        Args:
            config (ComponentConfig): The new configuration
            dependencies (Mapping[ResourceName, ResourceBase]): Any dependencies (both implicit and explicit)
        """
        attrs = struct_to_dict(config.attributes)
        
        LOGGER.debug("Reconfiguring distance calculation module...")
        
        # set ultrasonic sensor
        sensor_resource = dependencies.get(
            Sensor.get_resource_name(str(attrs.get("sensor")))
        )
        self.sensor = cast(Sensor, sensor_resource)

        if not isinstance(self.sensor, Sensor):
            raise Exception(f"Sensor '{sensor_resource}' not found during reconfiguration.")
        
        LOGGER.debug(f"SENSOR IS SET, {self.sensor}")

        return super().reconfigure(config, dependencies)

    async def get_readings(
        self,
        *,
        extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, SensorReading]:
        try:
            reading = (await self.sensor.get_readings())["distance"]

            # Readings are returned as meters
            # Calculate conversions
            dist_inches = reading * METER_TO_INCH_MULTIPLE
            dist_centimeters = reading * METER_TO_CENTIMETER_MULTIPLE

            data: dict[str, Any] = {
                "distanceInCentimeters": dist_centimeters,
                "distanceInInches": dist_inches
            }
            return data
        
        except Exception as err:
            LOGGER.error(f"Error in control logic: {err}")

    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, ValueTypes]:
        self.logger.error("`do_command` is not implemented")
        raise NotImplementedError()

    async def get_geometries(
        self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None
    ) -> List[Geometry]:
        self.logger.error("`get_geometries` is not implemented")
        raise NotImplementedError()

