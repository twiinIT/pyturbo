from pyturbo.systems.generic.generic_simple_geom import GenericSimpleGeom


class TestGenericSimpleGeom:
    def test_setup(self):
        # default constructor
        sys = GenericSimpleGeom("sys")

        data_inward = ["hub_in_r_ref", "tip_in_r_ref", "hub_out_r_ref", "tip_out_r_ref"]
        data_outward = ["hub_in_r", "tip_in_r", "hub_out_r", "tip_out_r"]

        for data in data_inward:
            assert data in sys.inwards
        for data in data_outward:
            assert data in sys.outwards

    def test_compute_generic_geom(self):
        sys = GenericSimpleGeom("sys")

        sys.hub_in_r_ref = 0.5
        sys.scale = 3.0

        sys.compute_generic_geom()
        assert sys.hub_in_r == 1.5
