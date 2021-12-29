# Running a dockerized Jupyterhub with ContaindDS Dashboard behind traefik as reverse proxy

This is just an attemp to get Jupyterhub with ContaindDS Dashboard behind a traefik reverse proxy up and running. At the moment everything works fine **except the ContainDS Dashboard**. I shared this github repo to find my configuration mistakes.

## Intention

Since I already had a few services (e.g. a nextcloud) running behind traefik, I was hoping that I could integrate jupyterhub the same way. However I only could find a quite outdated approach under
<https://github.com/defeo/jupyterhub-docker>, which I tried to follow. **Just as a warning: my Linux and Docker skills are low, thus the setup will probably have severe bugs!**

 ## Directory Structure and Structure of the docker-compose containers
 
 * **traefik** directory contains the docker-compose file for the traefik reverse proxy, which runs in it's own container. The necessary environmental variables for the configuration are provided by an .env file in the same directory. The reverse proxy basically provides a **traefik** network to be used by the other containers/services
 * **jupyter.myserver.de** directory contains the docker-compose file for a container with the jupyterhub and jupyterlab services and their .env file. Both services are generated from Images (jupyterhub_img, jupyterlab_img=DOCKER_JUPYTER_CONTAINER) which themselves are generated in the subdirectories **jupyterhub** and **jupyterlab**
 * in the **jupyterhub** directory the jupyterhub_img is build via a dockerfile based on a **jupyterhub/jupyterhub:2.0.1** (or a jupyterhub/jupyterhub:1.5.0) dockerfile
  * in the **jupyterlab** directory the jupyterlab_img is build via a dockerfile based on a **jupyter/scipy-notebook:hub-2.0.1** (or a jupyter/scipy-notebook:hub-1.5.0) dockerfile
  * the version numbers of the dockerfiles used for jupyterhub/jupyterlab images must match. Using 1.5.0 or 2.0.1 versions in my case leads to the same results.
  
 ## Network settings for jupyterhub/jupyterlab
 
 * jupyterhub and jupyterlab servicers are connected to each other via a "jupyter_net" network (environmental variable INTERNAL_NETWORK). 
 * jupyterhub in addition is connected to the "traefik" network
 * the jupyterhub container_name is stored in the environmental variable HUB_IP and provides the ip adress for jupyterhub to connect

 ## Basics Settings in jupyterhub_config.py
 
 Network:
 * the "jupyter_net" network is provided to jupyterhub via c.Spawner.network_name=os.environ['NTERNAL_NETWORK']
 * the jupyterhub container_name is provided to jupyterhub via 
	- c.JupyterHub.hub_connect_ip = os.environ['HUB_IP'];  
	- c.JupyterHub.hub_ip = '0.0.0.0' (or can be set to os.environ['HUB_IP'] as well)

Classes:
 * For authentication a github authenticator with **oauthenticator.LocalGitHubOAuthenticator** class was used
 * To spawn the jupyterlab containers for the ContainDS Dashboard a **cdsdashboards.hubextension.spawners.variabledocker.VariableDockerSpawner** class was used.
 * CDSDashboardsConfig.builder_class was configured with **cdsdashboards.builder.dockerbuilder.DockerBuilder** class
 
 ## Unsolved Problems with ContainDS Dashboard
 
 At the moment everything except spawning a ContainDS dashboard works fine:
 - authentication is ok
 - users can spawn their server or even additional servers
 - users can run voila dashboards from within their notebooks
 
 When trying to create a ContainDS dashboard on the dashboard interface using voila a HTTP 500 Error occurs during the startup phase of the dashboard:
 
 ```
 Build failed: HTTP 500: Internal Server Error (Spawner failed to start [status=ExitCode=1, Error='', FinishedAt=2021-12-29T21:11:06.031322228Z]. The logs for tstreibl:dash-test-dashboard may contain details.)
Event log
Builder requested
Starting builder
Starting up final server for Dashboard, after build
Spawner progress: Server requested
Spawner progress: Spawning server...
Build failed: HTTP 500: Internal Server Error (Spawner failed to start [status=ExitCode=1, Error='', FinishedAt=2021-12-29T21:11:06.031322228Z]. The logs for tstreibl:dash-test-dashboard may contain details.)
```
The log of the jupyterlab container states that the dashboard container reached the finale build phase "In do_final_build", but never shows up "server never showed up" which finally results in a timeout.

Looking at the container itself the log shows, that "jhsingle_native_proxy.main" module could not be found, which seems to be the root cause:

```
Entered start.sh with args: python3 -m jhsingle_native_proxy.main --destport=0 python3 {-}m voila {presentation_path} {--}port={port} {--}no-browser {--}Voila.base_url={base_url}/ {--}Voila.server_url=/ --progressive --presentation-path=/home/jovyan/voila_test.ipynb --ip=0.0.0.0 --port=8888 {--}debug --debug
Granting jovyan passwordless sudo rights!
Running as jovyan: python3 -m jhsingle_native_proxy.main --destport=0 python3 {-}m voila {presentation_path} {--}port={port} {--}no-browser {--}Voila.base_url={base_url}/ {--}Voila.server_url=/ --progressive --presentation-path=/home/jovyan/voila_test.ipynb --ip=0.0.0.0 --port=8888 {--}debug --debug
/opt/conda/bin/python3: Error while finding module specification for 'jhsingle_native_proxy.main' (ModuleNotFoundError: No module named 'jhsingle_native_proxy')
```

To avoid this error the module jhsingle_native_proxy was pip installed into the jupyterhub_img and jupyterlab_img. 

This didn't change anything. 

Controlling the jpyterlab_img container with "python3 -m pip list"  shows that 
jhsingle-native-proxy 0.8.0 is installed (the "-" instead of the "_" in the name doesn't seem to matter since the calling convention "jhsingle_native_proxy.main" is correct).

Excerpts from the logs can be found in the **logs** directory
