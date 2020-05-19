import json
import asyncio
from azure.iot.device.aio import IoTHubModuleClient
import sys
from device_provisioning_service import Device
from sensor import Sensor
import os

import ptvsd
ptvsd.enable_attach(address=('0.0.0.0', 3000))
# ptvsd.wait_for_attach()


async def main():
    # scopeID = None
    # deviceId = None
    # key = None

    # scopeID = os.getenv('SCOPE_ID')
    # deviceId = os.getenv('DEVICE_ID')
    # key = os.getenv('DEVICE_KEY')

    # if scopeID is None or deviceId is None or key is None:
    #     sys.exit(1)

    # dps = Device(scopeID, deviceId, key)

    # conn_str = await dps.connection_string

    # device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    module_client = IoTHubModuleClient.create_from_edge_environment()
    await module_client.connect()

    sensor = Sensor()

    async def message_listener(module_client):
        while True:
            message = await module_client.receive_message_on_input("input1")   # blocking call
            print("the data in the message received was ")
            print(message.data)
            print("custom properties are")
            print(message.custom_properties)

    asyncio.create_task(message_listener(module_client))

    while True:
        try:
            telemetry = await sensor.readSensor()
            if telemetry is not None:

                print(telemetry)
                data = json.dumps(telemetry)

                await module_client.send_message_to_output(data, "output1")

                await asyncio.sleep(10)

        except:
            print("Unexpected error:", sys.exc_info()[0])

    await module_client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())

    # If using Python 3.6 or below, use the following code instead of asyncio.run(main()):
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.close()
