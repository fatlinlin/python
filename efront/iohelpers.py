import subprocess
import logging

def setup_log(log_base, loglevel=logging.INFO):
    format = '%(name)-8s %(levelname)-8s %(message)s'
    logfile = '{}.log'.format(log_base)
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s " + format,
                        datefmt='%m-%d %H:%M',
                        filename=logfile,
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(loglevel)
    logging.getLogger('').addHandler(console)
    logging.info("logging to {}".format(logfile))

def cmd(command, *args, **kwargs):
    log = kwargs.pop("logger", logging.info)
    dry_run = kwargs.pop("dry_run", False)
    skip_pause = kwargs.pop("skip_pause", False)
    if skip_pause:
        kwargs["stdin"] = subprocess.PIPE
    log(command)
    if dry_run:
        return


    p = subprocess.Popen(command,
                         *args,
                         shell=True,
                         stdout=subprocess.PIPE,
                         **kwargs)
    if skip_pause:
        stdout, stderr = p.communicate(b" ")
    else:
        stdout, stderr = p.communicate()
    for line in stdout.decode("latin-1").split('\n'):
        log(line.strip())
    p.wait()
    if p.returncode:
        raise subprocess.CalledProcessError(p.returncode, command)

def run_script(root, tool):
    logging.info("launching {}".format(tool))
    cmd(
        tool,
        skip_pause=True,
        cwd=root,
        logger=logging.getLogger(tool).debug)
