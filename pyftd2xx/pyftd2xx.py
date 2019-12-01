"""
Module for accessing functions from FTD2XX in an easier to use
_pythonic_ way. For full documentation please refer to the FTDI
Programming Guide. This module is based on Pablo Bleyers d2xx module,
except this uses ctypes instead of an extension approach.
"""

import sys as _sys
if _sys.platform == 'win32':
    from . import ftd2xx_win32 as _lib 
elif _sys.platform.startswith('linux'):
    from . import ftd2xx_linux as _lib
elif _sys.platform == 'darwin':
    from . import ftd2xx_darwin as _lib

import ctypes as _c
from . import defines as _FT
from munch import Munch as _ret


class _StatusError(Exception):
    """Exception class for status messages"""
    def __init__(self, error):
        self.message = _FT.STATUS[error]

    def __str__(self):
        return self.message
 
def _check_status(status):
    """Call an FTDI function and check the status. Raise exception on error"""
    if not _FT.SUCCESS(status):
        raise _StatusError(status)

def SetVIDPID(VID, PID):
    """Linux only. Set the VID and PID of the device"""
    _check_status(_lib.FT_SetVIDPID(_lib.DWORD(VID), _lib.DWORD(PID)))
    return None

def GetVIDPID():
    """Linux only. Get the VID and PID of the device"""
    VID = _lib.DWORD()
    PID = _lib.DWORD()
    _check_status(_lib.FT_GetVIDPID(_c.byref(VID), _c.byref(PID)))
    return _ret(VID = VID.value, PID = PID.value)

def CreateDeviceInfoList():
    """Create the internal device info list and return number of entries"""
    NumDevs = _lib.DWORD()
    _check_status(_lib.FT_CreateDeviceInfoList(_c.byref(NumDevs)))
    return NumDevs.value

def GetDeviceInfoList(NumDevs):
    """Not implemented"""
    raise NotImplementedError()

def GetDeviceInfoDetail(Index=0):
    """Get an entry from the internal device info list. Set update to
    False to avoid a slow call to createDeviceInfoList."""
    Flags = _lib.DWORD()
    Type = _lib.DWORD()
    ID = _lib.DWORD()
    LocId = _lib.DWORD()
    Handle = _lib.FT_HANDLE()
    SerialNumber = _c.c_buffer(_FT.MAX_DESCRIPTION_SIZE)
    Description = _c.c_buffer(_FT.MAX_DESCRIPTION_SIZE)
    _check_status(_lib.FT_GetDeviceInfoDetail(_lib.DWORD(Index), _c.byref(Flags),
            _c.byref(Type), _c.byref(ID), _c.byref(LocId), SerialNumber,
            Description, _c.byref(Handle)))
    return _ret(Index = Index, Flags = Flags.value, Type = Type.value,
            ID = ID.value, Location = LocId.value,
            SerialNumber = SerialNumber.value, Description = Description.value,
            Handle = Handle)

def ListDevices(flags=0):
    """Return a list of serial numbers(default), descriptions or
    locations (Windows only) of the connected FTDI devices depending on value
    of flags"""
    n = _lib.DWORD()
    _check_status(_lib.FT_ListDevices(_c.byref(n), None, _lib.DWORD(_FT.LIST_NUMBER_ONLY)))
    devcount = n.value
    if devcount:
        # since ctypes has no pointer arithmetic.
        bd = [_c.c_buffer(_FT.MAX_DESCRIPTION_SIZE) for i in range(devcount)] +\
            [None]
        # array of pointers to those strings, initially all NULL
        ba = (_c.c_char_p *(devcount + 1))()
        for i in range(devcount):
            ba[i] = _c.cast(bd[i], _c.c_char_p)
        _check_status(_lib.FT_ListDevices(ba, _c.byref(n), _lib.DWORD(_FT.LIST_ALL|flags)))
        return [res for res in ba[:devcount]]
    else:
        return None

def Open(Device=0):
    """Open a Handle to a usb device by index and return an FTD2XX instance for
    it"""
    Handle = _lib.FT_HANDLE()
    _check_status(_lib.FT_Open(Device, _c.byref(Handle)))
    return Handle

def OpenEx(Arg1, Flags):
    """Open a Handle to a usb device by serial number(default), description or
    location(Windows only) depending on value of flags and return an FTD2XX
    instance for it"""
    Handle = _lib.FT_HANDLE()
    _check_status(_lib.FT_OpenEx(_c.create_string_buffer(Arg1), _lib.DWORD(Flags), _c.byref(Handle)))
    return Handle

def Close(Handle):
    """Close the device Handle"""
    _check_status(_lib.FT_Close(Handle))
    return None

def Read(Handle, BytesToRead):
    """Read up to nchars bytes of data from the device. Can return fewer if
    timedout. Use getQueueStatus to find how many bytes are available"""
    Buffer = _c.create_string_buffer(BytesToRead)
    BytesReturned = _lib.DWORD()
    _check_status(_lib.FT_Read(Handle, Buffer, _lib.DWORD(BytesToRead), _c.byref(BytesReturned)))
    return Buffer.raw[0:BytesReturned.value]

def Write(Handle, Buffer, BytesToWrite):
    """Send the data to the device. Data must be a string representing the
    bytes to be sent"""
    BytesWritten = _lib.DWORD()
    _check_status(_lib.FT_Write(Handle, _c.create_string_buffer(Buffer), _lib.DWORD(BytesToWrite), _c.byref(BytesWritten)))
    return BytesWritten.value

def SetBaudRate(Handle, BaudRate):
    """Set the baud rate"""
    _check_status(_lib.FT_SetBaudRate(Handle, _lib.DWORD(BaudRate)))
    return None

def SetDivisor(Handle, Divisor):
    """Set the clock divider. The clock will be set to 6e6/(div + 1)."""
    _check_status(_lib.FT_SetDivisor(Handle, _lib.USHORT(Divisor)))
    return None

def SetDataCharacteristics(Handle, WordLength, StopBits, Parity):
    """Set the data characteristics for UART"""
    _check_status(_lib.FT_SetDataCharacteristics(Handle,
            _lib.UCHAR(WordLength), _lib.UCHAR(StopBits), _lib.UCHAR(Parity)))
    return None

def SetTimeouts(Handle, ReadTimeout, WriteTimeout):
    _check_status(_lib.FT_SetTimeouts(Handle, _lib.DWORD(ReadTimeout),
            _lib.DWORD(WriteTimeout)))
    return None

def SetFlowControl(Handle, FlowControl, Xon, Xoff):
    _check_status(_lib.FT_SetFlowControl(Handle,
            _lib.USHORT(FlowControl), _lib.UCHAR(Xon), _lib.UCHAR(Xoff)))
    return None

def SetDtr(Handle):
    _check_status(_lib.FT_SetDtr(Handle))
    return None

def ClrDtr(Handle):
    _check_status(_lib.FT_ClrDtr(Handle))
    return None

def SetRts(Handle):
    _check_status(_lib.FT_SetRts(Handle))
    return None

def ClrRts(Handle):
    _check_status(_lib.FT_ClrRts(Handle))
    return None

def GetModemStatus(Handle):
    ModemStatus = _lib.DWORD()
    _check_status(_lib.FT_GetModemStatus(Handle, _c.byref(ModemStatus)))
    return ModemStatus.value

def GetQueueStatus(Handle):
    """Get number of bytes in receive queue."""
    AmountInRxQueue = _lib.DWORD()
    _check_status(_lib.FT_GetQueueStatus(Handle, _c.byref(AmountInRxQueue)))
    return AmountInRxQueue.value

def GetDeviceInfo(Handle):
    """Returns a dictionary describing the device. """
    Type = _lib.FT_DEVICE()
    ID = _lib.DWORD()
    Description = _c.create_string_buffer(_FT.MAX_DESCRIPTION_SIZE)
    SerialNumber = _c.create_string_buffer(_FT.MAX_DESCRIPTION_SIZE)
    Dummy = _lib.PVOID()
    _check_status(_lib.FT_GetDeviceInfo(Handle, _c.byref(Type),
            _c.byref(ID), SerialNumber, Description, Dummy))
    return _ret(Type = Type.value, ID = ID.value,
             SerialNumber = SerialNumber.value, Description = Description.value)
    
def GetDriverVersion(Handle):
    DriverVersion = _lib.DWORD()
    _check_status(_lib.FT_GetDriverVersion(Handle, _c.byref(DriverVersion)))
    return DriverVersion.value

def GetLibraryVersion():
    """Return a long representing library version"""
    DLLVersion = _lib.DWORD()
    _check_status(_lib.FT_GetLibraryVersion(_c.byref(DLLVersion)))
    return DLLVersion.value

def GetComPortNumber(Handle):
    """Return a long representing the COM port number"""
    ComPortNumber = _lib.LONG()
    _check_status(_lib.FT_GetComPortNumber(Handle, _c.byref(ComPortNumber)))
    return ComPortNumber.value

def GetStatus(Handle):
    """Return a 3-tuple of rx queue bytes, tx queue bytes and event
    status"""
    AmountInRxQueue = _lib.DWORD()
    AmountInTxQueue = _lib.DWORD()
    EventStatus = _lib.DWORD()
    _check_status(_lib.FT_GetStatus(Handle, _c.byref(AmountInRxQueue),
            _c.byref(AmountInTxQueue), _c.byref(EventStatus)))
    return _ret(AmountInRxQueue = AmountInRxQueue.value, AmountInTxQueue = AmountInTxQueue.value, EventStatus = EventStatus.value)

def SetEventNotification(Handle, EventMask, Arg):
    _check_status(_lib.FT_SetEventNotification(Handle,
            _lib.DWORD(EventMask), _lib.PVOID(Arg)))
    return None

def SetChars(Handle, EventCh, EventChEn, ErrorCh, ErrorChEn):
    _check_status(_lib.FT_SetChars(Handle, _lib.UCHAR(EventCh),
            _lib.UCHAR(EventChEn), _lib.UCHAR(ErrorCh), _lib.UCHAR(ErrorChEn)))
    return None

def SetBreakOn(Handle):
    _check_status(_lib.FT_SetBreakOn(Handle))
    return None

def SetBreakOff(Handle):
    _check_status(_lib.FT_SetBreakOff(Handle))
    return None

def Purge(Handle, Mask):
    _check_status(_lib.FT_Purge(Handle, _lib.DWORD(Mask)))
    return None
    
def ResetDevice(Handle):
    """Reset the device"""
    _check_status(_lib.FT_ResetDevice(Handle))
    return None

def ResetPort(Handle):
    _check_status(_lib.FT_ResetPort(Handle))
    return None

def CyclePort(Handle):
    _check_status(_lib.FT_CyclePort(Handle))
    return None

def Rescan():
    _check_status(_lib.FT_Rescan())
    return None

def Reload(VID, PID):
    _check_status(_lib.FT_Reload(_lib.WORD(VID), _lib.WORD(PID)))
    return None

def SetResetPipeRetryCount(Handle, Count):
    _check_status(_lib.FT_SetResetPipeRetryCount(Handle, _lib.DWORD(Count)))
    return None

def StopInTask(Handle):
    _check_status(_lib.FT_StopInTask(Handle))
    return None

def RestartInTask(Handle):
    _check_status(_lib.FT_RestartInTask(Handle))
    return None

def SetDeadmanTimeout(Handle, DeadmanTimeout):
    _check_status(_lib.FT_SetDeadmanTimeout(Handle, _lib.DWORD(DeadmanTimeout)))
    return None

def IoCtl(Handle):
    """Not implemented"""
    raise NotImplementedError()

def SetWaitMask(Handle, mask):
    """Not implemented"""
    raise NotImplementedError()

def WaitOnMask(Handle):
    """Not implemented"""
    raise NotImplementedError()

def ReadEE():
    """Not implemented"""
    raise NotImplementedError()

def WriteEE():
    """Not implemented"""
    raise NotImplementedError()

def EraseEE():
    """Not implemented"""
    raise NotImplementedError()

def EE_Read():
    """Not implemented"""
    raise NotImplementedError()

def EE_ReadEx():
    """Not implemented"""
    raise NotImplementedError()

def EE_Program():
    """Not implemented"""
    raise NotImplementedError()
    
def EE_ProgramEx():
    """Not implemented"""
    raise NotImplementedError()

def EE_UASize(Handle):
    """Get the EEPROM user area size"""
    Size = _lib.DWORD()
    _check_status(_lib.FT_EE_UASize(Handle, _c.byref(Size)))
    return Size.value

def EE_UARead(Handle, DataLen):
    """Read b_to_read bytes from the EEPROM user area"""
    Data = _c.create_string_buffer(DataLen)
    BytesRead = _lib.DWORD()
    _check_status(_lib.FT_EE_UARead(Handle, Data,
            _lib.DWORD(DataLen), _c.byref(BytesRead)))
    return Data.raw[0:BytesRead.value]

def EE_UAWrite(Handle, Data, DataLen):
    """Write data to the EEPROM user area. data must be a string with
    appropriate byte values"""
    _check_status(_lib.FT_EE_UAWrite(Handle, _c.create_string_buffer(Data), _lib.DWORD(DataLen)))
    return None

def EEPROM_Read():
    """Not implemented"""
    raise NotImplementedError()

def EEPROM_Program():
    """Not implemented"""
    raise NotImplementedError()

def SetLatencyTimer(Handle, Timer):
    _check_status(_lib.FT_SetLatencyTimer(Handle, _lib.UCHAR(Timer)))
    return None

def GetLatencyTimer(Handle):
    Timer = _lib.UCHAR()
    _check_status(_lib.FT_GetLatencyTimer(Handle, _c.byref(Timer)))
    return Timer.value

def SetBitMode(Handle, Mask, Mode):
    _check_status(_lib.FT_SetBitMode(Handle, _lib.UCHAR(Mask),
            _lib.UCHAR(Mode)))
    return None

def GetBitMode(Handle):
    Mode = _lib.UCHAR()
    _check_status(_lib.FT_GetBitMode(Handle, _c.byref(Mode)))
    return Mode.value

def SetUSBParameters(Handle, InTransferSize, OutTransferSize=0):
    _check_status(_lib.FT_SetUSBParameters(Handle, _lib.DWORD(InTransferSize),
            _lib.DWORD(OutTransferSize)))
    return None

