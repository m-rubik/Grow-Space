"""!
Contains the algorithms (functions) that are needed to translate the sensor readings
into actionable quantities.

These algorithms analyse the sensor data found within the master database, and use it to generate control messages.
These message are passed back to the main thread, so that the information can be:
1. Relayed to the GUI for display
2. Used to start up control processes.
"""

import statistics
import numbers


def environment_algorithm(db):
    msg = ["environment_sensor", {}]
    temperature = int(db['latest']['environment_sensor']['temperature'])
    if temperature >= db['Temperature_High']:
        flag = "HIGH"
    elif temperature <= db['Temperature_Low']:
        flag = "LOW"
    else:
        flag = None
    msg[1]['temperature'] = {'value': temperature, 'flag': flag}

    humidity = int(db['latest']['environment_sensor']['humidity'])
    if humidity >= db['Humidity_High']:
        flag = "HIGH" # As we are not controlling humidity and only measuring, no action needed
    elif humidity <= db['Humidity_Low']:
        flag = "LOW" # As we are not controlling humidity and only measuring, no action needed
    else:
        flag = None
    msg[1]['humidity'] = {'value': humidity, 'flag': flag}

    gas = round(int(db['latest']['environment_sensor']['gas'])/1000, 2)
    if gas >= db['VOC_High']:
        flag = "HIGH" # TODO: What to do about high VOC? Turn on fan?
    elif gas <= db['VOC_Low']:
        flag = "LOW" # if VOC is low, then no action needed
    else:
        flag = None
    msg[1]['gas'] = {'value': gas, 'flag': flag}
    return msg


def watering_algorithm(db, water_list):
    """!
    The watering algorithm takes the raw sensor data and determines
    if the soil moisture within the enclosure is within the acceptable range
    (as provided by the configuraiton file).
     Physical Parameters dictate that the sensors should be 12cm apart (center2center), centred in the enclosure.
    """
    try:
        # Get the most recent soil_moisture_levels
        current_level_1 = int(db['latest']['soil_moisture_sensor_1'])

        # Will return the average and std. of numbers only, ignoring "None" entries
        try:
            water_average = statistics.mean([x for x in water_list if isinstance(x, numbers.Number)])
            water_std = statistics.stdev([x for x in water_list if isinstance(x, numbers.Number)])
        except statistics.StatisticsError:
            print("System initialization: No values for water average")
        # for x in [x for x in water_list if isinstance(x, numbers.Number)]:
        try:
            for x in range(len(water_list)):
                if isinstance(water_list[x], numbers.Number):
                    if water_std < abs(water_average-water_list[x]):
                        water_list[x] = "None"
                    else:
                        pass
                else:
                    pass
        except UnboundLocalError:
            print("System initialization: No values for water average")

        try:
            water_average = statistics.mean([x for x in water_list if isinstance(x, numbers.Number)])
        except statistics.StatisticsError:
            print("System initialization: No values for water average")

        # current_level_2 = int(db['latest']['soil_moisture_sensor_2'])

        # Calculate the overall soil moisture level
        #  TODO: Find a better way of calculating the level or maybe don't even do it this way idk
        #  calculated_level = int(statistics.mean([current_level_1, current_level_2]))

        measured_level = int(current_level_1)

        #  First run the calculated level won't work as the water_average won't work. Set to raw value.
        try:
            calculated_level = int(water_average)
        except UnboundLocalError:
            calculated_level = measured_level

        # Determine the flag from the accepted range & the calculated level
        flag = None
        if measured_level < db['Moisture_Low']:
            flag = "LOW"
        elif measured_level > db['Moisture_High']:
            flag = "HIGH"

    except KeyError as err:
        print("Unable to obtain latest sensor data for", str(err) + ". Likely due to the system just starting up.")
        measured_level = '-'
        flag = None

    # Generate & relay the message containing the calculated level for the GUI to display
    msg = ['soil_moisture_sensor', measured_level, flag, calculated_level]
    return msg


def lighting_algorithm(curr, prev):
    """!
    The purpose of the lighting algorithm is to determine what state the RGB and UV LEDs
    should be in at any given time.

    The current algorithm detects when the hour changes.
    It checks for hour changes because the current config files only contain hourly light data.

    @param curr: The current time
    @param prev: The previous time that the algorithm ran
    """
    if not curr.hour == prev.hour:
        return True
    else:
        return False


