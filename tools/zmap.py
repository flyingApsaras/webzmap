from django.utils import timezone
from webzmap import settings
import os
import sys
import subprocess
import time
import datetime


class ZmapStatus(object):
    def __init__(self):
        self.read_time = None
        self.time_elapsed = 0
        self.time_remaining = 0
        self.percent_complete = 0
        self.active_send_threads = 0
        self.sent_total = 0
        self.hit_rate = 0
        self.sent_last_one_sec = 0
        self.sent_avg_per_sec = 0
        self.recv_success_total = 0
        self.recv_success_last_one_sec = 0
        self.recv_success_avg_per_sec = 0
        self.recv_total = 0
        self.recv_total_last_one_sec = 0
        self.recv_total_avg_per_sec = 0
        self.pcap_drop_total = 0
        self.drop_last_one_sec = 0
        self.drop_avg_per_sec = 0
        self.sendto_fail_total = 0
        self.sendto_fail_last_one_sec = 0
        self.sendto_fail_avg_per_sec = 0


class ShellExecuteError(BaseException):
    def __init__(self, error_msg):
        super(ShellExecuteError, self).__init__(error_msg)


def create_parent_dir(path):
    parent = os.path.dirname(path)
    if not os.path.exists(parent):
        os.makedirs(parent)


def get_last_line(path):
    cmd = "tail -n 1 %s" % path
    p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    return_code = p.wait()
    if return_code == 0:
        return p.stdout.read().strip()
    else:
        raise ShellExecuteError(p.stderr.read())


def get_current_status(status_path):
    """
    real-time,
    time-elapsed,
    time-remaining,
    percent-complete,
    hit-rate,
    active-send-threads,
    sent-total,
    sent-last-one-sec,
    sent-avg-per-sec,
    recv-success-total,
    recv-success-last-one-sec,
    recv-success-avg-per-sec,
    recv-total,
    recv-total-last-one-sec,
    recv-total-avg-per-sec,
    pcap-drop-total,
    drop-last-one-sec,
    drop-avg-per-sec,
    sendto-fail-total,
    sendto-fail-last-one-sec,
    sendto-fail-avg-per-sec
    :param status_path:
    :return:
    """
    try:
        line = get_last_line(status_path)
    except ShellExecuteError:
        return None
    if line.startswith("real-time"):
        return None
    status = ZmapStatus()
    items = line.split(",")
    t = time.strptime(items[0], "%Y-%m-%d %X")
    y, m, d, h, M, s = t[0:6]
    status.read_time = datetime.datetime(y, m, d, h, M, s, tzinfo=timezone.LocalTimezone())
    status.time_elapsed = int(items[1])
    status.time_remaining = int(items[2])
    status.percent_complete = float(items[3])
    status.hit_rate = float(items[4])
    status.active_send_threads = int(items[5])
    status.sent_total = long(items[6])
    status.sent_last_one_sec = int(items[7])
    status.sent_avg_per_sec = int(items[8])
    status.recv_success_total = long(items[9])
    status.recv_success_last_one_sec = int(items[10])
    status.recv_success_avg_per_sec = int(items[11])
    status.recv_total = long(items[12])
    status.recv_total_last_one_sec = int(items[13])
    status.recv_total_avg_per_sec = int(items[14])
    status.pcap_drop_total = long(items[15])
    status.drop_last_one_sec = int(items[16])
    status.drop_avg_per_sec = int(items[17])
    status.sendto_fail_total = long(items[18])
    status.sendto_fail_last_one_sec = int(items[19])
    status.sendto_fail_avg_per_sec = int(items[20])
    return status


class Zmap(object):
    def __init__(self, execute_bin='zmap', verbosity=3, cwd=None, logger=None):
        self.execute_bin = execute_bin
        self.verbosity = verbosity
        self.cwd = cwd
        self.logger = logger

    def run_job(self, job):
        pass

    def scan(self, job, port, subnets=None, output_path=None, log_path=None, bandwidth=2, white_list=None, black_list=None,
             verbosity=None, status_updates_path=None, quiet=False, stdout=None, stderr=None):
        if verbosity:
            self.verbosity = verbosity
        cmd = "%s -p %s" % (self.execute_bin, port)
        # if output_path:
        #     output_path = os.path.join(self.cwd, output_path)
        #     create_parent_dir(output_path)
        #     cmd += ' -o %s' % output_path
        if bandwidth:
            # cmd += " -B %sM" % bandwidth
            cmd += " -r %s" % bandwidth
        if white_list:
            white_list = os.path.join(self.cwd, white_list)
            create_parent_dir(white_list)
            cmd += " -w %s" % white_list
        if black_list:
            black_list = os.path.join(self.cwd, black_list)
            create_parent_dir(black_list)
            cmd += " -b %s" % black_list
        if status_updates_path:
            status_updates_path = os.path.join(self.cwd, status_updates_path)
            create_parent_dir(status_updates_path)
            cmd += " -u %s" % status_updates_path
        if log_path:
            log_path = os.path.join(self.cwd, log_path)
            create_parent_dir(log_path)
            cmd += " -l %s" % log_path
        cmd += ' -v %s' % self.verbosity
        if subnets:
            cmd += ' ' + subnets
        if quiet:
            cmd += ' -q'
        if self.logger:
            self.logger.info("cmd is " + cmd)
        cmd = filter(lambda x: x.strip() != '', cmd.split(" "))
        r, w = os.pipe()
        zmap_pid = subprocess.Popen(cmd, stdout=w, stderr=sys.stderr)
        service = get_service(port)
        zgrab_arg = [settings.zgrab2_path, service]
        zgrab_pid = subprocess.Popen(zgrab_arg, stdin=r, stderr=sys.stderr)
        self.logger.info("cmd is fuck")
        return zmap_pid, zgrab_pid


def get_service(port):
    port_to_service = {
        102: "siemens",
        502: "modbus",
        789: "crimson",
        1911: "fox",
        1962: "pcworx",
        2404: "iec104",
        9600: "omron",
        20000: "dnp3",
        20547: "proconos",
        44818: "ethip",
        47808: "bacnet",
    }
    return port_to_service[port]


if __name__ == '__main__':
    import signal
    zmap = Zmap(logger=None)
    p, q = zmap.scan(
        job="ss",
        subnets='118.25.94.0/24',
        port=80,
        stderr=None,
        stdout=None,
        quiet=False,
        )
    import time
    p_exit_code = p.poll()
    q_exit_code = q.poll()
    while p_exit_code is None:
        print(p.poll())
        if p.poll() == 0:
            q.send_signal(signal.SIGKILL)
            break
        time.sleep(2)

