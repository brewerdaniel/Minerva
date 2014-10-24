import subprocess
from subprocess import Popen, PIPE
import re


CPUProcess = Popen(["cat","/sys/class/thermal/thermal_zone0/temp"],stdout=subprocess.PIPE)
GPUProcess = Popen(["/opt/vc/bin/vcgencmd","measure_temp"],stdout=subprocess.PIPE)
CPU, err = CPUProcess.communicate()
GPU, err = GPUProcess.communicate()
CPU = float(CPU)
CPU /= 1000
GPU = float(re.findall("\d+.\d+", GPU)[0])

print CPU, GPU
