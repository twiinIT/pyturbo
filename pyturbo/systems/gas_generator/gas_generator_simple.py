from cosapp.systems import System
from pyoccad.create import CreateTopology

from pyturbo.systems import CombustorSimple, CompressorSimple, TurbineSimple
from pyturbo.systems.gas_generator.gas_generator_simple_geom import GasGeneratorSimpleGeom


class GasGeneratorSimple(System):
    """A simple gas generator model.

    This model includes a compressor, a combustor and a turbine. The power transmission
    between the turbine and the compressor is direct without and intermediate shaft model.
    """

    def setup(self):
        # children
        geom = self.add_child(GasGeneratorSimpleGeom("geom"))

        cmp = self.add_child(CompressorSimple("compressor"), pulling=["fl_in"])
        cmb = self.add_child(CombustorSimple("combustor"), pulling=["fuel_in"])
        trb = self.add_child(TurbineSimple("turbine"), pulling=["fl_out"])

        # connection
        self.connect(geom.compressor_kp, cmp.kp)
        self.connect(geom.combustor_kp, cmb.kp)
        self.connect(geom.turbine_kp, trb.kp)

        self.connect(self.turbine.shaft_out, self.compressor.shaft_in)
        self.connect(self.compressor.fl_out, self.combustor.fl_in)
        self.connect(self.combustor.fl_out, self.turbine.fl_in)

        # init
        self.compressor.shaft_in.power = 10e6

        # design method
        # geometries
        geom_sizing = geom.design_methods["sizing"]
        cmp_sizing = cmp.design_methods["sizing"]
        cmb_sizing = cmb.design_methods["sizing"]
        trb_sizing = trb.design_methods["sizing"]

        self.add_design_method("sizing").extend(geom_sizing).extend(cmp_sizing).extend(
            cmb_sizing
        ).extend(trb_sizing)

    def _to_occt(self):
        return CreateTopology.make_compound(
            self.compressor.geom.to_occt(),
            self.combustor.geom.to_occt(),
            self.turbine.geom.to_occt(),
        )

    def jupyter_view(self):
        try:
            from pyoccad.render import JupyterThreeJSRenderer
        except ImportError:
            raise ImportError("Please install 'pythonocc_helpers' before using this function")

        super(System, self).__setattr__("_render", None)
        self._render = JupyterThreeJSRenderer(
            view_size=(1800, 800), camera_target=(1.0, 0.0, 0.0), camera_position=(-2.0, 1.0, 2.0)
        )
        self._render.add_shape(self._to_occt(), uid=self.name)
        return self._render.show()

    def update_jupyter_view(self):
        self._render.update_shape(self._to_occt(), uid=self.name)
