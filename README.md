# pyftd2xx

[pyftd2xx](https://github.com/JulianS-Uni/pyftd2xx) is a simple python wrapper around the official [d2xx FTDI driver](https://www.ftdichip.com/Drivers/D2XX.htm) libraries.
In order for this python module to work you need this driver to be installed and working.

Version 0.9 is the first release and compatible with Python 3.

## Usage

This module is not really ment to be used on its own as it only provides bare functions. A documentation is available from FTDI [here](https://www.ftdichip.com/Support/Documents/ProgramGuides/D2XX_Programmer's_Guide(FT_000071).pdf). Those C functions are wrapped in a pythonic way, so that one does not need to mess around with pointers amd references. The naming of function and parameters should match with the documentation except they would violate Python buildins like `type`. Then they are prefixed with a `_`.

### Example:

So instead of declaring each variable in advance, let the function change them and then check them, one can just call it and get all the results.

C way to do it:

``` C
FT_STATUS ftStatus;
FT_HANDLE ftHandleTemp;
DWORD numDevs;
DWORD Flags;
DWORD ID;
DWORD Type;
DWORD LocId;
char SerialNumber[16];
char Description[64];

ftStatus = FT_GetDeviceInfoDetail(0, &Flags, &Type, &ID, &LocId, SerialNumber,
Description, &ftHandleTemp);
```

Python way to do it:

``` Python
import pyftd2xx as ft

ft.createDeviceInfoList()
result = ft.getDeviceInfoDetail(index=0)
print(result)   #{'index': 0, 'flags': 2, 'type': 8, 'id': 67330068, 'location': 25, 'serial': b'', 'description': b'Single RS232-HS', 'handle': c_void_p(None)}
```

## Credits

This is a heavily changed fork from [Satya Mishra](https://github.com/snmishra/ftd2xx) which probably is more stable than mine. So make sure to give some credit.