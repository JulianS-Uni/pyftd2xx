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
    """A command to include a custom VID and PID combination within the internal device list table. This will
allow the driver to load for the specified VID and PID combination.

    Args:
        VID (int): Device Vendor ID (VID).
        PID (int): Device Product ID (PID).
        
    Raises:
        StatusError: Gives a FT device error message.
    
    Returns:
        None
    
    Supported Operating System:
        Linux
        Mac OS X (10.4 and later)
    
    Remarks:
        By default, the driver will support a limited set of VID and PID matched devices (VID 0x0403 with PIDs
        0x6001, 0x6010, 0x6006 only).
        In order to use the driver with other VID and PID combinations the SetVIDPID function must be used
        prior to calling ListDevices, Open, OpenEx or CreateDeviceInfoList.
    """
    _check_status(_lib.FT_SetVIDPID(_lib.DWORD(VID), _lib.DWORD(PID)))
    return None

def GetVIDPID():
    """A command to retrieve the current VID and PID combination from within the internal device list table.
    
    Raises:
        StatusError: Gives a FT device error message.
    
    Returns:
        dict: A dict also accecible as a munch.
            VID (int): Device Vendor ID (VID).
            PID (int): Device Product ID (PID).
    
    Supported Operating System:
        Linux
        Mac OS X (10.4 and later)
    
    Remarks:
        See SetVIDPID.
    """
    VID = _lib.DWORD()
    PID = _lib.DWORD()
    _check_status(_lib.FT_GetVIDPID(_c.byref(VID), _c.byref(PID)))
    return _ret(VID = VID.value, PID = PID.value)

def CreateDeviceInfoList():
    """This function builds a device information list and returns the number of D2XX devices connected to the
system. The list contains information about both unopen and open devices.
    
    Raises:
        StatusError: Gives a FT device error message.
    
    Returns:
        int: Number of devices connected.
    
    Supported Operating System:
        Linux
        Mac OS X (10.4 and later)
        Windows (2000 and later)
        Windows CE (4.2 and later)
    
    Remarks:
        An application can use this function to get the number of devices attached to the system. It can then
        allocate space for the device information list and retrieve the list using GetDeviceInfoList or
        GetDeviceInfoDetail GetDeviceInfoDetail.
        If the devices connected to the system change, the device info list will not be updated until
        CreateDeviceInfoList is called again.
    """
    NumDevs = _lib.DWORD()
    _check_status(_lib.FT_CreateDeviceInfoList(_c.byref(NumDevs)))
    return NumDevs.value

def GetDeviceInfoList():
    """This function returns a device information list and the number of D2XX devices in the list.
    
    Raises:
        StatusError: Gives a FT device error message.
    
    Returns:
        list(dict): A list with dicts also accecible as a munch.
                    Flags (list): Lists the properties given by the Flags.
                    Type (str): The device type.
                    ID (int): The device ID.
                    LocId (int): The device location ID.
                    SerialNumber (str): The device serial number.
                    Description (str): The device description.
    
    Supported Operating System:
        (Linux)
        (Mac OS X (10.4 and later))
        Windows (2000 and later)
        (Windows CE (4.2 and later) )
    
    Remarks:
        This function should only be called after calling FT_CreateDeviceInfoList. If the devices connected to the
        system change, the device info list will not be updated until FT_CreateDeviceInfoList is called again.
        Location ID information is not returned for devices that are open when FT_CreateDeviceInfoList is called.
        Information is not available for devices which are open in other processes. In this case, the Flags
        parameter of the FT_DEVICE_LIST_INFO_NODE will indicate that the device is open, but other fields will
        be unpopulated.
        8
        Product Page
        Document Feedback Copyright © Future Technology Devices International Limited
        D2XX Programmer's Guide
        Version 1.4
        Document Reference No.: FT_000071 Clearance No.: FTDI# 170
        The flag value is a 4-byte bit map containing miscellaneous data as defined Appendix A – Type
        Definitions. Bit 0 (least significant bit) of this number indicates if the port is open (1) or closed (0). Bit 1
        indicates if the device is enumerated as a high-speed USB device (2) or a full-speed USB device (0). The
        remaining bits (2 - 31) are reserved.
        The array of FT_DEVICE_LIST_INFO_NODES contains all available data on each device. The structure of
        FT_DEVICE_LIST_INFO_NODES is given in the Appendix. The storage for the list must be allocated by
        the application. The number of devices returned by FT_CreateDeviceInfoList can be used to do this.
        When programming in Visual Basic, LabVIEW or similar languages, FT_GetDeviceInfoDetail may be
        required instead of this function.
        Please note that Linux, Mac OS X and Windows CE do not support location IDs. As such, the Location ID
        parameter in the structure will be empty under these operating systems.
    """
    NumDevs = ListDevices([_FT.LIST_NUMBER_ONLY])
    Dest = (_lib.FT_DEVICE_LIST_INFO_NODE * NumDevs)()
    _check_status(_lib.FT_GetDeviceInfoList(Dest, _lib.DWORD(NumDevs)))
    def getdict(struct):
        ret = _ret()
        ret.Flags = list(_FT.DEVICE_INFO_FLAGS[flag] for flag in _FT.DEVICE_INFO_FLAGS if (struct.Flags & flag) != 0)
        ret.Type = _FT.DEVICES[struct.Type]
        ret.ID = struct.ID
        ret.LocId = struct.LocId
        ret.SerialNumber = struct.SerialNumber.decode('utf-8')
        ret.Description = struct.Description.decode('utf-8')
        return ret
    return list(getdict(i) for i in Dest)

def GetDeviceInfoDetail(Index=0):
    """This function returns an entry from the device information list.
    
    Args:
        Index (int, optional): Index of the entry in the device info list. Defaults to 0.
    
    Raises:
        StatusError: Gives a FT device error message.
    
    Returns:
        dict: A dict also accecible as a munch.
            Flags (list): Lists the properties given by the Flags.
            Type (str): The device type.
            ID (int): The device ID.
            LocId (int): The device location ID.
            SerialNumber (str): The device serial number.
            Description (str): The device description.
            ftHandle (ctypes.c_void_p): Ctypes pointer to the handle of the device.
    
    Supported Operating System:
        (Linux)
        (Mac OS X (10.4 and later))
        Windows (2000 and later)
        (Windows CE (4.2 and later))
    
    Remarks:
        This function should only be called after calling FT_CreateDeviceInfoList. If the devices connected to the
        system change, the device info list will not be updated until FT_CreateDeviceInfoList is called again.
        The index value is zero-based.
        The flag value is a 4-byte bit map containing miscellaneous data as defined Appendix A – Type
        Definitions. Bit 0 (least significant bit) of this number indicates if the port is open (1) or closed (0). Bit 1
        indicates if the device is enumerated as a high-speed USB device (2) or a full-speed USB device (0). The
        remaining bits (2 - 31) are reserved.
        Location ID information is not returned for devices that are open when FT_CreateDeviceInfoList is called.
        Information is not available for devices which are open in other processes. In this case, the lpdwFlags
        parameter will indicate that the device is open, but other fields will be unpopulated.
        To return the whole device info list as an array of FT_DEVICE_LIST_INFO_NODE structures, use
        FT_CreateDeviceInfoList.
        Please note that Linux, Mac OS X and Windows CE do not support location IDs. As such, the Location ID
        parameter in the structure will be empty under these operating systems.
    """
    Flags = _lib.DWORD()
    Type = _lib.FT_DEVICE()
    ID = _lib.DWORD()
    LocId = _lib.DWORD()
    Handle = _lib.FT_HANDLE()
    SerialNumber = _c.create_string_buffer(16)
    Description = _c.create_string_buffer(64)
    _check_status(_lib.FT_GetDeviceInfoDetail(_lib.DWORD(Index), _c.byref(Flags),
            _c.byref(Type), _c.byref(ID), _c.byref(LocId), SerialNumber,
            Description, _c.byref(Handle)))
    Flags = list(_FT.DEVICE_INFO_FLAGS[flag] for flag in _FT.DEVICE_INFO_FLAGS if (Flags.value & flag) != 0)
    return _ret(Index = Index, Flags = Flags, Type = _FT.DEVICES[Type.value],
            ID = ID.value, Location = LocId.value,
            SerialNumber = SerialNumber.value.decode('utf-8'), Description = Description.value.decode('utf-8'),
            Handle = Handle)

def ListDevices(Flags, Arg1=0):
    """Gets information concerning the devices currently connected. This function can return information such
as the number of devices connected, the device serial number and device description strings, and the
location IDs of connected devices.
    
    Args:
        Flags (list): Determines format of returned information. One of FT.LIST_ flags and one of FT.OPEN_BY_ flags.
        Arg1 (int, optional): Only used if Flags contains FT.LIST_BY_INDEX, then it defines the index of the device to get informations from. Defaults to 0.
    
    Raises:
        StatusError: Gives a FT device error message.
    
    Returns:
        int, str, list(str), list(int): Depends on content of Flags.
                                        If FT.LIST_NUMBER_ONLY is set an (int) with the number of connected devices is returned.
                                        If FT.LIST_BY_INDEX is set and FT.OPEN_BY_SERIAL_NUMBER or FT.OPEN_BY_DESCRIPTION is set a (str) describing the SerialNumber or the Description is returned.
                                        If FT.LIST_BY_INDEX is set and FT.OPEN_BY_LOCATION is set an (int) describing the Location is returned.
                                        If FT.LIST_ALL is set and FT.OPEN_BY_SERIAL_NUMBER or FT.OPEN_BY_DESCRIPTION is set a (list) of (str) describing the SerialNumbers or the Descriptions is returned.
                                        If FT.LIST_ALL is set and FT.OPEN_BY_LOCATION is set a (list) of (int) describing the Locations is returned.
                                        
    Supported Operating System:
        (Linux)
        (Mac OS X (10.4 and later))
        Windows (2000 and later)
        (Windows CE (4.2 and later)) 
    
    Remarks:
        This function can be used in a number of ways to return different types of information. A more powerful
        way to get device information is to use the FT_CreateDeviceInfoList, FT_GetDeviceInfoList and
        FT_GetDeviceInfoDetail functions as they return all the available information on devices.
        In its simplest form, it can be used to return the number of devices currently connected. If
        FT_LIST_NUMBER_ONLY bit is set in dwFlags, the parameter pvArg1 is interpreted as a pointer to a
        DWORD location to store the number of devices currently connected.
        It can be used to return device information: if FT_OPEN_BY_SERIAL_NUMBER bit is set in dwFlags, the
        serial number string will
        be returned; if FT_OPEN_BY_DESCRIPTION bit is set in dwFlags, the product description string will be
        returned; if FT_OPEN_BY_LOCATION bit is set in dwFlags, the Location ID will be returned; if none of
        these bits is set, the serial number string will be returned by default.
        It can be used to return device string information for a single device. If FT_LIST_BY_INDEX and
        FT_OPEN_BY_SERIAL_NUMBER or FT_OPEN_BY_DESCRIPTION bits are set in dwFlags, the parameter
        pvArg1 is interpreted as the index of the device, and the parameter pvArg2 is interpreted as a pointer to
        a buffer to contain the appropriate string. Indexes are zero-based, and the error code
        FT_DEVICE_NOT_FOUND is returned for an invalid index.
        It can be used to return device string information for all connected devices. If FT_LIST_ALL and
        FT_OPEN_BY_SERIAL_NUMBER or FT_OPEN_BY_DESCRIPTION bits are set in dwFlags, the parameter
        pvArg1 is interpreted as a pointer to an array of pointers to buffers to contain the appropriate strings and
        the parameter pvArg2 is interpreted as a pointer to a DWORD location to store the number of devices
        currently connected. Note that, for pvArg1, the last entry in the array of pointers to buffers should be a
        NULL pointer so the array will contain one more location than the number of devices connected.
        The location ID of a device is returned if FT_LIST_BY_INDEX and FT_OPEN_BY_LOCATION bits are set in
        dwFlags. In this case the parameter pvArg1 is interpreted as the index of the device, and the parameter
        pvArg2 is interpreted as a pointer to a variable of type long to contain the location ID. Indexes are zerobased, and the error code FT_DEVICE_NOT_FOUND is returned for an invalid index. Please note that
        Windows CE and Linux do not support location IDs.
        The location IDs of all connected devices are returned if FT_LIST_ALL and FT_OPEN_BY_LOCATION bits
        are set in dwFlags. In this case, the parameter pvArg1 is interpreted as a pointer to an array of variables
        of type long to contain the location IDs, and the parameter pvArg2 is interpreted as a pointer to a
        DWORD location to store the number of devices currently connected.
    """
    Flags = _FT.JOIN_FLAGS(Flags)
    if (Flags & _FT.LIST_NUMBER_ONLY) != 0:
        Arg1 = _lib.PVOID()
        Arg2 = _lib.PVOID(None)
        _check_status(_lib.FT_ListDevices(_c.byref(Arg1), _c.byref(Arg2), _lib.DWORD(Flags)))
        return Arg1.value
    elif (Flags & _FT.LIST_BY_INDEX) != 0:
        Arg2 = _c.create_string_buffer(64)
        _check_status(_lib.FT_ListDevices(_lib.PVOID(Arg1), _c.byref(Arg2), _lib.DWORD(Flags)))
        return int.from_bytes(Arg2.value, 'little') if (Flags & _FT.OPEN_BY_LOCATION) != 0 else Arg2.value.decode('utf-8')
    elif (Flags & _FT.LIST_ALL) != 0:
        if (Flags & _FT.OPEN_BY_LOCATION) != 0:
            Arg1 = (_lib.DWORD * ListDevices([_FT.LIST_NUMBER_ONLY]))()
            Arg2 = _lib.PVOID()
            _check_status(_lib.FT_ListDevices(_c.byref(Arg1), _c.byref(Arg2), _lib.DWORD(Flags)))
            ret = list(i for i in Arg1)
        else:
            Arg1 = (_lib.PCHAR * ListDevices([_FT.LIST_NUMBER_ONLY]))()
            for i, _ in enumerate(Arg1):
                Arg1[i] = _c.cast(_c.create_string_buffer(64), _lib.PCHAR)
            Arg2 = _lib.PVOID()
            _check_status(_lib.FT_ListDevices(_c.byref(Arg1), _c.byref(Arg2), _lib.DWORD(Flags)))
            ret = list(i.decode('utf-8') for i in Arg1)
        return ret

def Open(Device=0):
    """Open the device and return a handle which will be used for subsequent accesses.
    
    Args:
        Device (int, optional): Index of the device to open. Indices are 0 based. Defaults to 0.
    
    Raises:
        StatusError: Gives a FT device error message.
    
    Returns:
        ctypes.c_void_p: Ctypes pointer to the handle of the device.
    
    Supported Operating System:
        Linux
        Mac OS X (10.4 and later)
        Windows (2000 and later)
        Windows CE (4.2 and later)
    
    Remarks:
        Although this function can be used to open multiple devices by setting iDevice to 0, 1, 2 etc. there is no
        ability to open a specific device. To open named devices, use the function FT_OpenEx.
    """
    Handle = _lib.FT_HANDLE()
    _check_status(_lib.FT_Open(Device, _c.byref(Handle)))
    return Handle

def OpenEx(Arg1, Flags):
    """Open the specified device and return a handle that will be used for subsequent accesses. The device can
        be specified by its serial number, device description or location.
        This function can also be used to open multiple devices simultaneously. Multiple devices can be specified
        by serial number, device description or location ID (location information derived from the physical
        location of a device on USB). Location IDs for specific USB ports can be obtained using the utility
        USBView and are given in hexadecimal format. Location IDs for devices connected to a system can be
        obtained by calling FT_GetDeviceInfoList or FT_ListDevices with the appropriate flags.

    Args:
        Arg1 (str, int): The SerialNumber (str), Description (str) or Location (int) of the device, depends on the Flags given.
        Flags (int): One of FT.OPEN_BY_SERIAL_NUMBER, FT.OPEN_BY_DESCRIPTION or FT.OPEN_BY_LOCATION.
    
    Raises:
        StatusError: Gives a FT device error message.
    
    Returns:
        ctypes.c_void_p: Ctypes pointer to the handle of the device.
    
    Supported Operating System:
        Linux
        Mac OS X (10.4 and later)
        Windows (2000 and later)
        Windows CE (4.2 and later)
    
    Remarks:
        The parameter specified in pvArg1 depends on dwFlags: if dwFlags is FT_OPEN_BY_SERIAL_NUMBER,
        pvArg1 is interpreted as a pointer to a null-terminated string that represents the serial number of the
        device; if dwFlags is FT_OPEN_BY_DESCRIPTION, pvArg1 is interpreted as a pointer to a nullterminated string that represents the device description; if dwFlags is FT_OPEN_BY_LOCATION, pvArg1
        is interpreted as a long value that contains the location ID of the device. Please note that Windows CE
        and Linux do not support location IDs.
        ftHandle is a pointer to a variable of type FT_HANDLE where the handle is to be stored. This handle must
        be used to access the device.
    """
    if isinstance(Arg1, str):
        Arg1 = Arg1.encode('utf-8')
    Handle = _lib.FT_HANDLE()
    _check_status(_lib.FT_OpenEx(_lib.PCHAR(Arg1), _lib.DWORD(Flags), _c.byref(Handle)))
    return Handle

def Close(Handle):
    """Close an open device.
    
    Args:
        Handle (ctypes.c_void_p): Ctypes pointer to the handle of the device.
  
    Raises:
        StatusError: Gives a FT device error message.
    
    Returns:
        None
    
    Supported Operating System:
        Linux
        Mac OS X (10.4 and later)
        Windows (2000 and later)
        Windows CE (4.2 and later)
    """
    _check_status(_lib.FT_Close(Handle))
    return None

def Read(Handle, BytesToRead):
    """Read data from the device.
    
    Args:
        Handle (ctypes.c_void_p): Ctypes pointer to the handle of the device.
        BytesToRead (int): The number of bytes to read from the device.
    
    Raises:
        StatusError: Gives a FT device error message.
    
    Returns:
        bytes: The bytes read from the device. The lenghts may differ from the BytesToRead because of timeouts.
    
    Supported Operating System:
        Linux
        Mac OS X (10.4 and later)
        Windows (2000 and later)
        Windows CE (4.2 and later)
    """
    Buffer = _c.create_string_buffer(BytesToRead)
    BytesReturned = _lib.DWORD()
    _check_status(_lib.FT_Read(Handle, _c.byref(Buffer), _lib.DWORD(BytesToRead), _c.byref(BytesReturned)))
    return bytes(Buffer.value)

def Write(Handle, Buffer):
    """Write data to the device
    
    Args:
        Handle (ctypes.c_void_p): Ctypes pointer to the handle of the device.
        Buffer (bytes, str): The bytes or string to write to the device.
    
    Raises:
        StatusError: Gives a FT device error message.
    
    Returns:
        int: The number of bytes which where written to the device. May differ from Buffer lenghts because of timeouts.
    
    Supported Operating System:
        Linux
        Mac OS X (10.4 and later)
        Windows (2000 and later)
        Windows CE (4.2 and later)
    """
    if isinstance(Buffer, str):
        Buffer = Buffer.encode('utf-8')
    Buffer = bytes(Buffer)
    BytesToWrite = len(Buffer)
    BytesWritten = _lib.DWORD()
    _check_status(_lib.FT_Write(Handle, _lib.PCHAR(Buffer), _lib.DWORD(BytesToWrite), _c.byref(BytesWritten)))
    return BytesWritten.value

def SetBaudRate(Handle, BaudRate):
    """This function sets the baud rate for the device.
    
    Args:
        Handle (ctypes.c_void_p): Ctypes pointer to the handle of the device.
        BaudRate (int): One of FT.BAUD_300 to FT.BAUD_921600
    
    Raises:
        StatusError: Gives a FT device error message.
    
    Returns:
        None
    
    Supported Operating System:
        Linux
        Mac OS X (10.4 and later)
        Windows (2000 and later)
        Windows CE (4.2 and later)
    """
    _check_status(_lib.FT_SetBaudRate(Handle, _lib.DWORD(BaudRate)))
    return None

def SetDivisor(Handle, Divisor):
    """This function sets the divisor for the device. It is used to set non-standard baud rates.
    When using the FT_SetDivisor, the Baud rate divisor must be calculated using the following formula:
    Integer Divisor + Sub-Integer Divisor = 3000000/Baud Rate where the Integer Divisor is any integer between
    2 and 16384 and the Sub-Integer Divisor can be any one of 0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75 or 0.875.
    Note that the FT8U232AM device will only support Sub-Integer Divisors of 0, 0.125, 0.25 and 0.5.
    
    Args:
        Handle (ctypes.c_void_p): Ctypes pointer to the handle of the device.
        Divisor (float): The divisor used in this formula. Integer Divisor + Sub-Integer Divisor = 3000000/Baud
    
    Raises:
        StatusError: Gives a FT device error message.
    
    Returns:
        None
    
    Supported Operating System:
        Linux
        Mac OS X (10.4 and later)
        Windows (2000 and later)
        Windows CE (4.2 and later) 
    
    Remarks:
        This function is no longer required as FT_SetBaudRate will now automatically calculate the required
        divisor for a requested baud rate. The application note "Setting baud rates for the FT8U232AM" is
        available from the Application Notes section of the FTDI website describes how to calculate the divisor for
        a non-standard baud rate.
        See https://www.ftdichip.com/Support/Knowledgebase/index.html?whatbaudratesareachieveabl.htm
    """
    _check_status(_lib.FT_SetDivisor(Handle, _lib.USHORT(Divisor)))
    return None

def SetDataCharacteristics(Handle, WordLength, StopBits, Parity):
    """Set the data characteristics for UART"""
    _check_status(_lib.FT_SetDataCharacteristics(Handle,
            _lib.UCHAR(WordLength), _lib.UCHAR(StopBits), _lib.UCHAR(Parity)))
    return None

def SetTimeouts(Handle, ReadTimeout, WriteTimeout):
    """This function sets the read and write timeouts for the device.
    Args:
        Handle (ctypes.c_void_p): Ctypes pointer to the handle of the device.
        ReadTimeout (int): Read timeout in milliseconds.
        WriteTimeout (int): Write timeout in milliseconds.
    
    Raises:
        StatusError: Gives a FT device error message.
    
    Returns:
        None
    
    Supported Operating System:
        Linux
        Mac OS X (10.4 and later)
        Windows (2000 and later)
        Windows CE (4.2 and later)
    """
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
    """Get device information for an open device
    
    Args:
        Handle (ctypes.c_void_p): Ctypes pointer to the handle of the device.
    
    Raises:
        StatusError: Gives a FT device error message.
    
    Returns:
        dict: A dict also accecible as a munch.
            Type (str): The device type.
            ID (int): The device ID.
            SerialNumber (str): The device serial number.
            Description (str): The device description.
    
    Supported Operating System:
        Linux
        Mac OS X (10.4 and later)
        Windows (2000 and later)
        Windows CE (4.2 and later) 
    
    Remarks:
        This function is used to return the device type, device ID, device description and serial number.
        The device ID is encoded in a DWORD - the most significant word contains the vendor ID, and the least
        significant word contains the product ID. So the returned ID 0x04036001 corresponds to the device ID
        VID_0403&PID_6001.
    """
    Type = _lib.FT_DEVICE()
    ID = _lib.DWORD()
    Description = _c.create_string_buffer(64)
    SerialNumber = _c.create_string_buffer(16)
    Dummy = _lib.PVOID()
    _check_status(_lib.FT_GetDeviceInfo(Handle, _c.byref(Type), _c.byref(ID), SerialNumber, Description, Dummy))
    return _ret(Type = _FT.DEVICES[Type.value], ID = ID.value,
             SerialNumber = SerialNumber.value.decode('utf-8'), Description = Description.value.decode('utf-8'))
    
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
    """Enables different chip modes.
    
    Args:
        Handle (ctypes.c_void_p): Ctypes pointer to the handle of the device.
        Mask (int): This sets up which Pins are input(0) and output(1). As a bit mask from right (pin 0) to left (pin 16)
        Mode (int): The Mode value. Can be one of FT.BITMODE_
    
    Raises:
        StatusError: Gives a FT device error message.
    
    Returns:
        None
    
    Supported Operating System:
        Linux
        Mac OS X (10.4 and later)
        Windows (2000 and later)
        Windows CE (4.2 and later) 
    
    Remarks:
        For a description of available bit modes for the FT232R, see the application note "Bit Bang Modes for the
        FT232R and FT245R".
        For a description of available bit modes for the FT2232, see the application note "Bit Mode Functions for
        the FT2232".
        For a description of Bit Bang Mode for the FT232B and FT245B, see the application note "FT232B/FT245B
        Bit Bang Mode".
        Application notes are available for download from the FTDI website.
        Note that to use CBUS Bit Bang for the FT232R, the CBUS must be configured for CBUS Bit Bang in the
        EEPROM.
        Note that to use Single Channel Synchronous 245 FIF
    """
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

