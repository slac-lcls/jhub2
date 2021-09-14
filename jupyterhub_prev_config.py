c = get_config()
c.JupyterHub.base_url = 'jupyterhubprev'

c.JupyterHub.authenticator_class = 'jhub_remote_user_authenticator.remote_user_auth.RemoteUserAuthenticator'
c.JupyterHub.spawner_class = 'sshspawner.SSHSpawner'

c.JupyterHub.port = 8839
from jupyter_client.localinterfaces import public_ips
# to make hub accessible for remote spwaners
c.JupyterHub.hub_ip = public_ips()[0]
c.Spawner.ip = '0.0.0.0'

c.ConfigurableHTTPProxy.api_url = 'http://localhost:8802'

c.JupyterHub.hub_ip = '172.21.49.203'
c.JupyterHub.hub_port = 54388


c.Authenticator.admin_users = set(['mshankar', 'wilko'])

c.Spawner.options_form = '''
<label for="cmd">Please choose</label>
<select name="cmd">
  <option value="jupyterhub-singleuser">Classic Notebook</option>
  <option value="jupyter-labhub">Jupyter Lab</option>
</select>
'''

c.JupyterHub.services = [
    {
        'name': 'cull-idle',
        'admin': True,
        'command': 'python cull_idle_servers.py --timeout=172800'.split(),
    }
]
