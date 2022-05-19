from typing import Sequence

from pyturbo.ports import ShaftPort
from pyturbo.systems import Shaft


class TestShaft:
    @staticmethod
    def has_ports(m: dict, names: Sequence[str]):
        return all([n in m for n in names])

    @staticmethod
    def has_n_shaft_ports(m: dict, count: int):
        return len([p for p in m.values() if type(p) == ShaftPort]) == count

    def test_single_input(self):
        # default constructor
        s = Shaft("shaft")
        assert TestShaft.has_ports(s.inputs, ("sh_in",))
        assert TestShaft.has_n_shaft_ports(s.inputs, 1)

        # test different sequences
        for in_sh_arg in [
            {
                "fan_in",
            },
            [
                "fan_in",
            ],
            ("fan_in",),
        ]:
            s = Shaft("shaft", input_shafts=in_sh_arg)
            assert TestShaft.has_ports(s.inputs, in_sh_arg)
            assert TestShaft.has_n_shaft_ports(s.inputs, 1)

    def test_single_output(self):
        # default constructor
        s = Shaft("shaft")
        assert TestShaft.has_ports(s.outputs, ("sh_out",))
        assert TestShaft.has_n_shaft_ports(s.outputs, 1)

        # test different sequences
        for out_sh_arg in [
            {
                "fan_out",
            },
            [
                "fan_out",
            ],
            ("fan_out",),
        ]:
            s = Shaft("shaft", output_shafts=out_sh_arg)
            assert TestShaft.has_ports(s.outputs, out_sh_arg)
            assert TestShaft.has_n_shaft_ports(s.outputs, 1)
