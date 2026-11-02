import os
import subprocess
import sys

import pytest


@pytest.fixture(scope="session", autouse=True)
def trained_model():
    if not os.path.exists("models/model.joblib"):
        subprocess.check_call([sys.executable, "src/train.py"])
