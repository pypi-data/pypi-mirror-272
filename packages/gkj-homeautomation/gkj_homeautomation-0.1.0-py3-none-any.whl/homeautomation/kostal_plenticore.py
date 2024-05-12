import pyModbusTCP.client as mtcpc
import homeautomation.helpfuncs as hf
import numpy as np

# def read_active_power_W(c:mtcpc.ModbusClient) -> float|None:
#     p=read_uint32(c=c, addr=0)
#     if p:
#         return float(p)/10.0
#     return



# def read_timestamp(c:mtcpc.ModbusClient) -> dt.datetime|None:
#     ts = read_uint64(c=c, addr=8245)
#     if ts:
#         return dt.datetime.fromtimestamp(float(ts)/1000.0)
#     return

# def read_manufacturer_id(c:mtcpc.ModbusClient) -> np.uint16|None:
#     return read_uint16(c=c, addr=8192)

# def read_device_id(c:mtcpc.ModbusClient) -> np.uint16|None:
#     return read_uint16(c=c, addr=8193)

# def read_product_version(c:mtcpc.ModbusClient) -> np.uint16|None:
#     return read_uint16(c=c, addr=8194)

# def read_firmware_version(c:mtcpc.ModbusClient) -> np.uint16|None:
#     return read_uint16(c=c, addr=8195)

# def read_measuring_interval_ms(c:mtcpc.ModbusClient) -> np.uint16|None:
#     return read_uint16(c=c, addr=8244)

# def read_vendor_name(c:mtcpc.ModbusClient) -> str|None:
#     return read_string(c=c, addr=8196, size=16)

def read_product_name(c:mtcpc.ModbusClient) -> str|None:
    return read_string(c=c, addr=6, size=8)

def read_serial_number(c:mtcpc.ModbusClient) -> str|None:
    return read_string(c=c, addr=14, size=8)

def read_home_own_consumption_from_pv(c:mtcpc.ModbusClient) -> float|None:
    return read_float(c=c, addr=116)

def read_total_ac_active_power_W(c:mtcpc.ModbusClient) -> float|None:
    return read_float(c=c, addr=100)

def read_grid_frequency_hz(c:mtcpc.ModbusClient) -> float|None:
    return read_float(c=c, addr=152)

def read_actual_state_of_battery_charge(c: mtcpc.ModbusClient) -> float|None:
    return read_float(c=c, addr=210)

def read_actual_inverter_network_name(c: mtcpc.ModbusClient) -> str|None:
    return read_string(c=c, addr=384, size=32)


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

def read_float(c: mtcpc.ModbusClient, addr:np.uint32) -> np.uint32|None:
    regs = c.read_holding_registers(addr,2)
    if regs:
        return hf.uint16array2float(in_array=regs)
    return


def main():
    pass

if __name__=="__main__":
    main()