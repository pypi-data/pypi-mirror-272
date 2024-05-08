"""

See Levin 1999 paper: "Filling an N-sided hole using combined subdivision schemes
"""

import matplotlib.pyplot as plt
import numpy as np


class Boundary:
    def __init__(self):
        pass

    def coord(self, u: float):
        raise NotImplementedError

    def deriv(self, u: float):
        raise NotImplementedError
