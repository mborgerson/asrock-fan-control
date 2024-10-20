#!/usr/bin/env python
"""
Fan speed controller for a ASRock EP2C602-4L/D16

modprobe ipmi_devintf
modprobe ipmi_si
modprobe nct6775

List fan configuration
----------------------

$ ipmitool raw 0x3a 0x02
01 1e 1e 1e 1e 1e
^  ^  ^  ^  ^  ^-- FRNT_FAN3
|  |  |  |  |----- FRNT_FAN2
|  |  |  |-------- FRNT_FAN1
|  |  |----------- ???
|  |-------------- CPU_FAN1_1
|----------------- CPU_FAN1 0=AUTO 1=MANUAL

$ ipmitool raw 0x3a 0x12
01 1e 1e 1e
^  ^  ^  ^
|  |  |  |-------- ???
|  |  |----------- ???
|  |-------------- CPU_FAN2_1
|----------------- CPU_FAN2 0=AUTO 1=MANUAL

Set fan configuration
---------------------

$ ipmitool raw 0x3a 0x01 1 0x1e 0x64 0x1e 0x1e 0x1e
                         ^ ^    ^    ^    ^    ^
                         | |    |    |    |    |--- FRNT_FAN3
                         | |    |    |    |-------- FRNT_FAN2
                         | |    |    |------------- FRNT_FAN1 (LOUDEST)
                         | |    |------------------ REAR_FAN1
                         | |----------------------- CPU_FAN1_1
                         |------------------------- CPU_FAN1_1 0=AUTO 1=MANUAL

$ ipmitool raw 0x3a 0x11 1 0x1e 0x1e 0x1e
                         ^ ^    ^    ^
                         | |    |    |------------- FRNT_FAN4
                         | |    |------------------ REAR_FAN2
                         | |----------------------- CPU_FAN2_1
                         |------------------------- CPU_FAN2_1 0=AUTO 1=MANUAL

Fan duty is given in 0-100 (hex above, but decimal can be used)

$ ipmitool sensor
ATX+5VSB         | 5.040      | Volts      | ok    | 4.230     | 4.710     | na        | na        | 5.550     | 5.610     
+3VSB            | 3.500      | Volts      | ok    | 2.780     | 2.820     | na        | na        | 3.660     | 3.680     
Vcore1           | 0.830      | Volts      | ok    | 0.540     | 0.570     | 0.600     | 1.490     | 1.560     | 1.640     
Vcore2           | 1.070      | Volts      | ok    | 0.540     | 0.570     | 0.600     | 1.490     | 1.560     | 1.640     
VCCMA/B          | 1.520      | Volts      | ok    | 1.090     | 1.120     | na        | na        | 1.720     | 1.750     
VCCMC/D          | 1.520      | Volts      | ok    | 1.090     | 1.120     | na        | na        | 1.720     | 1.750     
+1.10_PCH        | 1.100      | Volts      | ok    | 0.890     | 0.940     | 0.990     | 1.210     | 1.270     | 1.330     
+1.50_PCH        | 1.530      | Volts      | ok    | 1.200     | 1.280     | 1.380     | 1.650     | 1.730     | 1.810     
VCCME/F          | 1.520      | Volts      | ok    | 1.090     | 1.120     | na        | na        | 1.720     | 1.750     
VCCMG/H          | 1.520      | Volts      | ok    | 1.090     | 1.120     | na        | na        | 1.720     | 1.750     
BAT              | 2.480      | Volts      | cr    | 2.380     | 2.500     | na        | na        | 3.580     | 3.680     
+3V              | 3.280      | Volts      | ok    | 2.780     | 2.820     | na        | na        | 3.660     | 3.680     
+5V              | 5.040      | Volts      | ok    | 4.230     | 4.710     | na        | na        | 5.550     | 5.610     
+12V             | 12.300     | Volts      | ok    | 10.100    | 10.300    | na        | na        | 13.300    | 13.400    
CPU_FAN1_1       | 700.000    | RPM        | ok    | na        | na        | 100.000   | na        | na        | na        
CPU_FAN2_1       | 800.000    | RPM        | ok    | na        | na        | 100.000   | na        | na        | na        
REAR_FAN1        | na         | RPM        | na    | na        | na        | 100.000   | na        | na        | na        
REAR_FAN2        | na         | RPM        | na    | na        | na        | 100.000   | na        | na        | na        
FRNT_FAN1        | 0.000      | RPM        | nc    | na        | na        | 1000.000  | na        | na        | na        
FRNT_FAN2        | 0.000      | RPM        | nc    | na        | na        | 100.000   | na        | na        | na        
FRNT_FAN3        | 0.000      | RPM        | nc    | na        | na        | 100.000   | na        | na        | na        
FRNT_FAN4        | na         | RPM        | na    | na        | na        | 100.000   | na        | na        | na        
CPU_FAN1_2       | na         | RPM        | na    | na        | na        | 100.000   | na        | na        | na        
CPU_FAN2_2       | na         | RPM        | na    | na        | na        | 100.000   | na        | na        | na        
MB Temperature   | 33.000     | degrees C  | ok    | na        | na        | na        | na        | na        | 80.000    
TR1 Temperature  | 0.000      | degrees C  | ok    | na        | na        | na        | na        | na        | 75.000    
CPU_BSP1 Temp    | 37.000     | degrees C  | ok    | na        | na        | na        | na        | na        | 91.000    
CPU_AP1 Temp     | 45.000     | degrees C  | ok    | na        | na        | na        | na        | na        | 91.000    
SATAIII_0        | na         | discrete   | na    | na        | na        | na        | na        | na        | na        
SATAIII_1        | na         | discrete   | na    | na        | na        | na        | na        | na        | na        
SCU_PORT_0       | na         | discrete   | na    | na        | na        | na        | na        | na        | na        
SCU_PORT_1       | na         | discrete   | na    | na        | na        | na        | na        | na        | na        
SCU_PORT_2       | na         | discrete   | na    | na        | na        | na        | na        | na        | na        
SCU_PORT_3       | na         | discrete   | na    | na        | na        | na        | na        | na        | na 

"""

import subprocess
import argparse
import re
import time
import logging


log = logging.getLogger(__name__)

def set_fan_speeds(cpu0, cpu1, front, mid, rear):
    cpu_fan1_1 = int(cpu0)
    cpu_fan2_1 = int(cpu1)
    frnt_fan4 = int(front)
    frnt_fan1 = frnt_fan2 = frnt_fan3 = int(mid) # 2x120mm
    rear_fan1 = rear_fan2 = int(rear)            # 2x80mm
    subprocess.check_call(f"ipmitool raw 0x3a 0x01 1 {cpu_fan1_1} {rear_fan1} {frnt_fan1} {frnt_fan2} {frnt_fan3}", shell=True)
    subprocess.check_call(f"ipmitool raw 0x3a 0x11 1 {cpu_fan2_1} {rear_fan2} {frnt_fan4}", shell=True)

def get_temps():
    sensor_data = subprocess.check_output("sensors", shell=True).decode('utf-8')
    temps = re.findall(r"Package id (\d):\s+\+([\d\.]+)", sensor_data)

    cpu_temps = {
        int(temps[0][0]): int(float(temps[0][1])),
        int(temps[1][0]): int(float(temps[1][1])),
    }

    mb_temp = int(float(re.findall(r"SYSTIN:\s+\+([\d\.]+)", sensor_data)[0]))
    return cpu_temps[0], cpu_temps[1], mb_temp

def main():
    while True:
        try:
            cpu0_temp, cpu1_temp, mb_temp = get_temps()

            # Scale CPU fan linearly from 35-70 degrees
            min_temp = 35
            max_temp = 70
            fan_scale = max(0, min((cpu0_temp-min_temp)/(max_temp-min_temp), 1))
            cpu0_fan = int(25 + 75*fan_scale)

            fan_scale = max(0, min((cpu1_temp-min_temp)/(max_temp-min_temp), 1))
            cpu1_fan = int(25 + 75*fan_scale)

            front_fan = min(max(cpu0_fan, cpu1_fan, 30), 100)

            mid_fan = front_fan if (front_fan > 50 or mb_temp > 45) else 15
            rear_fan = min(front_fan, 100)

            stats = (f"""Current Temps:
- CPU0: {cpu0_temp}
- CPU1: {cpu1_temp}
- MB: {mb_temp}

Setting Fans:
- CPU 0: {cpu0_fan}%
- CPU 1: {cpu1_fan}%
- Front: {front_fan}%
- Mid:   {mid_fan}%
- Rear:  {rear_fan}%
""")

        except:
            cpu0_fan = cpu1_fan = front_fan = mid_fan = rear_fan = 100
            stats = "Failed to get fan stats!"

        with open("/tmp/fans", "w", encoding="utf-8") as f:
            f.write(stats)
            print(stats)

        set_fan_speeds(cpu0_fan, cpu1_fan, front_fan, mid_fan, rear_fan)

        time.sleep(2)


if __name__ == '__main__':
    main()
