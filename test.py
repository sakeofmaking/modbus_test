import logging
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.client.sync import ModbusTcpClient

# Setup logging for DEBUG
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)


def read_registers():
    """Read register 40001 - 40030 on client"""
    with ModbusTcpClient('10.192.1.9', port=502) as client:
        response = client.read_holding_registers(0, 30, unit=1)
        print(response.registers)


def write_register():
    """
    Write to single register
    @source: https://stackoverflow.com/questions/30784965/pymodbus-read-write-floats-real
    """
    client = ModbusTcpClient('10.192.1.9', port=502)
    if client.connect():  # connection is OK
        # write float
        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Little)
        builder.add_32bit_float(50.5)
        payload = builder.build()
        result = client.write_registers(3, payload, skip_encode=True)
        # read floats
        result = client.read_holding_registers(3, 4)
        decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big, wordorder=Endian.Little)
        print("read_holding_registers: " + str(decoder.decode_32bit_float()))

        client.close()


if __name__ == '__main__':
    # read_registers()
    write_register()


