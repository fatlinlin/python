import subprocess
import logging

def setup_log(app_name, loglevel=logging.INFO):
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='./{}.log'.format(app_name),
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(loglevel)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

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
