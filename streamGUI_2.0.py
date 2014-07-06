import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg

import u3
from time import sleep
from datetime import datetime
import struct
import traceback

# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import Tkinter as Tk

root = Tk.Tk()
root.wm_title("LabJack Streaming GUI")

f = Figure(figsize=(5,4), dpi=80)
a = f.add_subplot(111)
a.set_ylim((-2.0,2.0))
a.set_xlabel("Time (sec)")
a.set_ylabel("Amplitude (V)")

# a tk.DrawingArea
canvas = FigureCanvasTkAgg(f, master=root)
canvas.show()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

#toolbar = NavigationToolbar2TkAgg( canvas, root )
#toolbar.update()
canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

def on_key_event(event):
    print('you pressed %s'%event.key)
    key_press_handler(event, canvas, toolbar)

canvas.mpl_connect('key_press_event', on_key_event)

def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
# Fatal Python Error: PyEval_RestoreThread: NULL tstate


def _start():
    d = u3.U3()
    d.configU3()
    d.getCalibrationData()
    d.configIO(FIOAnalog = 2)      #Set the FIO0 to Analog
    fs = 5000.0                    #SampleFrequency Hz
    T  = 1.0/fs                    #SampleInterval
    MAX_REQUESTS = 40              #MAX_REQUESTS is the number of packets to be read.
    x = np.linspace(0.0, 2.0, num = 2*fs)     #Initializing x-array
    y = np.zeros(2*fs)                        #Initializing y-array
    line, = a.plot(x,y)                       #creating a line to plot
    
    print "configuring U3 stream"
    d.streamConfig( NumChannels = 1,
                   PChannels = [ 0 ],
                   NChannels = [ 31 ],
                   Resolution = 3,
                   ScanFrequency = fs
                   )
#a.plot(t,s)
#canvas.draw()
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
                canvas.draw()
                
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


button = Tk.Button(master=root, text='Quit', command=_quit)
button.pack(side=Tk.BOTTOM)

button2 = Tk.Button(master=root, text='Start', command=_start)
button2.pack(side=Tk.BOTTOM)

Tk.mainloop()