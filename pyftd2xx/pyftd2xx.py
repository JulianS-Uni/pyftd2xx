"""
Module for accessing functions from FTD2XX in an easier to use
_pythonic_ way. For full documentation please refer to the FTDI
Programming Guide. This module is based on Pablo Bleyers d2xx module,
except this uses ctypes instead of an extension approach.
"""

import sys
if sys.platform == 'win32':
    from . import ftd2xx_win32 as lib 
elif sys.platform.startswith('linux'):
    from . import ftd2xx_linux as lib
elif sys.platform == 'darwin':
    from . import ftd2xx_darwin as lib

import ctypes as c
from . import defines as FT
from munch import Munch as ret


class StatusError(Exception):
    """Exception class for status messages"""
    def __init__(self, error):
        self.message = FT.STATUS[error]

    def __str__(self):
        return self.message
 
def check_status(status):
    """Call an FTDI function and check the status. Raise exception on error"""
    if not FT.SUCCESS(status):
        raise StatusError(status)

def SetVIDPID(VID, PID):
    """Linux only. Set the VID and PID of the device"""
    check_status(lib.FT_SetVIDPID(lib.DWORD(VID), lib.DWORD(PID)))
    return None

def GetVIDPID():
    """Linux only. Get the VID and PID of the device"""
    VID = lib.DWORD()
    PID = lib.DWORD()
    check_status(lib.FT_GetVIDPID(c.byref(VID), c.byref(PID)))
    return ret(VID = VID.value, PID = PID.value)

def CreateDeviceInfoList():
    """Create the internal device info list and return number of entries"""
    NumDevs = lib.DWORD()
    check_status(lib.FT_CreateDeviceInfoList(c.byref(NumDevs)))
    return NumDevs.value

def GetDeviceInfoList():
    """Not implemented"""
    raise NotImplementedError()

def GetDeviceInfoDetail(Index=0):
    """Get an entry from the internal device info list. Set update to
    False to avoid a slow call to createDeviceInfoList."""
    Flags = lib.DWORD()
    Type = lib.DWORD()
    ID = lib.DWORD()
    LocId = lib.DWORD()
    Handle = lib.FT_HANDLE()
    SerialNumber = c.c_buffer(FT.MAX_DESCRIPTION_SIZE)
    Description = c.c_buffer(FT.MAX_DESCRIPTION_SIZE)
    check_status(lib.FT_GetDeviceInfoDetail(lib.DWORD(Index), c.byref(Flags),
            c.byref(Type), c.byref(ID), c.byref(LocId), SerialNumber,
            Description, c.byref(Handle)))
    return ret(Index = Index, Flags = Flags.value, Type = Type.value,
            ID = ID.value, Location = LocId.value,
            SerialNumber = SerialNumber.value, Description = Description.value,
            Handle = Handle)

def ListDevices(flags=0):
    """Return a list of serial numbers(default), descriptions or
    locations (Windows only) of the connected FTDI devices depending on value
    of flags"""
    n = lib.DWORD()
    check_status(lib.FT_ListDevices(c.byref(n), None, lib.DWORD(FT.LIST_NUMBER_ONLY)))
    devcount = n.value
    if devcount:
        # since ctypes has no pointer arithmetic.
        bd = [c.c_buffer(FT.MAX_DESCRIPTION_SIZE) for i in range(devcount)] +\
            [None]
        # array of pointers to those strings, initially all NULL
        ba = (c.c_char_p *(devcount + 1))()
        for i in range(devcount):
            ba[i] = c.cast(bd[i], c.c_char_p)
        check_status(lib.FT_ListDevices(ba, c.byref(n), lib.DWORD(FT.LIST_ALL|flags)))
        return [res for res in ba[:devcount]]
    else:
        return None

def Open(Device=0):
    """Open a Handle to a usb device by index and return an FTD2XX instance for
    it"""
    Handle = lib.FT_HANDLE()
    check_status(lib.FT_Open(Device, c.byref(Handle)))
    return Handle

def OpenEx(Arg1, Flags):
    """Open a Handle to a usb device by serial number(default), description or
    location(Windows only) depending on value of flags and return an FTD2XX
    instance for it"""
    Handle = lib.FT_HANDLE()
    check_status(lib.FT_OpenEx(c.create_string_buffer(Arg1), lib.DWORD(Flags), c.byref(Handle)))
    return Handle

def Close(Handle):
    """Close the device Handle"""
    check_status(lib.FT_Close(Handle))
    return None

def Read(Handle, BytesToRead):
    """Read up to nchars bytes of data from the device. Can return fewer if
    timedout. Use getQueueStatus to find how many bytes are available"""
    Buffer = c.create_string_buffer(BytesToRead)
    BytesReturned = lib.DWORD()
    check_status(lib.FT_Read(Handle, Buffer, lib.DWORD(BytesToRead), c.byref(BytesReturned)))
    return Buffer.raw[0:BytesReturned.value]

def Write(Handle, Buffer, BytesToWrite):
    """Send the data to the device. Data must be a string representing the
    bytes to be sent"""
    BytesWritten = lib.DWORD()
    check_status(lib.FT_Write(Handle, c.create_string_buffer(Buffer), lib.DWORD(BytesToWrite), c.byref(BytesWritten)))
    return BytesWritten.value

def SetBaudRate(Handle, BaudRate):
    """Set the baud rate"""
    check_status(lib.FT_SetBaudRate(Handle, lib.DWORD(BaudRate)))
    return None

def SetDivisor(Handle, Divisor):
    """Set the clock divider. The clock will be set to 6e6/(div + 1)."""
    check_status(lib.FT_SetDivisor(Handle, lib.USHORT(Divisor)))
    return None

def SetDataCharacteristics(Handle, WordLength, StopBits, Parity):
    """Set the data characteristics for UART"""
    check_status(lib.FT_SetDataCharacteristics(Handle,
            lib.UCHAR(WordLength), lib.UCHAR(StopBits), lib.UCHAR(Parity)))
    return None

def SetTimeouts(Handle, ReadTimeout, WriteTimeout):
    check_status(lib.FT_SetTimeouts(Handle, lib.DWORD(ReadTimeout),
            lib.DWORD(WriteTimeout)))
    return None

def SetFlowControl(Handle, FlowControl, Xon, Xoff):
    check_status(lib.FT_SetFlowControl(Handle,
            lib.USHORT(FlowControl), lib.UCHAR(Xon), lib.UCHAR(Xoff)))
    return None

def SetDtr(Handle):
    check_status(lib.FT_SetDtr(Handle))
    return None

def ClrDtr(Handle):
    check_status(lib.FT_ClrDtr(Handle))
    return None

def SetRts(Handle):
    check_status(lib.FT_SetRts(Handle))
    return None

def ClrRts(Handle):
    check_status(lib.FT_ClrRts(Handle))
    return None

def GetModemStatus(Handle):
    ModemStatus = lib.DWORD()
    check_status(lib.FT_GetModemStatus(Handle, c.byref(ModemStatus)))
    return ModemStatus.value

def GetQueueStatus(Handle):
    """Get number of bytes in receive queue."""
    AmountInRxQueue = lib.DWORD()
    check_status(lib.FT_GetQueueStatus(Handle, c.byref(AmountInRxQueue)))
    return AmountInRxQueue.value

def GetDeviceInfo(Handle):
    """Returns a dictionary describing the device. """
    Type = lib.FT_DEVICE()
    ID = lib.DWORD()
    Description = c.create_string_buffer(FT.MAX_DESCRIPTION_SIZE)
    SerialNumber = c.create_string_buffer(FT.MAX_DESCRIPTION_SIZE)
    Dummy = lib.PVOID()
    check_status(lib.FT_GetDeviceInfo(Handle, c.byref(Type),
            c.byref(ID), SerialNumber, Description, Dummy))
    return ret(Type = Type.value, ID = ID.value,
             SerialNumber = SerialNumber.value, Description = Description.value)
    
def GetDriverVersion(Handle):
    DriverVersion = lib.DWORD()
    check_status(lib.FT_GetDriverVersion(Handle, c.byref(DriverVersion)))
    return DriverVersion.value

def GetLibraryVersion():
    """Return a long representing library version"""
    DLLVersion = lib.DWORD()
    check_status(lib.FT_GetLibraryVersion(c.byref(DLLVersion)))
    return DLLVersion.value

def GetComPortNumber(Handle):
    """Return a long representing the COM port number"""
    ComPortNumber = lib.LONG()
    check_status(lib.FT_GetComPortNumber(Handle, c.byref(ComPortNumber)))
    return ComPortNumber.value

def GetStatus(Handle):
    """Return a 3-tuple of rx queue bytes, tx queue bytes and event
    status"""
    AmountInRxQueue = lib.DWORD()
    AmountInTxQueue = lib.DWORD()
    EventStatus = lib.DWORD()
    check_status(lib.FT_GetStatus(Handle, c.byref(AmountInRxQueue),
            c.byref(AmountInTxQueue), c.byref(EventStatus)))
    return ret(AmountInRxQueue = AmountInRxQueue.value, AmountInTxQueue = AmountInTxQueue.value, EventStatus = EventStatus.value)

def SetEventNotification(Handle, EventMask, Arg):
    check_status(lib.FT_SetEventNotification(Handle,
            lib.DWORD(EventMask), lib.PVOID(Arg)))
    return None

def SetChars(Handle, EventCh, EventChEn, ErrorCh, ErrorChEn):
    check_status(lib.FT_SetChars(Handle, lib.UCHAR(EventCh),
            lib.UCHAR(EventChEn), lib.UCHAR(ErrorCh), lib.UCHAR(ErrorChEn)))
    return None

def SetBreakOn(Handle):
    check_status(lib.FT_SetBreakOn(Handle))
    return None

def SetBreakOff(Handle):
    check_status(lib.FT_SetBreakOff(Handle))
    return None

def Purge(Handle, Mask):
    check_status(lib.FT_Purge(Handle, lib.DWORD(Mask)))
    return None
    
def ResetDevice(Handle):
    """Reset the device"""
    check_status(lib.FT_ResetDevice(Handle))
    return None

def ResetPort(Handle):
    check_status(lib.FT_ResetPort(Handle))
    return None

def CyclePort(Handle):
    check_status(lib.FT_CyclePort(Handle))
    return None

def Rescan():
    check_status(lib.FT_Rescan())
    return None

def Reload(VID, PID):
    check_status(lib.FT_Reload(lib.WORD(VID), lib.WORD(PID)))
    return None

def SetResetPipeRetryCount(Handle, Count):
    check_status(lib.FT_SetResetPipeRetryCount(Handle, lib.DWORD(Count)))
    return None

def StopInTask(Handle):
    check_status(lib.FT_StopInTask(Handle))
    return None

def RestartInTask(Handle):
    check_status(lib.FT_RestartInTask(Handle))
    return None

def SetDeadmanTimeout(Handle, DeadmanTimeout):
    check_status(lib.FT_SetDeadmanTimeout(Handle, lib.DWORD(DeadmanTimeout)))
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
    Size = lib.DWORD()
    check_status(lib.FT_EE_UASize(Handle, c.byref(Size)))
    return Size.value

def EE_UARead(Handle, DataLen):
    """Read b_to_read bytes from the EEPROM user area"""
    Data = c.create_string_buffer(DataLen)
    BytesRead = lib.DWORD()
    check_status(lib.FT_EE_UARead(Handle, Data,
            lib.DWORD(DataLen), c.byref(BytesRead)))
    return Data.raw[0:BytesRead.value]

def EE_UAWrite(Handle, Data, DataLen):
    """Write data to the EEPROM user area. data must be a string with
    appropriate byte values"""
    check_status(lib.FT_EE_UAWrite(Handle, c.create_string_buffer(Data), lib.DWORD(DataLen)))
    return None

def EEPROM_Read():
    """Not implemented"""
    raise NotImplementedError()

def EEPROM_Program():
    """Not implemented"""
    raise NotImplementedError()

def SetLatencyTimer(Handle, Timer):
    check_status(lib.FT_SetLatencyTimer(Handle, lib.UCHAR(Timer)))
    return None

def GetLatencyTimer(Handle):
    Timer = lib.UCHAR()
    check_status(lib.FT_GetLatencyTimer(Handle, c.byref(Timer)))
    return Timer.value

def SetBitMode(Handle, Mask, Mode):
    check_status(lib.FT_SetBitMode(Handle, lib.UCHAR(Mask),
            lib.UCHAR(Mode)))
    return None

def GetBitMode(Handle):
    Mode = lib.UCHAR()
    check_status(lib.FT_GetBitMode(Handle, c.byref(Mode)))
    return Mode.value

def SetUSBParameters(Handle, InTransferSize, OutTransferSize=0):
    check_status(lib.FT_SetUSBParameters(Handle, lib.DWORD(InTransferSize),
            lib.DWORD(OutTransferSize)))
    return None

__all__ = ['Close', 'ClrDtr', 'ClrRts', 'CreateDeviceInfoList', 'CyclePort',
'EE_Program', 'EE_ProgramEx', 'EE_Read', 'EE_ReadEx','EE_UARead', 'EE_UASize',
'EE_UAWrite', 'EEPROM_Program', 'EEPROM_Read', 'EraseEE',
'GetBitMode', 'GetComPortNumber', 'GetDeviceInfo', 'GetDeviceInfoDetail',
'GetDeviceInfoList', 'GetDriverVersion', 'GetLatencyTimer', 'GetLibraryVersion',
'GetModemStatus', 'GetQueueStatus', 'GetStatus', 'GetVIDPID', 'IoCtl',
'ListDevices', 'Open', 'OpenEx', 'Purge', 'Read', 'ReadEE', 'Reload', 'Rescan',
'ResetDevice', 'ResetPort', 'RestartInTask', 'SetBaudRate', 'SetBitMode',
'SetBreakOff', 'SetBreakOn', 'SetChars', 'SetDataCharacteristics',
'SetDeadmanTimeout', 'SetDivisor', 'SetDtr', 'SetEventNotification', 'SetFlowControl',
'SetLatencyTimer', 'SetResetPipeRetryCount', 'SetRts', 'SetTimeouts',
'SetUSBParameters', 'SetVIDPID', 'SetWaitMask', 'StopInTask', 'WaitOnMask',
'Write', 'WriteEE']
