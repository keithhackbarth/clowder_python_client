# Clowder Python Client

This is the python repository for the Clowder python client.

### How to install
```
sudo pip install https://github.com/keithhackbarth/clowder_client/zipball/master
```


### How to test

Basic example for tracking memory usage on server

```
import clowder
import psutil

clowder.ok({
   'name': 'Memory Utilization',
   'value': psutil.phymem_usage().percent
})
```



