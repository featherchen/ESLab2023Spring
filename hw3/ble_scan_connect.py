# ble_scan_connect.py:
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
    print("===================") 
    print("test 0xfff4")
    ch = dev.getCharacteristics(uuid=UUID(0xfff4))[0] 
    if (ch.supportsRead()):
        print("test read")
        print (ch.read())
        print("read AC")
    ch_cccd = ch.getDescriptors(forUUID=0x2902)[0] 
    #print(ch.getDescriptors()[0].uuid)
    #ch_cccd.write(b"\0x01\0x00", True)
    #print(ch_cccd.uuid)
    #dev.writeCharacteristic(ch_cccd.handle, bytes([1,0]), withResponse=True)
    #print(ch_cccd.read())
    if ("WRITE" in ch.propertiesToString()):
        print("test write")
        ch.write(b"a", withResponse=True)
        if (ch.read()==b'a'):
            print("write AC")
        else:
            print("write WA")

    if ("INDICATE" in ch.propertiesToString()):
        dev.writeCharacteristic(ch_cccd.handle, bytes([2,0]), withResponse=True)
        print(ch_cccd.read())
        print("test indicate")
        while True:
            if dev.waitForNotifications(10):
                print("indicate AC")  
                break
            print("not receive data")
            break

    if ("NOTIFY" in ch.propertiesToString()):
        dev.writeCharacteristic(ch_cccd.handle, bytes([1,0]), withResponse=True)
        print(ch_cccd.read())
        print("test notify")
        while True:
            if dev.waitForNotifications(10):
                print("notify AC")
                break
            print("not receive data")
            break
finally:
    dev.disconnect()
