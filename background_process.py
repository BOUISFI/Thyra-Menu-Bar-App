import subprocess
import logging

logging.getLogger().setLevel(logging.INFO)


class Process:
    """
    Args:
        cmd (str): command to run by the process.
    """
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None
        self.pid = None

    def start(self):
        """
        Starts the process.
        """
        try:
            proc = subprocess.Popen(self.cmd,
                                    shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT,
                                    universal_newlines=True
                                    )
            self.process = proc
            self.pid = proc.pid
            logging.info("Launching process {} with pid {}...".format(self.cmd, self.pid))
        except Exception as e:
            logging.error("Error while starting process {}: {}".format(self.cmd, e))

    def stop(self):
        """
        Stops the process.
        """
        try:
            logging.info("Killing process with pid {}...".format(self.pid))
            self.process.kill()
        except Exception as e:
            logging.error("Error while stopping process {}: {}".format(self.cmd, e))
