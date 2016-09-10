import os
from docker import Client

def cname_to_host(name):
    """
    Translates container's name into hostname for host machine

    Change this function, if you want to apply your own hostname
    constuction rules.
    """
    return name + ".docker"

def update_hosts(ip, hostname, *, add_new=False):
    """
    Removes from /etc/hosts all the lines, denotes to `ip` or `hostname`.
    If add_new is set, new host rule for `ip` and `hostname` will be appended
    to the file.
    """
    hosts = '/etc/hosts'

    # We read the lines...
    with open(hosts, 'r') as f:
        lines = [l for l in f]

    # ...and write them again, with filtering.
    with open(hosts, 'w') as f:
        for line in lines:
            if line.startswith(ip + ' '):
                continue
            if line.endswith(' ' + hostname):
                continue
            f.write(line)
        if add_new:
            f.write("{} {}\n".format(ip, hostname))

def on_start(name, ip):
    """
    React to start of a container.
    name is the container's name, ip is its ip.
    """
    update_hosts(ip, cname_to_host(name), add_new=True)

def on_kill(name, ip):
    """
    React to kill of a container.
    name is the container's name, ip is its ip.
    """
    update_hosts(ip, cname_to_host(name))

def process_event(e):
    """
    Process docker event.
    """

    # Only process container events
    if e['Type'] != 'container':
        return

    status = e['status']
    # Only process containers starts and stops
    if status not in ['start', 'kill']:
        return

    cid = e['id']
    inspect = c.inspect_container(cid)

    # Retreive container's name
    name = inspect['Name'][1:]

    # Retreive it's ip, either from global network settings, or from
    # settings of a single network.
    netset = inspect['NetworkSettings']
    ip = netset['IPAddress']

    if not ip:
        nets = netset['Networks']
        ips = [net['IPAddress'] for net in nets.values()]
        ip = ips[0]

    if not ip:
        return

    # Do the work
    if status == 'start':
        on_start(name, ip)
    elif status == 'kill':
        on_kill(name, ip)


if __name__ == '__main__':
    c = Client()
    for e in c.events(decode=True):
        process_event(e)
