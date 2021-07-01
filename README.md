
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


## Configuration *jupyterhubtest_config.py*. 

The configurations *c.JupyterHub.hub_ip* and *c.JupyterHub.hub_port* needed to be added because two 
hubs are running on the same node and there was a port conflict. This port and IP are used by the 
*--error-target* option to the node configurable-http-proxy service.

