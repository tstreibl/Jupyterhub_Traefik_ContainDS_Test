# see https://hub.docker.com/r/jupyterhub/jupyterhub/tags
#FROM jupyterhub/jupyterhub:1.5.0
FROM jupyterhub/jupyterhub:2.0.1

COPY jupyterhub_config.py .

#Example see https://stackoverflow.com/questions/27701930/how-to-add-users-to-docker-container 
#system user tstreibl and normal user testuser
RUN useradd -r -m -s /bin/bash -g users -G sudo,users -p meinpasswort tstreibl 
#RUN useradd -m -s /bin/bash -g users -p meinpasswort tstreibl 
RUN useradd -m -s /bin/bash -g users -p testuserpasswort testuser                           

USER root
RUN apt-get -y update && apt-get install 

# voila-gridstack would be an option
RUN pip3 install --no-cache-dir \
    dockerspawner \
    voila \
    streamlit \
    dash \
	cdsdashboards \
	jhsingle-native-proxy \
    jupyter-containds \
    oauthenticator 

#USER tstreibl  # does not work, seems to be necessary that at the end user is root 

