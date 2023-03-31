# ble_scan_connect.py:
import time
from bluepy.btle import Peripheral, UUID
from bluepy.btle import Scanner, DefaultDelegate

class ScanDelegate(DefaultDelegate): 
    def __init__(self):
        DefaultDelegate.__init__(self)
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
                print ("Discovered device", dev.addr)
        elif isNewData:
            print ("Received new data from", dev.addr)

def enable_notify(ch):
    setup_data = b"\x01\x00"
    #notify_handle = ch.getHandle() + 2
    notify_handle = ch.getHandle()
    res = dev.writeCharacteristic(notify_handle, setup_data, withResponse=True)
    print(res)

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(1.0)
n=0
addr = []

myDevice = 0
devices =  sorted(devices, key=lambda x: x.rssi, reverse=True)
for dev in devices:
    print ("%d: Device %s (%s), RSSI=%d dB" % (n, dev.addr, dev.addrType, dev.rssi))
    addr.append(dev.addr)
    n += 1
    for (adtype, desc, value) in dev.getScanData():
        print (" %s = %s" % (desc, value))
#        if "Galaxy" in value:
#            myDevice = n - 1
#            print("//////////////////////////////////////////////////////////////////////////////////////////////////////\n\n")

print(myDevice)
number = input('Enter your device number: ')
print ('Device', number)
num = int(number)
print (addr[num])


print ("Connecting...")
dev = Peripheral(addr[num], 'random')
print ("Services...")
for svc in dev.services:
    print (str(svc))
try:
    testService = dev.getServiceByUUID(UUID(0xfff0)) 
    for ch in testService.getCharacteristics():
        print (str(ch))
        print("properties: "+ ch.propertiesToString())
        print('%#x'%ch.getHandle())
    print("===================") 
    ch = dev.getCharacteristics(uuid=UUID(0xfff4))[0] 
    if (ch.supportsRead()):
        print("xxx")
        print (ch.read())
    ch_cccd = ch.getDescriptors(forUUID=0x2902)[0] 
    #print(ch.getDescriptors()[0].uuid)
    #ch_cccd.write(b"\0x01\0x00", True)
    #print(ch_cccd.uuid)
    print(ch_cccd.read())
    print("start notify")
    #enable_notify(ch_cccd)
    while True:
        #time.sleep(0.2)
        if dev.waitForNotifications(100000):
            print("Yes")
        else:
            print("Not Yet")


    if ("NOTIFY" in ch.propertiesToString()):
        print("start notifying")
        enable_notify(ch)
        while True:
            if dev.waitForNotifications(1.0):
                print("notification success")
                #time.sleep(0.2)
            else:
                print("no notification")

finally:
    dev.disconnect()
