# YOLOR Run Guide for Accuinsight

## Requirements
* torch
    * Must install version **1.11.0**. Version 1.12.0 throws a runtime error(casting issues). 
* torchvision
    * Must install verion **0.12.0**.
* tensorboard
* scipy
* pyyaml
* pycocotools
* opencv-python
* tqdm

### Required Modules Installation Command
Replace *hj_yolor_base* with the name of the virtual environment to use.
```python
!/opt/conda/envs/hj_yolor_base/bin/pip install torch==1.11.0 torchvision==0.12.0 tensorboard scipy pyyaml pycocotools opencv-python tqdm
```
