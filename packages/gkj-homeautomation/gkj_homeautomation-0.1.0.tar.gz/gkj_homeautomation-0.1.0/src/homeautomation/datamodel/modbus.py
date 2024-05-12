from dataclasses import dataclass
import pyModbusTCP.client as mtcpc
import homeautomation.helpfuncs as hf
from enum import Enum
import numpy as np

@dataclass
class CDataType(Enum):
    BOOL = 1
    FLOAT = 2
    STR = 3
    UINT16 = 4
    UINT32 = 5
    UINT64 = 6

@dataclass
class CDeviceType(Enum):
    SEM = 1
    INVERTER = 2

@dataclass
class CRegister: 
    address: np.uint32|None
    name: str|None
    description: str|None
    unit: str|None
    size: np.uint16|None
    data_type: CDataType|None
    is_readonly: bool = True

@dataclass(frozen = False)
class CDevice:
    device_type: CDeviceType|None
    name: str|None
    host: str|None
    port: str|None
    unit_id: np.uint32|None
    r_values: list[CDataType]|None = None
    mb_client: mtcpc.ModbusClient|None = None

    def __post_init__(self):
        self.mb_client = mtcpc.ModbusClient(
            host = self.host,
            port = self.port,
            unit_id = self.unit_id,
            debug=False
        )
        self.r_values = self.set_register()

    def set_register(self):
        if self.device_type == CDeviceType.INVERTER:
            return read_register_values_from_csv(fname = "src/homeautomation/datamodel/plenticore_registers.csv")
        return []
    
    def get_register_value(self, name, return_raw_data: bool = False):
        reg_set = self._get_reg_set_by_name(name = name)
        reg_vals = self.mb_client.read_holding_registers(reg_addr=reg_set.address, reg_nb=reg_set.size)
        if return_raw_data:
            return reg_vals
        return convert_raw(reg=reg_vals, dtype=reg_set.data_type)
    
    def _get_reg_set_by_name(self, name: str) -> CRegister|None:
        for reg in self.r_values:
            if reg.name == name:
                return reg
        return
    
def convert_raw(reg: list[np.uint16], dtype: CDataType) -> str:
    # Convert the input registers to a string-value
    match(dtype.name):
        case "BOOL":
            if reg[0] == 1:
                return "True"
            return "False"
        case "STR":
            return str(hf.uint16array2string(in_array=reg))
        case "FLOAT":
            return f"{hf.uint16array2float(in_array=reg):0.3f}"
        case "UINT16":
            return f"{reg[0]}"
    return "unknown"

    
def read_register_values_from_csv(fname: str) -> list[CRegister]:
    r_table = []
    with open(fname,"rt") as fh:
        while line:=fh.readline():
            l_values=line.split(';')
            if l_values:
                r_val = CRegister(
                    address=np.uint16(l_values[1]),
                    name=l_values[2].replace(' ','_'),
                    description=l_values[2],
                    unit=l_values[3],
                    data_type=get_data_type(l_values[4]),
                    size=np.uint16(l_values[5]),
                    is_readonly=get_is_readonly(l_values[6])
                )
                r_table.append(r_val)
    return r_table

def get_data_type(in_str: str) -> CDataType:
    match(in_str):
        case "Bool":
            return CDataType.BOOL
        case "Float":
            return CDataType.FLOAT
        case "U16":
            return CDataType.UINT16
        case "U32":
            return CDataType.UINT32
        case "U64":
            return CDataType.UINT64
        case "String":
            return CDataType.STR
        case _:
            return CDataType.UINT16
        
def get_is_readonly(in_str: str) -> bool:
    match(in_str):
        case "RO":
            return True
        case "R/W":
            return False
        case _: 
            return True






def main():
    pass

if __name__=="__main__":
    main()