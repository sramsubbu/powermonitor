import os
import signal
import sys
from pathlib import Path

from daemon import DaemonContext

from powermonitor.monitor import monitor_event_loop

PID_FILE = "/tmp/test.pid"


class DaemonRunner:
    def __init__(self, pid_filepath, main_loop, **main_loop_args):
        self.pid_file = pid_filepath
        self.main_loop = main_loop
        self.main_loop_args = main_loop_args

    def is_daemon_running(self):
        pid = self.get_pid()
        if pid is None:
            return False
        try:
            os.kill(pid, signal.SIG_DFL)
        except ProcessLookupError:
            return False
        return True

    def get_pid(self):
        try:
            with open(self.pid_file) as fp:
                content = fp.read()
        except FileNotFoundError:
            return None
        if content == "":
            return None
        return int(content)

    def start(self, cwd, **daemon_args):
        if self.is_daemon_running():
            print("Process already running")  # noqa: T001
            sys.exit(1)
        daemon = DaemonContext(**daemon_args)
        print("Daemon starting...")  # noqa: T001
        with daemon:
            pid = os.getpid()
            with open(self.pid_file, "w") as fp:
                fp.write(f"{pid}")
            os.chdir(cwd)
            self.main_loop(**self.main_loop_args)

    def stop(self):
        if not self.is_daemon_running():
            print("No process running")  # noqa: T001
            sys.exit(1)
        pid = self.get_pid()
        os.kill(pid, signal.SIGTERM)

    def restart(self, cwd, **daemon_args):
        self.stop()
        self.start(**daemon_args)

    def run(self, cwd, **daemon_args):
        argv = sys.argv
        if len(argv) < 2:
            print("Usage: {progname} start|stop|restart")  # noqa: T001
            sys.exit(1)
        action = argv[1]
        if action == "start":
            self.start(cwd, **daemon_args)
        elif action == "stop":
            self.stop()
        elif action == "restart":
            self.restart(cwd, **daemon_args)
        else:
            print("Usage: {progname} start|stop|restart")  # noqa: T001


if __name__ == "__main__":
    CWD = Path.cwd()
    runner = DaemonRunner(PID_FILE, monitor_event_loop)
    runner.run(CWD)
