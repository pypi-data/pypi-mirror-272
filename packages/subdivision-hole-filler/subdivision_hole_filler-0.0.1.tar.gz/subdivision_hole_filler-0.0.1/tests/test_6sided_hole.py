import os
import pytest


class Test6SidedHole:
    def test_6sided_hole(self):
        from subdivision_hole_filler import Boundary

if __name__ == "__main__":
    pytest.main(["-s", "-k", "Test6SidedHole"])