
# Installation testhub 2021-07

* runs in systemd using *jupytertesthub.service*
* the app-name in syslog is **testhub** (the production is *jupyterhub*)


## Created hub environment

The jupyterhub environment is created in the **dm** conda installation:

    > /cds/sw/ds/dm/conda
    > . /cds/sw/ds/dm/conda/etc/profile.d/conda.sh

```
% conda create -n jhubtest  -c conda-forge jupyterhub
% conda activate jhubtest
% conda install -c conda-forge jupyterlab 
% conda install -c conda-forge notebook
% conda install jupyterlab\_widgets
% pip install pip install jhub\_remote\_user\_authenticator
```

## Configuration 

See *jupyterhub_config.py*. 

The configurations *c.JupyterHub.hub_ip* and *c.JupyterHub.hub_port* needed to be added because two 
hubs are running on the same node and there was a port conflict. This port and IP are used by the 
*--error-target* option to the node configurable-http-proxy service.

