
# Installation jupyterhub_test 2021-07

* runs in systemd using *jupyterhub_test.service*
* the app-name in syslog is **hubtest** (the production is *jupyterhub*)


## Created hub environment

The jupyterhub environment is created in the **dm** conda installation:

    > /cds/sw/ds/dm/conda
    > . /cds/sw/ds/dm/conda/etc/profile.d/conda.sh

```
% conda create -n jhubtest  -c conda-forge jupyterhub
% conda activate jhubtest
% pip install pip install jhub_remote_user_authenticator
% conda install -c conda-forge jupyterlab 
% conda install -c conda-forge notebook
% conda install jupyterlab_widgets
% conda install -c conda-forge ipympl

% conda install -c conda-forge jupyter_bokeh
```

* Installed jupyter_bokeh and bokeh in order to get a kernel working that used bokeh.


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

