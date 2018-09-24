import os
import re
import pwd
import signal
import shlex
import asyncio
from tornado import web
from jupyterhub.spawner import Spawner
from jupyterhub.utils import random_port
from traitlets import (Integer, Unicode)


async def execute(user, host, cmd):
    fmt = 'runuser -u {user} -- {ssh} {user}@{host} \" env -i bash --norc --noprofile -c \' {cmd} \' \" '
    cmd = fmt.format(ssh='ssh -o StrictHostKeyChecking=no -o PasswordAuthentication=no',
                    user=user, host=host, cmd=cmd)
    proc = await asyncio.create_subprocess_exec(*shlex.split(cmd),
                                                stdout=asyncio.subprocess.PIPE,
                                                stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    return proc.returncode, stdout.decode(), stderr.decode()


class SSHSpawner(Spawner):
    pid = Integer(0)
    hostname = Unicode('')

    def load_state(self, state):
        super(SSHSpawner, self).load_state(state)
        if 'pid' in state:
            self.pid = state['pid']
        if 'hostname' in state:
            self.hostname = state['hostname']

    def get_state(self):
        state = super(SSHSpawner, self).get_state()
        if self.pid:
            state['pid'] = self.pid
        if self.hostname:
            state['hostname'] = self.hostname
        return state

    def clear_state(self):
        super(SSHSpawner, self).clear_state()
        self.pid = 0
        self.hostname = ''

    def user_env(self, env):
        env['USER'] = self.user.name
        env['HOME'] = pwd.getpwnam(self.user.name).pw_dir
        env['JUPYTER_PATH'] = '/reg/g/psdm/sw/conda/jhub_config/prod-rhel7/'
        env['SHELL'] = os.getenv('SHELL', '/bin/bash')
        return env

    def get_env(self):
        env = super().get_env()
        env = self.user_env(env)
        return env

    async def start(self):
        self.port = random_port()
        env = self.get_env()
        cmd = ['export %s=%s;' % item for item in env.items()]
        cmd += ['echo host=$(hostname);']
        cmd.extend(self.user_options.get('cmd', ['jupyterhub-singleuser']))
        cmd += self.get_args()
        cmd += [' > ~/.jhub.log 2>&1 & pid=$!; echo pid=$pid']
        cmd = ' '.join(cmd)
        ret, stdout, stderr = await execute(self.user.name, 'psana', cmd)
        if ret:
            self.log.info('Error in spawning juptyterhub-singleuser %s\n', stderr)
            if 'Permission denied' in stderr:
                self.log.info('Problem with ssh keys\n')
                raise web.HTTPError(511)

        match = re.search("host=(psana\w+\d+)\npid=(\d+)", stdout)
        self.hostname = match.group(1)
        self.pid = int(match.group(2))
        self.log.info('hostname: %s port: %s pid: %d' % (self.hostname, self.port, self.pid))
        return (self.hostname, self.port)

    async def poll(self):
        if not self.pid:
            self.clear_state()
            return 0
        cmd = 'ps -p {pid}; status=$?; echo status=$status'.format(pid=self.pid)
        ret, stdout, stderr = await execute('psjhub', self.hostname, cmd)

        if ret:
            self.log.info('ssh to poll server %s failed' % self.hostname)
            self.clear_state()
            return 0

        match = re.search('status=(\d+)', stdout)
        status = int(match.group(1))
        # process died
        if status:
            self.log.info('Server died')
            self.log.info("stdout=%s stderr=%s", stdout, stderr)
            self.clear_state()
            return 0
        # process is alive
        else:
            return None

    async def stop(self):
        cmd = 'kill -s {signal} {pid}'.format(signal=signal.SIGTERM, pid=self.pid)
        ret, stdout, stderr = await execute(self.user.name, self.hostname, cmd)
        if ret:
            self.log.info('Error in stoping notebook server %s\n', stderr)
