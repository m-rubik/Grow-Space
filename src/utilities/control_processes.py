"""!
Contains all functions that work directly with the control elements.
There should be a minimal amount of computation done in these functions.
"""


import datetime
import time
import statistics
import sys

def watering_process(msg, controls, queue):
    """!
    Based on the calculated level it is provided, the watering_process
    will determine how long it needs to water for, then it will
    actuate the pump for the appropriate amount of time.
    """

    current_level = msg[1]
    # TODO: flow will be determined by the moisture level, also needs to be dynamically calculated
    # flow = 3000  # Units of mL, aim for 3L of water per water cycle
    flow = 200 # FOR TESTING
    flow_per_second = 20  # [mL/s]  # TODO: find watering speed of pump
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

    