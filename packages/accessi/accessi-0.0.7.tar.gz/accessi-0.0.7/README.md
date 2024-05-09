# Siemens Access-i Interface library
Library for Siemens Access-i MR Scanner Interface to integrate and control the MR Scanner. Based on Version 1.1.2 for NX (Access-i Developer Guide)

## Install
This is the easiest way to use the install the library, if you do not need to modify it.
```
pip install accessi
```

## Siemens Documentation
The library is based on this document:
[Access-i Dev Guide NX V1.1.2](documentation/Access-i_Dev_Guide_NX_V1.1.2.pdf)

## Usage guide
A sample test suite (tests.py) has been created which demonstrates basic Access-i usage.  
The tests.py requires Access-i simulator to be running on the background, on the same local computer.  
The tests.py demonstrates most of the implemented methods, as well as receiving images over websocket.  

### Usage examples
Here are some projects which have used this library:
- [Martin Reinok Thesis Software GitHub](https://github.com/martinreinok/master-thesis/tree/master/tracking-software)

## Access-i Licence for real MR at TechMed (Also works with simulator)
```
name="UTwente", 
start_date="20231102", 
warn_date="20251002",
expire_date="20251102", 
system_id="152379",
hash="uTwo2ohlQvMNHhfrzceCRzfRSLYDAw7zqojGjlP%2BCEmqPq1IxUoyx5hOGYbiO%2FEIyiaA4oFHFB2fwTctDbRWew%3D%3D",
informal_name="This name shows up on MR computer"
```
### Connection and IP Addresses
The Access-i in TechMed is running on this IP address:
```
10.89.184.9
Access-i Version: v1
```

Simulator IP:
```
127.0.0.1
Access-i Version: v2
```

In order to connect, the client must have the following networking settings:
```
Client IP: 192.168.182.20 (Maybe something else works too, have not tried)
Subnet: 255.255.255.0
Gateway: 192.168.182.1
DNS1: 192.168.182.1
```
### Multiple network adapters on the same computer
To be able to use both, Access-i and WAN (external interent) at the same time, some configurations are necessary. These are only compatible with Windows for now.

Find out what is the interface number, which is connected to Access-i:
```
route print
```

Using the interface number, create a route:
```
route add 10.89.184.0 mask 255.255.255.0 192.168.182.20 if 8 -p
```
Here __if 8__ is the interface number in this particular case, __-p__ means persistant so it will stay after reboot.

## Collaborating
The majority of Access-i functionality is not yet implemented here, if you need more functionality, any additions are accepted.
