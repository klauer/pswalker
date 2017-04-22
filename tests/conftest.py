############
# Standard #
############

###############
# Third Party #
###############
import pytest
from ophyd.ophydobj import OphydObject

##########
# Module #
##########
from pswalker.examples import YAG, Mirror


@pytest.fixture(scope='function')
def one_bounce_system():
    """
    Generic single bounce system consisting one mirror with a linear
    relationship with YAG centroid
    """
    mv = Mirror('mirror', 0, 0, 0)
    yag = YAG('yag', mv, 'motor', 100.0)
    return mv, yag


class FakePath(OphydObject):
    SUB_PTH_CHNG = "fake"
    _default_sub = SUB_PTH_CHNG

    def __init__(self, *devices):
        self.devices = sorted(devices, key=lambda d: d.read()["z"]["value"])
        super.__init__()
        for dev in self.devices:
            dev.subscribe(self._run_subs)

    def clear(self, *args, **kwargs):
        for device in self.devices:
            if device.blocking:
                device.set("OUT")

    @property
    def blocking_devices(self):
        return [d for d in self.devices if d.blocking]


@pytest.fixture(scope='function')
def fake_path_two_bounce():
    """
    pswalker-compatible lightpath.BeamPath with fake objects. Pretends to be
    the HOMS system.
    """
    p1h = YAG("p1h", 0, 0)
    feem1 = Mirror("feem1", 0, 10, 0)
    p2h = YAG("p2h", 0, 20)
    feem2 = Mirror("feem2", 0, 30, 0)
    p3h = YAG("p3h", 0, 40)
    hx2_pim = YAG("hx2_pim", 0, 50)
    um6_pim = YAG("um6_pim", 0, 60)
    dg3_pim = YAG("dg3_pim", 0, 70)
    path = FakePath(p1h, feem1, p2h, feem2, p3h, hx2_pim, um6_pim, dg3_pim)
    return path
