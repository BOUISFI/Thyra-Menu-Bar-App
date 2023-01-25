import signal
import subprocess
import logging
import time
import os
import re
import psutil
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

    def start(self, timeout=1, expected_output=[]):
        # Compile a regular expression to filter the date/time part of the output
        date_regex = re.compile(r'\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2} ')
        try:
            proc = subprocess.Popen(self.cmd,
                                    shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT,
                                    universal_newlines=True,
                                    )
            self.process = proc
            self.pid = proc.pid
            logging.info("Launching process {} with pid {}...".format(self.cmd, self.pid))

            start_time = time.time()
            line_count = 2
            while time.time() - start_time < timeout and line_count < len(expected_output):
                # Check if stdout is ready to be read
                if proc.stdout :
                    line = proc.stdout.readline()
                    logging.info(line.strip())
                    # Filter the date/time part of the output
                    line = date_regex.sub('', line)
                    if line.strip() == expected_output[line_count]:
                        line_count += 1
                    else:
                        break
            if line_count != len(expected_output):
                logging.info("Outputs are not the same as expected while starting process {}: please update your thyra".format(self.cmd))
            return True
        except Exception as e:
            logging.error("Error while starting process {}: {}".format(self.cmd, e))
            return False

    def stop(self):
        """
        Stops the process.
        """
        try:
            logging.info("killing process {} with pid {}...".format(self.cmd, self.pid))
            # Send the signal to all the process groups (plugins)
            kill_child_processes(self.pid)
            self.process.kill()
        except Exception as e:
            logging.error("Error while stopping process {}: {}".format(self.cmd, e))

    def quit(self):
        """
        Stops the process.
        """
        try:
            logging.info(
                "killing process {} with pid {} as well as its sub-processes, plugins ...".format(self.cmd, self.pid))
            # Send the signal to all the process groups (plugins)
            os.killpg(os.getpgid(self.pid), signal.SIGTERM)
        except Exception as e:
            logging.error("Error while stopping process {}: {}".format(self.cmd, e))


def kill_child_processes(pid):
    parent = psutil.Process(pid)
    for proc in psutil.process_iter():
        if proc.ppid() == parent.pid:
            proc.kill()
