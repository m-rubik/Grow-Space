"""!
Contains all functions that work directly with the control elements.
There should be a minimal amount of computation done in these functions.
"""


import datetime
import time
import statistics
import sys


def watering_process(msg, controls, queue, db):
    """!
    Based on the calculated level it is provided, the watering_process
    will determine how long it needs to water for, then it will
    actuate the pump for the appropriate amount of time.
    """

    current_level = msg[1]
    moisture_low = db["Moisture_Low"]
    moisture_high = db["Moisture_High"]
    LH = moisture_low-moisture_high
    max_flow = 2000
    flow = (max_flow/LH)*current_level + max_flow*(1-moisture_low/LH)
    flow_per_second = 0.905  # [mL/s]  # TODO: find watering speed of pump
    pump_time = int(flow/flow_per_second)

    # Operate the pump
    controls['pump'].turn_on()
    time.sleep(pump_time)
    controls['pump'].turn_off()

    # Relay that it is finished
    queue.put("Finished pumping for " + str(pump_time) + "s.")

    # Terminate the process
    sys.exit(0)


def fan_process(msg, controls, queue):
    if msg[1]['temperature']['flag'] == "HIGH":
        controls['fan'].turn_on()
    elif msg[1]['temperature']['flag'] == "LOW":
        controls['fan'].turn_off()
    queue.put("Control process finished")
    sys.exit(0)


def light_process(db, controls, off):
    if off:
        controls['RGB LED'].adjust_color(red_content=0, green_content=0, blue_content=0)
        controls['UV LED'].turn_off()
        db['RGB LED Status'] = [0, 0, 0]
        return
    import datetime
    hour = str(datetime.datetime.now().hour)
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

