import funcnodes_pandas
import funcnodes_numpy
import funcnodes as fn
from .covariance import COVARIANCE_NODE_SHELFE

__version__ = "0.1.0"

NODE_SHELF = fn.Shelf(
    name="sklearn",
    description="scikit-learn for funcnodes",
    nodes=[],
    subshelves=[COVARIANCE_NODE_SHELFE],
)
