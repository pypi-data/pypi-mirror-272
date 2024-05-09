import itksn
from itksn.core import SerialNumberStruct

parsed = SerialNumberStruct.parse(b"20UPIyynnnnnnn")
#parsed = SerialNumberStruct.parse(b"20Uxxyynnnnnnn")
print(parsed)
breakpoint()
