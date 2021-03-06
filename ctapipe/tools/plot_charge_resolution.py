"""
Plot charge resolutions generated by ChargeResolutionCalculator.
"""
import numpy as np
from traitlets import Dict, List, Unicode
from ctapipe.core import Tool
from ctapipe.plotting.charge_resolution import ChargeResolutionPlotter


class ChargeResolutionViewer(Tool):
    name = "ChargeResolutionViewer"
    description = ("Plot charge resolutions generated by "
                   "ChargeResolutionCalculator.")

    input_files = List(
        Unicode, None,
        help='Input HDF5 files produced by ChargeResolutionCalculator'
    ).tag(config=True)

    aliases = Dict(dict(
        f='ChargeResolutionViewer.input_files',
        B='ChargeResolutionPlotter.n_bins',
        o='ChargeResolutionPlotter.output_path',
    ))
    classes = List([
        ChargeResolutionPlotter,
    ])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.calculator = None
        self.plotter = None

    def setup(self):
        self.log_format = "%(levelname)s: %(message)s [%(name)s.%(funcName)s]"
        kwargs = dict(config=self.config, tool=self)

        self.plotter = ChargeResolutionPlotter(**kwargs)

    def start(self):
        for fp in self.input_files:
            self.plotter.plot_camera(fp)

    def finish(self):
        q = np.arange(1, 1000)
        self.plotter.plot_poisson(q)
        self.plotter.plot_requirement(q)
        self.plotter.save()


def main():
    exe = ChargeResolutionViewer()
    exe.run()


if __name__ == '__main__':
    main()
