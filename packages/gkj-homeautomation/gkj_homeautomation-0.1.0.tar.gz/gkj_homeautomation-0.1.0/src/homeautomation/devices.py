import pyModbusTCP as mtcpc
import homeautomation.datamodel.modbus as dm_mod


WB1 = dm_mod.CDevice(
    device_type=dm_mod.CDeviceType.SEM,
    name="Wallbox aussen",
    host="10.5.11.77",
    port=502,
    unit_id=255
    )

SEM = dm_mod.CDevice(
    device_type=dm_mod.CDeviceType.SEM,
    name="Kostal Smart Energy Meter",
    host="10.5.11.69",
    port=502,
    unit_id=1
    )

WR1 = dm_mod.CDevice(
    device_type=dm_mod.CDeviceType.INVERTER,
    name="scb",
    host="10.5.11.70",
    port=1502,
    unit_id=71
    )

WR2 = dm_mod.CDevice(
    device_type=dm_mod.CDeviceType.INVERTER,
    name="KostalWechselrichterNordRechts",
    host="10.5.11.71",
    port=1502,
    unit_id=71
    )

WR2 = dm_mod.CDevice(
    device_type=dm_mod.CDeviceType.INVERTER,
    name="KostalWechselrichterNordLinks",
    host="10.5.11.72",
    port=1502,
    unit_id=71
    )

def main():
    pass

if __name__=="__main__":
    main()