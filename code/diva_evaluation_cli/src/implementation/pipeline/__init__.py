# --------------------------------------------------------
# DIVA pipeline
# Copyright (c) 2015 LTI
# Licensed under The MIT License [see LICENSE for details]
# --------------------------------------------------------

"""Set up paths for Diva@PIPELINE."""

import os.path as osp
import sys
from . import config

def add_path(path):
    if path not in sys.path:
        sys.path.insert(0, path)

our_path = osp.abspath(osp.join(osp.dirname("__file__"),osp.pardir))
# Add to PYTHONPATH
add_path(our_path)