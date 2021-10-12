#  AUTHOR: Brad Atkinson
#    DATE: 10/6/2020
# PURPOSE: Configuration file info containing username, password, and IPs

# CONNECTIVITY CONFIGURATIONS
# Update password with the new password entered during management IP
# configuration. Also, update the firewall_ip section with 2 IP addresses
# for a HA cluster.

paloalto = {
    'username': '<USERNAME>',
    'password': '<PASSWORD>',
    'key': '<API_KEY>',
    'firewall_ip': ['<IP_ADDRESS1>', '<IP_ADDRESS2>']
    }

# PAN-OS VERSION
# Update version with the PAN-OS version the firewall is needed to be
# upgraded to.

version = '<PANOS_VERSION>'