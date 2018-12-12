#! python3
# Scratch space for PS implementations

# Copyright AGoldfarb on May 2016


import psutil  # pip install psutil
import subprocess


# Not sure how this even works. WMIC ->  Windows Management Instrumentation Command-line.
# Might be able to work remotely (For windows only of course) (/node:COMPUTERNAME /user:USERNAME /pass:PASSWORD.
# http://www.dedoimedo.com/computers/windows-wmic.html

def wmic():
    wmic_cmd = """wmic process where "name='python.exe' or name='pythonw.exe'" get commandline,processid"""
    wmic_prc = subprocess.Popen(wmic_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    wmic_out, wmic_err = wmic_prc.communicate()
    wmic_pythons = [item.rsplit(None, 1) for item in wmic_out.splitlines() if item][1:]
    wmic_pythons = [[cmdline, int(pid)] for [cmdline, pid] in wmic_pythons]


# Needs psutil installed, but is much simpler. (May be slower?)
def ps(process_name=None):

    # pythons = [[" ".join(p.cmdline), p.pid] for p in psutil.process_iter()
    #            if p.name().lower() in ("python.exe", "pythonw.exe")]
    processes = []
    for p in psutil.process_iter():
        if process_name is not None:
            # if p.name().lower() in ("python.exe", "pythonw.exe", "python3.4m.exe"):
            if p.name().lower() in process_name.lower():
                try:
                    processes.append((p.cmdline()))  # , p.pid))
                except psutil.Error:
                    pass
        else:
            try:
                processes.append((p.cmdline()))  # , p.pid))
            except psutil.Error:
                pass

    return processes


def check_process(name, location=None):
    """
    Checks to see if specified process is running.

    :param name:
    :type name: str
    :param location:
    :type location: str | None
    :return: returns number of process found
    :rtype: int
    """
    if location is None or location == 'local':
        processes = ps(name)
        return len(processes)
    else:
        raise NotImplementedError

if __name__ == '__main__':
    py = ps()
    for proccess in py:
        print(proccess)
    # print(py)
    print("")