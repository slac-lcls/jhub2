c = get_config()
c.JupyterHub.base_url = 'jupyterhubtest'

c.JupyterHub.authenticator_class = 'jhub_remote_user_authenticator.remote_user_auth.RemoteUserAuthenticator'
c.JupyterHub.spawner_class = 'sshspawner.SSHSpawner'

c.JupyterHub.port = 9839
c.JupyterHub.hub_ip = '0.0.0.0'

c.Spawner.ip = '0.0.0.0'

c.ConfigurableHTTPProxy.api_url = 'http://localhost:9002'

c.JupyterHub.hub_ip = '172.21.49.203'
c.JupyterHub.hub_port = 54321


c.Authenticator.admin_users = set(['mshankar', 'wilko'])

c.Spawner.options_form = '''
<label for="cmd">Please choose</label>
<select name="cmd">
  <option value="jupyter-labhub">Jupyter Lab</option>
  <option value="jupyterhub-singleuser">Classic Notebook</option>
</select>

<label for="loc">Please choose</label>
<select name="loc">
  <option value="psana">ana</option>
  <option value="psffb">ffb</option>
</select>
'''

c.JupyterHub.services = [
    {
        'name': 'cull-idle',
        'admin': True,
        'command': 'python cull_idle_servers.py --timeout=172800'.split(),
    }
]
