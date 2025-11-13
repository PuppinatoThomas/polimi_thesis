import random
import os
import numpy as np
from dotenv import load_dotenv
import google.generativeai as genai

from scripts.utils.constants import RANDOM_SEED

def setup(dotenv=False):
    print("Setting up the environment...")
    _setup_seed()
    if dotenv:
        load_dotenv()
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def _setup_seed():
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)