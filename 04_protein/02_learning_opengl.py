from manim import *
from manim.mobject.opengl.opengl_mobject import OpenGLGroup, OpenGLMobject
import moderngl


class OpenGLSurface(OpenGLMobject):
    shader_dtype = [
        ("point", np.float32, (3,)),
        ("du_point", np.float32, (3,)),
        ("dv_point", np.float32, (3,)),
        ("color", np.float32, (4,)),
    ]
    shader_folder = "surface"

    def __init__(
            self,
            uv_func=None,
            u_range=None,
            v_range=None,
            resolution=None,
            axes=None,
            color=GREY,
            colorscale=None,
            colorscale_axis=2,
            opacity=1.0,
            gloss=0.3,
            shadow=0.4,
            prefered_creation_axis=1,
            # For du and dv steps.  Much smaller and numerical error
            # can crop up in the shaders.
            epsilon=1e-5,
            render_primitive=moderngl.TRIANGLES,
            depth_test=True,
            shader_folder=None,
            **kwargs,
    ):
        self.passed_uv_func = uv_func
        self.u_range = u_range if u_range is not None else (0, 1)
        self.v_range = v_range if v_range is not None else (0, 1)
        # Resolution counts number of points sampled, which for
        # each coordinate is one more than the the number of
        # rows/columns of approximating squares
        self.resolution = resolution if resolution is not None else (101, 101)
        self.axes = axes
        self.colorscale = colorscale
        self.colorscale_axis = colorscale_axis
        self.prefered_creation_axis = prefered_creation_axis
        # For du and dv steps.  Much smaller and numerical error
        # can crop up in the shaders.
        self.epsilon = epsilon

        self.triangle_indices = None
        super().__init__(
            color=color,
            opacity=opacity,
            gloss=gloss,
            shadow=shadow,
            shader_folder=shader_folder if shader_folder is not None else "surface",
            render_primitive=render_primitive,
            depth_test=depth_test,
            **kwargs,
        )
        self.compute_triangle_indices()

    def uv_func(self, u, v):
        # To be implemented in subclasses
        if self.passed_uv_func:
            return self.passed_uv_func(u, v)
        return (u, v, 0.0)

    def compute_triangle_indices(self):
        # TODO, if there is an event which changes
        # the resolution of the surface, make sure
        # this is called.
        nu, nv = self.resolution
        if nu == 0 or nv == 0:
            self.triangle_indices = np.zeros(0, dtype=int)
            return
        index_grid = np.arange(nu * nv).reshape((nu, nv))
        indices = np.zeros(6 * (nu - 1) * (nv - 1), dtype=int)
        indices[0::6] = index_grid[:-1, :-1].flatten()  # Top left
        indices[1::6] = index_grid[+1:, :-1].flatten()  # Bottom left
        indices[2::6] = index_grid[:-1, +1:].flatten()  # Top right
        indices[3::6] = index_grid[:-1, +1:].flatten()  # Top right
        indices[4::6] = index_grid[+1:, :-1].flatten()  # Bottom left
        indices[5::6] = index_grid[+1:, +1:].flatten()  # Bottom right
        self.triangle_indices = indices

    # pointwise_become_partial、get_shader_data
    def get_surface_points_and_nudged_points(self):
        points = self.points
        k = len(points) // 3
        return points[:k], points[k: 2 * k], points[2 * k:]

    # pointwise_become_partial
    def get_partial_points_array(self, points, a, b, resolution, axis):
        if len(points) == 0:
            return points
        nu, nv = resolution[:2]
        points = points.reshape(resolution)
        max_index = resolution[axis] - 1
        lower_index, lower_residue = integer_interpolate(0, max_index, a)
        upper_index, upper_residue = integer_interpolate(0, max_index, b)
        if axis == 0:
            points[:lower_index] = interpolate(
                points[lower_index],
                points[lower_index + 1],
                lower_residue,
            )
            points[upper_index + 1:] = interpolate(
                points[upper_index],
                points[upper_index + 1],
                upper_residue,
            )
        else:
            shape = (nu, 1, resolution[2])
            points[:, :lower_index] = interpolate(
                points[:, lower_index],
                points[:, lower_index + 1],
                lower_residue,
            ).reshape(shape)
            points[:, upper_index + 1:] = interpolate(
                points[:, upper_index],
                points[:, upper_index + 1],
                upper_residue,
            ).reshape(shape)
        return points.reshape((nu * nv, *resolution[2:]))

    # get_shader_data
    def fill_in_shader_color_info(self, shader_data):
        """Fills in the shader color data when the surface
        is all one color.

        Parameters
        ----------
        shader_data
            The vertices of the surface.

        Returns
        -------
        shader_dtype
            An array containing the shader data (vertices and
            color of each vertex)
        """
        self.read_data_to_shader(shader_data, "color", "rgbas")
        return shader_data

    # get_shader_data
    def _get_color_by_value(self, s_points):
        """Matches each vertex to a color associated to it's z-value.

        Parameters
        ----------
        s_points
           The vertices of the surface.

        Returns
        -------
        List
            A list of colors matching the vertex inputs.
        """
        if type(self.colorscale[0]) in (list, tuple):
            new_colors, pivots = [
                [i for i, j in self.colorscale],
                [j for i, j in self.colorscale],
            ]
        else:
            new_colors = self.colorscale

            pivot_min = self.axes.z_range[0]
            pivot_max = self.axes.z_range[1]
            pivot_frequency = (pivot_max - pivot_min) / (len(new_colors) - 1)
            pivots = np.arange(
                start=pivot_min,
                stop=pivot_max + pivot_frequency,
                step=pivot_frequency,
            )

        return_colors = []
        for point in s_points:
            axis_value = self.axes.point_to_coords(point)[self.colorscale_axis]
            if axis_value <= pivots[0]:
                return_colors.append(color_to_rgba(new_colors[0], self.opacity))
            elif axis_value >= pivots[-1]:
                return_colors.append(color_to_rgba(new_colors[-1], self.opacity))
            else:
                for i, pivot in enumerate(pivots):
                    if pivot > axis_value:
                        color_index = (axis_value - pivots[i - 1]) / (
                                pivots[i] - pivots[i - 1]
                        )
                        color_index = max(min(color_index, 1), 0)
                        temp_color = interpolate_color(
                            new_colors[i - 1],
                            new_colors[i],
                            color_index,
                        )
                        break
                return_colors.append(color_to_rgba(temp_color, self.opacity))

        return return_colors

    def init_points(self):
        dim = self.dim
        nu, nv = self.resolution
        u_range = np.linspace(*self.u_range, nu)
        v_range = np.linspace(*self.v_range, nv)

        # Get three lists:
        # - Points generated by pure uv values
        # - Those generated by values nudged by du
        # - Those generated by values nudged by dv
        point_lists = []
        for du, dv in [(0, 0), (self.epsilon, 0), (0, self.epsilon)]:
            uv_grid = np.array([[[u + du, v + dv] for v in v_range] for u in u_range])
            point_grid = np.apply_along_axis(lambda p: self.uv_func(*p), 2, uv_grid)
            point_lists.append(point_grid.reshape((nu * nv, dim)))
        # Rather than tracking normal vectors, the points list will hold on to the
        # infinitesimal nudged values alongside the original values.  This way, one
        # can perform all the manipulations they'd like to the surface, and normals
        # are still easily recoverable.
        self.set_points(np.vstack(point_lists))

    def pointwise_become_partial(self, smobject, a, b, axis=None):
        assert isinstance(smobject, OpenGLSurface)
        if axis is None:
            axis = self.prefered_creation_axis
        if a <= 0 and b >= 1:
            self.match_points(smobject)
            return self

        nu, nv = smobject.resolution
        self.set_points(
            np.vstack(
                [
                    self.get_partial_points_array(
                        arr.copy(),
                        a,
                        b,
                        (nu, nv, 3),
                        axis=axis,
                    )
                    for arr in smobject.get_surface_points_and_nudged_points()
                ],
            ),
        )
        return self

    def get_shader_data(self):
        """Called by parent Mobject to calculate and return
        the shader data.

        Returns
        -------
        shader_dtype
            An array containing the shader data (vertices and
            color of each vertex)
        """
        s_points, du_points, dv_points = self.get_surface_points_and_nudged_points()
        shader_data = np.zeros(len(s_points), dtype=self.shader_dtype)
        if "points" not in self.locked_data_keys:
            shader_data["point"] = s_points
            shader_data["du_point"] = du_points
            shader_data["dv_point"] = dv_points
            if self.colorscale:
                if not hasattr(self, "color_by_val"):
                    self.color_by_val = self._get_color_by_value(s_points)
                shader_data["color"] = self.color_by_val
            else:
                self.fill_in_shader_color_info(shader_data)
        return shader_data

    def get_shader_vert_indices(self):
        return self.triangle_indices


class OpenGLSphere(OpenGLSurface):
    def __init__(self, center=ORIGIN, **kwargs):
        super().__init__(self.uv_func, u_range=(0, TAU), v_range=(0, PI), **kwargs)
        self.shift(center)
        self.scale(0.4)

    def uv_func(self, u, v):
        return np.array([np.cos(u) * np.sin(v), np.sin(u) * np.sin(v), -np.cos(v)])


class SphereGroup(OpenGLGroup):
    def __init__(self, cords: List = None, **kwargs):
        super().__init__(**kwargs)
        atoms_group = OpenGLGroup()
        for c in cords:
            atoms_group.add(OpenGLSphere(c))

        self.add(atoms_group)
        self.move_to(ORIGIN)


class OpenGLSpherePoint(OpenGLMobject):
    def __init__(self, input_points=None, **kwargs):
        super().__init__(**kwargs)
        self.input_points = input_points

    def init_points(self):
        pass


class Atoms(ThreeDScene):
    config.renderer = "opengl"
    config.background_color = "#1C1C1C"

    def construct(self):
        self.add(SphereGroup([ORIGIN, LEFT, RIGHT]))


Atoms().render()
