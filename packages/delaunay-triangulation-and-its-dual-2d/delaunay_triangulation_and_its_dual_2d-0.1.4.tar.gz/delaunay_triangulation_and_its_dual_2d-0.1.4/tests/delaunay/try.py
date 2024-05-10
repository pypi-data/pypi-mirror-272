import sys

import matplotlib.collections
import matplotlib.pyplot as plt
import numpy as np
import scipy.spatial

import delaunay_triangulation_and_its_dual_2d
import delaunay_triangulation_and_its_dual_2d.exceptions


def visualize_mocked_scipy_spatial_delaunay_and_voronoi():
    points = np.array(
        [[0, 0], [3, 0], [1, 1], [3, 2], [4, 2], [1, 3], [2, 4], [4, 4]],
        dtype=np.float32,
    )
    delaunay = delaunay_triangulation_and_its_dual_2d.Delaunay(points=points)
    delaunay_diagram = delaunay.get_mocked_scipy_spatial_delaunay()
    fig = scipy.spatial.delaunay_plot_2d(delaunay_diagram)
    barycentric_dual_diagram = (
        delaunay.get_barycentric_dual_as_mocked_scipy_spatial_voronoi()
    )
    fig = scipy.spatial.voronoi_plot_2d(
        barycentric_dual_diagram, ax=fig.axes[0]
    )
    voronoi_diagram = delaunay.get_mocked_scipy_spatial_voronoi()
    fig = scipy.spatial.voronoi_plot_2d(voronoi_diagram, ax=fig.axes[0])
    fig.axes[0].set_xlim(-2, 6)
    fig.axes[0].set_ylim(-2, 6)
    plt.grid()
    plt.show()


# def visualize_are_line_segments_within_rectangle():
#     line_segments = np.random.randint(0, 10, (5, 2, 2)).astype(np.float_)
#     line_segments_within_rectangle = delaunay_triangulation_and_its_dual_2d.Delaunay._are_line_segments_within_rectangle(
#         min_x=2, min_y=2, max_x=8, max_y=8, line_segments=line_segments
#     )
#     colors = np.where(line_segments_within_rectangle, "green", "red")
#     fig, ax = plt.subplots()
#     # Reference: https://stackoverflow.com/a/21357666
#     ax.add_collection(
#         matplotlib.collections.LineCollection(line_segments, colors=colors)
#     )
#     rectangle = np.array(
#         [
#             [[2, 2], [2, 8]],
#             [[2, 8], [8, 8]],
#             [[8, 8], [8, 2]],
#             [[8, 2], [2, 2]],
#         ]
#     ).astype(np.float_)
#     ax.add_collection(
#         matplotlib.collections.LineCollection(rectangle, colors="blue")
#     )
#     ax.autoscale()
#     ax.grid()
#     plt.show()


def try_compute_bounded_line_segments_of_dual():
    points = np.array(
        [[0, 0], [3, 0], [1, 1], [3, 2], [4, 2], [1, 3], [2, 4], [4, 4]],
        dtype=np.float32,
    )
    delaunay = delaunay_triangulation_and_its_dual_2d.Delaunay(points=points)
    bounded_line_segments = delaunay.compute_bounded_line_segments_of_dual(
        dual="voronoi"
    )
    print("bounded_line_segments.shape: ", bounded_line_segments.shape)


if __name__ == "__main__":
    # Reference: https://stackoverflow.com/a/52837375
    globals()[sys.argv[1]]()
