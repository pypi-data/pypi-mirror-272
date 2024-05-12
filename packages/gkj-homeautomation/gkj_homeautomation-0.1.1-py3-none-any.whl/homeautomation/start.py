import pyModbusTCP.client as mtcpc
import homeautomation.kostal_sem as ksem
import homeautomation.kostal_plenticore as pcore
import homeautomation.devices as dev


def test_connection():
    # TCP auto connect on first modbus request

    # regs = c.read_holding_registers(8228, 16)

    # if regs:
    #     print(regs)
    #     print(uint16array2string(regs))
    # else:
    #     print("read error")

    print(ksem.read_manufacturer_id(c=dev.SEM.mb_client))
    print(ksem.read_device_id(c=dev.SEM.mb_client))
    print(ksem.read_product_version(c=dev.SEM.mb_client))
    print(ksem.read_firmware_version(c=dev.SEM.mb_client))
    print(ksem.read_vendor_name(c=dev.SEM.mb_client))
    print(ksem.read_product_name(c=dev.SEM.mb_client))
    print(ksem.read_serial_number(c=dev.SEM.mb_client))
    print(ksem.read_timestamp(c=dev.SEM.mb_client))
    print(ksem.read_measuring_interval_ms(c=dev.SEM.mb_client))
    print(f"Active power +: {ksem.read_active_power_plus_W(c=dev.SEM.mb_client)}W")
    print(f"Active power -: {ksem.read_active_power_minus_W(c=dev.SEM.mb_client)}W")
    print(f"Reactive power +: {ksem.read_reactive_power_plus_W(c=dev.SEM.mb_client)}W")
    print(f"Reactive power -: {ksem.read_reactive_power_minus_W(c=dev.SEM.mb_client)}W")
    print(f"Apparent power +: {ksem.read_apparent_power_plus_W(c=dev.SEM.mb_client)}W")
    print(f"Apparent power -: {ksem.read_apparent_power_minus_W(c=dev.SEM.mb_client)}W")


def test_connection_plenticore(client: mtcpc.ModbusClient = dev.WR1.mb_client):
    print(pcore.read_product_name(c=client))
    print(pcore.read_serial_number(c=client))
    print(pcore.read_home_own_consumption_from_pv(c=client))
    print(pcore.read_total_ac_active_power_W(c=client))
    print(pcore.read_grid_frequency_hz(c=client))
    print(pcore.read_actual_state_of_battery_charge(c=client))
    print(pcore.read_actual_inverter_network_name(c=client))
    print(dev.WR1.get_register_value(name="MODBUS_Enable", return_raw_data=False))
    print(dev.WR1.get_register_value(name="MODBUS_Enable", return_raw_data=True))
    print(dev.WR1.get_register_value(name="Number_of_AC_phases", return_raw_data=False))
    print(dev.WR1.get_register_value(name="Number_of_AC_phases", return_raw_data=True))
    print(dev.WR1._get_reg_set_by_name(name="Software-Version_Maincontroller_(MC)").data_type)
    print(dev.WR1.get_register_value(name="Software-Version_Maincontroller_(MC)", return_raw_data=False))
    print(dev.WR1.get_register_value(name="Software-Version_Maincontroller_(MC)", return_raw_data=True))
    print(dev.WR1._get_reg_set_by_name(name="Grid_frequency").data_type)
    print(dev.WR1.get_register_value(name="Grid_frequency", return_raw_data=False))
    print(dev.WR1.get_register_value(name="Grid_frequency", return_raw_data=True))
    c = dev.WB1.mb_client
    reg = c.read_holding_registers(reg_addr=1000, reg_nb=2)
    print(reg)
    # print(hf.uint16array2uint32(in_array=reg))

def main():
    pass

if __name__=="__main__":
    main()