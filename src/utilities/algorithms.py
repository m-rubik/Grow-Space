"""!
Contains all data algorithms within Grow-Space enclosure. These algorithms will generate control signals, as they deem necessary.
"""

import datetime
import time


def time_keeper_1h(db, controls, simulate_environment):
    start_time = datetime.datetime.now()


def watering_algorithm(db, controls, simulate_environment):
    msg = ['soil_moisture_sensor_1', db['latest']['soil_moisture_sensor_1'], "None"]
    if int(db['latest']['soil_moisture_sensor_1']) < db['Moisture_Low']:
        # TODO: flow will be determined by the moisture level, also needs to be dynamically calculated
        flow = 3000  # Units of mL, aim for 3L of water per water cycle
        flag = "LOW"
        if not simulate_environment:
            controls['pump'].turn_on()
            flow_per_second = 20  # [mL/s]  # TODO: find watering speed of pump
            time.sleep(flow/flow_per_second)
            last_watering = datetime.datetime.now()
            controls['pump'].turn_off()
    else:
        flag = None
    msg = ['soil_moisture_sensor_1', db['latest']['soil_moisture_sensor_1'], flag]
    return msg


def lighting_algorithm(db, controls, simulate_environment, off):
    if simulate_environment:
        return
    if off:
        controls['RGB LED'].adjust_color(red_content=0, green_content=0, blue_content=0)
        controls['UV LED'].turn_off()
        db['RGB LED Status'] = [0, 0, 0]
        return
    hour = str(datetime.datetime.hour())
    rgb_data = db['RGB_data'][hour]
    red = rgb_data['R']
    green = rgb_data['G']
    blue = rgb_data['B']
    controls['RGB LED'].adjust_color(red_content=red, green_content=green, blue_content=blue)
    db['RGB LED Status'] = [red, green, blue]
    if db['UV_data'][hour]:
        controls['UV LED'].turn_on()
    else:
        controls['UV LED'].turn_off()


def environment_algorithm(db, controls, simulate_environment):
    msg = ["environment_sensor", {}]
    temperature = int(db['latest']['environment_sensor']['temperature'])
    if temperature >= db['Temperature_High']:
        flag = "HIGH"
        # TODO check if the LEDs produce non-negligible heat
        # If so, then:
        lighting_algorithm(db, controls, simulate_environment, True)
        controls['fan'].turn_on()
    elif temperature <= db['Temperature_Low']:
        flag = "LOW"
        lighting_algorithm(db, controls, simulate_environment, False)
        controls['fan'].turn_off()
    else:
        flag = None
    msg[1]['temperature'] = {'value': temperature, 'flag': flag}

    humidity = int(db['latest']['environment_sensor']['humidity'])
    if humidity >= db['Humidity_High']:
        flag = "HIGH"
        # As we are not controlling humidity and only measuring, no action needed
    elif humidity <= db['Humidity_Low']:
        flag = "LOW"
        # # As we are not controlling humidity and only measuring, no action needed
    else:
        flag = None
    msg[1]['humidity'] = {'value': humidity, 'flag': flag}

    gas = round(int(db['latest']['environment_sensor']['gas'])/1000, 2)
    if gas >= db['VOC_High']:
        flag = "HIGH"
        # TODO: What to do about high VOC? Turn on fan?
    elif gas <= db['VOC_Low']:
        flag = "LOW"
        # if VOC is low, then no action needed
    else:
        flag = None
    msg[1]['gas'] = {'value': gas, 'flag': flag}
    return msg
