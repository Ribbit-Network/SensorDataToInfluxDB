import os
import functions_framework
from datetime import datetime, timedelta
from influxdb_client import InfluxDBClient, Point, WritePrecision  # type: ignore
from influxdb_client.client.write_api import SYNCHRONOUS  # type: ignore

BUCKET = "frog_fleet"
ORG = "Ribbit Network"
URL = "https://us-west-2-1.aws.cloud2.influxdata.com/"
TOKEN = os.environ['INFLUXDB_TOKEN']

@functions_framework.http
def send_data_2_influx(request):
    
    request_json = request.get_json(silent=True)
    request_args = request.args

    golioth_msg = request_json

    print(golioth_msg)
    
    ribbit_msg = golioth_msg[data]['ribbitnetwork.datapoint']
    gps_fix = ribbit_msg['gps']['has_fix']

    # Check if the gps fix is valid, only send a datapoint if so
    if gps_fix:
        client = InfluxDBClient(url=URL, token=TOKEN, org=ORG)
        write_api = client.write_api(write_options=SYNCHRONOUS)

        # Get metadata
        device_id = golioth_msg['device_id'] + '_golioth_esp32s3'
        timestamp = datetime.utcnow()
        
        # Parse Data
        scd30_co2_ppm = ribbit_msg['scd30']['co2']
        scd30_humidity = ribbit_msg['scd30']['humidity']
        scd30_temp = ribbit_msg['scd30']['temperature']

        gps_lat = ribbit_msg['gps']['latitude']
        gps_lon = ribbit_msg['gps']['longitude']
        gps_alt = ribbit_msg['gps']['altitude']
        
        dps310_pressure = ribbit_msg['dps310']['pressure']
        dps310_temp = ribbit_msg['dps310']['temperature']

        allocated_mem = ribbit_msg['memory']['allocated']
        free_mem = ribbit_msg['memory']['free']

        battery_voltage = 0.0
        if 'battery' in ribbit_msg:
            battery_voltage = ribbit_msg['battery']['voltage']

        point = (
            Point("ghg_reading")
            .tag("host", device_id)
            .time(timestamp, WritePrecision.NS)
            .field("co2", float(scd30_co2_ppm))
            .field("temperature", scd30_temp)
            .field("humidity", scd30_humidity)
            .field("lat", gps_lat)
            .field("lon", gps_lon)
            .field("alt", gps_alt)
            .field("baro_pressure", dps310_pressure)
            .field("baro_temperature", dps310_temp)
            .field("mem_allocated", allocated_mem)
            .field("mem_free", free_mem)
            .field("bat_volts", battery_voltage)
        )
        write_api.write(BUCKET, ORG, point)

    else:
        print('no gps_fix: not submitting to influxDB')

    #Must send HTTP Return Code
    return 'OK'
