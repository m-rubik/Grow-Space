"""!
Contains all data algorithms within Grow-Space enclosure. These algorithms will generate control signals, as they deem necessary.
"""

import datetime
import time


def watering_algorithm(db, controls, simulate_environment):
    if int(db['latest']['soil_moisture_sensor_1']) < db['Moisture_Low']:
        flag = "LOW"
        time_at = datetime.datetime.now()
        if not simulate_environment:
            # Calculate how long to turn on pump

            # TODO: Turn on the pump
            controls['pump'].turn_on()
            # TODO: Wait, need to find pump watering speed
            # TODO: Turn off the pump
            controls['pump'].turn_off()
            pass
    else:
        flag = None
    msg = ['soil_moisture_sensor_1', db['latest']['soil_moisture_sensor_1'], flag]
    return msg  


def lighting_algorithm(db, controls, simulate_environment):
    if simulate_environment:
        return
    controls['RGB LED'].turn_on()
    start_time = datetime.datetime.now()
    while True:
        if controls['RGB LED'].is_off:
            run_time = datetime.datetime.now() - start_time


def environment_algorithm(db, controls, simulate_environment):
    msg = ["environment_sensor", {}]
    temperature = int(db['latest']['environment_sensor']['temperature'])
    if temperature >= db['Temperature_High']:
        flag = "HIGH"
        # controls['UV LED'].turn_off()
        # controls['RGB LED'].turn_off()
        controls['fan'].turn_on()
    elif temperature <= db['Temperature_Low']:
        #  TODO check if lights on produce a lot of heat or not
        # TODO do we want the lights to turn on if temp is low? check above TODO
        flag = "LOW"
        # controls['UV LED'].turn_on()
        # controls['RGB LED'].turn_on()
        controls['fan'].turn_off()
    else:
        flag = None
    msg[1]['temperature'] = {'value': temperature, 'flag': flag}

    humidity = int(db['latest']['environment_sensor']['humidity'])
    if humidity >= db['Humidity_High']:
        flag = "HIGH"
        controls['fan'].turn_on()
        # TODO: research how much fan reduces humidity
    elif humidity <= db['Humidity_Low']:
        flag = "LOW"
        controls['fan'].turn_off()
        # TODO: research how fan deals with humidity
    else:
        flag = None
    msg[1]['humidity'] = {'value': humidity, 'flag': flag}

    gas = round(int(db['latest']['environment_sensor']['gas'])/1000, 2)
    if gas >= db['VOC_High']:
        flag = "HIGH"
        # TODO: What to do about high VOC? Turn on fan?
    elif gas <= db['VOC_Low']:
        flag = "LOW"
        # TODO: AFAIK it's a good thing if VOC is low, so this should be fine as is
    else:
        flag = None
    msg[1]['gas'] = {'value': gas, 'flag': flag}

    return msg
