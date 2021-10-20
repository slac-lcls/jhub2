
# Installation jupyterhub_test 2021-07

* runs in systemd using *jupyterhub_test.service*
* the app-name in syslog is **hubtest** (the production is *jupyterhub*)


## Created hub environment

The jupyterhub environment is created in the **dm** conda installation, _/cds/sw/ds/dm/conda_. 
To install a new jhub environment run the following commands:

```
% . /cds/sw/ds/dm/conda/etc/profile.d/conda.sh
% conda create -n jhub-<vers> -c conda-forge jupyterhub jupyterlab ipympl jupyter_bokeh
% conda activate jhub-<vers>
% pip install jhub_remote_user_authenticator 
```

Before version 2 the jhub version was using the version from the jupyterhub package. However, 
from jhub-2.0.0 we use our own version.

*jupyter_bokeh* is needed in order to get a kernel working that used bokeh.


## Hub instances 

There are three different instances of the Jupyterhub running. Each one has uses it's own workdir and a clone of the 
jhub2 repo (https://github.com/slac-lcls/jhub2.git). The same code is used except for the config files and systemd 
service file. The configuration is in the jupyterhub*_config.py, in particular the port settings.

### production

* workdir: /u1/jupyterhub/prod/jhub2/
* name: jupyterhub
* config: jupyterhub_config.py
* systemd-service: jupyterhub.service

### previous (prev)

* workdir: /u1/jupyterhub/prev/jhub2/
* name: jupyterhubprev
* config: jupyterhub_prev_config.py
* systemd-service: jupyterhub_prev.service

### test (prev)

* workdir: /u1/jupyterhub/test/jhub2/
* name: jupyterhubtest
* config: jupyterhub_test_config.py
* systemd-service: jupyterhub_test.service


## Configuration *jupyterhubtest_config.py*. 

The configurations *c.JupyterHub.hub_ip* and *c.JupyterHub.hub_port* needed to be added because two 
hubs are running on the same node and there was a port conflict. This port and IP are used by the 
*--error-target* option to the node configurable-http-proxy service.


## Selecting the jhub version that an instances is using

Which jhub version an instance is running is configured in the systemd .service file for that instance. 
The version has to be set in the *Environment="PATH..."* and *ExecStart* lines.


# Changelog

## jhub-2.0.0

- Fix problem with matplotlib and ipympl. In the previous version using "%matplotlib widget" gave an
  error when trying to display interactive plots.
  
  
