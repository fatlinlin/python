import subprocess
import logging

def setup_log(app_name, loglevel=logging.INFO):
    format = '%(name)-8s %(levelname)-8s %(message)s'
    logfile = './{}.log'.format(app_name)
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s " + format,
                        datefmt='%m-%d %H:%M',
                        filename=logfile,
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(loglevel)
    formatter = logging.Formatter(format)
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logging.info("logging to {}".format(logfile))

def cmd(command, *args, **kwargs):
    log = kwargs.pop("logger", logging.info)
    dry_run = kwargs.pop("dry_run", False)
    log(command)
    if dry_run:
        return
    p = subprocess.Popen(command, *args, shell=True, stdout=subprocess.PIPE, **kwargs) 
    for line in p.stdout:
        log(line.strip())
    p.wait()
    if p.returncode:
        raise subprocess.CalledProcessError(p.returncode, command)
