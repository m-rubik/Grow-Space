"""!
Contains the algorithms (functions) that are needed to translate the sensor readings
into actionable quantities.

These algorithms analyse the sensor data found within the master database, and use it to generate control messages.
These message are passed back to the main thread, so that the information can be:
1. Relayed to the GUI for display
2. Used to start up control processes.
"""


import statistics


def environment_algorithm(db):
    """!
    This algorithm interprets the data obtained from the environment sensors.
    @param db: The master database
    """

    # Check Temperature level
    msg = ["environment_sensor", {}]
    temperature = int(db['latest']['environment_sensor']['temperature'])
    if temperature >= db['Temperature_High']:
        flag = "HIGH"
    elif temperature <= db['Temperature_Low']:
        flag = "LOW"
    else:
        flag = None
    msg[1]['temperature'] = {'value': temperature, 'flag': flag}

    #  Check Humidity level
    humidity = int(db['latest']['environment_sensor']['humidity'])
    if humidity >= db['Humidity_High']:
        flag = "HIGH" # As we are not controlling humidity and only measuring, no action needed
    elif humidity <= db['Humidity_Low']:
        flag = "LOW" # As we are not controlling humidity and only measuring, no action needed
    else:
        flag = None
    msg[1]['humidity'] = {'value': humidity, 'flag': flag}

    # Check VOC/gas level
    gas = round(int(db['latest']['environment_sensor']['gas'])/1000, 2)
    if gas >= db['VOC_High']:
        flag = "HIGH" # NOTE: In future iterations, poor VOC readings may result in the fan being turned on
    elif gas <= db['VOC_Low']:
        flag = "LOW" # If VOC is acceptable, no need to take any action.
    else:
        flag = None
    msg[1]['gas'] = {'value': gas, 'flag': flag}
    return msg


def watering_algorithm(db, water_list):
    """!
    The watering algorithm takes the raw sensor data and determines
    if the soil moisture within the enclosure is within the acceptable range
    (as provided by the configuraiton file).
    @param db: The master database
    @param water_list: List of water values recorded over time
    """
    try:
        # Get the most recent soil_moisture_levels
        measured_level = int(db['latest']['soil_moisture_sensor_1'])

        # Will return the average and std. of numbers only, ignoring Nonetype entries
        try:
            water_average = statistics.mean([x for x in water_list if isinstance(x, float)])
            water_std = statistics.stdev([x for x in water_list if isinstance(x, float)])
        except statistics.StatisticsError:
            print("System initialization: No values for water average")
        try:
            for x in range(0, len(water_list)):
                if water_list[x] is not None:
                    if water_std < abs(water_average-water_list[x]):
                        water_list[x] = None # Reject "bad" entries
                    else:
                        pass # Pass "good" entries
                else:
                    pass # Ignore None entries
        except UnboundLocalError:
            print("System initialization: No values for water average")

        # Compute the new average
        try:
            water_average = statistics.mean([x for x in water_list if isinstance(x, float)])
        except statistics.StatisticsError:
            print("System initialization: No values for water average")

        #  First run the calculated level won't work as the water_average won't work. Set to raw value.
        try:
            calculated_level = int(water_average)
        except UnboundLocalError:
            calculated_level = measured_level

        # Determine the flag from the accepted range & the calculated level
        flag = None
        print("Calculated Level:", calculated_level)
        if calculated_level < db['Moisture_Low']:
            flag = "LOW"
        elif calculated_level > db['Moisture_High']:
            flag = "HIGH"

    except KeyError as err:
        print("Unable to obtain latest sensor data for", str(err) + ". Likely due to the system just starting up.")
        measured_level = '-'
        calculated_level = '-'
        flag = None

    # Generate & relay the message containing the calculated level for the GUI to display
    msg = ['soil_moisture_sensor', measured_level, flag, calculated_level]
    return msg


def time_keeper(curr, prev):
    """!
    The purpose of the time_keeper is to determine what state the RGB & UV LEDs and the Fan
    should be in at any given time.
    The current algorithm detects when the hour changes.

    @param curr: The current time
    @param prev: The previous time that the algorithm ran
    """
    if not curr.hour == prev.hour:
        return True
    else:
        return False


