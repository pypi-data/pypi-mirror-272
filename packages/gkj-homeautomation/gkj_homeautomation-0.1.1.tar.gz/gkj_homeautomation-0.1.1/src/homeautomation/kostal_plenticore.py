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


def get_register_str() -> str:
    return r"""0x02;2;MODBUS Enable;;Bool;1;R/W;0x03/0x06
0x04;4;MODBUS Unit-ID;;U16;1;R/W;0x03/0x06
0x06;6;Inverter article number;;String;8;RO;0x03
0x0E;14;Inverter serial number;;String;8;RO;0x03
0x1E;30;Number of bidirectional converter;;U16;1;RO;0x03
0x20;32;Number of AC phases;;U16;1;RO;0x03
0x22;34;Number of PV strings;;U16;1;RO;0x03
0x24;36;Hardware-Version;;U16;2;RO;0x03
0x26;38;Software-Version Maincontroller (MC);;String;8;RO;0x03
0x2E;46;Software-Version IO-Controller (IOC);;String;8;RO;0x03
0x36;54;Power-ID;;U16;2;RO;0x03
0x38;56;Inverter state2;;U16;2;RO;0x03
0x64;100;Total DC power;W;Float;2;RO;0x03
0x68;104;State of energy manager;;U32;2;RO;0x03
0x6A;106;Home own consumption from battery;W;Float;2;RO;0x03
0x6C;108;Home own consumption from grid;W;Float;2;RO;0x03
0x6E;110;Total home consumption Battery;Wh;Float;2;RO;0x03
0x70;112;Total home consumption Grid;Wh;Float;2;RO;0x03
0x72;114;Total home consumption PV;Wh;Float;2;RO;0x03
0x74;116;Home own consumption from PV;W;Float;2;RO;0x03
0x76;118;Total home consumption;Wh;Float;2;RO;0x03
0x78;120;Isolation resistance;Ohm;Float;2;RO;0x03
0x7A;122;Power limit from EVU;%;Float;2;RO;0x03
0x7C;124;Total home consumption rate;%;Float;2;RO;0x03
0x90;144;Worktime;s;Float;2;RO;0x03
0x96;150;Actual cos φ;;Float;2;RO;0x03
0x98;152;Grid frequency;Hz;Float;2;RO;0x03
"""
def main():
    pass

if __name__=="__main__":
    main()