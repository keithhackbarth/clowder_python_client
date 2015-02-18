# Clowder Python Client

This is the python repository for the Clowder python client.

### How to install
```
sudo pip install https://github.com/keithhackbarth/clowder_client/zipball/master
```


### How to test

Basic example for tracking memory usage on server
Create a python file memory_usage.py

```
import clowder
import psutil

clowder.ok({
   'name': 'Memory Utilization',
   'value': psutil.phymem_usage().percent
})
```

Run the file and make sure it works

```
python memory_usage.py
```

Then create a cron job to run every 5 minutes

```
*/5 * * * * python memory_usage.py
```



