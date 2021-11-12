#!/usr/bin/env bash

COMMON_FOLDER_PATH='/media/paulati/Nuevo vol/paula/dh/2021/dsad_2021/common'

cd $COMMON_FOLDER_PATH

conda init bash

conda remove --yes --name dhdsblend2021 --all

conda create --yes --name dhdsblend2021 python=3.8

conda install --yes --name dhdsblend2021 --file requirements.txt

conda install -c conda-forge --yes --name dhdsblend2021 --file requirements_conda-forge.txt

conda install -c plotly --yes --name dhdsblend2021 --file requirements_plotly.txt

conda activate dhdsblend2021

# Jupyter widgets extension
jupyter labextension install @jupyter-widgets/jupyterlab-manager

# jupyterlab renderer support
jupyter labextension install jupyterlab-plotly@4.14.1 --no-build

# FigureWidget support
jupyter labextension install plotlywidget@4.14.1 --no-build

# Build extensions (must be done to activate extensions since --no-build is used above)
jupyter lab build

#unset NODE_OPTIONS
