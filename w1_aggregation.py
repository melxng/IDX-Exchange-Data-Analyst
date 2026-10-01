"""
Week 1 - Monthly Dataset Aggregation

Load and concatenate all monthly MLS files from January 2024 through the most recently completed
calendar month into analysis-ready combined datasets.
"""


import pandas as pd
import os
import numpy as np
import re

