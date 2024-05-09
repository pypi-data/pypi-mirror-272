# Copyright (c) 2024 The View AI Contributors
# Distributed under the MIT software license

import warnings
warnings.filterwarnings("ignore")

import sys
import requests
from enum import Enum

# BASE
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from time import time

import os
import orjson
import argparse
import logging

# PREPROCESSING
from sklearn.model_selection import (
    train_test_split,
    cross_val_score,
    StratifiedKFold,
    KFold,
)

# XAI
import plotly.graph_objs as go
import numpy as np
import pandas as pd
from shap.utils import approximate_interactions, convert_name
from shap.utils._general import encode_array_if_needed
import shap
import plotly.express as px
from interpret.blackbox import LimeTabular

# RESULTS
from sklearn.inspection import permutation_importance
from tabulate import tabulate
from sklearn.metrics import *
# from raiwidgets import ExplanationDashboard
# from raiwidgets.explanation_dashboard_input import ExplanationDashboardInput
# from responsibleai.serialization_utilities import serialize_json_safe


# SERIALIZATION
import joblib
import pickle

# DASK
# from dask.distributed import Client, LocalCluster
# from dask_kubernetes import HelmCluster #use in deployment
# from dask.distributed import performance_report