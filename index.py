import json
from flask import Flask, render_template, jsonify
import datetime
import psutil
import time
app = Flask(__name__)

@app.route("/")
def index():
   return render_template('index.html')

@app.route("/configuration")
def configuration():
   return render_template('configuration.html')

@app.route("/bios")
def bios():
   return render_template('bios.html')   

@app.route("/roms")
def roms():
   return render_template('roms.html')      

@app.route("/logs")
def logs():
   return render_template('logs.html')   

@app.route("/monitoring")
def monitoring():
   now = datetime.datetime.now()
   timeString = now.strftime("%Y-%m-%d %H:%M")
   templateData = {
      'diskio' : get_diskio_info(),
      'netio' : get_netio_info(),
      'system': get_system_info(),
      'time': timeString,
      'temp': get_cpu_temp(),
      'cpus': get_cpu_infos(),
      'memory': get_memory_infos(),
      'fs': get_filesystem_infos()
      }
   return render_template('monitoring.html', **templateData)

@app.route("/api/monitoring/cpus", methods=['GET'])
def serve_api_monitoring_cpus():
   return jsonify(get_cpu_infos())

@app.route("/api/monitoring/temp", methods=['GET'])
def serve_api_monitoring_temp():
   return jsonify(get_cpu_temp())   

@app.route("/api/monitoring/memory", methods=['GET'])
def serve_api_monitoring_memory():
   return jsonify(get_memory_infos()) 

@app.route("/api/monitoring/network", methods=['GET'])
def serve_api_monitoring_network():
   return jsonify(get_netio_info())    

@app.route("/api/monitoring/system", methods=['GET'])
def serve_api_monitoring_system():
   return jsonify(get_system_info())  

@app.route("/api/monitoring/fs", methods=['GET'])
def serve_api_monitoring_filesystem():
   return jsonify({
      'fs' : get_filesystem_infos(),
      'di' : get_diskio_info()
   })

def get_filesystem_infos():
   context = []

   for disk_part in psutil.disk_partitions():
         usage = psutil.disk_usage(disk_part.mountpoint)
         context.append({
            'device': disk_part.device,
            'mountpoint': disk_part.mountpoint,
            'fstype': disk_part.fstype,
            'total': usage.total,
            'free': usage.free,
            'used_bytes': usage.used,
            'used_percent': usage.percent,
         })
   
   return context

def get_diskio_info():
   return psutil.disk_io_counters()

def get_netio_info():
   return psutil.net_io_counters()   

def get_system_info():
   now = datetime.datetime.now()
   timeString = now.strftime("%Y-%m-%d %H:%M")   
   return {
      'boot_time': str(datetime.timedelta(seconds= time.time() - psutil.boot_time())),  # pylint: disable=no-member
      'time': timeString
   }

def get_memory_infos():
   return {
      'virtual_memory': psutil.virtual_memory(),
      'swap_memory': psutil.swap_memory(),
      'cpu_count': psutil.cpu_count(),
      'cpu_stats': psutil.cpu_stats(),         
   }

def get_cpu_infos():
   return {
         'count': psutil.cpu_count(),
         'usage': psutil.cpu_percent(interval=0.5, percpu=True),
   }

def get_cpu_temp():
   return psutil.sensors_temperatures()['cpu_thermal'][0][1]

@app.template_filter()
def numberFormat(value):
    return format(int(value), ',d')

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8888, debug=True)