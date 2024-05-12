import numpy as np
import struct

def uint16array2string(in_array: list[np.uint16]) -> str:
    out_str = ''
    for r in in_array:
        r1 = r>>8 & 0xff
        r2 = r & 0xff
        out_str+=chr(r1)+chr(r2)
    return out_str

def uint16array2uint64(in_array: list[np.uint16,np.uint16,np.uint16,np.uint16]) -> np.uint64:
    res:np.uint64 = in_array[0]<<48
    res += in_array[1]<<32
    res += in_array[2]<<16
    res += in_array[3]
    return res

def uint16array2uint32(in_array: list[np.uint16,np.uint16]) -> np.uint32:
    res:np.uint64 = in_array[0]<<16
    res += in_array[1]
    return res

def uint16array2float(in_array: list[np.uint16,np.uint16]) -> np.uint32:
    res:np.uint64 = in_array[1]<<16
    res += in_array[0]
    rb = struct.pack('<I', res)
    # print(in_array)
    # print(rb)
    return struct.unpack('f',rb)[0]

def main():
    pass

if __name__=="__main__":
    main()