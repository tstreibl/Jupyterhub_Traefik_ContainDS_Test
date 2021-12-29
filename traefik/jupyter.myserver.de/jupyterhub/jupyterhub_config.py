# JupyterHub configuration
#
## If you update this file, do not forget to delete the `jupyterhub_data` volume before restarting the jupyterhub service:
## b
##     docker volume rm jupyterhub_jupyterhub_data
##
## or, if you changed the COMPOSE_PROJECT_NAME to <name>:
##
##    docker volume rm <name>_jupyterhub_data
##

import os, sys
import shutil

#print shows up in logs with "flush=True"
print("This is a testoutput from jupyterhub_config.py using print",flush=True)

c.JupyterHub.log_level = 10

# Files are created from the certdumper docker service (see docker-compose for traefic)
# traefic and letsencrypt provides automatically an acme.json file
# the certdumper docker service only converts the acme.json file into the key and cert files
# would be much easier if we could load the acme.json directly at this place  
c.JupyterHub.ssl_key = '/certs/privatekey.key'  #aus dem Laufwerk des Containers
c.JupyterHub.ssl_cert = '/certs/certificate.crt'

c.JupyterHub.trusted_downstream_ips = [os.environ['HOST_IP']]  
c.JupyterHub.cleanup_proxy = True
c.JupyterHub.cleanup_servers = True

c.JupyterHub.hub_ip = '0.0.0.0' #os.environ['HUB_IP'] works also
c.JupyterHub.hub_connect_ip = os.environ['HUB_IP']  #mandatory
#  Default: 8081 
#  c.JupyterHub.hub_port = 8081
 
c.CDSDashboardsConfig.builder_class = 'cdsdashboards.builder.dockerbuilder.DockerBuilder'

## Generic
c.JupyterHub.admin_access = True
c.Spawner.default_url = '/lab'  #{username} will be expanded to the user’s username
c.JupyterHub.shutdown_on_logout = True # von mir; Session nach logout zu machen


## Authenticator

from oauthenticator.github import LocalGitHubOAuthenticator
c.JupyterHub.authenticator_class = 'oauthenticator.LocalGitHubOAuthenticator' # GitHubOAuthenticator

c.Authenticator.auto_login_oauth2_authorize = False
c.Authenticator.oauth_callback_url = os.environ['oauth_callback_url']
c.Authenticator.client_id = os.environ['client_id']
c.Authenticator.client_secret = os.environ['client_secret'] 

c.Authenticator.allowed_users = {'tstreibl','testuser'}
c.Authenticator.admin_users = {'tstreibl'}  
c.Authenticator.create_system_users = True

#Enabling ContainDS Dashboard; see https://cdsdashboards.readthedocs.io/en/stable/chapters/setup/docker.html#installing-cdsdashboards
from cdsdashboards.app import CDS_TEMPLATE_PATHS
from cdsdashboards.hubextension import cds_extra_handlers
#from cdsdashboards.app import CDSDashboardsConfig 

c.JupyterHub.template_paths = CDS_TEMPLATE_PATHS
c.JupyterHub.extra_handlers = cds_extra_handlers

# c.VariableMixin.proxy_force_alive = True
# c.VariableMixin.proxy_last_activity_interval = 300
# c.VariableMixin.proxy_request_timeout = 0

import secrets
os.environ['JPY_COOKIE_SECRET'] = secrets.token_hex(16)
c.JupyterHub.cookie_secret = bytes.fromhex(os.environ['JPY_COOKIE_SECRET'])

c.CDSDashboardsConfig.builder_class = 'cdsdashboards.builder.dockerbuilder.DockerBuilder'
c.CDSDashboardsConfig.allow_custom_conda_env = False
c.CDSDashboardsConfig.include_auth_state = True
c.CDSDashboardsConfig.include_servers = True
c.CDSDashboardsConfig.include_servers_state = True


c.JupyterHub.spawner_class = 'cdsdashboards.hubextension.spawners.variabledocker.VariableDockerSpawner'
c.Spawner.debug = True
c.JupyterHub.allow_named_servers = True

c.Spawner.image = os.environ['DOCKER_JUPYTER_CONTAINER']
#servername = os.environ['HOST'] 
c.Spawner.extra_host_config = {'network_mode': os.environ['INTERNAL_NETWORK']}
c.Spawner.hub_ip_connect =  os.environ['HUB_IP']  
c.Spawner.network_name = os.environ['INTERNAL_NETWORK'] #"jupyter_net"
c.Spawner.use_internal_ip = True
c.Spawner.remove = False # remove user containers when done. True works better but difficult to debug
c.Spawner.debug = True
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR')
c.Spawner.notebook_dir = notebook_dir
c.Spawner.extra_create_kwargs = {'user': 'root'} #jovyan

c.Spawner.environment = {
  'GRANT_SUDO': '1',
  'UID': '0', # workaround https://github.com/jupyter/docker-stacks/pull/420
}

c.Spawner.name_template = "{prefix}-{username}-{servername}"
c.Spawner.volumes = {"{prefix}-{username}-{servername}": notebook_dir }

c.Spawner.cpu_limit = 1
c.Spawner.mem_limit = '10G'


