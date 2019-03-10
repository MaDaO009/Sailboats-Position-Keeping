
import time
import globalvar as gl
import threading
import reader
import plot_data

b=0
flag=False
t1 = threading.Thread(target= reader.run)
t1.setDaemon(True)
t1.start()
my_plot=plot_data.plot()
my_plot.plot()
