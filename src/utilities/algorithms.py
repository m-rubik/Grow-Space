"""!
Contains all data algorithms within Grow-Space enclosure. These algorithms will generate control signals, as they deem necessary.
"""

import datetime


def watering_algorithm(db, simulate_environment):
    if int(db['latest']['soil_moisture_sensor_1']) < db['Moisture_Low']:
        flag = "Moisture below LOW threshold"
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