

from .base import BasePlugin
import psutil

class ProcPlugin(BasePlugin):

    def windows(self):
        pass

    def linux(self):

        ret = []
        for i in psutil.pids():
            p = psutil.Process(pid=i)

            exe = p.exe()
            if exe:
                if '/' in exe:
                    exe = exe.split('/')[-1]

                data = {
                    'name':exe,
                    'status':p.status(),
                    'username':p.username(),
                    'create_time':p.create_time(),
                    'pid':p.pid,
                    'cmdline':' '.join(p.cmdline())
                }
                ret.append(data)

        return ret




