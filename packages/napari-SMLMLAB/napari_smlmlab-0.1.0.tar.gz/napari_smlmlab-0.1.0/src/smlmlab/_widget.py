import os
import traceback
from functools import partial
from multiprocessing import Manager
from typing import TYPE_CHECKING

import matplotlib.colors as mcolors
import numpy as np
import pandas as pd
import pyqtgraph as pg
from qtpy.QtCore import QThreadPool
from qtpy.QtWidgets import QSizePolicy, QVBoxLayout, QWidget
from scipy.optimize import curve_fit

if TYPE_CHECKING:
    import napari

import trackpy as tp

from smlmlab.gui import Ui_Frame as gui
from smlmlab.utils.compute_utils import _utils_compute
from smlmlab.utils.events_utils import _events_utils
from smlmlab.utils.import_utils import _import_utils
from smlmlab.utils.loc_utils import _loc_utils
from smlmlab.utils.picasso_utils import _picasso_detect_utils
from smlmlab.utils.plot_utils import CustomMatplotlibWidget, _plot_utils
from smlmlab.utils.undrift_utils import _undrift_utils
from smlmlab.utils.viewer_utils import _viewer_utils


class smlmlabWidget(
    QWidget,
    gui,
    _import_utils,
    _events_utils,
    _picasso_detect_utils,
    _loc_utils,
    _viewer_utils,
    _utils_compute,
    _undrift_utils,
    _plot_utils,
):

    def __init__(self, viewer: "napari.viewer.Viewer"):
        super().__init__()
        self.viewer = viewer

        self.gui = gui()
        self.gui.setupUi(self)

        # create pyqt graph container
        self.graph_container = self.gui.graph_container
        self.graph_container.setLayout(QVBoxLayout())

        self.graph_canvas = pg.GraphicsLayoutWidget()
        self.graph_container.layout().addWidget(self.graph_canvas)

        # create pyqt graph container
        self.lifetime_graph = self.gui.lifetime_graph
        self.lifetime_graph.setLayout(QVBoxLayout())
        self.lifetime_graph.setMinimumWidth(100)

        self.lifetime_graph_canvas = CustomMatplotlibWidget(self)
        self.lifetime_graph.layout().addWidget(self.lifetime_graph_canvas)
        self.lifetime_graph_canvas.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        self.lifetime_graph_canvas.axes.clear()

        self.gui.import_data.clicked.connect(self.import_image_data)

        self.viewer.dims.events.current_step.connect(
            partial(self.draw_molecules, update_vis=False)
        )

        self.gui.picasso_detect.clicked.connect(
            partial(self.pixseq_picasso, detect=True, fit=False)
        )
        self.gui.picasso_fit.clicked.connect(
            partial(self.pixseq_picasso, detect=False, fit=True)
        )
        self.gui.picasso_detectfit.clicked.connect(
            partial(self.pixseq_picasso, detect=True, fit=True)
        )
        self.gui.picasso_render.clicked.connect(self.picasso_render)
        self.gui.export_locs.clicked.connect(self.initialise_export_locs)

        self.gui.picasso_undrift.clicked.connect(self.initialise_undrift)

        self.gui.picasso_vis_mode.currentIndexChanged.connect(
            partial(self.draw_molecules, update_vis=True)
        )
        self.gui.picasso_vis_mode.currentIndexChanged.connect(
            partial(self.draw_bounding_boxes, update_vis=True)
        )
        self.gui.picasso_vis_size.currentIndexChanged.connect(
            partial(self.draw_molecules, update_vis=True)
        )
        self.gui.picasso_vis_size.currentIndexChanged.connect(
            partial(self.draw_bounding_boxes, update_vis=True)
        )
        self.gui.picasso_vis_opacity.currentIndexChanged.connect(
            partial(self.draw_molecules, update_vis=True)
        )
        self.gui.picasso_vis_opacity.currentIndexChanged.connect(
            partial(self.draw_bounding_boxes, update_vis=True)
        )
        self.gui.picasso_vis_edge_width.currentIndexChanged.connect(
            partial(self.draw_molecules, update_vis=True)
        )
        self.gui.picasso_vis_edge_width.currentIndexChanged.connect(
            partial(self.draw_bounding_boxes, update_vis=True)
        )

        self.gui.picasso_dataset.currentIndexChanged.connect(
            lambda: self.update_channel_selector(
                dataset_selector="picasso_dataset",
                channel_selector="picasso_channel",
            )
        )
        self.gui.picasso_render_dataset.currentIndexChanged.connect(
            lambda: self.update_channel_selector(
                dataset_selector="picasso_render_dataset",
                channel_selector="picasso_render_channel",
            )
        )
        self.gui.plot_dataset.currentIndexChanged.connect(
            lambda: self.update_channel_selector(
                dataset_selector="plot_dataset",
                channel_selector="plot_channel",
                efficiency=True,
            )
        )
        self.gui.locs_export_dataset.currentIndexChanged.connect(
            lambda: self.update_channel_selector(
                dataset_selector="locs_export_dataset",
                channel_selector="locs_export_channel",
            )
        )
        self.gui.picasso_undrift_dataset.currentIndexChanged.connect(
            lambda: self.update_channel_selector(
                dataset_selector="picasso_undrift_dataset",
                channel_selector="picasso_undrift_channel",
            )
        )

        self.gui.plot_mode.currentIndexChanged.connect(
            self.update_plot_channel
        )
        self.gui.plot_dataset.currentIndexChanged.connect(self.draw_line_plot)
        self.gui.plot_channel.currentIndexChanged.connect(self.draw_line_plot)
        self.gui.subtract_background.clicked.connect(self.draw_line_plot)

        self.gui.add_line.clicked.connect(
            lambda: self.draw_shapes(mode="line")
        )
        self.gui.add_box.clicked.connect(lambda: self.draw_shapes(mode="box"))
        self.gui.add_background.clicked.connect(
            lambda: self.draw_shapes(mode="background")
        )

        self.gui.dataset_selector.currentIndexChanged.connect(
            partial(
                self.update_active_image,
                dataset=self.gui.dataset_selector.currentText(),
            )
        )

        self.gui.plot_lifetime_hist.clicked.connect(
            self.plot_lifetime_histogram
        )
        self.gui.export_lifetime_data.clicked.connect(
            self.export_lifetime_data
        )

        self.verbose = False

        self.dataset_dict = {}
        self.localisation_dict = {"bounding_boxes": {}, "molecules": {}}
        self.traces_dict = {}
        self.plot_dict = {}
        self.contrast_dict = {}

        self.active_dataset = None
        self.active_channel = None

        self.threadpool = QThreadPool()

        manager = Manager()
        self.stop_event = manager.Event()

        self.worker = None
        self.multiprocessing_active = False

        self.viewer.layers.events.inserted.connect(self.on_add_layer)

        # keybind F1

        # self.viewer.bind_key("t", func = self.tracking, overwrite = True)

    def export_lifetime_data(self, viewer=None):

        try:

            dataset = self.gui.lifetimes_dataset.currentText()
            channel = self.gui.lifetimes_channel.currentText()

            if dataset != "" and channel != "":

                import_path = self.dataset_dict[dataset][channel.lower()][
                    "path"
                ]
                base, ext = os.path.splitext(import_path)

                lifetime_path = base + "_lifetimes.csv"

                lifetimes = self.get_lifetimes()

                if len(lifetimes) > 0:

                    np.savetxt(lifetime_path, lifetimes, delimiter=",")
                    print(f"Exported lifetime data to {lifetime_path}")

        except:
            print(traceback.format_exc())

    def get_lifetimes(self):

        lifetimes = []

        try:

            dataset = self.gui.lifetimes_dataset.currentText()
            channel = self.gui.lifetimes_channel.currentText()

            if dataset != "" and channel != "":
                loc_dict, n_locs, fitted = self.get_loc_dict(
                    dataset, channel.lower(), type="molecules"
                )

                if n_locs > 0:

                    min_lifetime = int(self.gui.min_lifetime.text())
                    max_lifetime = int(self.gui.max_lifetime.text())

                    locs = loc_dict["localisations"].copy()

                    columns = list(locs.dtype.names)

                    df = pd.DataFrame(locs, columns=columns)

                    # Link particles across frames
                    tracked = tp.link(df, search_range=2, memory=1)

                    lifetimes = tracked["particle"].value_counts().to_numpy()

                    lifetimes = lifetimes[lifetimes > min_lifetime]
                    lifetimes = lifetimes[lifetimes < max_lifetime]

        except:
            print(traceback.format_exc())

        return lifetimes

    def plot_lifetime_histogram(self, viewer=None):

        try:

            dataset = self.gui.lifetimes_dataset.currentText()
            channel = self.gui.lifetimes_channel.currentText()
            lifetime_bins = int(self.gui.lifetime_bins.text())
            fit_exponential = self.gui.fit_exponential.isChecked()
            min_lifetime = int(self.gui.min_lifetime.text())
            max_lifetime = int(self.gui.max_lifetime.text())

            if dataset != "" and channel != "":

                loc_dict, n_locs, fitted = self.get_loc_dict(
                    dataset, channel.lower(), type="molecules"
                )

                if n_locs > 0:

                    lifetimes = self.get_lifetimes()

                    hist, bin_edges = np.histogram(
                        lifetimes, bins=lifetime_bins, density=True
                    )

                    self.lifetime_graph_canvas.axes.clear()

                    axes = self.lifetime_graph_canvas.axes

                    axes.hist(
                        lifetimes,
                        bins=lifetime_bins,
                        label="Lifetime data",
                        density=True,
                    )

                    if fit_exponential:

                        def exp_decay(t, A, k):
                            return A * np.exp(-k * t)

                        bin_centers = (
                            bin_edges[:-1] + bin_edges[1:]
                        ) / 2  # Calculate bin centers
                        params, cov = curve_fit(
                            exp_decay, bin_centers, hist, p0=[1, 0.1]
                        )

                        axes.plot(
                            bin_centers,
                            exp_decay(bin_centers, *params),
                            "b--",
                            lw=2,
                            label=f"Fit: A={params[0]:.2f}, k={params[1]:.2f}",
                        )

                    axes.set_xlabel("Fluorophore Lifetime (Frames)")
                    axes.set_ylabel("Probability Density")

                    axes.set_xlim(min_lifetime, max_lifetime)
                    axes.legend()

                    self.lifetime_graph_canvas.canvas.draw()

                    print("Lifetime histogram plotted")

        except:
            print(traceback.format_exc())

    def get_shapes_layer(self):

        layer_names = [layer.name for layer in self.viewer.layers]

        if "Shapes" not in layer_names:
            properties = {"mode": [], "ndim": 2}
            shapes_layer = self.viewer.add_shapes(
                name="Shapes",
                face_color="transparent",
                edge_color="red",
                edge_width=0.1,
                ndim=2,
                properties=properties,
            )
        else:
            shapes_layer = self.viewer.layers["Shapes"]

        return shapes_layer

    def on_add_layer(self, event):

        if event.value.name == "Shapes":

            properties = {"mode": [], "ndim": 2}

            self.shapes_layer = self.viewer.layers["Shapes"]
            self.shapes_layer.properties = properties

            self.shapes_layer.events.data.connect(self.shapes_layer_updated)

            self.shapes_layer.current_edge_color = list(
                mcolors.to_rgb("green")
            )
            self.shapes_layer.current_face_color = [0, 0, 0, 0]
            self.shapes_layer.current_edge_width = 1
