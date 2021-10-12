```
> docker-compose up
Creating network "pan_upgrade_aa_default" with the default driver
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
 ---> c0a3dc597254
Step 5/9 : WORKDIR /code
 ---> Running in 31cedcafc150
Removing intermediate container 31cedcafc150
 ---> e97b10191a46
Step 6/9 : RUN pip install -r requirements.txt
 ---> Running in 8aa7953a15a9
Collecting pan-os-python
  Downloading pan_os_python-1.0.2-py2.py3-none-any.whl (122 kB)
Collecting pandevice
  Downloading pandevice-0.14.0.tar.gz (151 kB)
Collecting prettytable
  Downloading prettytable-2.0.0-py3-none-any.whl (22 kB)
Requirement already satisfied: setuptools in /usr/local/lib/python3.9/site-packages (from prettytable->-r requirements.txt (line 3)) (51.0.0)
Collecting pan-python<0.17.0,>=0.16.0
  Downloading pan_python-0.16.0-py2.py3-none-any.whl (59 kB)
Collecting wcwidth
  Downloading wcwidth-0.2.5-py2.py3-none-any.whl (30 kB)
Building wheels for collected packages: pandevice
  Building wheel for pandevice (setup.py): started
  Building wheel for pandevice (setup.py): finished with status 'done'
  Created wheel for pandevice: filename=pandevice-0.14.0-py2.py3-none-any.whl size=116090 sha256=210281c77feb6043445679088a9943c5fa2fe75c014fc0b92a814e64799b0131
  Stored in directory: /root/.cache/pip/wheels/21/7f/b6/45523566899aa5fa9074462925231a6970281bed6f76e5a981
Successfully built pandevice
Installing collected packages: wcwidth, pan-python, prettytable, pandevice, pan-os-python
Successfully installed pan-os-python-1.0.2 pan-python-0.16.0 pandevice-0.14.0 prettytable-2.0.0 wcwidth-0.2.5
WARNING: You are using pip version 20.3.1; however, version 21.0.1 is available.
You should consider upgrading via the '/usr/local/bin/python -m pip install --upgrade pip' command.
Removing intermediate container 8aa7953a15a9
 ---> 837b7150eadc
Step 7/9 : COPY ./pan_upgrade.py /code
 ---> 515701c286cf
Step 8/9 : COPY ./config.py /code
 ---> 1e14efa7c220
Step 9/9 : CMD ["python", "-u", "pan_upgrade.py"]
 ---> Running in 7250adcb5f29
Removing intermediate container 7250adcb5f29
 ---> f4324163ae3d

Successfully built f4324163ae3d
Successfully tagged pan_upgrade_aa_python:latest
WARNING: Image for service python was built because it did not already exist. To rebuild this image you must use `docker-compose build` or `docker-compose up --build`.
Creating pan_upgrade_aa ... done
Attaching to pan_upgrade_aa
pan_upgrade_aa |
pan_upgrade_aa | ### PRE-CHECKS ###
pan_upgrade_aa |
pan_upgrade_aa | Checking HA Health...
pan_upgrade_aa | -- HA health is good
pan_upgrade_aa |
pan_upgrade_aa | Checking for pending changes...
pan_upgrade_aa | -- No pending changes on FW-AA-01P
pan_upgrade_aa | -- No pending changes on FW-AA-01S
pan_upgrade_aa |
pan_upgrade_aa | Connecting to device FW-AA-01P...
pan_upgrade_aa | -- Connected
pan_upgrade_aa |
pan_upgrade_aa | Performing device checks...
pan_upgrade_aa | -- Checking HA status
pan_upgrade_aa | -- Checking config synchronization
pan_upgrade_aa | -- Checking current PAN-OS version
pan_upgrade_aa | -- Checking session counts
pan_upgrade_aa |
pan_upgrade_aa | Connecting to device FW-AA-01S...
pan_upgrade_aa | -- Connected
pan_upgrade_aa |
pan_upgrade_aa | Performing device checks...
pan_upgrade_aa | -- Checking HA status
pan_upgrade_aa | -- Checking config synchronization
pan_upgrade_aa | -- Checking current PAN-OS version
pan_upgrade_aa | -- Checking session counts
pan_upgrade_aa |
pan_upgrade_aa | +-----------+--------+------------------+---------------+---------------+
pan_upgrade_aa | | Hostname  | PAN-OS |     HA State     | HA Connection | Session Count |
pan_upgrade_aa | +-----------+--------+------------------+---------------+---------------+
pan_upgrade_aa | | FW-AA-01P | 9.0.12 |  active-primary  |       up      |       0       |
pan_upgrade_aa | | FW-AA-01S | 9.0.12 | active-secondary |       up      |       0       |
pan_upgrade_aa | +-----------+--------+------------------+---------------+---------------+
pan_upgrade_aa |
pan_upgrade_aa |
pan_upgrade_aa | ### UPGRADING -  FW-AA-01S ###
pan_upgrade_aa | Upgrading PAN-OS version...
pan_upgrade_aa | Note: This step will take some time
pan_upgrade_aa | -- Upgraded
pan_upgrade_aa |
pan_upgrade_aa |
pan_upgrade_aa | ### INTERIM-CHECKS ###
pan_upgrade_aa |
pan_upgrade_aa | Connecting to device FW-AA-01P...
pan_upgrade_aa | -- Connected
pan_upgrade_aa |
pan_upgrade_aa | Performing device checks...
pan_upgrade_aa | -- Checking HA status
pan_upgrade_aa | -- Checking current PAN-OS version
pan_upgrade_aa | -- Checking session counts
pan_upgrade_aa |
pan_upgrade_aa | Connecting to device FW-AA-01S...
pan_upgrade_aa | -- Connected
pan_upgrade_aa |
pan_upgrade_aa | Performing device checks...
pan_upgrade_aa | -- Checking HA status
pan_upgrade_aa | -- Checking current PAN-OS version
pan_upgrade_aa | -- Checking session counts
pan_upgrade_aa |
pan_upgrade_aa | +-----------+--------+------------------+---------------+---------------+
pan_upgrade_aa | | Hostname  | PAN-OS |     HA State     | HA Connection | Session Count |
pan_upgrade_aa | +-----------+--------+------------------+---------------+---------------+
pan_upgrade_aa | | FW-AA-01P | 9.0.12 |  active-primary  |       up      |       1       |
pan_upgrade_aa | | FW-AA-01S | 9.1.7  | active-secondary |       up      |       0       |
pan_upgrade_aa | +-----------+--------+------------------+---------------+---------------+
pan_upgrade_aa |
pan_upgrade_aa |
pan_upgrade_aa | ### UPGRADING -  FW-AA-01P ###
pan_upgrade_aa | Upgrading PAN-OS version...
pan_upgrade_aa | Note: This step will take some time
pan_upgrade_aa | -- Upgraded
pan_upgrade_aa |
pan_upgrade_aa |
pan_upgrade_aa | ### POST-CHECKS ###
pan_upgrade_aa |
pan_upgrade_aa | Connecting to device FW-AA-01P...
pan_upgrade_aa | -- Connected
pan_upgrade_aa |
pan_upgrade_aa | Performing device checks...
pan_upgrade_aa | -- Checking HA status
pan_upgrade_aa | -- Checking config synchronization
pan_upgrade_aa | -- Checking current PAN-OS version
pan_upgrade_aa | -- Checking session counts
pan_upgrade_aa |
pan_upgrade_aa | Connecting to device FW-AA-01S...
pan_upgrade_aa | -- Connected
pan_upgrade_aa |
pan_upgrade_aa | Performing device checks...
pan_upgrade_aa | -- Checking HA status
pan_upgrade_aa | -- Checking config synchronization
pan_upgrade_aa | -- Checking current PAN-OS version
pan_upgrade_aa | -- Checking session counts
pan_upgrade_aa |
pan_upgrade_aa | +-----------+--------+------------------+---------------+---------------+
pan_upgrade_aa | | Hostname  | PAN-OS |     HA State     | HA Connection | Session Count |
pan_upgrade_aa | +-----------+--------+------------------+---------------+---------------+
pan_upgrade_aa | | FW-AA-01P | 9.1.7  | active-secondary |       up      |       0       |
pan_upgrade_aa | | FW-AA-01S | 9.1.7  |  active-primary  |       up      |       0       |
pan_upgrade_aa | +-----------+--------+------------------+---------------+---------------+
pan_upgrade_aa |
pan_upgrade_aa |
pan_upgrade_aa | ### SETTING FIREWALLS TO ORIGINAL HA STATE ###
pan_upgrade_aa |
pan_upgrade_aa | Suspending the active device
pan_upgrade_aa | Making the device functional again
pan_upgrade_aa |
pan_upgrade_aa | +-----------+------------------+---------------+
pan_upgrade_aa | | Hostname  |     HA State     | HA Connection |
pan_upgrade_aa | +-----------+------------------+---------------+
pan_upgrade_aa | | FW-AA-01P |  active-primary  |       up      |
pan_upgrade_aa | | FW-AA-01S | active-secondary |       up      |
pan_upgrade_aa | +-----------+------------------+---------------+
pan_upgrade_aa |
pan_upgrade_aa |
pan_upgrade_aa exited with code 0

Total time for upgrade: 1h 1m 38s


> docker-compose down --rmi all

Removing pan_upgrade_aa ... done
Removing network pan_upgrade_aa_default
Removing image pan_upgrade_aa_python
```