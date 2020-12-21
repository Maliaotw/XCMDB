

from .base import BasePlugin
import socket
from socket import AF_INET, SOCK_STREAM, SOCK_DGRAM
import psutil

AD = "-"
AF_INET6 = getattr(socket, 'AF_INET6', object())
proto_map = {
    (AF_INET, SOCK_STREAM): 'tcp',
    (AF_INET6, SOCK_STREAM): 'tcp6',
    (AF_INET, SOCK_DGRAM): 'udp',
    (AF_INET6, SOCK_DGRAM): 'udp6',
}




class NetPlugin(BasePlugin):

    def windows(self):
        pass

    def linux(self):
        ret = []
        proc_names = {}
        for p in psutil.process_iter(attrs=['pid', 'name']):
            proc_names[p.info['pid']] = p.info['name']
        for c in psutil.net_connections(kind='inet'):
            if c.status == 'LISTEN':

                laddr = "%s:%s" % (c.laddr)
                data = {
                    'proto':proto_map[(c.family, c.type)],
                    'port':laddr.split(':')[-1],
                    'pid': c.pid or AD,
                    'name':proc_names.get(c.pid, '?')[:15]

                }
                ret.append(data)
                # print(data)


        return ret




