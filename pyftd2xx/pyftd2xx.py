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
from munch import Munch as M


class StatusError(Exception):
    """Exception class for status messages"""
    def __init__(self, error):
        self.message = FT.STATUS[error]

    def __str__(self):
        return self.message
 
def checkFT(status):
    """Call an FTDI function and check the status. Raise exception on error"""
    if not FT.SUCCESS(status):
        raise StatusError(status)

def getVIDPID():
    """Linux only. Get the VID and PID of the device"""
    vid = lib.DWORD()
    pid = lib.DWORD()
    checkFT(lib.FT_GetVIDPID(c.byref(vid), c.byref(pid)))
    return (vid.value, pid.value)

def setVIDPID(vid, pid):
    """Linux only. Set the VID and PID of the device"""
    checkFT(lib.FT_SetVIDPID(lib.DWORD(vid), lib.DWORD(pid)))
    return None

def createDeviceInfoList():
    """Create the internal device info list and return number of entries"""
    numDevs = lib.DWORD()
    checkFT(lib.FT_CreateDeviceInfoList(c.byref(numDevs)))
    return numDevs.value

def getDeviceInfoList():
    pass

def getDeviceInfoDetail(index=0):
    """Get an entry from the internal device info list. Set update to
    False to avoid a slow call to createDeviceInfoList."""
    flags = lib.DWORD()
    _type = lib.DWORD()
    _id = lib.DWORD()
    locId = lib.DWORD()
    handle = lib.FT_HANDLE()
    serialNumber = c.c_buffer(FT.MAX_DESCRIPTION_SIZE)
    description = c.c_buffer(FT.MAX_DESCRIPTION_SIZE)
    checkFT(lib.FT_GetDeviceInfoDetail(lib.DWORD(index), c.byref(flags),
            c.byref(_type), c.byref(_id), c.byref(locId), serialNumber,
            description, c.byref(handle)))
    return M({'index': index, 'flags': flags.value, 'type': _type.value,
            'id': _id.value, 'location': locId.value,
            'serial': serialNumber.value, 'description': description.value,
            'handle': handle})

def listDevices(flags=0):
    """Return a list of serial numbers(default), descriptions or
    locations (Windows only) of the connected FTDI devices depending on value
    of flags"""
    n = lib.DWORD()
    checkFT(lib.FT_ListDevices(c.byref(n), None, lib.DWORD(FT.LIST_NUMBER_ONLY)))
    devcount = n.value
    if devcount:
        # since ctypes has no pointer arithmetic.
        bd = [c.c_buffer(FT.MAX_DESCRIPTION_SIZE) for i in range(devcount)] +\
            [None]
        # array of pointers to those strings, initially all NULL
        ba = (c.c_char_p *(devcount + 1))()
        for i in range(devcount):
            ba[i] = c.cast(bd[i], c.c_char_p)
        checkFT(lib.FT_ListDevices(ba, c.byref(n), lib.DWORD(FT.LIST_ALL|flags)))
        return [res for res in ba[:devcount]]
    else:
        return None

def open(device=0):
    """Open a handle to a usb device by index and return an FTD2XX instance for
    it"""
    handle = lib.FT_HANDLE()
    checkFT(lib.FT_Open(device, c.byref(handle)))
    return handle

def openEx(arg1, flags=FT.OPEN_BY_SERIAL_NUMBER):
    """Open a handle to a usb device by serial number(default), description or
    location(Windows only) depending on value of flags and return an FTD2XX
    instance for it"""
    handle = lib.FT_HANDLE()
    checkFT(lib.FT_OpenEx(c.create_string_buffer(arg1), lib.DWORD(flags), c.byref(handle)))
    return handle

def close(handle):
    """Close the device handle"""
    checkFT(lib.FT_Close(handle))
    return None

def read(handle, bytesToRead):
    """Read up to nchars bytes of data from the device. Can return fewer if
    timedout. Use getQueueStatus to find how many bytes are available"""
    bytesReturned = lib.DWORD()
    buffer = c.create_string_buffer(bytesToRead)
    checkFT(lib.FT_Read(handle, buffer, bytesToRead, c.byref(bytesReturned)))
    return buffer.raw[:bytesReturned.value]

def write(handle, buffer, bytesToWrite=None):
    """Send the data to the device. Data must be a string representing the
    bytes to be sent"""
    if bytesToWrite is None:
        bytesToWrite = len(buffer)
    bytesWritten = lib.DWORD()
    checkFT(lib.FT_Write(handle, buffer, len(buffer), c.byref(bytesWritten)))
    return bytesWritten.value

def setBaudRate(handle, baudRate):
    """Set the baud rate"""
    checkFT(lib.FT_SetBaudRate(handle, lib.DWORD(baudRate)))
    return None

def setDivisor(handle, divisor):
    """Set the clock divider. The clock will be set to 6e6/(div + 1)."""
    checkFT(lib.FT_SetDivisor(handle, lib.USHORT(divisor)))
    return None

def setDataCharacteristics(handle, wordLength, stopBits, parity):
    """Set the data characteristics for UART"""
    checkFT(lib.FT_SetDataCharacteristics(handle,
            lib.UCHAR(wordLength), lib.UCHAR(stopBits), lib.UCHAR(parity)))
    return None

def setTimeouts(handle, readTimeout, writeTimeout):
    checkFT(lib.FT_SetTimeouts(handle, lib.DWORD(readTimeout),
            lib.DWORD(writeTimeout)))
    return None

def setFlowControl(handle, flowControl, xOn=-1, xOff=-1):
    if flowControl == FT.FLOW_XON_XOFF and (xOn == -1 or xOff == -1):
        raise ValueError
    checkFT(lib.FT_SetFlowControl(handle,
            lib.USHORT(flowControl), lib.UCHAR(xOn), lib.UCHAR(xOff)))
    return None

def setDtr(handle):
    checkFT(lib.FT_SetDtr(handle))
    return None

def clrDtr(handle):
    checkFT(lib.FT_ClrDtr(handle))
    return None

def setRts(handle):
    checkFT(lib.FT_SetRts(handle))
    return None

def clrRts(handle):
    checkFT(lib.FT_ClrRts(handle))
    return None

def getModemStatus(handle):
    modemStatus = lib.DWORD()
    checkFT(lib.FT_GetModemStatus(handle, c.byref(modemStatus)))
    return modemStatus.value

def getQueueStatus(handle):
    """Get number of bytes in receive queue."""
    amountInRxQueue = lib.DWORD()
    checkFT(lib.FT_GetQueueStatus(handle, c.byref(amountInRxQueue)))
    return amountInRxQueue.value

def getDeviceInfo(handle):
    """Returns a dictionary describing the device. """
    type = lib.DWORD()
    id = lib.DWORD()
    description = c.c_buffer(FT.MAX_DESCRIPTION_SIZE)
    serialNumber = c.c_buffer(FT.MAX_DESCRIPTION_SIZE)
    dummy = None

    checkFT(lib.FT_GetDeviceInfo(handle, c.byref(type),
            c.byref(id), serialNumber, description, dummy))
    return M({'type': type.value, 'id': id.value,
            'description': description.value, 'serial': serialNumber.value})
    
def getDriverVersion(handle):
    driverVersion = lib.DWORD()
    checkFT(lib.FT_GetDriverVersion(handle, c.byref(driverVersion)))
    return driverVersion.value

def getLibraryVersion():
    """Return a long representing library version"""
    dllVersion = lib.DWORD()
    checkFT(lib.FT_GetLibraryVersion(c.byref(dllVersion)))
    return dllVersion.value

def getComPortNumber(handle):
    """Return a long representing the COM port number"""
    comPortNumber = lib.LONG()
    checkFT(lib.FT_GetComPortNumber(handle, c.byref(comPortNumber)))
    return comPortNumber.value

def getStatus(handle):
    """Return a 3-tuple of rx queue bytes, tx queue bytes and event
    status"""
    amountInRxQueue = lib.DWORD()
    amountInTxQueue = lib.DWORD()
    eventStatus = lib.DWORD()
    checkFT(lib.FT_GetStatus(handle, c.byref(amountInRxQueue),
            c.byref(amountInTxQueue), c.byref(eventStatus)))
    return (amountInRxQueue.value, amountInTxQueue.value, eventStatus.value)

def setEventNotification(handle, eventMask, arg):
    checkFT(lib.FT_SetEventNotification(handle,
            lib.DWORD(eventMask), lib.HANDLE(arg)))
    return None

def setChars(handle, eventCh, eventChEn, errorCh, errorChEn):
    checkFT(lib.FT_SetChars(handle, lib.UCHAR(eventCh),
            lib.UCHAR(eventChEn), lib.UCHAR(errorCh), lib.UCHAR(errorChEn)))
    return None

def setBreakOn(handle):
    checkFT(lib.FT_SetBreakOn(handle))
    return None

def setBreakOff(handle):
    checkFT(lib.FT_SetBreakOff(handle))
    return None

def purge(handle, mask):
    checkFT(lib.FT_Purge(handle, lib.DWORD(mask)))
    return None
    
def resetDevice(handle):
    """Reset the device"""
    checkFT(lib.FT_ResetDevice(handle))
    return None

def resetPort(handle):
    checkFT(lib.FT_ResetPort(handle))
    return None

def cyclePort(handle):
    checkFT(lib.FT_CyclePort(handle))
    return None

def rescan():
    checkFT(lib.FT_Rescan())
    return None

def reload(vid, pid):
    checkFT(lib.FT_Reload(lib.WORD(vid), lib.WORD(pid)))
    return None

def setResetPipeRetryCount(handle, count):
    checkFT(lib.FT_SetResetPipeRetryCount(handle, lib.DWORD(count)))
    return None

def stopInTask(handle):
    checkFT(lib.FT_StopInTask(handle))
    return None

def restartInTask(handle):
    checkFT(lib.FT_RestartInTask(handle))
    return None

def setDeadmanTimeout(handle, timeout):
    checkFT(lib.FT_SetDeadmanTimeout(handle, lib.DWORD(timeout)))
    return None

def ioCtl(handle):
    """Not implemented"""
    pass

def setWaitMask(handle, mask):
    checkFT(lib.FT_SetWaitMask(handle, lib.DWORD(mask)))
    return None

def waitOnMask(handle):
    mask = lib.DWORD()
    checkFT(lib.FT_WaitOnMask(handle, c.byref(mask)))
    return mask.value

def readEE():
    pass

def writeEE():
    pass

def eraseEE():
    pass

def eeRead(handle):
    """Get the program information from the EEPROM"""
##        if self.devInfo['type'] == 4:
##            version = 1
##        elif self.devInfo['type'] == 5:
##            version = 2
##        else:
##            version = 0
    progdata = lib.ft_program_data(
                    Signature1=0, Signature2=0xffffffff,
                    Version=2,
                    Manufacturer = c.cast(c.c_buffer(256), c.c_char_p),
                    ManufacturerId = c.cast(c.c_buffer(256), c.c_char_p),
                    Description = c.cast(c.c_buffer(256), c.c_char_p),
                    SerialNumber = c.cast(c.c_buffer(256), c.c_char_p))

    checkFT(lib.FT_EE_Read(handle, c.byref(progdata)))
    return progdata

def eeReadEx():
    pass

def eeProgram(handle, progdata=None, *args, **kwds):
    """Program the EEPROM with custom data. If SerialNumber is null, a new
    serial number is generated from ManufacturerId"""
    if progdata is None:
        progdata = lib.ft_program_data(**kwds)
##        if self.devInfo['type'] == 4:
##            version = 1
##        elif self.devInfo['type'] == 5:
##            version = 2
##        else:
##            version = 0
    progdata.Signature1 = lib.DWORD(0)
    progdata.Signature2 = lib.DWORD(0xffffffff)
    progdata.Version = lib.DWORD(2)
    checkFT(lib.FT_EE_Program(handle, progdata))
    return None
    
def eeProgramEx():
    pass

def eeUASize(handle):
    """Get the EEPROM user area size"""
    uasize = lib.DWORD()
    checkFT(lib.FT_EE_UASize(handle, c.byref(uasize)))
    return uasize.value

def eeUARead(handle, b_to_read):
    """Read b_to_read bytes from the EEPROM user area"""
    b_read = lib.DWORD()
    buf = c.c_buffer(b_to_read)
    checkFT(lib.FT_EE_UARead(handle, c.cast(buf, lib.PUCHAR),
            b_to_read, c.byref(b_read)))
    return buf.value[:b_read.value]

def eeUAWrite(handle, data):
    """Write data to the EEPROM user area. data must be a string with
    appropriate byte values"""
    checkFT(lib.FT_EE_UAWrite(handle, c.cast(data, lib.PUCHAR),
            len(data)))
    return None

def eepromRead():
    pass

def eepromProgram():
    pass

def setLatencyTimer(handle, latency):
    checkFT(lib.FT_SetLatencyTimer(handle, lib.UCHAR(latency)))
    return None

def getLatencyTimer(handle):
    latency = lib.UCHAR()
    checkFT(lib.FT_GetLatencyTimer(handle, c.byref(latency)))
    return latency.value

def setBitMode(handle, mask, enable):
    checkFT(lib.FT_SetBitMode(handle, lib.UCHAR(mask),
            lib.UCHAR(enable)))
    return None

def getBitMode(handle):
    mask = lib.UCHAR()
    checkFT(lib.FT_GetBitMode(handle, c.byref(mask)))
    return mask.value

def setUSBParameters(handle, in_tx_size, out_tx_size=0):
    checkFT(lib.FT_SetUSBParameters(handle, lib.ULONG(in_tx_size),
            lib.ULONG(out_tx_size)))
    return None

__all__ = ['close', 'clrDtr', 'clrRts', 'createDeviceInfoList', 'cyclePort',
'eeProgram', 'eeProgramEx', 'eeRead', 'eeReadEx','eeUARead', 'eeUASize',
'eeUAWrite', 'eepromProgram', 'eepromRead', 'eraseEE',
'getBitMode', 'getComPortNumber', 'getDeviceInfo', 'getDeviceInfoDetail',
'getDeviceInfoList', 'getDriverVersion', 'getLatencyTimer', 'getLibraryVersion',
'getModemStatus', 'getQueueStatus', 'getStatus', 'getVIDPID', 'ioCtl',
'listDevices', 'open', 'openEx', 'purge', 'read', 'readEE', 'reload', 'rescan',
'resetDevice', 'resetPort', 'restartInTask', 'setBaudRate', 'setBitMode',
'setBreakOff', 'setBreakOn', 'setChars', 'setDataCharacteristics',
'setDeadmanTimeout', 'setDivisor', 'setDtr', 'setEventNotification', 'setFlowControl',
'setLatencyTimer', 'setResetPipeRetryCount', 'setRts', 'setTimeouts',
'setUSBParameters', 'setVIDPID', 'setWaitMask', 'stopInTask', 'waitOnMask',
'write', 'writeEE']
