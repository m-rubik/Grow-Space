"""!
Contains all data algorithms within Grow-Space enclosure. These algorithms will generate control signals, as they deem necessary.
"""

import datetime


def watering_algorithm(db, simulate_environment):
    if int(db['latest']['soil_moisture_sensor_1']) < db['Moisture_Low']:
        flag = "LOW"
        time = datetime.datetime.now()
        if "last_watering" in db:
            if time > db["last_watering"]+datetime.timedelta(minutes=10): # TODO: Obtain the actual pumping interval
                print("Pumping now")
                if simulate_environment:
                    pass
                else:
                    # TODO: Turn on the pump
                    # TODO: Wait
                    # TODO: Turn off the pump
                    pass
        else:
            db["last_watering"] = time
            print("Pumping now")
            if simulate_environment:
                pass
            else:
                # TODO: Turn on the pump
                # TODO: Wait
                # TODO: Turn off the pump
                pass
    else:
        flag = None
    msg = ["soil_moisture_sensor_1", db['latest']['soil_moisture_sensor_1'], flag]
    return msg


def lighting_algorithm(db, simulate_environment):
    pass

def environment_algorithm(db, simulate_environment):
    msg = ["environment_sensor", {}]

    temperature = int(db['latest']['environment_sensor']['temperature'])
    if temperature >= db['Temperature_High']:
        flag = "HIGH"
        # TODO: Turn lights off, fan on
    elif temperature <= db['Temperature_Low']:
        flag = "LOW"
        # TODO: Turn lights on, fan off
    else:
        flag = None
    msg[1]['temperature'] = {'value': temperature, 'flag': flag}

    humidity = int(db['latest']['environment_sensor']['humidity'])
    if humidity >= db['Humidity_High']:
       flag = "HIGH"
        # TODO: ??? What to do about high humidity ?
    elif humidity <= db['Humidity_Low']:
        flag = "LOW"
        # TODO: ??? What to do about low humidity ?
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