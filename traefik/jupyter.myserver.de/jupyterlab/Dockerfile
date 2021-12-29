
#see https://hub.docker.com/r/jupyter/scipy-notebook/tags
#FROM jupyter/scipy-notebook:hub-1.5.0
FROM jupyter/scipy-notebook:hub-2.0.1
#FROM jupyter/scipy-notebook:latest

USER root

# vermutlich braucht man keines der Zusatzpackages; sagemath ist aber ein nettes addon
# APT packages   
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    fonts-dejavu \
    tzdata \
    gfortran \
    gcc \
    scilab \
    pari-gp \
    libpari-dev \
    sagemath \
    sagemath-jupyter \
    libgmp-dev \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*


USER $NB_UID
#tornado is already installed
#jhsingle-native-proxy seems to be required for cdsdashboards but is not automatically installed 
RUN pip3 install --no-cache-dir \
    voila \
    streamlit \
    dash \
    cdsdashboards \
    jupyter-containds \
    jhsingle-native-proxy \
    bqplot  && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}" 

#  RUN conda install --quiet --yes \
#     tornado \
#     voila \
#     streamlit \
#     dash \
#     cdsdashboards \
#     jupyter-containds \
#     jhsingle-native-proxy \
#     bqplot  && \
#     fix-permissions $CONDA_DIR

USER $NB_UID  #seems to be mandatory that the user is not root at the end

