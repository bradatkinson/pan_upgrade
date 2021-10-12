#!/usr/bin/env python3
#
#  AUTHOR: Brad Atkinson
#    DATE: 11/7/2020
# PURPOSE: To upgrade PAN firewalls

import sys
import time
import prettytable
from panos import base
import config


def connect_device(fw_ip):
    """Connect To Device

    Args:
        fw_ip (str): A string containing the firewall IP address

    Returns:
        fw_conn (PanDevice): A panos object for device
    """
    username = config.paloalto['username']
    password = config.paloalto['password']
    try:
        fw_conn = base.PanDevice.create_from_device(
            hostname=fw_ip,
            api_username=username,
            api_password=password)
        return fw_conn
    except:
        print('Host was unable to connect to device. Please check '
              'connectivity to device.\n', file=sys.stderr)
        sys.exit(1)


def find_active_device():
    """Find Active Device

    Returns:
        fws_state_dict (dict): A dictionary containing firewall info
    """
    fws_state_dict = {}
    for fw_ip in config.paloalto['firewall_ip']:
        fw_conn = connect_device(fw_ip)
        results = get_system_info(fw_conn)
        hostname = get_hostname(results)
        fws_state_dict[hostname] = {'ip': fw_ip}

    fw_ip1 = config.paloalto['firewall_ip'][0]
    fw_ip2 = config.paloalto['firewall_ip'][1]

    fw1_state = check_ha_cluster_state(fw_ip1, fw_ip2)
    fw2_state = check_ha_cluster_state(fw_ip2, fw_ip1)
    print('-- HA health is good')

    active_tuple = ('active', 'active-primary')
    if fw1_state in active_tuple:
        fws_state_dict = assigning_state(
            fws_state_dict,
            fw_ip1,
            fw_ip2,
            fw1_state,
            fw2_state
        )
    elif fw2_state in active_tuple:
        fws_state_dict = assigning_state(
            fws_state_dict,
            fw_ip2,
            fw_ip1,
            fw2_state,
            fw1_state
        )

    return fws_state_dict


def get_system_info(fw_conn):
    """Get Show System Info

    Args:
        fw_conn (PanDevice): A panos object for device

    Returns:
        results (Element): XML results from firewall
    """
    results = fw_conn.op(cmd='show system info')
    return results


def get_hostname(results):
    """Get Hostname

    Args:
        results (Element): XML results from firewall

    Returns:
        hostname (str): A string containing the hostname
    """
    hostname = results.find('./result/system/hostname').text
    return hostname


def assigning_state(fws_state_dict, fw1_ip, fw2_ip, fw1_state, fw2_state):
    """Assigning HA State

    Args:
        fws_state_dict (dict): A dictionary containing firewall info
        fw1_ip (str): A string containing the firewall IP address
        fw2_ip (str): A string containing the firewall IP address
        fw1_state (str): A string containing the firewall HA state
        fw2_state (str): A string containing the firewall HA state

    Returns:
        fws_state_dict (dict): A dictionary containing firewall info
    """
    key_chain = find_value(fws_state_dict, [fw1_ip])
    fw_state_dict = fws_state_dict.get(key_chain[0])
    fw_state_dict['state'] = fw1_state

    key_chain = find_value(fws_state_dict, [fw2_ip])
    fw_state_dict = fws_state_dict.get(key_chain[0])
    fw_state_dict['state'] = fw2_state

    return fws_state_dict


def find_value(firewalls_dict, find_item):
    """Finds Value in Nested Dictionaries

    Args:
        firewalls_dict (dict): A dictionary of firewall HA information
        find_item (str): The value to find in a dictionary

    Raises:
        KeyError (exception): If the value hasn't been found

    Returns:
        this_key_chain (list): A list of dictionary keys to use to find value
    """
    reverse_linked_q = list()
    reverse_linked_q.append((list(), firewalls_dict))
    while reverse_linked_q:
        this_key_chain, this_value = reverse_linked_q.pop()

        if this_value in find_item:
            return this_key_chain

        try:
            items = this_value.items()
        except AttributeError:
            continue

        for key, value in items:
            reverse_linked_q.append((this_key_chain + [key], value))

    raise KeyError


def check_ha_cluster_state(fw_ip1, fw_ip2):
    """Check HA Cluster State

    Args:
        fw_ip1 (str): A string containing the firewall IP address
        fw_ip2 (str): A string containing the firewall IP address

    Returns:
        fw_state (str): A string containing the firewall HA state
    """
    username = config.paloalto['username']
    password = config.paloalto['password']

    device = base.PanDevice.create_from_device(
        hostname=fw_ip1,
        api_username=username,
        api_password=password)

    device.set_ha_peers(base.PanDevice.create_from_device(
        hostname=fw_ip2,
        api_username=username,
        api_password=password))

    fw_state = device.refresh_ha_active()
    ha_states = ('active', 'passive', 'active-primary', 'active-secondary')

    if fw_state in ha_states:
        return fw_state

    print('-- Get firewall HA state healthy before upgrading, because HA '
          'state is {} for {}.\n'.format(fw_state, fw_ip1), file=sys.stderr)
    sys.exit(1)


def check_current_version(fw_conn):
    """Check Current Version

    Args:
        fw_conn (PanDevice): A panos object for device

    Returns:
        version (str): A string containing the PAN-OS version
    """
    version = fw_conn.refresh_version()
    return version


def check_pending_changes(firewalls_dict):
    """Check Pending Changes

    Args:
        firewalls_dict (dict): A dictionary of firewall HA information
    """
    for hostname in firewalls_dict:
        firewall_dict = firewalls_dict.get(hostname)
        fw_ip = firewall_dict.get('ip')
        fw_conn = connect_device(fw_ip)

        if fw_conn.pending_changes():
            print('-- Pending changes on {}'.format(hostname))
            print('-- Please commit changes and restart script.\n', file=sys.stderr)
            sys.exit(1)
        else:
            print('-- No pending changes on {}'.format(hostname))


def check_ha_status(fw_conn):
    """Check HA Status

    Args:
        fw_conn (PanDevice): A panos object for device

    Returns:
        results (Element): XML results from firewall
    """
    command = ('<show><high-availability><state>'
               '</state></high-availability></show>')
    results = fw_conn.op(cmd=command, cmd_xml=False)
    return results


def process_ha_status(results):
    """Process HA Status

    Args:
        results (Element): XML results from firewall

    Returns:
        ha_status (str): A string containing the HA status
        connection_status (str): A string containing the connection status
    """
    try:
        ha_status = results.find('./result/group/local-info/state').text
        connection_status = results.find('./result/group/peer-info/conn-status').text
    except AttributeError:
        ha_status = 'initial'
        connection_status = 'down'
    return ha_status, connection_status


def check_session_count(fw_conn):
    """Check Session Count

    Args:
        fw_conn (PanDevice): A panos object for device

    Returns:
        results (Element): XML results from firewall
    """
    command = '<show><session><info></info></session></show>'
    results = fw_conn.op(cmd=command, cmd_xml=False)
    return results


def process_session_count(results):
    """Process Session Count

    Args:
        results (Element): XML results from firewall

    Returns:
        session_count (str): A string containing the session count number
    """
    session_count = results.find('./result/num-active').text
    return session_count


def check_config_sync(fw_conn):
    """Check Config Synchronization

    Args:
        fw_conn (PanDevice): A panos object for device
    """
    try:
        if not fw_conn.config_synced():
            print('Synchronizing config with peer...')
            fw_conn.synchronize_config()

            if fw_conn.config_synced():
                sync_state = fw_conn.config_sync_state()
                print('Config is now {}'.format(sync_state))
    except:
        print('Failed to synchronize due to version mismatch, but continuing'
              ' on with upgrade')


def upgrade_device(fw_conn):
    """Upgrade Device

    Args:
        fw_conn (PanDevice): A panos object for device
    """
    print('Upgrading PAN-OS version...')
    print('Note: This step will take some time')
    fw_conn.software.upgrade_to_version(config.version)
    print('-- Upgraded')


def suspend_ha(fw_conn):
    """Suspend HA

    Args:
        fw_conn (PanDevice): A panos object for device

    Returns:
        results (Element): XML results from firewall
    """
    command = ('<request><high-availability><state><suspend>'
               '</suspend></state></high-availability></request>')
    results = fw_conn.op(cmd=command, cmd_xml=False)
    return results


def unsuspend_ha(fw_conn):
    """Unsuspend HA

    Args:
        fw_conn (PanDevice): A panos object for device

    Returns:
        results (Element): XML results from firewall
    """
    command = ('<request><high-availability><state><functional>'
               '</functional></state></high-availability></request>')
    results = fw_conn.op(cmd=command, cmd_xml=False)
    return results


def process_ha_state(results):
    """Process HA State

    Args:
        results (Element): XML results from firewall

    Returns:
        ha_state (str): A string containing the HA state
    """
    ha_state = results.find('./result').text
    return ha_state


def firewall_checks(firewalls_dict, tag='na'):
    """Firewall Checks

    Args:
        firewalls_dict (dict): A dictionary of firewall HA information
        tag (str, optional): A string referencing the stage. Defaults to 'na'.

    Returns:
        ha_state_dict (dict): A dictionary containing hostnames and HA states.
    """
    table = prettytable.PrettyTable(['Hostname',
                                     'PAN-OS',
                                     'HA State',
                                     'HA Connection',
                                     'Session Count'
                                     ])
    ha_state_dict = {}
    for num, hostname in enumerate(firewalls_dict):
        firewall_dict = firewalls_dict.get(hostname)
        fw_ip = firewall_dict.get('ip')
        print('\nConnecting to device {}...'.format(hostname))
        fw_conn = connect_device(fw_ip)
        print('-- Connected')

        print('\nPerforming device checks...')
        print('-- Checking HA status')
        ha_status = 'initial'
        connection_status = 'down'
        while ha_status == 'initial' or connection_status == 'down':
            ha_results = check_ha_status(fw_conn)
            ha_status, connection_status = process_ha_status(ha_results)
            time.sleep(30)

        num = num + 1
        ha_state_dict['device' + str(num)] = {
            'hostname': hostname,
            'state': ha_status
            }

        if tag in ('pre', 'post'):
            print('-- Checking config synchronization')
            check_config_sync(fw_conn)

        print('-- Checking current PAN-OS version')
        version = check_current_version(fw_conn)
        print('-- Checking session counts')
        session_results = check_session_count(fw_conn)
        session_count = process_session_count(session_results)
        table.add_row([hostname,
                       version,
                       ha_status,
                       connection_status,
                       session_count])
    print('\r')
    print(table)
    return ha_state_dict


def perform_upgrade(firewalls_dict, ha_tuple):
    """Perform Upgrade

    Args:
        firewalls_dict (dict): A dictionary of firewall HA information
        ha_tuple (tuple): A tuple of HA states

    Returns:
        fw_ip (str): A string containing the firewall IP address
    """
    key_chain = find_value(firewalls_dict, ha_tuple)
    firewall_dict = firewalls_dict.get(key_chain[0])
    hostname = key_chain[0]

    print('\n\n### UPGRADING -  {} ###'.format(hostname))
    fw_ip = firewall_dict.get('ip')
    fw_conn = connect_device(fw_ip)
    suspend_ha(fw_conn)
    panos_version = check_current_version(fw_conn)

    if panos_version == config.version:
        print('Firewall already at PAN-OS version {}'.format(config.version))
        unsuspend_ha(fw_conn)
    else:
        upgrade_device(fw_conn)

    time.sleep(90)
    return fw_ip


def main():
    """Function Calls
    """
    print('\n### PRE-CHECKS ###')
    print('\nChecking HA Health...')
    firewalls_dict = find_active_device()
    print('\nChecking for pending changes...')
    check_pending_changes(firewalls_dict)
    pre_ha_state_dict = firewall_checks(firewalls_dict, tag='pre')

    passive_tuple = ('passive', 'active-secondary')
    passive_fw_ip = perform_upgrade(firewalls_dict, passive_tuple)

    print('\n\n### INTERIM-CHECKS ###')
    firewall_checks(firewalls_dict)

    active_tuple = ('active', 'active-primary')
    perform_upgrade(firewalls_dict, active_tuple)

    print('\n\n### POST-CHECKS ###')
    post_ha_state_dict = firewall_checks(firewalls_dict, tag='post')

    print('\n\n### SETTING FIREWALLS TO ORIGINAL HA STATE ###')
    pre_device1_ha_state = pre_ha_state_dict['device1'].get('state')
    pre_device2_ha_state = pre_ha_state_dict['device2'].get('state')
    post_device1_ha_state = post_ha_state_dict['device1'].get('state')
    post_device2_ha_state = post_ha_state_dict['device2'].get('state')

    if (post_device1_ha_state != pre_device1_ha_state and
        post_device2_ha_state != pre_device2_ha_state):
        table = prettytable.PrettyTable(['Hostname', 'HA State', 'HA Connection'])
        fw_conn = connect_device(passive_fw_ip)
        print('\nSuspending the active device')
        suspend_ha(fw_conn)
        time.sleep(10)
        print('Making the device functional again')
        unsuspend_ha(fw_conn)
        time.sleep(120)

        for hostname in firewalls_dict:
            firewall_dict = firewalls_dict.get(hostname)
            fw_ip = firewall_dict.get('ip')
            fw_conn = connect_device(fw_ip)

            ha_status = 'initial'
            connection_status = 'down'
            while ha_status == 'initial' or connection_status == 'down':
                ha_results = check_ha_status(fw_conn)
                ha_status, connection_status = process_ha_status(ha_results)
                time.sleep(30)

            table.add_row([hostname, ha_status, connection_status])

        print('\r')
        print(table)

    print('\n')


if __name__ == "__main__":
    main()
