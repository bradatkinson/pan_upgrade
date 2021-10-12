```
> docker-compose up
Creating network "pan_upgrade_ap_default" with the default driver
Building python
Step 1/9 : FROM python:3.9-slim
 ---> fdbfbc1456f2
Step 2/9 : LABEL maintainer="Brad Atkinson <brad.scripting@gmail.com>"
 ---> Using cache
 ---> dbb5b1077c1b
Step 3/9 : RUN mkdir /code
 ---> Using cache
 ---> 820a24295945
Step 4/9 : COPY ./requirements.txt /code
 ---> Using cache
 ---> c0a3dc597254
Step 5/9 : WORKDIR /code
 ---> Using cache
 ---> e97b10191a46
Step 6/9 : RUN pip install -r requirements.txt
 ---> Using cache
 ---> 837b7150eadc
Step 7/9 : COPY ./pan_upgrade.py /code
 ---> Using cache
 ---> 515701c286cf
Step 8/9 : COPY ./config.py /code
 ---> c5ac9c294221
Step 9/9 : CMD ["python", "-u", "pan_upgrade.py"]
 ---> Running in e9362dca2d68
Removing intermediate container e9362dca2d68
 ---> e10afbcfc46b

Successfully built e10afbcfc46b
Successfully tagged pan_upgrade_ap_python:latest
WARNING: Image for service python was built because it did not already exist. To rebuild this image you must use `docker-compose build` or `docker-compose up --build`.
Creating pan_upgrade_ap ... done
Attaching to pan_upgrade_ap
pan_upgrade_ap |
pan_upgrade_ap | ### PRE-CHECKS ###
pan_upgrade_ap |
pan_upgrade_ap | Checking HA Health...
pan_upgrade_ap | -- HA health is good
pan_upgrade_ap |
pan_upgrade_ap | Checking for pending changes...
pan_upgrade_ap | -- No pending changes on FW-AP-02P
pan_upgrade_ap | -- No pending changes on FW-AP-02S
pan_upgrade_ap |
pan_upgrade_ap | Connecting to device FW-AP-02P...
pan_upgrade_ap | -- Connected
pan_upgrade_ap |
pan_upgrade_ap | Performing device checks...
pan_upgrade_ap | -- Checking HA status
pan_upgrade_ap | -- Checking config synchronization
pan_upgrade_ap | -- Checking current PAN-OS version
pan_upgrade_ap | -- Checking session counts
pan_upgrade_ap |
pan_upgrade_ap | Connecting to device FW-AP-02S...
pan_upgrade_ap | -- Connected
pan_upgrade_ap |
pan_upgrade_ap | Performing device checks...
pan_upgrade_ap | -- Checking HA status
pan_upgrade_ap | -- Checking config synchronization
pan_upgrade_ap | -- Checking current PAN-OS version
pan_upgrade_ap | -- Checking session counts
pan_upgrade_ap |
pan_upgrade_ap | +-----------+--------+----------+---------------+---------------+
pan_upgrade_ap | | Hostname  | PAN-OS | HA State | HA Connection | Session Count |
pan_upgrade_ap | +-----------+--------+----------+---------------+---------------+
pan_upgrade_ap | | FW-AP-02P | 9.0.12 | passive  |       up      |       0       |
pan_upgrade_ap | | FW-AP-02S | 9.0.12 |  active  |       up      |       0       |
pan_upgrade_ap | +-----------+--------+----------+---------------+---------------+
pan_upgrade_ap |
pan_upgrade_ap |
pan_upgrade_ap | ### UPGRADING -  FW-AP-02P ###
pan_upgrade_ap | Upgrading PAN-OS version...
pan_upgrade_ap | Note: This step will take some time
pan_upgrade_ap | -- Upgraded
pan_upgrade_ap |
pan_upgrade_ap |
pan_upgrade_ap | ### INTERIM-CHECKS ###
pan_upgrade_ap |
pan_upgrade_ap | Connecting to device FW-AP-02P...
pan_upgrade_ap | -- Connected
pan_upgrade_ap |
pan_upgrade_ap | Performing device checks...
pan_upgrade_ap | -- Checking HA status
pan_upgrade_ap | -- Checking current PAN-OS version
pan_upgrade_ap | -- Checking session counts
pan_upgrade_ap |
pan_upgrade_ap | Connecting to device FW-AP-02S...
pan_upgrade_ap | -- Connected
pan_upgrade_ap |
pan_upgrade_ap | Performing device checks...
pan_upgrade_ap | -- Checking HA status
pan_upgrade_ap | -- Checking current PAN-OS version
pan_upgrade_ap | -- Checking session counts
pan_upgrade_ap |
pan_upgrade_ap | +-----------+--------+----------+---------------+---------------+
pan_upgrade_ap | | Hostname  | PAN-OS | HA State | HA Connection | Session Count |
pan_upgrade_ap | +-----------+--------+----------+---------------+---------------+
pan_upgrade_ap | | FW-AP-02P | 9.1.7  | passive  |       up      |       0       |
pan_upgrade_ap | | FW-AP-02S | 9.0.12 |  active  |       up      |       0       |
pan_upgrade_ap | +-----------+--------+----------+---------------+---------------+
pan_upgrade_ap |
pan_upgrade_ap |
pan_upgrade_ap | ### UPGRADING -  FW-AP-02S ###
pan_upgrade_ap | Upgrading PAN-OS version...
pan_upgrade_ap | Note: This step will take some time
pan_upgrade_ap | -- Upgraded
pan_upgrade_ap |
pan_upgrade_ap |
pan_upgrade_ap | ### POST-CHECKS ###
pan_upgrade_ap |
pan_upgrade_ap | Connecting to device FW-AP-02P...
pan_upgrade_ap | -- Connected
pan_upgrade_ap |
pan_upgrade_ap | Performing device checks...
pan_upgrade_ap | -- Checking HA status
pan_upgrade_ap | -- Checking config synchronization
pan_upgrade_ap | Synchronizing config with peer...
pan_upgrade_ap | Config is now synchronized
pan_upgrade_ap | -- Checking current PAN-OS version
pan_upgrade_ap | -- Checking session counts
pan_upgrade_ap |
pan_upgrade_ap | Connecting to device FW-AP-02S...
pan_upgrade_ap | -- Connected
pan_upgrade_ap |
pan_upgrade_ap | Performing device checks...
pan_upgrade_ap | -- Checking HA status
pan_upgrade_ap | -- Checking config synchronization
pan_upgrade_ap | -- Checking current PAN-OS version
pan_upgrade_ap | -- Checking session counts
pan_upgrade_ap |
pan_upgrade_ap | +-----------+--------+----------+---------------+---------------+
pan_upgrade_ap | | Hostname  | PAN-OS | HA State | HA Connection | Session Count |
pan_upgrade_ap | +-----------+--------+----------+---------------+---------------+
pan_upgrade_ap | | FW-AP-02P | 9.1.7  |  active  |       up      |       0       |
pan_upgrade_ap | | FW-AP-02S | 9.1.7  | passive  |       up      |       0       |
pan_upgrade_ap | +-----------+--------+----------+---------------+---------------+
pan_upgrade_ap |
pan_upgrade_ap |
pan_upgrade_ap | ### SETTING FIREWALLS TO ORIGINAL HA STATE ###
pan_upgrade_ap |
pan_upgrade_ap | Suspending the active device
pan_upgrade_ap | Making the device functional again
pan_upgrade_ap |
pan_upgrade_ap | +-----------+----------+---------------+
pan_upgrade_ap | | Hostname  | HA State | HA Connection |
pan_upgrade_ap | +-----------+----------+---------------+
pan_upgrade_ap | | FW-AP-02P | passive  |       up      |
pan_upgrade_ap | | FW-AP-02S |  active  |       up      |
pan_upgrade_ap | +-----------+----------+---------------+
pan_upgrade_ap |
pan_upgrade_ap |
pan_upgrade_ap exited with code 0

Total time for upgrade: 1h 2m 17s


> docker-compose down --rmi all

Removing pan_upgrade_ap ... done
Removing network pan_upgrade_ap_default
Removing image pan_upgrade_ap_python
```