import sys as _sys
import ctypes as _ctypes


# Select library
if _sys.platform == 'win32':
    try:
        _library = _ctypes.CDLL('ftd2xx64.dll')
    except FileNotFoundError:
        print('Unable to find D2XX64 DLL. Fallback to D2XX32.')
        try:
            _library = _ctypes.CDLL('ftd2xx.dll')
        except FileNotFoundError:
            raise FileNotFoundError('Unable to find D2XX DLL. Please make sure ftd2xx.dll or ftd2xx64.dll is in the path.')
elif _sys.platform.startswith('linux'):
    """Not implemented"""
    raise NotImplementedError()
elif _sys.platform == 'darwin':
    """Not implemented"""
    raise NotImplementedError()


# Typedefs
STRING = _ctypes.c_char_p
DWORD = _ctypes.c_uint32
ULONG = _ctypes.c_uint32
USHORT = _ctypes.c_uint16
SHORT = _ctypes.c_uint16
UCHAR = _ctypes.c_ubyte
WORD = _ctypes.c_uint16
WCHAR = _ctypes.c_uint16
BYTE = _ctypes.c_ubyte
LPBYTE = _ctypes.POINTER(BYTE)
BOOL = _ctypes.c_uint32
BOOLEAN = _ctypes.c_ubyte
CHAR = _ctypes.c_ubyte
LPBOOL = _ctypes.POINTER(BOOL)
PUCHAR = _ctypes.POINTER(UCHAR)
LPCSTR = STRING
PCHAR = STRING
PVOID = _ctypes.c_void_p
HANDLE = PVOID
LONG = _ctypes.c_uint32
INT = _ctypes.c_int32
UINT = _ctypes.c_uint32
LPSTR = STRING
LPTSTR = STRING
LPCTSTR = STRING
LPDWORD = _ctypes.POINTER(DWORD)
LPWORD = _ctypes.POINTER(WORD)
PULONG = _ctypes.POINTER(ULONG)
LPLONG = _ctypes.POINTER(LONG)
LPVOID = PVOID
PUSHORT = _ctypes.POINTER(USHORT)
ULONGLONG = _ctypes.c_ulonglong

FT_HANDLE = PVOID
FT_STATUS = ULONG
PFT_EVENT_HANDLER = _ctypes.POINTER(_ctypes.CFUNCTYPE(None, ULONG, ULONG))
FT_DEVICE = ULONG


# Structures
class struct_ft_program_data(_ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('Signature1', DWORD),
    ('Signature2', DWORD),
    ('Version', DWORD),
    ('VendorId', WORD),
    ('ProductId', WORD),
    ('Manufacturer', STRING),
    ('ManufacturerId', STRING),
    ('Description', STRING),
    ('SerialNumber', STRING),
    ('MaxPower', WORD),
    ('PnP', WORD),
    ('SelfPowered', WORD),
    ('RemoteWakeup', WORD),
    ('Rev4', UCHAR),
    ('IsoIn', UCHAR),
    ('IsoOut', UCHAR),
    ('PullDownEnable', UCHAR),
    ('SerNumEnable', UCHAR),
    ('USBVersionEnable', UCHAR),
    ('USBVersion', WORD),
    ('Rev5', UCHAR),
    ('IsoInA', UCHAR),
    ('IsoInB', UCHAR),
    ('IsoOutA', UCHAR),
    ('IsoOutB', UCHAR),
    ('PullDownEnable5', UCHAR),
    ('SerNumEnable5', UCHAR),
    ('USBVersionEnable5', UCHAR),
    ('USBVersion5', WORD),
    ('AIsHighCurrent', UCHAR),
    ('BIsHighCurrent', UCHAR),
    ('IFAIsFifo', UCHAR),
    ('IFAIsFifoTar', UCHAR),
    ('IFAIsFastSer', UCHAR),
    ('AIsVCP', UCHAR),
    ('IFBIsFifo', UCHAR),
    ('IFBIsFifoTar', UCHAR),
    ('IFBIsFastSer', UCHAR),
    ('BIsVCP', UCHAR),
    ('UseExtOsc', UCHAR),
    ('HighDriveIOs', UCHAR),
    ('EndpointSize', UCHAR),
    ('PullDownEnableR', UCHAR),
    ('SerNumEnableR', UCHAR),
    ('InvertTXD', UCHAR),
    ('InvertRXD', UCHAR),
    ('InvertRTS', UCHAR),
    ('InvertCTS', UCHAR),
    ('InvertDTR', UCHAR),
    ('InvertDSR', UCHAR),
    ('InvertDCD', UCHAR),
    ('InvertRI', UCHAR),
    ('Cbus0', UCHAR),
    ('Cbus1', UCHAR),
    ('Cbus2', UCHAR),
    ('Cbus3', UCHAR),
    ('Cbus4', UCHAR),
    ('RIsD2XX', UCHAR),
    ('PullDownEnable7', UCHAR),
    ('SerNumEnable7', UCHAR),
    ('ALSlowSlew', UCHAR),
    ('ALSchmittInput', UCHAR),
    ('ALDriveCurrent', UCHAR),
    ('AHSlowSlew', UCHAR),
    ('AHSchmittInput', UCHAR),
    ('AHDriveCurrent', UCHAR),
    ('BLSlowSlew', UCHAR),
    ('BLSchmittInput', UCHAR),
    ('BLDriveCurrent', UCHAR),
    ('BHSlowSlew', UCHAR),
    ('BHSchmittInput', UCHAR),
    ('BHDriveCurrent', UCHAR),
    ('IFAIsFifo7', UCHAR),
    ('IFAIsFifoTar7', UCHAR),
    ('IFAIsFastSer7', UCHAR),
    ('AIsVCP7', UCHAR),
    ('IFBIsFifo7', UCHAR),
    ('IFBIsFifoTar7', UCHAR),
    ('IFBIsFastSer7', UCHAR),
    ('BIsVCP7', UCHAR),
    ('PowerSaveEnable', UCHAR),
    ('PullDownEnable8', UCHAR),
    ('SerNumEnable8', UCHAR),
    ('ASlowSlew', UCHAR),
    ('ASchmittInput', UCHAR),
    ('ADriveCurrent', UCHAR),
    ('BSlowSlew', UCHAR),
    ('BSchmittInput', UCHAR),
    ('BDriveCurrent', UCHAR),
    ('CSlowSlew', UCHAR),
    ('CSchmittInput', UCHAR),
    ('CDriveCurrent', UCHAR),
    ('DSlowSlew', UCHAR),
    ('DSchmittInput', UCHAR),
    ('DDriveCurrent', UCHAR),
    ('ARIIsTXDEN', UCHAR),
    ('BRIIsTXDEN', UCHAR),
    ('CRIIsTXDEN', UCHAR),
    ('DRIIsTXDEN', UCHAR),
    ('AIsVCP8', UCHAR),
    ('BIsVCP8', UCHAR),
    ('CIsVCP8', UCHAR),
    ('DIsVCP8', UCHAR),
    ('PullDownEnableH', UCHAR),
    ('SerNumEnableH', UCHAR),
    ('ACSlowSlewH', UCHAR),
    ('ACSchmittInputH', UCHAR),
    ('ACDriveCurrentH', UCHAR),
    ('ADSlowSlewH', UCHAR),
    ('ADSchmittInputH', UCHAR),
    ('ADDriveCurrentH', UCHAR),
    ('Cbus0H', UCHAR),
    ('Cbus1H', UCHAR),
    ('Cbus2H', UCHAR),
    ('Cbus3H', UCHAR),
    ('Cbus4H', UCHAR),
    ('Cbus5H', UCHAR),
    ('Cbus6H', UCHAR),
    ('Cbus7H', UCHAR),
    ('Cbus8H', UCHAR),
    ('Cbus9H', UCHAR),
    ('IsFifoH', UCHAR),
    ('IsFifoTarH', UCHAR),
    ('IsFastSerH', UCHAR),
    ('IsFT1248H', UCHAR),
    ('FT1248CpolH', UCHAR),
    ('FT1248LsbH', UCHAR),
    ('FT1248FlowControlH', UCHAR),
    ('IsVCPH', UCHAR),
    ('PowerSaveEnableH', UCHAR),
     ]
PFT_PROGRAM_DATA = _ctypes.POINTER(struct_ft_program_data)
FT_PROGRAM_DATA = struct_ft_program_data


class struct_ft_eeprom_header(_ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('deviceType', DWORD),
    ('VendorId', WORD),
    ('ProductId', WORD),
    ('SerNumEnable', UCHAR),
    ('MaxPower', WORD),
    ('SelfPowered', UCHAR),
    ('RemoteWakeup', UCHAR),
    ('PullDownEnable', UCHAR),
     ]
FT_EEPROM_HEADER = struct_ft_eeprom_header
PFT_EEPROM_HEADER = _ctypes.POINTER(struct_ft_eeprom_header)


class struct_ft_eeprom_232b(_ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('common', FT_EEPROM_HEADER),
     ]
FT_EEPROM_232B = struct_ft_eeprom_232b
PFT_EEPROM_232B = _ctypes.POINTER(struct_ft_eeprom_232b)


class struct_ft_eeprom_2232(_ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('common', FT_EEPROM_HEADER),
    ('AIsHighCurrent', UCHAR),
    ('BIsHighCurrent', UCHAR),
    ('AIsFifo', UCHAR),
    ('AIsFifoTar', UCHAR),
    ('AIsFastSer', UCHAR),
    ('BIsFifo', UCHAR),
    ('BIsFifoTar', UCHAR),
    ('BIsFastSer', UCHAR),
    ('ADriverType', UCHAR),
    ('BDriverType', UCHAR),
     ]
FT_EEPROM_2232 = struct_ft_eeprom_2232
PFT_EEPROM_2232 = _ctypes.POINTER(struct_ft_eeprom_2232)


class struct_ft_eeprom_232r(_ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('common', FT_EEPROM_HEADER),
    ('IsHighCurrent', UCHAR),
    ('UseExtOsc', UCHAR),
    ('InvertTXD', UCHAR),
    ('InvertRXD', UCHAR),
    ('InvertRTS', UCHAR),
    ('InvertCTS', UCHAR),
    ('InvertDTR', UCHAR),
    ('InvertDSR', UCHAR),
    ('InvertDCD', UCHAR),
    ('InvertRI', UCHAR),
    ('Cbus0', UCHAR),
    ('Cbus1', UCHAR),
    ('Cbus2', UCHAR),
    ('Cbus3', UCHAR),
    ('Cbus4', UCHAR),
    ('DriverType', UCHAR),
     ]
FT_EEPROM_232R = struct_ft_eeprom_232r
PFT_EEPROM_232R = _ctypes.POINTER(struct_ft_eeprom_232r)


class struct_ft_eeprom_2232h(_ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('common', FT_EEPROM_HEADER),
    ('ALSlowSlew', UCHAR),
    ('ALSchmittInput', UCHAR),
    ('ALDriveCurrent', UCHAR),
    ('AHSlowSlew', UCHAR),
    ('AHSchmittInput', UCHAR),
    ('AHDriveCurrent', UCHAR),
    ('BLSlowSlew', UCHAR),
    ('BLSchmittInput', UCHAR),
    ('BLDriveCurrent', UCHAR),
    ('BHSlowSlew', UCHAR),
    ('BHSchmittInput', UCHAR),
    ('BHDriveCurrent', UCHAR),
    ('AIsFifo', UCHAR),
    ('AIsFifoTar', UCHAR),
    ('AIsFastSer', UCHAR),
    ('BIsFifo', UCHAR),
    ('BIsFifoTar', UCHAR),
    ('BIsFastSer', UCHAR),
    ('PowerSaveEnable', UCHAR),
    ('ADriverType', UCHAR),
    ('BDriverType', UCHAR),
     ]
PFT_EEPROM_2232H = _ctypes.POINTER(struct_ft_eeprom_2232h)
FT_EEPROM_2232H = struct_ft_eeprom_2232h


class struct_ft_eeprom_4232h(_ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('common', FT_EEPROM_HEADER),
    ('ASlowSlew', UCHAR),
    ('ASchmittInput', UCHAR),
    ('ADriveCurrent', UCHAR),
    ('BSlowSlew', UCHAR),
    ('BSchmittInput', UCHAR),
    ('BDriveCurrent', UCHAR),
    ('CSlowSlew', UCHAR),
    ('CSchmittInput', UCHAR),
    ('CDriveCurrent', UCHAR),
    ('DSlowSlew', UCHAR),
    ('DSchmittInput', UCHAR),
    ('DDriveCurrent', UCHAR),
    ('ARIIsTXDEN', UCHAR),
    ('BRIIsTXDEN', UCHAR),
    ('CRIIsTXDEN', UCHAR),
    ('DRIIsTXDEN', UCHAR),
    ('ADriverType', UCHAR),
    ('BDriverType', UCHAR),
    ('CDriverType', UCHAR),
    ('DDriverType', UCHAR),
     ]
PFT_EEPROM_4232H = _ctypes.POINTER(struct_ft_eeprom_4232h)
FT_EEPROM_4232H = struct_ft_eeprom_4232h


class struct_ft_eeprom_232h(_ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('common', FT_EEPROM_HEADER),
    ('ACSlowSlew', UCHAR),
    ('ACSchmittInput', UCHAR),
    ('ACDriveCurrent', UCHAR),
    ('ADSlowSlew', UCHAR),
    ('ADSchmittInput', UCHAR),
    ('ADDriveCurrent', UCHAR),
    ('Cbus0', UCHAR),
    ('Cbus1', UCHAR),
    ('Cbus2', UCHAR),
    ('Cbus3', UCHAR),
    ('Cbus4', UCHAR),
    ('Cbus5', UCHAR),
    ('Cbus6', UCHAR),
    ('Cbus7', UCHAR),
    ('Cbus8', UCHAR),
    ('Cbus9', UCHAR),
    ('FT1248Cpol', UCHAR),
    ('FT1248Lsb', UCHAR),
    ('FT1248FlowControl', UCHAR),
    ('IsFifo', UCHAR),
    ('IsFifoTar', UCHAR),
    ('IsFastSer', UCHAR),
    ('IsFT1248', UCHAR),
    ('PowerSaveEnable', UCHAR),
    ('DriverType', UCHAR),
     ]
PFT_EEPROM_232H = _ctypes.POINTER(struct_ft_eeprom_232h)
FT_EEPROM_232H = struct_ft_eeprom_232h


class struct_ft_eeprom_x_series(_ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('common', FT_EEPROM_HEADER),
    ('ACSlowSlew', UCHAR),
    ('ACSchmittInput', UCHAR),
    ('ACDriveCurrent', UCHAR),
    ('ADSlowSlew', UCHAR),
    ('ADSchmittInput', UCHAR),
    ('ADDriveCurrent', UCHAR),
    ('Cbus0', UCHAR),
    ('Cbus1', UCHAR),
    ('Cbus2', UCHAR),
    ('Cbus3', UCHAR),
    ('Cbus4', UCHAR),
    ('Cbus5', UCHAR),
    ('Cbus6', UCHAR),
    ('InvertTXD', UCHAR),
    ('InvertRXD', UCHAR),
    ('InvertRTS', UCHAR),
    ('InvertCTS', UCHAR),
    ('InvertDTR', UCHAR),
    ('InvertDSR', UCHAR),
    ('InvertDCD', UCHAR),
    ('InvertRI', UCHAR),
    ('BCDEnable', UCHAR),
    ('BCDForceCbusPWREN', UCHAR),
    ('BCDDisableSleep', UCHAR),
    ('I2CSlaveAddress', WORD),
    ('I2CDeviceId', DWORD),
    ('I2CDisableSchmitt', UCHAR),
    ('FT1248Cpol', UCHAR),
    ('FT1248Lsb', UCHAR),
    ('FT1248FlowControl', UCHAR),
    ('RS485EchoSuppress', UCHAR),
    ('PowerSaveEnable', UCHAR),
    ('DriverType', UCHAR),
     ]
PFT_EEPROM_X_SERIES = _ctypes.POINTER(struct_ft_eeprom_x_series)
FT_EEPROM_X_SERIES = struct_ft_eeprom_x_series


class struct__FTCOMSTAT(_ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('fCtsHold', DWORD, 1),
    ('fDsrHold', DWORD, 1),
    ('fRlsdHold', DWORD, 1),
    ('fXoffHold', DWORD, 1),
    ('fXoffSent', DWORD, 1),
    ('fEof', DWORD, 1),
    ('fTxim', DWORD, 1),
    ('fReserved', DWORD, 25),
    ('cbInQue', DWORD),
    ('cbOutQue', DWORD),
     ]
FTCOMSTAT = struct__FTCOMSTAT
LPFTCOMSTAT = _ctypes.POINTER(struct__FTCOMSTAT)


class struct__FTDCB(_ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('DCBlength', DWORD),
    ('BaudRate', DWORD),
    ('fBinary', DWORD, 1),
    ('fParity', DWORD, 1),
    ('fOutxCtsFlow', DWORD, 1),
    ('fOutxDsrFlow', DWORD, 1),
    ('fDtrControl', DWORD, 2),
    ('fDsrSensitivity', DWORD, 1),
    ('fTXContinueOnXoff', DWORD, 1),
    ('fOutX', DWORD, 1),
    ('fInX', DWORD, 1),
    ('fErrorChar', DWORD, 1),
    ('fNull', DWORD, 1),
    ('fRtsControl', DWORD, 2),
    ('fAbortOnError', DWORD, 1),
    ('fDummy2', DWORD, 17),
    ('wReserved', WORD),
    ('XonLim', WORD),
    ('XoffLim', WORD),
    ('ByteSize', UCHAR),
    ('Parity', UCHAR),
    ('StopBits', UCHAR),
    ('XonChar', _ctypes.c_char),
    ('XoffChar', _ctypes.c_char),
    ('ErrorChar', _ctypes.c_char),
    ('EofChar', _ctypes.c_char),
    ('EvtChar', _ctypes.c_char),
    ('wReserved1', WORD),
     ]
FTDCB = struct__FTDCB
LPFTDCB = _ctypes.POINTER(struct__FTDCB)


class struct__FTTIMEOUTS(_ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('ReadIntervalTimeout', DWORD),
    ('ReadTotalTimeoutMultiplier', DWORD),
    ('ReadTotalTimeoutConstant', DWORD),
    ('WriteTotalTimeoutMultiplier', DWORD),
    ('WriteTotalTimeoutConstant', DWORD),
     ]
LPFTTIMEOUTS = _ctypes.POINTER(struct__FTTIMEOUTS)
FTTIMEOUTS = struct__FTTIMEOUTS


class struct__ft_device_list_info_node(_ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('Flags', DWORD),
    ('Type', DWORD),
    ('ID', DWORD),
    ('LocId', DWORD),
    ('SerialNumber', _ctypes.c_char * 16),
    ('Description', _ctypes.c_char * 64),
    ('ftHandle', FT_HANDLE),
     ]
FT_DEVICE_LIST_INFO_NODE = struct__ft_device_list_info_node


class struct__SECURITY_ATTRIBUTES(_ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('nLength', DWORD),
    ('lpSecurityDescriptor', PVOID),
    ('bInheritHandle', BOOL),
     ]
LPSECURITY_ATTRIBUTES = _ctypes.POINTER(struct__SECURITY_ATTRIBUTES)


class struct__OVERLAPPED(_ctypes.Structure):
    _fields_ = [
    ('Internal', DWORD),
    ('InternalHigh', DWORD),
    ('Offset', DWORD),
    ('OffsetHigh', DWORD),
    ('hEvent', HANDLE),
]
LPOVERLAPPED = _ctypes.POINTER(struct__OVERLAPPED)
OVERLAPPED = struct__OVERLAPPED


# C-Functions
FT_Open = _library.FT_Open
FT_Open.restype = FT_STATUS
# FT_Open(deviceNumber, pHandle)
FT_Open.argtypes = [_ctypes.c_int32, _ctypes.POINTER(_ctypes.POINTER(None))]
FT_Open.__doc__ = \
    """FT_STATUS FT_Open(c_int32 deviceNumber, LP_LP_None pHandle)
    .\ftd2xx.h:366"""
FT_OpenEx = _library.FT_OpenEx
FT_OpenEx.restype = FT_STATUS
# FT_OpenEx(pArg1, Flags, pHandle)
FT_OpenEx.argtypes = [PVOID, DWORD, _ctypes.POINTER(_ctypes.POINTER(None))]
FT_OpenEx.__doc__ = \
    """FT_STATUS FT_OpenEx(PVOID pArg1, DWORD Flags, LP_LP_None pHandle)
    .\ftd2xx.h:372"""
FT_ListDevices = _library.FT_ListDevices
FT_ListDevices.restype = FT_STATUS
# FT_ListDevices(pArg1, pArg2, Flags)
FT_ListDevices.argtypes = [PVOID, PVOID, DWORD]
FT_ListDevices.__doc__ = \
    """FT_STATUS FT_ListDevices(PVOID pArg1, PVOID pArg2, DWORD Flags)
    .\ftd2xx.h:379"""
FT_Close = _library.FT_Close
FT_Close.restype = FT_STATUS
# FT_Close(ftHandle)
FT_Close.argtypes = [FT_HANDLE]
FT_Close.__doc__ = \
    """FT_STATUS FT_Close(FT_HANDLE ftHandle)
    .\ftd2xx.h:386"""
FT_Read = _library.FT_Read
FT_Read.restype = FT_STATUS
# FT_Read(ftHandle, lpBuffer, dwBytesToRead, lpBytesReturned)
FT_Read.argtypes = [FT_HANDLE, LPVOID, DWORD, LPDWORD]
FT_Read.__doc__ = \
    """FT_STATUS FT_Read(FT_HANDLE ftHandle, LPVOID lpBuffer, DWORD dwBytesToRead, LPDWORD lpBytesReturned)
    .\ftd2xx.h:391"""
FT_Write = _library.FT_Write
FT_Write.restype = FT_STATUS
# FT_Write(ftHandle, lpBuffer, dwBytesToWrite, lpBytesWritten)
FT_Write.argtypes = [FT_HANDLE, LPVOID, DWORD, LPDWORD]
FT_Write.__doc__ = \
    """FT_STATUS FT_Write(FT_HANDLE ftHandle, LPVOID lpBuffer, DWORD dwBytesToWrite, LPDWORD lpBytesWritten)
    .\ftd2xx.h:399"""
FT_IoCtl = _library.FT_IoCtl
FT_IoCtl.restype = FT_STATUS
# FT_IoCtl(ftHandle, dwIoControlCode, lpInBuf, nInBufSize, lpOutBuf, nOutBufSize, lpBytesReturned, lpOverlapped)
FT_IoCtl.argtypes = [FT_HANDLE, DWORD, LPVOID, DWORD, LPVOID, DWORD, LPDWORD, LPOVERLAPPED]
FT_IoCtl.__doc__ = \
    """FT_STATUS FT_IoCtl(FT_HANDLE ftHandle, DWORD dwIoControlCode, LPVOID lpInBuf, DWORD nInBufSize, LPVOID lpOutBuf, DWORD nOutBufSize, LPDWORD lpBytesReturned, LPOVERLAPPED lpOverlapped)
    .\ftd2xx.h:407"""
FT_SetBaudRate = _library.FT_SetBaudRate
FT_SetBaudRate.restype = FT_STATUS
# FT_SetBaudRate(ftHandle, BaudRate)
FT_SetBaudRate.argtypes = [FT_HANDLE, ULONG]
FT_SetBaudRate.__doc__ = \
    """FT_STATUS FT_SetBaudRate(FT_HANDLE ftHandle, ULONG BaudRate)
    .\ftd2xx.h:419"""
FT_SetDivisor = _library.FT_SetDivisor
FT_SetDivisor.restype = FT_STATUS
# FT_SetDivisor(ftHandle, Divisor)
FT_SetDivisor.argtypes = [FT_HANDLE, USHORT]
FT_SetDivisor.__doc__ = \
    """FT_STATUS FT_SetDivisor(FT_HANDLE ftHandle, USHORT Divisor)
    .\ftd2xx.h:425"""
FT_SetDataCharacteristics = _library.FT_SetDataCharacteristics
FT_SetDataCharacteristics.restype = FT_STATUS
# FT_SetDataCharacteristics(ftHandle, WordLength, StopBits, Parity)
FT_SetDataCharacteristics.argtypes = [FT_HANDLE, UCHAR, UCHAR, UCHAR]
FT_SetDataCharacteristics.__doc__ = \
    """FT_STATUS FT_SetDataCharacteristics(FT_HANDLE ftHandle, UCHAR WordLength, UCHAR StopBits, UCHAR Parity)
    .\ftd2xx.h:431"""
FT_SetFlowControl = _library.FT_SetFlowControl
FT_SetFlowControl.restype = FT_STATUS
# FT_SetFlowControl(ftHandle, FlowControl, XonChar, XoffChar)
FT_SetFlowControl.argtypes = [FT_HANDLE, USHORT, UCHAR, UCHAR]
FT_SetFlowControl.__doc__ = \
    """FT_STATUS FT_SetFlowControl(FT_HANDLE ftHandle, USHORT FlowControl, UCHAR XonChar, UCHAR XoffChar)
    .\ftd2xx.h:439"""
FT_ResetDevice = _library.FT_ResetDevice
FT_ResetDevice.restype = FT_STATUS
# FT_ResetDevice(ftHandle)
FT_ResetDevice.argtypes = [FT_HANDLE]
FT_ResetDevice.__doc__ = \
    """FT_STATUS FT_ResetDevice(FT_HANDLE ftHandle)
    .\ftd2xx.h:447"""
FT_SetDtr = _library.FT_SetDtr
FT_SetDtr.restype = FT_STATUS
# FT_SetDtr(ftHandle)
FT_SetDtr.argtypes = [FT_HANDLE]
FT_SetDtr.__doc__ = \
    """FT_STATUS FT_SetDtr(FT_HANDLE ftHandle)
    .\ftd2xx.h:452"""
FT_ClrDtr = _library.FT_ClrDtr
FT_ClrDtr.restype = FT_STATUS
# FT_ClrDtr(ftHandle)
FT_ClrDtr.argtypes = [FT_HANDLE]
FT_ClrDtr.__doc__ = \
    """FT_STATUS FT_ClrDtr(FT_HANDLE ftHandle)
    .\ftd2xx.h:457"""
FT_SetRts = _library.FT_SetRts
FT_SetRts.restype = FT_STATUS
# FT_SetRts(ftHandle)
FT_SetRts.argtypes = [FT_HANDLE]
FT_SetRts.__doc__ = \
    """FT_STATUS FT_SetRts(FT_HANDLE ftHandle)
    .\ftd2xx.h:462"""
FT_ClrRts = _library.FT_ClrRts
FT_ClrRts.restype = FT_STATUS
# FT_ClrRts(ftHandle)
FT_ClrRts.argtypes = [FT_HANDLE]
FT_ClrRts.__doc__ = \
    """FT_STATUS FT_ClrRts(FT_HANDLE ftHandle)
    .\ftd2xx.h:467"""
FT_GetModemStatus = _library.FT_GetModemStatus
FT_GetModemStatus.restype = FT_STATUS
# FT_GetModemStatus(ftHandle, pModemStatus)
FT_GetModemStatus.argtypes = [FT_HANDLE, _ctypes.POINTER(_ctypes.c_uint32)]
FT_GetModemStatus.__doc__ = \
    """FT_STATUS FT_GetModemStatus(FT_HANDLE ftHandle, LP_ctypes_uint32 pModemStatus)
    .\ftd2xx.h:472"""
FT_SetChars = _library.FT_SetChars
FT_SetChars.restype = FT_STATUS
# FT_SetChars(ftHandle, EventChar, EventCharEnabled, ErrorChar, ErrorCharEnabled)
FT_SetChars.argtypes = [FT_HANDLE, UCHAR, UCHAR, UCHAR, UCHAR]
FT_SetChars.__doc__ = \
    """FT_STATUS FT_SetChars(FT_HANDLE ftHandle, UCHAR EventChar, UCHAR EventCharEnabled, UCHAR ErrorChar, UCHAR ErrorCharEnabled)
    .\ftd2xx.h:478"""
FT_Purge = _library.FT_Purge
FT_Purge.restype = FT_STATUS
# FT_Purge(ftHandle, Mask)
FT_Purge.argtypes = [FT_HANDLE, ULONG]
FT_Purge.__doc__ = \
    """FT_STATUS FT_Purge(FT_HANDLE ftHandle, ULONG Mask)
    .\ftd2xx.h:487"""
FT_SetTimeouts = _library.FT_SetTimeouts
FT_SetTimeouts.restype = FT_STATUS
# FT_SetTimeouts(ftHandle, ReadTimeout, WriteTimeout)
FT_SetTimeouts.argtypes = [FT_HANDLE, ULONG, ULONG]
FT_SetTimeouts.__doc__ = \
    """FT_STATUS FT_SetTimeouts(FT_HANDLE ftHandle, ULONG ReadTimeout, ULONG WriteTimeout)
    .\ftd2xx.h:493"""
FT_GetQueueStatus = _library.FT_GetQueueStatus
FT_GetQueueStatus.restype = FT_STATUS
# FT_GetQueueStatus(ftHandle, dwRxBytes)
FT_GetQueueStatus.argtypes = [FT_HANDLE, _ctypes.POINTER(_ctypes.c_uint32)]
FT_GetQueueStatus.__doc__ = \
    """FT_STATUS FT_GetQueueStatus(FT_HANDLE ftHandle, LP_ctypes_uint32 dwRxBytes)
    .\ftd2xx.h:500"""
FT_SetEventNotification = _library.FT_SetEventNotification
FT_SetEventNotification.restype = FT_STATUS
# FT_SetEventNotification(ftHandle, Mask, Param)
FT_SetEventNotification.argtypes = [FT_HANDLE, DWORD, PVOID]
FT_SetEventNotification.__doc__ = \
    """FT_STATUS FT_SetEventNotification(FT_HANDLE ftHandle, DWORD Mask, PVOID Param)
    .\ftd2xx.h:506"""
FT_GetStatus = _library.FT_GetStatus
FT_GetStatus.restype = FT_STATUS
# FT_GetStatus(ftHandle, dwRxBytes, dwTxBytes, dwEventDWord)
FT_GetStatus.argtypes = [FT_HANDLE, _ctypes.POINTER(_ctypes.c_uint32), _ctypes.POINTER(_ctypes.c_uint32), _ctypes.POINTER(_ctypes.c_uint32)]
FT_GetStatus.__doc__ = \
    """FT_STATUS FT_GetStatus(FT_HANDLE ftHandle, LP_ctypes_uint32 dwRxBytes, LP_ctypes_uint32 dwTxBytes, LP_ctypes_uint32 dwEventDWord)
    .\ftd2xx.h:513"""
FT_SetBreakOn = _library.FT_SetBreakOn
FT_SetBreakOn.restype = FT_STATUS
# FT_SetBreakOn(ftHandle)
FT_SetBreakOn.argtypes = [FT_HANDLE]
FT_SetBreakOn.__doc__ = \
    """FT_STATUS FT_SetBreakOn(FT_HANDLE ftHandle)
    .\ftd2xx.h:521"""
FT_SetBreakOff = _library.FT_SetBreakOff
FT_SetBreakOff.restype = FT_STATUS
# FT_SetBreakOff(ftHandle)
FT_SetBreakOff.argtypes = [FT_HANDLE]
FT_SetBreakOff.__doc__ = \
    """FT_STATUS FT_SetBreakOff(FT_HANDLE ftHandle)
    .\ftd2xx.h:526"""
FT_SetWaitMask = _library.FT_SetWaitMask
FT_SetWaitMask.restype = FT_STATUS
# FT_SetWaitMask(ftHandle, Mask)
FT_SetWaitMask.argtypes = [FT_HANDLE, DWORD]
FT_SetWaitMask.__doc__ = \
    """FT_STATUS FT_SetWaitMask(FT_HANDLE ftHandle, DWORD Mask)
    .\ftd2xx.h:531"""
FT_WaitOnMask = _library.FT_WaitOnMask
FT_WaitOnMask.restype = FT_STATUS
# FT_WaitOnMask(ftHandle, Mask)
FT_WaitOnMask.argtypes = [FT_HANDLE, _ctypes.POINTER(_ctypes.c_uint32)]
FT_WaitOnMask.__doc__ = \
    """FT_STATUS FT_WaitOnMask(FT_HANDLE ftHandle, LP_ctypes_uint32 Mask)
    .\ftd2xx.h:537"""
FT_GetEventStatus = _library.FT_GetEventStatus
FT_GetEventStatus.restype = FT_STATUS
# FT_GetEventStatus(ftHandle, dwEventDWord)
FT_GetEventStatus.argtypes = [FT_HANDLE, _ctypes.POINTER(_ctypes.c_uint32)]
FT_GetEventStatus.__doc__ = \
    """FT_STATUS FT_GetEventStatus(FT_HANDLE ftHandle, LP_ctypes_uint32 dwEventDWord)
    .\ftd2xx.h:543"""
FT_ReadEE = _library.FT_ReadEE
FT_ReadEE.restype = FT_STATUS
# FT_ReadEE(ftHandle, dwWordOffset, lpwValue)
FT_ReadEE.argtypes = [FT_HANDLE, DWORD, LPWORD]
FT_ReadEE.__doc__ = \
    """FT_STATUS FT_ReadEE(FT_HANDLE ftHandle, DWORD dwWordOffset, LPWORD lpwValue)
    .\ftd2xx.h:549"""
FT_WriteEE = _library.FT_WriteEE
FT_WriteEE.restype = FT_STATUS
# FT_WriteEE(ftHandle, dwWordOffset, wValue)
FT_WriteEE.argtypes = [FT_HANDLE, DWORD, WORD]
FT_WriteEE.__doc__ = \
    """FT_STATUS FT_WriteEE(FT_HANDLE ftHandle, DWORD dwWordOffset, WORD wValue)
    .\ftd2xx.h:556"""
FT_EraseEE = _library.FT_EraseEE
FT_EraseEE.restype = FT_STATUS
# FT_EraseEE(ftHandle)
FT_EraseEE.argtypes = [FT_HANDLE]
FT_EraseEE.__doc__ = \
    """FT_STATUS FT_EraseEE(FT_HANDLE ftHandle)
    .\ftd2xx.h:563"""
FT_EE_Program = _library.FT_EE_Program
FT_EE_Program.restype = FT_STATUS
# FT_EE_Program(ftHandle, pData)
FT_EE_Program.argtypes = [FT_HANDLE, PFT_PROGRAM_DATA]
FT_EE_Program.__doc__ = \
    """FT_STATUS FT_EE_Program(FT_HANDLE ftHandle, PFT_PROGRAM_DATA pData)
    .\ftd2xx.h:732"""
FT_EE_ProgramEx = _library.FT_EE_ProgramEx
FT_EE_ProgramEx.restype = FT_STATUS
# FT_EE_ProgramEx(ftHandle, pData, Manufacturer, ManufacturerId, Description, SerialNumber)
FT_EE_ProgramEx.argtypes = [FT_HANDLE, PFT_PROGRAM_DATA, STRING, STRING, STRING, STRING]
FT_EE_ProgramEx.__doc__ = \
    """FT_STATUS FT_EE_ProgramEx(FT_HANDLE ftHandle, PFT_PROGRAM_DATA pData, LP_ctypes_ctypeshar Manufacturer, LP_ctypes_ctypeshar ManufacturerId, LP_ctypes_ctypeshar Description, LP_ctypes_ctypeshar SerialNumber)
    .\ftd2xx.h:738"""
FT_EE_Read = _library.FT_EE_Read
FT_EE_Read.restype = FT_STATUS
# FT_EE_Read(ftHandle, pData)
FT_EE_Read.argtypes = [FT_HANDLE, PFT_PROGRAM_DATA]
FT_EE_Read.__doc__ = \
    """FT_STATUS FT_EE_Read(FT_HANDLE ftHandle, PFT_PROGRAM_DATA pData)
    .\ftd2xx.h:748"""
FT_EE_ReadEx = _library.FT_EE_ReadEx
FT_EE_ReadEx.restype = FT_STATUS
# FT_EE_ReadEx(ftHandle, pData, Manufacturer, ManufacturerId, Description, SerialNumber)
FT_EE_ReadEx.argtypes = [FT_HANDLE, PFT_PROGRAM_DATA, STRING, STRING, STRING, STRING]
FT_EE_ReadEx.__doc__ = \
    """FT_STATUS FT_EE_ReadEx(FT_HANDLE ftHandle, PFT_PROGRAM_DATA pData, LP_ctypes_ctypeshar Manufacturer, LP_ctypes_ctypeshar ManufacturerId, LP_ctypes_ctypeshar Description, LP_ctypes_ctypeshar SerialNumber)
    .\ftd2xx.h:754"""
FT_EE_UASize = _library.FT_EE_UASize
FT_EE_UASize.restype = FT_STATUS
# FT_EE_UASize(ftHandle, lpdwSize)
FT_EE_UASize.argtypes = [FT_HANDLE, LPDWORD]
FT_EE_UASize.__doc__ = \
    """FT_STATUS FT_EE_UASize(FT_HANDLE ftHandle, LPDWORD lpdwSize)
    .\ftd2xx.h:764"""
FT_EE_UAWrite = _library.FT_EE_UAWrite
FT_EE_UAWrite.restype = FT_STATUS
# FT_EE_UAWrite(ftHandle, pucData, dwDataLen)
FT_EE_UAWrite.argtypes = [FT_HANDLE, PUCHAR, DWORD]
FT_EE_UAWrite.__doc__ = \
    """FT_STATUS FT_EE_UAWrite(FT_HANDLE ftHandle, PUCHAR pucData, DWORD dwDataLen)
    .\ftd2xx.h:770"""
FT_EE_UARead = _library.FT_EE_UARead
FT_EE_UARead.restype = FT_STATUS
# FT_EE_UARead(ftHandle, pucData, dwDataLen, lpdwBytesRead)
FT_EE_UARead.argtypes = [FT_HANDLE, PUCHAR, DWORD, LPDWORD]
FT_EE_UARead.__doc__ = \
    """FT_STATUS FT_EE_UARead(FT_HANDLE ftHandle, PUCHAR pucData, DWORD dwDataLen, LPDWORD lpdwBytesRead)
    .\ftd2xx.h:777"""
FT_EEPROM_Read = _library.FT_EEPROM_Read
FT_EEPROM_Read.restype = FT_STATUS
# FT_EEPROM_Read(ftHandle, eepromData, eepromDataSize, Manufacturer, ManufacturerId, Description, SerialNumber)
FT_EEPROM_Read.argtypes = [FT_HANDLE, _ctypes.POINTER(None), DWORD, STRING, STRING, STRING, STRING]
FT_EEPROM_Read.__doc__ = \
    """FT_STATUS FT_EEPROM_Read(FT_HANDLE ftHandle, LP_None eepromData, DWORD eepromDataSize, LP_ctypes_ctypeshar Manufacturer, LP_ctypes_ctypeshar ManufacturerId, LP_ctypes_ctypeshar Description, LP_ctypes_ctypeshar SerialNumber)
    .\ftd2xx.h:1000"""
FT_EEPROM_Program = _library.FT_EEPROM_Program
FT_EEPROM_Program.restype = FT_STATUS
# FT_EEPROM_Program(ftHandle, eepromData, eepromDataSize, Manufacturer, ManufacturerId, Description, SerialNumber)
FT_EEPROM_Program.argtypes = [FT_HANDLE, _ctypes.POINTER(None), DWORD, STRING, STRING, STRING, STRING]
FT_EEPROM_Program.__doc__ = \
    """FT_STATUS FT_EEPROM_Program(FT_HANDLE ftHandle, LP_None eepromData, DWORD eepromDataSize, LP_ctypes_ctypeshar Manufacturer, LP_ctypes_ctypeshar ManufacturerId, LP_ctypes_ctypeshar Description, LP_ctypes_ctypeshar SerialNumber)
    .\ftd2xx.h:1012"""
FT_SetLatencyTimer = _library.FT_SetLatencyTimer
FT_SetLatencyTimer.restype = FT_STATUS
# FT_SetLatencyTimer(ftHandle, ucLatency)
FT_SetLatencyTimer.argtypes = [FT_HANDLE, UCHAR]
FT_SetLatencyTimer.__doc__ = \
    """FT_STATUS FT_SetLatencyTimer(FT_HANDLE ftHandle, UCHAR ucLatency)
    .\ftd2xx.h:1024"""
FT_GetLatencyTimer = _library.FT_GetLatencyTimer
FT_GetLatencyTimer.restype = FT_STATUS
# FT_GetLatencyTimer(ftHandle, pucLatency)
FT_GetLatencyTimer.argtypes = [FT_HANDLE, PUCHAR]
FT_GetLatencyTimer.__doc__ = \
    """FT_STATUS FT_GetLatencyTimer(FT_HANDLE ftHandle, PUCHAR pucLatency)
    .\ftd2xx.h:1030"""
FT_SetBitMode = _library.FT_SetBitMode
FT_SetBitMode.restype = FT_STATUS
# FT_SetBitMode(ftHandle, ucMask, ucEnable)
FT_SetBitMode.argtypes = [FT_HANDLE, UCHAR, UCHAR]
FT_SetBitMode.__doc__ = \
    """FT_STATUS FT_SetBitMode(FT_HANDLE ftHandle, UCHAR ucMask, UCHAR ucEnable)
    .\ftd2xx.h:1036"""
FT_GetBitMode = _library.FT_GetBitMode
FT_GetBitMode.restype = FT_STATUS
# FT_GetBitMode(ftHandle, pucMode)
FT_GetBitMode.argtypes = [FT_HANDLE, PUCHAR]
FT_GetBitMode.__doc__ = \
    """FT_STATUS FT_GetBitMode(FT_HANDLE ftHandle, PUCHAR pucMode)
    .\ftd2xx.h:1043"""
FT_SetUSBParameters = _library.FT_SetUSBParameters
FT_SetUSBParameters.restype = FT_STATUS
# FT_SetUSBParameters(ftHandle, ulInTransferSize, ulOutTransferSize)
FT_SetUSBParameters.argtypes = [FT_HANDLE, ULONG, ULONG]
FT_SetUSBParameters.__doc__ = \
    """FT_STATUS FT_SetUSBParameters(FT_HANDLE ftHandle, ULONG ulInTransferSize, ULONG ulOutTransferSize)
    .\ftd2xx.h:1049"""
FT_SetDeadmanTimeout = _library.FT_SetDeadmanTimeout
FT_SetDeadmanTimeout.restype = FT_STATUS
# FT_SetDeadmanTimeout(ftHandle, ulDeadmanTimeout)
FT_SetDeadmanTimeout.argtypes = [FT_HANDLE, ULONG]
FT_SetDeadmanTimeout.__doc__ = \
    """FT_STATUS FT_SetDeadmanTimeout(FT_HANDLE ftHandle, ULONG ulDeadmanTimeout)
    .\ftd2xx.h:1056"""
FT_GetDeviceInfo = _library.FT_GetDeviceInfo
FT_GetDeviceInfo.restype = FT_STATUS
# FT_GetDeviceInfo(ftHandle, lpftDevice, lpdwID, SerialNumber, Description, Dummy)
FT_GetDeviceInfo.argtypes = [FT_HANDLE, _ctypes.POINTER(_ctypes.c_uint32), LPDWORD, PCHAR, PCHAR, LPVOID]
FT_GetDeviceInfo.__doc__ = \
    """FT_STATUS FT_GetDeviceInfo(FT_HANDLE ftHandle, LP_ctypes_uint32 lpftDevice, LPDWORD lpdwID, PCHAR SerialNumber, PCHAR Description, LPVOID Dummy)
    .\ftd2xx.h:1085"""
FT_StopInTask = _library.FT_StopInTask
FT_StopInTask.restype = FT_STATUS
# FT_StopInTask(ftHandle)
FT_StopInTask.argtypes = [FT_HANDLE]
FT_StopInTask.__doc__ = \
    """FT_STATUS FT_StopInTask(FT_HANDLE ftHandle)
    .\ftd2xx.h:1095"""
FT_RestartInTask = _library.FT_RestartInTask
FT_RestartInTask.restype = FT_STATUS
# FT_RestartInTask(ftHandle)
FT_RestartInTask.argtypes = [FT_HANDLE]
FT_RestartInTask.__doc__ = \
    """FT_STATUS FT_RestartInTask(FT_HANDLE ftHandle)
    .\ftd2xx.h:1100"""
FT_SetResetPipeRetryCount = _library.FT_SetResetPipeRetryCount
FT_SetResetPipeRetryCount.restype = FT_STATUS
# FT_SetResetPipeRetryCount(ftHandle, dwCount)
FT_SetResetPipeRetryCount.argtypes = [FT_HANDLE, DWORD]
FT_SetResetPipeRetryCount.__doc__ = \
    """FT_STATUS FT_SetResetPipeRetryCount(FT_HANDLE ftHandle, DWORD dwCount)
    .\ftd2xx.h:1105"""
FT_ResetPort = _library.FT_ResetPort
FT_ResetPort.restype = FT_STATUS
# FT_ResetPort(ftHandle)
FT_ResetPort.argtypes = [FT_HANDLE]
FT_ResetPort.__doc__ = \
    """FT_STATUS FT_ResetPort(FT_HANDLE ftHandle)
    .\ftd2xx.h:1111"""
FT_CyclePort = _library.FT_CyclePort
FT_CyclePort.restype = FT_STATUS
# FT_CyclePort(ftHandle)
FT_CyclePort.argtypes = [FT_HANDLE]
FT_CyclePort.__doc__ = \
    """FT_STATUS FT_CyclePort(FT_HANDLE ftHandle)
    .\ftd2xx.h:1116"""
FT_W32_CreateFile = _library.FT_W32_CreateFile
FT_W32_CreateFile.restype = FT_HANDLE
# FT_W32_CreateFile(lpszName, dwAccess, dwShareMode, lpSecurityAttributes, dwCreate, dwAttrsAndFlags, hTemplate)
FT_W32_CreateFile.argtypes = [LPCTSTR, DWORD, DWORD, LPSECURITY_ATTRIBUTES, DWORD, DWORD, HANDLE]
FT_W32_CreateFile.__doc__ = \
    """FT_HANDLE FT_W32_CreateFile(LPCTSTR lpszName, DWORD dwAccess, DWORD dwShareMode, LPSECURITY_ATTRIBUTES lpSecurityAttributes, DWORD dwCreate, DWORD dwAttrsAndFlags, HANDLE hTemplate)
    .\ftd2xx.h:1126"""
FT_W32_CloseHandle = _library.FT_W32_CloseHandle
FT_W32_CloseHandle.restype = BOOL
# FT_W32_CloseHandle(ftHandle)
FT_W32_CloseHandle.argtypes = [FT_HANDLE]
FT_W32_CloseHandle.__doc__ = \
    """BOOL FT_W32_CloseHandle(FT_HANDLE ftHandle)
    .\ftd2xx.h:1137"""
FT_W32_ReadFile = _library.FT_W32_ReadFile
FT_W32_ReadFile.restype = BOOL
# FT_W32_ReadFile(ftHandle, lpBuffer, nBufferSize, lpBytesReturned, lpOverlapped)
FT_W32_ReadFile.argtypes = [FT_HANDLE, LPVOID, DWORD, LPDWORD, LPOVERLAPPED]
FT_W32_ReadFile.__doc__ = \
    """BOOL FT_W32_ReadFile(FT_HANDLE ftHandle, LPVOID lpBuffer, DWORD nBufferSize, LPDWORD lpBytesReturned, LPOVERLAPPED lpOverlapped)
    .\ftd2xx.h:1142"""
FT_W32_WriteFile = _library.FT_W32_WriteFile
FT_W32_WriteFile.restype = BOOL
# FT_W32_WriteFile(ftHandle, lpBuffer, nBufferSize, lpBytesWritten, lpOverlapped)
FT_W32_WriteFile.argtypes = [FT_HANDLE, LPVOID, DWORD, LPDWORD, LPOVERLAPPED]
FT_W32_WriteFile.__doc__ = \
    """BOOL FT_W32_WriteFile(FT_HANDLE ftHandle, LPVOID lpBuffer, DWORD nBufferSize, LPDWORD lpBytesWritten, LPOVERLAPPED lpOverlapped)
    .\ftd2xx.h:1151"""
FT_W32_GetLastError = _library.FT_W32_GetLastError
FT_W32_GetLastError.restype = DWORD
# FT_W32_GetLastError(ftHandle)
FT_W32_GetLastError.argtypes = [FT_HANDLE]
FT_W32_GetLastError.__doc__ = \
    """DWORD FT_W32_GetLastError(FT_HANDLE ftHandle)
    .\ftd2xx.h:1160"""
FT_W32_GetOverlappedResult = _library.FT_W32_GetOverlappedResult
FT_W32_GetOverlappedResult.restype = BOOL
# FT_W32_GetOverlappedResult(ftHandle, lpOverlapped, lpdwBytesTransferred, bWait)
FT_W32_GetOverlappedResult.argtypes = [FT_HANDLE, LPOVERLAPPED, LPDWORD, BOOL]
FT_W32_GetOverlappedResult.__doc__ = \
    """BOOL FT_W32_GetOverlappedResult(FT_HANDLE ftHandle, LPOVERLAPPED lpOverlapped, LPDWORD lpdwBytesTransferred, BOOL bWait)
    .\ftd2xx.h:1165"""
FT_W32_CancelIo = _library.FT_W32_CancelIo
FT_W32_CancelIo.restype = BOOL
# FT_W32_CancelIo(ftHandle)
FT_W32_CancelIo.argtypes = [FT_HANDLE]
FT_W32_CancelIo.__doc__ = \
    """BOOL FT_W32_CancelIo(FT_HANDLE ftHandle)
    .\ftd2xx.h:1173"""
FT_W32_ClearCommBreak = _library.FT_W32_ClearCommBreak
FT_W32_ClearCommBreak.restype = BOOL
# FT_W32_ClearCommBreak(ftHandle)
FT_W32_ClearCommBreak.argtypes = [FT_HANDLE]
FT_W32_ClearCommBreak.__doc__ = \
    """BOOL FT_W32_ClearCommBreak(FT_HANDLE ftHandle)
    .\ftd2xx.h:1235"""
FT_W32_ClearCommError = _library.FT_W32_ClearCommError
FT_W32_ClearCommError.restype = BOOL
# FT_W32_ClearCommError(ftHandle, lpdwErrors, lpftComstat)
FT_W32_ClearCommError.argtypes = [FT_HANDLE, LPDWORD, LPFTCOMSTAT]
FT_W32_ClearCommError.__doc__ = \
    """BOOL FT_W32_ClearCommError(FT_HANDLE ftHandle, LPDWORD lpdwErrors, LPFTCOMSTAT lpftComstat)
    .\ftd2xx.h:1240"""
FT_W32_EscapeCommFunction = _library.FT_W32_EscapeCommFunction
FT_W32_EscapeCommFunction.restype = BOOL
# FT_W32_EscapeCommFunction(ftHandle, dwFunc)
FT_W32_EscapeCommFunction.argtypes = [FT_HANDLE, DWORD]
FT_W32_EscapeCommFunction.__doc__ = \
    """BOOL FT_W32_EscapeCommFunction(FT_HANDLE ftHandle, DWORD dwFunc)
    .\ftd2xx.h:1247"""
FT_W32_GetCommModemStatus = _library.FT_W32_GetCommModemStatus
FT_W32_GetCommModemStatus.restype = BOOL
# FT_W32_GetCommModemStatus(ftHandle, lpdwModemStatus)
FT_W32_GetCommModemStatus.argtypes = [FT_HANDLE, LPDWORD]
FT_W32_GetCommModemStatus.__doc__ = \
    """BOOL FT_W32_GetCommModemStatus(FT_HANDLE ftHandle, LPDWORD lpdwModemStatus)
    .\ftd2xx.h:1253"""
FT_W32_GetCommState = _library.FT_W32_GetCommState
FT_W32_GetCommState.restype = BOOL
# FT_W32_GetCommState(ftHandle, lpftDcb)
FT_W32_GetCommState.argtypes = [FT_HANDLE, LPFTDCB]
FT_W32_GetCommState.__doc__ = \
    """BOOL FT_W32_GetCommState(FT_HANDLE ftHandle, LPFTDCB lpftDcb)
    .\ftd2xx.h:1259"""
FT_W32_GetCommTimeouts = _library.FT_W32_GetCommTimeouts
FT_W32_GetCommTimeouts.restype = BOOL
# FT_W32_GetCommTimeouts(ftHandle, pTimeouts)
FT_W32_GetCommTimeouts.argtypes = [FT_HANDLE, _ctypes.POINTER(struct__FTTIMEOUTS)]
FT_W32_GetCommTimeouts.__doc__ = \
    """BOOL FT_W32_GetCommTimeouts(FT_HANDLE ftHandle, LP_struct__FTTIMEOUTS pTimeouts)
    .\ftd2xx.h:1265"""
FT_W32_PurgeComm = _library.FT_W32_PurgeComm
FT_W32_PurgeComm.restype = BOOL
# FT_W32_PurgeComm(ftHandle, dwMask)
FT_W32_PurgeComm.argtypes = [FT_HANDLE, DWORD]
FT_W32_PurgeComm.__doc__ = \
    """BOOL FT_W32_PurgeComm(FT_HANDLE ftHandle, DWORD dwMask)
    .\ftd2xx.h:1271"""
FT_W32_SetCommBreak = _library.FT_W32_SetCommBreak
FT_W32_SetCommBreak.restype = BOOL
# FT_W32_SetCommBreak(ftHandle)
FT_W32_SetCommBreak.argtypes = [FT_HANDLE]
FT_W32_SetCommBreak.__doc__ = \
    """BOOL FT_W32_SetCommBreak(FT_HANDLE ftHandle)
    .\ftd2xx.h:1277"""
FT_W32_SetCommMask = _library.FT_W32_SetCommMask
FT_W32_SetCommMask.restype = BOOL
# FT_W32_SetCommMask(ftHandle, ulEventMask)
FT_W32_SetCommMask.argtypes = [FT_HANDLE, ULONG]
FT_W32_SetCommMask.__doc__ = \
    """BOOL FT_W32_SetCommMask(FT_HANDLE ftHandle, ULONG ulEventMask)
    .\ftd2xx.h:1282"""
FT_W32_GetCommMask = _library.FT_W32_GetCommMask
FT_W32_GetCommMask.restype = BOOL
# FT_W32_GetCommMask(ftHandle, lpdwEventMask)
FT_W32_GetCommMask.argtypes = [FT_HANDLE, LPDWORD]
FT_W32_GetCommMask.__doc__ = \
    """BOOL FT_W32_GetCommMask(FT_HANDLE ftHandle, LPDWORD lpdwEventMask)
    .\ftd2xx.h:1288"""
FT_W32_SetCommState = _library.FT_W32_SetCommState
FT_W32_SetCommState.restype = BOOL
# FT_W32_SetCommState(ftHandle, lpftDcb)
FT_W32_SetCommState.argtypes = [FT_HANDLE, LPFTDCB]
FT_W32_SetCommState.__doc__ = \
    """BOOL FT_W32_SetCommState(FT_HANDLE ftHandle, LPFTDCB lpftDcb)
    .\ftd2xx.h:1294"""
FT_W32_SetCommTimeouts = _library.FT_W32_SetCommTimeouts
FT_W32_SetCommTimeouts.restype = BOOL
# FT_W32_SetCommTimeouts(ftHandle, pTimeouts)
FT_W32_SetCommTimeouts.argtypes = [FT_HANDLE, _ctypes.POINTER(struct__FTTIMEOUTS)]
FT_W32_SetCommTimeouts.__doc__ = \
    """BOOL FT_W32_SetCommTimeouts(FT_HANDLE ftHandle, LP_struct__FTTIMEOUTS pTimeouts)
    .\ftd2xx.h:1300"""
FT_W32_SetupComm = _library.FT_W32_SetupComm
FT_W32_SetupComm.restype = BOOL
# FT_W32_SetupComm(ftHandle, dwReadBufferSize, dwWriteBufferSize)
FT_W32_SetupComm.argtypes = [FT_HANDLE, DWORD, DWORD]
FT_W32_SetupComm.__doc__ = \
    """BOOL FT_W32_SetupComm(FT_HANDLE ftHandle, DWORD dwReadBufferSize, DWORD dwWriteBufferSize)
    .\ftd2xx.h:1306"""
FT_W32_WaitCommEvent = _library.FT_W32_WaitCommEvent
FT_W32_WaitCommEvent.restype = BOOL
# FT_W32_WaitCommEvent(ftHandle, pulEvent, lpOverlapped)
FT_W32_WaitCommEvent.argtypes = [FT_HANDLE, PULONG, LPOVERLAPPED]
FT_W32_WaitCommEvent.__doc__ = \
    """BOOL FT_W32_WaitCommEvent(FT_HANDLE ftHandle, PULONG pulEvent, LPOVERLAPPED lpOverlapped)
    .\ftd2xx.h:1313"""
FT_CreateDeviceInfoList = _library.FT_CreateDeviceInfoList
FT_CreateDeviceInfoList.restype = FT_STATUS
# FT_CreateDeviceInfoList(lpdwNumDevs)
FT_CreateDeviceInfoList.argtypes = [LPDWORD]
FT_CreateDeviceInfoList.__doc__ = \
    """FT_STATUS FT_CreateDeviceInfoList(LPDWORD lpdwNumDevs)
    .\ftd2xx.h:1342"""
FT_GetDeviceInfoList = _library.FT_GetDeviceInfoList
FT_GetDeviceInfoList.restype = FT_STATUS
# FT_GetDeviceInfoList(pDest, lpdwNumDevs)
FT_GetDeviceInfoList.argtypes = [_ctypes.POINTER(struct__ft_device_list_info_node), LPDWORD]
FT_GetDeviceInfoList.__doc__ = \
    """FT_STATUS FT_GetDeviceInfoList(LP_struct__ft_device_list_info_node pDest, LPDWORD lpdwNumDevs)
    .\ftd2xx.h:1347"""
FT_GetDeviceInfoDetail = _library.FT_GetDeviceInfoDetail
FT_GetDeviceInfoDetail.restype = FT_STATUS
# FT_GetDeviceInfoDetail(dwIndex, lpdwFlags, lpdwType, lpdwID, lpdwLocId, lpSerialNumber, lpDescription, pftHandle)
FT_GetDeviceInfoDetail.argtypes = [DWORD, LPDWORD, LPDWORD, LPDWORD, LPDWORD, LPVOID, LPVOID, _ctypes.POINTER(_ctypes.POINTER(None))]
FT_GetDeviceInfoDetail.__doc__ = \
    """FT_STATUS FT_GetDeviceInfoDetail(DWORD dwIndex, LPDWORD lpdwFlags, LPDWORD lpdwType, LPDWORD lpdwID, LPDWORD lpdwLocId, LPVOID lpSerialNumber, LPVOID lpDescription, LP_LP_None pftHandle)
    .\ftd2xx.h:1353"""
FT_GetDriverVersion = _library.FT_GetDriverVersion
FT_GetDriverVersion.restype = FT_STATUS
# FT_GetDriverVersion(ftHandle, lpdwVersion)
FT_GetDriverVersion.argtypes = [FT_HANDLE, LPDWORD]
FT_GetDriverVersion.__doc__ = \
    """FT_STATUS FT_GetDriverVersion(FT_HANDLE ftHandle, LPDWORD lpdwVersion)
    .\ftd2xx.h:1370"""
FT_GetLibraryVersion = _library.FT_GetLibraryVersion
FT_GetLibraryVersion.restype = FT_STATUS
# FT_GetLibraryVersion(lpdwVersion)
FT_GetLibraryVersion.argtypes = [LPDWORD]
FT_GetLibraryVersion.__doc__ = \
    """FT_STATUS FT_GetLibraryVersion(LPDWORD lpdwVersion)
    .\ftd2xx.h:1376"""
FT_Rescan = _library.FT_Rescan
FT_Rescan.restype = FT_STATUS
# FT_Rescan()
FT_Rescan.argtypes = []
FT_Rescan.__doc__ = \
    """FT_STATUS FT_Rescan()
    .\ftd2xx.h:1382"""
FT_Reload = _library.FT_Reload
FT_Reload.restype = FT_STATUS
# FT_Reload(wVid, wPid)
FT_Reload.argtypes = [WORD, WORD]
FT_Reload.__doc__ = \
    """FT_STATUS FT_Reload(WORD wVid, WORD wPid)
    .\ftd2xx.h:1387"""
FT_GetComPortNumber = _library.FT_GetComPortNumber
FT_GetComPortNumber.restype = FT_STATUS
# FT_GetComPortNumber(ftHandle, lpdwComPortNumber)
FT_GetComPortNumber.argtypes = [FT_HANDLE, LPLONG]
FT_GetComPortNumber.__doc__ = \
    """FT_STATUS FT_GetComPortNumber(FT_HANDLE ftHandle, LPLONG lpdwComPortNumber)
    .\ftd2xx.h:1393"""
FT_EE_ReadConfig = _library.FT_EE_ReadConfig
FT_EE_ReadConfig.restype = FT_STATUS
# FT_EE_ReadConfig(ftHandle, ucAddress, pucValue)
FT_EE_ReadConfig.argtypes = [FT_HANDLE, UCHAR, PUCHAR]
FT_EE_ReadConfig.__doc__ = \
    """FT_STATUS FT_EE_ReadConfig(FT_HANDLE ftHandle, UCHAR ucAddress, PUCHAR pucValue)
    .\ftd2xx.h:1404"""
FT_EE_WriteConfig = _library.FT_EE_WriteConfig
FT_EE_WriteConfig.restype = FT_STATUS
# FT_EE_WriteConfig(ftHandle, ucAddress, ucValue)
FT_EE_WriteConfig.argtypes = [FT_HANDLE, UCHAR, UCHAR]
FT_EE_WriteConfig.__doc__ = \
    """FT_STATUS FT_EE_WriteConfig(FT_HANDLE ftHandle, UCHAR ucAddress, UCHAR ucValue)
    .\ftd2xx.h:1411"""
FT_EE_ReadECC = _library.FT_EE_ReadECC
FT_EE_ReadECC.restype = FT_STATUS
# FT_EE_ReadECC(ftHandle, ucOption, lpwValue)
FT_EE_ReadECC.argtypes = [FT_HANDLE, UCHAR, LPWORD]
FT_EE_ReadECC.__doc__ = \
    """FT_STATUS FT_EE_ReadECC(FT_HANDLE ftHandle, UCHAR ucOption, LPWORD lpwValue)
    .\ftd2xx.h:1418"""
FT_GetQueueStatusEx = _library.FT_GetQueueStatusEx
FT_GetQueueStatusEx.restype = FT_STATUS
# FT_GetQueueStatusEx(ftHandle, dwRxBytes)
FT_GetQueueStatusEx.argtypes = [FT_HANDLE, _ctypes.POINTER(_ctypes.c_uint32)]
FT_GetQueueStatusEx.__doc__ = \
    """FT_STATUS FT_GetQueueStatusEx(FT_HANDLE ftHandle, LP_ctypes_uint32 dwRxBytes)
    .\ftd2xx.h:1425"""
FT_ComPortIdle = _library.FT_ComPortIdle
FT_ComPortIdle.restype = FT_STATUS
# FT_ComPortIdle(ftHandle)
FT_ComPortIdle.argtypes = [FT_HANDLE]
FT_ComPortIdle.__doc__ = \
    """FT_STATUS FT_ComPortIdle(FT_HANDLE ftHandle)
    .\ftd2xx.h:1431"""
FT_ComPortCancelIdle = _library.FT_ComPortCancelIdle
FT_ComPortCancelIdle.restype = FT_STATUS
# FT_ComPortCancelIdle(ftHandle)
FT_ComPortCancelIdle.argtypes = [FT_HANDLE]
FT_ComPortCancelIdle.__doc__ = \
    """FT_STATUS FT_ComPortCancelIdle(FT_HANDLE ftHandle)
    .\ftd2xx.h:1436"""
FT_VendorCmdGet = _library.FT_VendorCmdGet
FT_VendorCmdGet.restype = FT_STATUS
# FT_VendorCmdGet(ftHandle, Request, Buf, Len)
FT_VendorCmdGet.argtypes = [FT_HANDLE, UCHAR, _ctypes.POINTER(_ctypes.c_ubyte), USHORT]
FT_VendorCmdGet.__doc__ = \
    """FT_STATUS FT_VendorCmdGet(FT_HANDLE ftHandle, UCHAR Request, LP_ctypes_ubyte Buf, USHORT Len)
    .\ftd2xx.h:1441"""
FT_VendorCmdSet = _library.FT_VendorCmdSet
FT_VendorCmdSet.restype = FT_STATUS
# FT_VendorCmdSet(ftHandle, Request, Buf, Len)
FT_VendorCmdSet.argtypes = [FT_HANDLE, UCHAR, _ctypes.POINTER(_ctypes.c_ubyte), USHORT]
FT_VendorCmdSet.__doc__ = \
    """FT_STATUS FT_VendorCmdSet(FT_HANDLE ftHandle, UCHAR Request, LP_ctypes_ubyte Buf, USHORT Len)
    .\ftd2xx.h:1449"""
FT_VendorCmdGetEx = _library.FT_VendorCmdGetEx
FT_VendorCmdGetEx.restype = FT_STATUS
# FT_VendorCmdGetEx(ftHandle, wValue, Buf, Len)
FT_VendorCmdGetEx.argtypes = [FT_HANDLE, USHORT, _ctypes.POINTER(_ctypes.c_ubyte), USHORT]
FT_VendorCmdGetEx.__doc__ = \
    """FT_STATUS FT_VendorCmdGetEx(FT_HANDLE ftHandle, USHORT wValue, LP_ctypes_ubyte Buf, USHORT Len)
    .\ftd2xx.h:1457"""
FT_VendorCmdSetEx = _library.FT_VendorCmdSetEx
FT_VendorCmdSetEx.restype = FT_STATUS
# FT_VendorCmdSetEx(ftHandle, wValue, Buf, Len)
FT_VendorCmdSetEx.argtypes = [FT_HANDLE, USHORT, _ctypes.POINTER(_ctypes.c_ubyte), USHORT]
FT_VendorCmdSetEx.__doc__ = \
    """FT_STATUS FT_VendorCmdSetEx(FT_HANDLE ftHandle, USHORT wValue, LP_ctypes_ubyte Buf, USHORT Len)
    .\ftd2xx.h:1465"""
