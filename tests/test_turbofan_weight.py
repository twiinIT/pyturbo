from pyturbo.systems.turbofan_weight import TurbofanWeight


class TestTurbofanWeight:
    tfw = TurbofanWeight("tfw")

    def test_ref(self):

        tfw = self.tfw
        tfw.fan_diameter = tfw.fan_diameter_ref
        tfw.length = tfw.length_ref
        tfw.EIS = tfw.EIS_ref

        tfw.run_once()

        assert tfw.ipps_weight == tfw.ipps_weight_ref