import subprocess
import logging

logging.getLogger().setLevel(logging.INFO)


class Process(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None
        self.pid = None

    def start_process(self):
        proc = subprocess.Popen(self.cmd,
                                shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                universal_newlines=True
                                )
        self.process = proc
        self.pid = proc.pid
        logging.info("Launching process {} with pid {}...".format(self.cmd, self.pid))

    def stop_process(self):
        logging.info("Killing process with pid {}...".format(self.pid))
        self.process.kill()
