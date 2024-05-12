import pyModbusTCP.client as mtcpc
import datetime as dt
import homeautomation.helpfuncs as hf
import numpy as np

def read_active_power_plus_W(c:mtcpc.ModbusClient) -> float|None:
    p=read_uint32(c=c, addr=0)
    if p:
        return float(p)/10.0
    return 0.0

def read_active_power_minus_W(c:mtcpc.ModbusClient) -> float|None:
    p=read_uint32(c=c, addr=2)
    if p:
        return float(p)/10.0
    return 0.0

def read_reactive_power_plus_W(c:mtcpc.ModbusClient) -> float|None:
    p=read_uint32(c=c, addr=4)
    if p:
        return float(p)/10.0
    return 0.0

def read_reactive_power_minus_W(c:mtcpc.ModbusClient) -> float|None:
    p=read_uint32(c=c, addr=6)
    if p:
        return float(p)/10.0
    return 0.0

def read_apparent_power_plus_W(c:mtcpc.ModbusClient) -> float|None:
    p=read_uint32(c=c, addr=8)
    if p:
        return float(p)/10.0
    return 0.0

def read_apparent_power_minus_W(c:mtcpc.ModbusClient) -> float|None:
    p=read_uint32(c=c, addr=10)
    if p:
        return float(p)/10.0
    return 0.0



def read_timestamp(c:mtcpc.ModbusClient) -> dt.datetime|None:
    ts = read_uint64(c=c, addr=8245)
    if ts:
        return dt.datetime.fromtimestamp(float(ts)/1000.0)
    return

def read_manufacturer_id(c:mtcpc.ModbusClient) -> np.uint16|None:
    return read_uint16(c=c, addr=8192)

def read_device_id(c:mtcpc.ModbusClient) -> np.uint16|None:
    return read_uint16(c=c, addr=8193)

def read_product_version(c:mtcpc.ModbusClient) -> np.uint16|None:
    return read_uint16(c=c, addr=8194)

def read_firmware_version(c:mtcpc.ModbusClient) -> np.uint16|None:
    return read_uint16(c=c, addr=8195)

def read_measuring_interval_ms(c:mtcpc.ModbusClient) -> np.uint16|None:
    return read_uint16(c=c, addr=8244)

def read_vendor_name(c:mtcpc.ModbusClient) -> str|None:
    return read_string(c=c, addr=8196, size=16)

def read_product_name(c:mtcpc.ModbusClient) -> str|None:
    return read_string(c=c, addr=8212, size=16)

def read_serial_number(c:mtcpc.ModbusClient) -> str|None:
    return read_string(c=c, addr=8228, size=16)


def read_string(c:mtcpc.ModbusClient, addr:np.uint32, size:np.uint16) -> str|None:
    regs = c.read_holding_registers(addr,size)
    if regs:
        return hf.uint16array2string(regs)
    return

def read_uint16(c: mtcpc.ModbusClient, addr:np.uint32) -> np.uint64|None:
    regs = c.read_holding_registers(addr,1)
    if regs:
        return regs[0]
    return

def read_uint64(c: mtcpc.ModbusClient, addr:np.uint32) -> np.uint64|None:
    regs = c.read_holding_registers(addr,4)
    if regs:
        return hf.uint16array2uint64(in_array=regs)
    return

def read_uint32(c: mtcpc.ModbusClient, addr:np.uint32) -> np.uint32|None:
    regs = c.read_holding_registers(addr,2)
    if regs:
        return hf.uint16array2uint32(in_array=regs)
    return


def main():
    pass

if __name__=="__main__":
    main()