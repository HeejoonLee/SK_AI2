# Virtual Environment Guide for Accuinsight

## Creating a Virtual Environment
1. Open any console/notebook window

2. Run `!conda create -n [venv name] python=[python version] -y`
    * venv name: A name for the virtual environment
    * python version: Python version to install
        - Latest: 3.10.5
        - System: 3.7.6
    * `-y`: Silence confirmatioin
    * ex) `!conda create -n hj_yolor_base python=3.10.5 -y`

## Running Python in the virtual environment
1. Run `!/opt/conda/envs/[venv name]/bin/python`
    > `source` or `activate` does not work in *Accuinsight*, so the newly installed Python binary must be run *manually*.
    * ex) `!/opt/conda/envs/hj_yolor_base/bin/python`

## Installing Modules in the Virtual Environment
1. Run the *pip* binary in the virtual environment directory
    * ex) `!/opt/conda/envs/hj_yolor_base/bin/pip install torch`


