# ble_scan_connect.py:
from bluepy.btle import Peripheral, UUID
from bluepy.btle import Scanner, DefaultDelegate
import time

class ScanDelegate(DefaultDelegate): 
    def __init__(self):
        DefaultDelegate.__init__(self)
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
                print ("Discovered device", dev.addr)
        elif isNewData:
            print ("Received new data from", dev.addr)

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(1.0)
n=0
addr = []

myDevice = 0
devices =  sorted(devices, key=lambda x: x.rssi, reverse=True)
number = -1
found = False
MAC = "c5:de:e7:09:1c:10"
for dev in devices:
    if not found:
        print ("%d: Device %s (%s), RSSI=%d dB" % (n, dev.addr, dev.addrType, dev.rssi))
        addr.append(dev.addr)
        n += 1
        for (adtype, desc, value) in dev.getScanData():
            print (" %s = %s" % (desc, value))
            if(desc=="Complete Local Name" and value == "HHHHHHHeartrate"):
                print("\n\n\nACCCCCCCCC\n\n\n")
                number = n
                found = True

if MAC == "":
    print(myDevice)
    print ('Device', number)
    num = int(number)
    print (addr[num])

    print ("Connecting...")
    dev = Peripheral(addr[num], 'random')
    print ("Services...")
else:
    print ("Connecting...")
    dev = Peripheral(MAC, 'random')
    print ("Services...")

for svc in dev.services:
    print (str(svc))
try:
    accService = dev.getServiceByUUID(UUID(0xfff0)) 
    for ch in accService.getCharacteristics():
        print (str(ch))
        if(str(ch)=="Characteristic <Heart Rate Measurement>"):
            print("found")
            ch_acc = ch
        print("properties: "+ ch.propertiesToString())


    if ("READ" in ch_acc.propertiesToString()):
        print("test read")
        while True:
            time.sleep(0.1)
            b_str = ch_acc.read()
            print(b_str)
            b = [0 for i in range(3)]
            for i in range(3):
                b[i] = b_str[i << 1] | (b_str[i << 1 | 1] << 8)
                if b[i] >= 1 << 15:
                    b[i] -= 1 << 16
            print(b)
          
finally:
    dev.disconnect()
