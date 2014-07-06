import matplotlib.pyplot as plt
import numpy as np
import u3
from time import sleep
from datetime import datetime
import struct
import traceback

plt.ion()           #Turn on interaction mode for faster plotting via draw()

###############################################################################
## U3
# Uncomment these lines to stream from a U3
###############################################################################
# At high frequencies ( >5 kHz), the number of samples will be MAX_REQUESTS
# times 48 (packets per request) times 25 (samples per packet).
#
#   n = MAX_REQUESTS*48*25

d = u3.U3()
d.configU3()
d.getCalibrationData()
d.configIO(FIOAnalog = 2)   #Set the FIO0 to Analog
fs = 5000.0                 #SampleFrequency Hz
T  = 1.0/fs                 #SampleInterval
MAX_REQUESTS = 20           #MAX_REQUESTS is the number of packets to be read.

x = np.linspace(0.0, 2.0, num = 2*fs)     #Initializing x-array
y = np.zeros(2*fs)                        #Initializing y-array
line, = plt.plot(x,y)                     #creating a line to plot
plt.ylim((-2.0,2.0))                       
plt.draw()




print "configuring U3 stream"
d.streamConfig( NumChannels = 1,
                PChannels = [ 0 ],
                NChannels = [ 31 ],
                Resolution = 3,
                ScanFrequency = fs
               )

try:
    print "start stream",
    d.streamStart()
    start = datetime.now()
    print start
    
    missed = 0
    dataCount = 0
    packetCount = 0
    
    for r in d.streamData():
        if r is not None:
            # Our stop condition
            if dataCount >= MAX_REQUESTS:
                break
            
            if r['errors'] != 0:
                print "Error: %s ; " % r['errors'], datetime.now()
            
            if r['numPackets'] != d.packetsPerRequest:
                print "----- UNDERFLOW : %s : " % r['numPackets'], datetime.now()
            
            if r['missed'] != 0:
                missed += r['missed']
                print "+++ Missed ", r['missed']
        
            y1 = np.array(r['AIN0'])        #data pulled from labjack
            r_index = len(y1)               #length of data pulled from labjack
            y = y[r_index:len(x)]           #data shift left, move out old data
            y = np.hstack((y,y1))           #shift in new data from labjack
            line.set_ydata(y)               #update stream data
            plt.draw()
            
            dataCount += 1
            packetCount += r['numPackets']
        
        else:
            # Got no data back from our read.
            # This only happens if your stream isn't faster than the
            # the USB read timeout, ~1 sec.
            print "No data", datetime.now()
except:
    print "".join(i for i in traceback.format_exc())
finally:
    stop = datetime.now()
    d.streamStop()
    print "stream stopped."
    d.close()
    
    sampleTotal = packetCount * d.streamSamplesPerPacket
    
    scanTotal = sampleTotal / 2 #sampleTotal / NumChannels
    print "%s requests with %s packets per request with %s samples per packet = %s samples total." % ( dataCount, (float(packetCount) / dataCount), d.streamSamplesPerPacket, sampleTotal )
    print "%s samples were lost due to errors." % missed
    sampleTotal -= missed
    print "Adjusted number of samples = %s" % sampleTotal
    
    runTime = (stop-start).seconds + float((stop-start).microseconds)/1000000
    print "The experiment took %s seconds." % runTime
    print "Scan Rate : %s scans / %s seconds = %s Hz" % ( scanTotal, runTime, float(scanTotal)/runTime )
    print "Sample Rate : %s samples / %s seconds = %s Hz" % ( sampleTotal, runTime, float(sampleTotal)/runTime )
