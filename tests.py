import clowder
import datetime
import psutil

clowder.ok({
   'name': 'CPU Percent',
   'value': psutil.cpu_percent(interval=1),
   'frequency': datetime.timedelta(minutes=0.5)
})

clowder.ok({
   'name': 'Memory Utilization',
   'value': psutil.phymem_usage().percent
})
