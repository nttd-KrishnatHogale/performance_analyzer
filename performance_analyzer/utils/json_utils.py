
from dataclasses import asdict, is_dataclass
import numpy as np
import pandas as pd
def make_json_safe(obj):

    if is_dataclass(obj):
        obj = asdict(obj)

    if isinstance(obj, dict):
        return {
            str(k): make_json_safe(v)
            for k, v in obj.items()
        }

    if isinstance(obj, list):
        return [make_json_safe(i) for i in obj]

    if isinstance(obj, tuple):
        return [make_json_safe(i) for i in obj]

    # NumPy integers
    if isinstance(obj, np.integer):
        return int(obj)

    # NumPy floats
    if isinstance(obj, np.floating):
        return float(obj)

    # NumPy bool
    if isinstance(obj, np.bool_):
        return bool(obj)

    # ndarray
    if isinstance(obj, np.ndarray):
        return obj.tolist()

    # Pandas Timestamp
    if isinstance(obj, pd.Timestamp):
        return obj.isoformat()

    if hasattr(obj, "__dict__"):
        return make_json_safe(obj.__dict__)

    return obj