import os
import sys
import socket
import struct
import queue
import threading
from json import loads
import time
from TDSR_Support import TDSR_radioAPI

__version__ = "1.534"

if os.name == "nt":
    import winreg as compat_winreg

class Radio:
    def __init__(self, gui, messageTypes, interface, interfaceInfo):
        self.TxQueue = queue.Queue()
        # print(interfaceInfo, self.TxQueue)
        self.gui = gui
        self.shutDownThreads = False
        self.RxThread = None
        self.TxThread = None
        self.radioIf = None
        self.messageTypes = messageTypes
        self.messageQueues = {}
        self.interface = interface
        self.interfaceInfo = interfaceInfo
        if interface == 'ip':
            self.status = self.connectIP()


    # Transmits any packets in the TXQueue for radio
    def TxQueueThread(self):
        #If thread is active
        while not self.shutDownThreads:
            # print("TXsize", self.TxQueue.qsize())
            # print(f"size {self.TxQueue.qsize()} for TxThread Queue {self.TxQueue}")
            packet = None
            try:
                packet = self.TxQueue.get(timeout = 0.1)    # if packet in the transmit queue then send it.
                if packet != None:
                    # print("  TXQueueThread Sending:", packet)
                    # if self.gui.appSettings['enableLogging'] == 1:
                    #     self.gui.logFile.logToFile(packet, self.gui.appSettings['reqIP'])
                    self.radioIf.sendPacket(packet)
            except:
                pass

    # Thread to handle messages that are in the input fifo from radio to host
    def RxQueueThread(self):
        while not self.shutDownThreads:
            packet = None
            try:
                packet = self.radioIf.inputFIFO.get(timeout = 0.5)
                if packet != None:
                    packet = packet.decode("utf-8")
                    packet = loads(packet)
                    # print("  RxQueueThread Saw:", packet)
                    msgType = list(packet.keys())[0]
                    msgId = packet[msgType]['msgId']
                    # if msgType == "DATA_INFO":
                    #     print(f"RXQueueThread saw {msgType}")
                    #     print(packet)
                    # if msgType == "RANGE_INFO":
                    #     print(f"RXQueueThread saw {msgType}")
                    #     print(packet)
                    # if "CONFIRM" in msgType:
                    #     print(f"RXQueueThread saw {msgType}")
                    #     print(packet)
                    #     print()
                    #If msgType exists in API message handler (PythonAPI.py), and msgType has a queue registered.
                    if msgType in self.API.messageList.keys():
                        if msgType in self.messageQueues.keys():
                            # print("Pre length", self.messageQueues[msgType].qsize())
                            self.messageQueues[msgType].put(packet)
                            # print("inner", self.messageQueues['RADIO_GET_INFO_CONFIRM'])
                            # print("Post length", self.messageQueues[msgType].qsize())
                            # print(f"Adding to {msgType} Queue")
                            # print("RX Pack:", packet)
                        else:
                            if "CONFIRM" in msgType:
                                # print(packet)
                                self.messageQueues['General_Confirm'].put(packet)
                                # print(time.time())
                                # print(f"RXThread: Adding {msgType} to General_Confirm Queue")
                            else:
                                self.messageQueues['General_Msg'].put(packet)
                                # print(f"RX Thread: Adding {msgType} to General Message Queue")
                    else:
                        print("RX Thread: MessageType not in API keys")
                        print(f"   Type: {msgType}")
                        print(f"   Keys: {self.API.messageList.keys()}")
                        print(f"   Type: {packet}")
                    if self.gui.appSettings['enableLogging'] == 1:
                        self.gui.logFile.logToFile(packet, self.gui.appSettings['reqIP'])
            except:
                pass

    def connectIP(self):
        if self.radioIf != None:
            print("Radio is already connected")
            # return False
        connectPort = 8888
        self.radioIf = radioIfIp(self.interfaceInfo, connectPort)             #  Radio Interface Socket
        status = self.radioIf.connect()   # opens socket and starts read thread for radio to host input FIFO.
        if status == True:
            print("Connected to radio address:", self.interfaceInfo)
            self.API = TDSR_radioAPI.RadioAPI(self.messageQueues, self.messageTypes, self.TxQueue)
            self.connectCommon()
        return status

    def connectMultiCast(self):
        if self.radioIf != None:
            print("Radio is already connected")
            # return False
        connectPort = 8890
        self.radioIf = radioIfIp(self.interfaceInfo, connectPort)             #  Radio Interface Socket
        status = self.radioIf.connect()   # opens socket and starts read thread for radio to host input FIFO.
        if status == True:
            print("Connected to multicast address:", self.interfaceInfo)
            self.API = TDSR_radioAPI.RadioAPI(self.messageQueues, self.messageTypes, self.TxQueue)
            self.connectCommon()
        return status

    def connectUSB(self, usbAddr):
        if self.radioIf != None:
            print("Radio is already connected")
            # return False
        self.radioIf = radioIfUsb(self.interfaceInfo)
        status = self.radioIf.connect(usbAddr)
        if status == True:
            print("Connected to radio address:", self.interfaceInfo)
            self.API = TDSR_radioAPI.RadioAPI(self.messageQueues, self.messageTypes, self.TxQueue)
            self.connectCommon()
        return status

    # def connectUSB(self, usbAddr):
    #     if self.radioIfLocalObj != None:
    #         print("Radio is already connected")
    #         return False
    #     self.radioIfLocalObj = radioIf.radioIfUsb()
    #     result = self.radioIfLocalObj.connect(usbAddr)
    #     if result == False:
    #         return False
    #     self.connectCommon()
    #     return True

    def connectSerial(self, serAddr):
        if self.radioIfLocalObj != None:
            print("Radio is already connected")
            return False
        self.radioIfLocalObj = radioIf.radioIfSerial()
        result = self.radioIfLocalObj.connect(serAddr)
        if result == False:
            return False
        self.connectCommon()
        return True


    # Finishes connection after interface-specific _radioIfObj has been created and connected
    def connectCommon(self):
        # Clear TX queue
        self.TxQueue.queue.clear()
        print(f'Configuring message queues for radio {self.interfaceInfo}')
        self.getStatsConfirm_Queue = queue.Queue()
        self.getInfoConfirm_Queue = queue.Queue()
        self.dataSendConfirm_Queue = queue.Queue()
        self.sendRangeConfirm_Queue = queue.Queue()
        self.getNetworkStatsConfirm_Queue = queue.Queue()
        self.dataInfo_Queue = queue.Queue()
        self.rangeInfo_Queue = queue.Queue()
        self.generalConfirm_Queue = queue.Queue()
        self.generalMsg_Queue = queue.Queue()
        self.messageQueues['RADIO_GET_STATS_CONFIRM'] = self.getStatsConfirm_Queue
        self.messageQueues['RADIO_GET_INFO_CONFIRM'] = self.getInfoConfirm_Queue
        self.messageQueues['RANGE_SEND_RANGE_CONFIRM'] = self.sendRangeConfirm_Queue
        self.messageQueues['DATA_CONFIRM']= self.dataSendConfirm_Queue
        self.messageQueues['NETWORKING_GET_STATS_CONFIRM'] = self.getNetworkStatsConfirm_Queue
        self.messageQueues['DATA_INFO'] = self.dataInfo_Queue
        self.messageQueues['RANGE_INFO'] = self.rangeInfo_Queue
        self.messageQueues['General_Confirm'] = self.generalConfirm_Queue
        self.messageQueues['General_Msg'] = self.generalMsg_Queue
        # Start threads
        self.shutDownThreads = False
        self.TxThread = threading.Thread(target = self.TxQueueThread, name = "TX Thread for %s" % self.interfaceInfo)
        self.RxThread = threading.Thread(target = self.RxQueueThread, name = "RX Thread for %s" % self.interfaceInfo)
        self.TxThread.start()
        self.RxThread.start()


    # Redirects to commands to a remote radio. Must be already connected to a local radio.
    def connectOTA(self, targetNodeId):
        if self.radioIfLocalObj == None:
            print("Local radio must already be connected before connecting OTA")
            return False

        self.radioIfOTAObj = radioIf.radioIfOTA(self.radioIfLocalObj)
        self.radioIfOTAObj.remoteNodeId = targetNodeId

        self.radioIfInUseObj = self.radioIfOTAObj

        return True

    def disconnectOTA(self):
        if self.radioIfOTAObj != None:
            self.radioIfOTAObj = None

        self.radioIfInUseObj = self.radioIfLocalObj

    # Shut down threads and disconnect radio
    def disconnect(self):
        if self.radioIf == None:
            print("Radio is not connected")
            return
        else:
            print(f"Disconnecting Handler for ip {self.interfaceInfo}")
            self.shutDownThreads = True
            self.RxThread.join()
            self.TxThread.join()
            self.RxThread = None
            self.TxThread = None
            self.radioIf.disconnect()
            self.radioIf = None

class RadioError(Exception):
    pass

class radioInterface():
    def __init__(self):
        self.discardInfoMsgs = False
        self.readThread = None
        self.inputFIFO = queue.Queue(maxsize = 100)
        self.shutDown = False

    def __del__(self):
        self.shutDown = True

    def sendPacket(self, payload):
        pass

    def flushInput(self):
        with self.inputFIFO.mutex:
            self.inputFIFO.queue.clear()

    def readThreadFunc(self):  # timeout for thread set lower in this module
        while not self.shutDown:
            # Read packets and add to the FIFO.
            packet = self.readPacketInternal()
            if packet != None:
                # print(packet)
                if len(packet) >= 4:
                    if self.discardInfoMsgs:
                        if packet[0] & 0x03 == 0x02:
                            continue
                    try:
                        if self.inputFIFO.full():
                            # Discard oldest message
                            self.inputFIFO.get_nowait()
                    except:
                        pass
                    try:
                        self.inputFIFO.put(packet, block=False)
                        # print(f"   Stuffing incoming packet for {self.ip} into input FIFO")
                    except:
                        pass

    def readPacketInternal(self):
        return None

    def readPacket(self, msgType=0, timeout=1.0):
        startTime = time.monotonic()

        timedout = False

        while not timedout:
                timeRemaining = (startTime + timeout) - time.monotonic()
                if timeRemaining < 0.0:
                    timedout = True
                    break
                try:
                    packet = self.inputFIFO.get(timeout = timeRemaining)
                except:
                    timedout = True
                    break
                if msgType == 0:
                    # Return packet
                    return packet
                if msgType != 0:
                    # Check first two bytes for message type match
                    if ((msgType >> 8) & 0xff) == packet[0] and (msgType & 0xff) == packet[1]:
                        return packet
                if (time.monotonic() - startTime) >= timeout:
                    timedout = True
        # Timed out
        return None

    def read(self, count):
        pass
    def write(self, data):
        pass
    def setTimeout(self, timeout):
        pass


class radioIfIp(radioInterface):
    # port = 8888

    def __init__(self, ip, connectPort):
        super().__init__()
        self.sock = None
        self.ip = ip
        self.port = connectPort
        # self.sendBuffer = []
        # self.packetBuffer = []

    def connect(self):
        self.disconnect()
        self.shutDown = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(0)
        self.sock.settimeout(0.1)
        payload = '{"RADIO_GET_CONFIG_REQUEST": {"msgId": 1, "configId": 0}}'
        self.sendPacket(payload)
        try:
            packet, addr = self.sock.recvfrom(1500)
                # reaad Thread it to fill input FIFO with incoming traffic
            self.readThread = threading.Thread(target=self.readThreadFunc, name="Radio %s Read Thread" % self.ip)
            self.readThread.start()
            return True
        except socket.timeout:
            print("Unable to connect to radio", self.ip)
            return False

    def disconnect(self):
        self.shutDown = True
        if self.readThread != None:
            self.readThread.join()
            self.readThread = None
        if self.sock != None:
            self.sock.close()
            self.sock = None

    def sendPacket(self, payload):
        # if "GET_STATE" in payload or "SET_STATE" in payload:
        #     print(f'radioConnection: sendPacket sending to {self.ip} \n  Payload: {payload}')
        payload = payload.encode()
        # print(f'radioConnection: sendPacket sending to {self.ip} \n  Payload: {payload}')
        self.sock.sendto(payload, (self.ip, self.port))

    def readPacketInternal(self):
        # print("radioIf readPacketInternal")
        try:
            packet, addr = self.sock.recvfrom(1500)
            # print(f"RadioIF readpacketInternal from: {addr} received: {packet}")
        except socket.timeout:
            return None
        return packet

    def setTimeout(self, timeout):
        old = self.sock.gettimeout()
        self.sock.settimeout(timeout)
        return old

class RadioIfUsb(radioInterface):

    def __init__(self, port):
        # if port supplied, use it
        # if not, query USB
        # else fail
        if (1):  #port == None:
            radios = findUsbRadios()
            if len(radios) > 0:
                if len(radios) == 1:
                    portList = list(radios.values())
                    port = portList[0]
                else:
                    # find matching port
                    if port == "comx":
                        print("Which radio do you want to connect to?")
                        i = 1
                        for r in radios.keys():
                            print("    %d - %s" % (i, r))
                            i += 1
                        c = raw_input()
                        port = radios.values()[int(c) - 1]
        print ("Using", port)
        self.serial = serial.Serial(port, baudrate=4000000,timeout=.05)
        try:
            self.serial.open()
        except serial.SerialException as e:
            sys.stderr.write("Could not open serial port %s: %s\n" % (self.serial.portstr, e))
            sys.exit(1)

    def sendPacket(self, payload):
        lenbytes = struct.pack(">H", len(payload))
        packet = b"".join([bytes(b"\xa5\xa5"), lenbytes, payload])
        #print len(packet)
        self.serial.write(packet)
        """
        try:
            self.serial.write(packet)
        except serial.SerialTimeoutException:
            raise RadioError
        """

    def readPacket(self):
        """build packet from serial port"""
        #print "inWaiting1", self.serial.inWaiting()
        while True:
            data = self.serial.read(1)              # read first, blocking
            if len(data) == 0:
                raise RadioError
            #print "inWaiting2", self.serial.inWaiting()
            if ord(data) != 0xa5:
                continue
            data = self.serial.read(1)              # read second, blocking
            if len(data) == 0:
                raise RadioError
            #print "inWaiting3", self.serial.inWaiting()
            if ord(data) != 0xa5:
                continue
            # next 2 are packet len
            lenStr = self.serial.read(2)
            if len(lenStr) == 0:
                raise RadioError
            #print "inWaiting4", self.serial.inWaiting()
            if PY2:
                length = ord(lenStr[0]) * 256 + ord(lenStr[1])
            elif PY3:
                length = lenStr[0] * 256 + lenStr[1]


            #print length
            packet = self.serial.read(length)
            if len(packet) == 0:
                raise RadioError
            #print "inWaiting5", self.serial.inWaiting()
            if len(packet) < length:
                print ("Short read", len(packet))
            #for i in packet:
                #print ord(i),
            #print "got pkt"
            return packet

    def readPacketNoError(self):
        """build packet from serial port"""
        #print "inWaiting1", self.serial.inWaiting()
        while True:
            data = self.serial.read(1)              # read first, blocking
            if len(data) == 0:
                return []
            #print "inWaiting2", self.serial.inWaiting()
            if ord(data) != 0xa5:
                continue
            data = self.serial.read(1)              # read second, blocking
            if len(data) == 0:
                return []
            #print "inWaiting3", self.serial.inWaiting()
            if ord(data) != 0xa5:
                continue
            # next 2 are packet len
            lenStr = self.serial.read(2)
            if len(lenStr) == 0:
                return []
            #print "inWaiting4", self.serial.inWaiting()
            if PY2:
                length = ord(lenStr[0]) * 256 + ord(lenStr[1])
            elif PY3:
                length = lenStr[0] * 256 + lenStr[1]


            #print length
            packet = self.serial.read(length)
            if len(packet) == 0:
                return []
            #print "inWaiting5", self.serial.inWaiting()
            if len(packet) < length:
                print ("Short read", len(packet))
            #for i in packet:
                #print ord(i),
            #print "got pkt"
            return packet
    def readPacketRaw(self):
        """build packet from serial port"""
        #print "inWaiting1", self.serial.inWaiting()
        while True:
            data = self.serial.read(1)              # read first, blocking
            if len(data) == 0:
                return []
            #print "inWaiting2", self.serial.inWaiting()
            if ord(data) != 0xa5:
                continue
            data = self.serial.read(1)              # read second, blocking
            if len(data) == 0:
                raise RadioError
            #print "inWaiting3", self.serial.inWaiting()
            if ord(data) != 0xa5:
                continue
            # next 2 are packet len
            lenStr = self.serial.read(2)
            if len(lenStr) == 0:
                raise RadioError
            #print "inWaiting4", self.serial.inWaiting()
            if PY2:
                length = ord(lenStr[0]) * 256 + ord(lenStr[1])
            elif PY3:
                length = lenStr[0] * 256 + lenStr[1]


            #print length
            packet = self.serial.read(length)
            if len(packet) == 0:
               return []
            #print "inWaiting5", self.serial.inWaiting()
            if len(packet) < length:
                print ("Short read", len(packet))
            #for i in packet:
                #print ord(i),
            #print "got pkt"
            return packet

    def readPacketNoError(self):
        """build packet from serial port"""
        #print "inWaiting1", self.serial.inWaiting()
        while True:
            data = self.serial.read(1)              # read first, blocking
            if len(data) == 0:
                return []
            #print "inWaiting2", self.serial.inWaiting()
            if ord(data) != 0xa5:
                continue
            data = self.serial.read(1)              # read second, blocking
            if len(data) == 0:
                return []
            #print "inWaiting3", self.serial.inWaiting()
            if ord(data) != 0xa5:
                continue
            # next 2 are packet len
            lenStr = self.serial.read(2)
            if len(lenStr) == 0:
                return []
            #print "inWaiting4", self.serial.inWaiting()
            if PY2:
                length = ord(lenStr[0]) * 256 + ord(lenStr[1])
            elif PY3:
                length = lenStr[0] * 256 + lenStr[1]


            #print length
            packet = self.serial.read(length)
            if len(packet) == 0:
                return []
            #print "inWaiting5", self.serial.inWaiting()
            if len(packet) < length:
                print ("Short read", len(packet))
            #for i in packet:
                #print ord(i),
            #print "got pkt"
            return packet
    def threadRead(self, exitEvent, readQueue):
        while not exitEvent.isSet():
            packet =  self.readPacketNoError()
            if (len(packet) > 0):
                readQueue.put(packet)

    def findUsbRadios():
        # return dict of "nodeId":"com port" pairs
        radios = {}
        if os.name == 'nt':
            k = compat_winreg.OpenKey(compat_winreg.HKEY_LOCAL_MACHINE, r'HARDWARE\DEVICEMAP\SERIALCOMM')
            radioPorts = []
            try:
                i = 0
                while True:
                    val = compat_winreg.EnumValue(k, i)
                    if "USBSER" in val[0]:
                        radioPorts.append(val[1])
                    i += 1
            except WindowsError:
                # WindowsError: [Errno 259] No more data is available
                pass
            compat_winreg.CloseKey(k)
            if radioPorts != []:
                print (radioPorts)
                k = compat_winreg.OpenKey(compat_winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Enum\USB')
                radioIdsByPort = {}
                try:
                    i = 0
                    while True:
                        vidPidStr = compat_winreg.EnumKey(k, i)
                        if "VID_1027" in vidPidStr:
                            #print vidPidStr
                            vidPidKey = compat_winreg.OpenKey(k, vidPidStr)
                            j = 0
                            try:
                                while True:
                                    nodeIdStr = compat_winreg.EnumKey(vidPidKey, j)
                                    nodeIdKey = compat_winreg.OpenKey(vidPidKey, nodeIdStr+r'\Device Parameters')
                                    #print nodeIdStr, _winreg.QueryValueEx(nodeIdKey, 'PortName')[0]
                                    radioIdsByPort[compat_winreg.QueryValueEx(nodeIdKey, 'PortName')[0]] = nodeIdStr
                                    compat_winreg.CloseKey(nodeIdKey)
                                    j += 1
                            except WindowsError:
                                pass
                            compat_winreg.CloseKey(vidPidKey)
                        i += 1
                except WindowsError:
                    # WindowsError: [Errno 259] No more data is available
                    pass
                compat_winreg.CloseKey(k)
            #print radioIdsByPort
            for r in radioPorts:
                #print r, radioIdsByPort[r]
                if r in radioIdsByPort:
                    radios[radioIdsByPort[r]] = r
        else:
            file = os.popen("ls /dev/serial/by-id");
            devs = file.readlines()
            file.close()
            for l in devs:
                if l.find("TDSR") != -1 or l.find("1027") != -1:
                    nodeId = l.rstrip().split("_")[-1].split("-")[0]
                    radios[nodeId] = "/dev/serial/by-id/"+l.rstrip()
        return radios
