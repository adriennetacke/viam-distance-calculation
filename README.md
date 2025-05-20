# `distance-calculation` module

This module implements the [`rdk:component:sensor API`](https://docs.viam.com/dev/reference/apis/components/sensor/). It converts the raw distance readings returned from an HC-SR04 ultrasonic sensor (default unit is meters) into inches and centimeters.

## Requirements
This module assumes you have a Viam machine configured with a board component that is connected to an HC-SR04 ultrasonic sensor. (See the [proximity-alert workshop](https://codelabs.viam.com/guide/visual-proximity-alert/index.html) as an example)

## Model atacke:distance-calculation:ultrasonic-distance-calculation
Using the ultrasonic sensor's readings, a conversion to inches and centimeters is calculated and returned.

In your **CONTROL** tab or **TEST** panel for this module, you'll be able to see the readings returned like so:

!["distance calculation module returns measured distance in inches and centimeters from ultrasonic sensor](/distance-calculation-readings.gif)


### Configuration
The following attribute template can be used to configure this model:

```json
{
  "sensor": <string>,
}
```

#### Attributes

The following attributes are available for this model:

| Name          | Type   | Inclusion | Description                |
|---------------|--------|-----------|----------------------------|
| `sensor` | string  | Required  | The name of the HC-SR04 ultrasonic sensor component in the Viam app.|

#### Example Configuration

```json
{
  "sensor": "sensor-1"
}
```
