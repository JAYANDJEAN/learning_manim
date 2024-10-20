import os

import numpy as np
from manim import (TAU, PI, ORIGIN, Z_AXIS, Y_AXIS, LEFT, RIGHT, normalize, Mobject, Line3D, perpendicular_bisector)
from manim.mobject.opengl.opengl_mobject import OpenGLGroup, OpenGLMobject
from manim.mobject.opengl.opengl_surface import OpenGLSurface

from utils import mol_parser, Element, pdb_parser


class OpenGLSphere(OpenGLSurface):
    def __init__(
            self,
            center=ORIGIN,
            **kwargs,
    ):
        super().__init__(
            self.uv_func,
            u_range=(0, TAU),
            v_range=(0, PI),
            **kwargs,
        )

        self.shift(center)

    def uv_func(self, u, v):
        return np.array(
            [np.cos(u) * np.sin(v), np.sin(u) * np.sin(v), -np.cos(v)],
        )


class ThreeDAtom(OpenGLSphere):
    def __init__(self, element: Element, cords=np.array([0, 0, 0]), **kwargs):
        self.center = cords
        self.cords = cords
        self.element = element
        super().__init__(center=self.center, color=element.color, **kwargs)
        self.scale(0.2)


class ThreeDCylinder(OpenGLSurface):
    def __init__(self, radius: float = 1, height: float = 2, direction: np.ndarray = Z_AXIS,
                 v_range=(0.0, TAU), resolution=(24, 24), **kwargs) -> None:
        self.direction = direction
        self._height = height
        self.radius = radius
        super().__init__(
            self.uv_func,
            resolution=resolution,
            u_range=[-self._height / 2, self._height / 2],
            v_range=v_range,
            **kwargs,
        )
        self._current_phi = 0
        self._current_theta = 0
        self._rotate_to_direction()

    def uv_func(self, u: float, v: float) -> np.ndarray:
        height = u
        phi = v
        r = self.radius
        return np.array([r * np.cos(phi), r * np.sin(phi), height])

    def _rotate_to_direction(self):
        x, y, z = self.direction
        r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
        if r > 0:
            theta = np.arccos(z / r)
        else:
            theta = 0
        if x == 0:
            if y == 0:  # along the z axis
                phi = 0
            else:  # along the x axis
                phi = np.arctan(np.inf)
                if y < 0:
                    phi += PI
        else:
            phi = np.arctan(y / x)
        if x < 0:
            phi += PI
        # undo old rotation (in reverse direction)
        self.rotate(-self._current_phi, Z_AXIS, about_point=ORIGIN)
        self.rotate(-self._current_theta, Y_AXIS, about_point=ORIGIN)
        # do new rotation
        self.rotate(theta, Y_AXIS, about_point=ORIGIN)
        self.rotate(phi, Z_AXIS, about_point=ORIGIN)
        # store new values
        self._current_theta = theta
        self._current_phi = phi


class ThreeDLine(ThreeDCylinder):
    def __init__(self, start: np.ndarray = LEFT, end: np.ndarray = RIGHT,
                 thickness: float = 0.05, color=None, **kwargs):
        super().__init__(**kwargs)
        self.end = None
        self.start = None
        self.direction = None
        self.length = None
        self.vect = None
        self.thickness = thickness
        self.set_start_and_end_attrs(start, end, **kwargs)
        if color is not None:
            self.set_color(color)

    def set_start_and_end_attrs(self, start: np.ndarray, end: np.ndarray, **kwargs) -> None:
        """Sets the start and end points of the line.
        If either ``start`` or ``end`` are :class:`Mobjects <.Mobject>`,
        this gives their centers.
        Parameters
        ----------
        start
            Starting point or :class:`Mobject`.
        end
            Ending point or :class:`Mobject`.
        """
        rough_start = self.pointify(start)
        rough_end = self.pointify(end)
        self.vect = rough_end - rough_start
        self.length = np.linalg.norm(self.vect)
        self.direction = normalize(self.vect)
        # Now that we know the direction between them,
        # we can the appropriate boundary point from
        # start and end, if they're mobjects
        self.start = self.pointify(start, self.direction)
        self.end = self.pointify(end, -self.direction)
        super().__init__(
            height=np.linalg.norm(self.vect),
            radius=self.thickness,
            direction=self.direction,
            **kwargs,
        )
        self.shift((self.start + self.end) / 2)

    def pointify(self, mob_or_point: Mobject or float, direction: np.ndarray = None) -> np.ndarray:
        """Gets a point representing the center of the :class:`Mobjects <.Mobject>`.
        Parameters
        ----------
        mob_or_point
            :class:`Mobjects <.Mobject>` or point whose center should be returned.
        direction
            If an edge of a :class:`Mobjects <.Mobject>` should be returned, the direction of the edge.
        Returns
        -------
        :class:`numpy.array`
            Center of the :class:`Mobjects <.Mobject>` or point, or edge if direction is given.
        """
        if isinstance(mob_or_point, (Mobject, OpenGLMobject)):
            mob = mob_or_point
            if direction is None:
                return mob.get_center()
            else:
                return mob.get_boundary_point(direction)
        return np.array(mob_or_point)

    @classmethod
    def parallel_to(cls, line: Line3D, point=ORIGIN, length: float = 5, **kwargs) -> Line3D:
        """Returns a line parallel to another line going through
        a given point.
        Parameters
        ----------
        line
            The line to be parallel to.
        point
            The point to pass through.
        length
            Length of the parallel line.
        kwargs
            Additional parameters to be passed to the class.
        Returns
        -------
        :class:`Line3D`
            Line parallel to ``line``.

        Examples
        --------
        .. manim:: ParallelLineExample
            :save_last_frame:

            class ParallelLineExample(ThreeDScene):
                def construct(self):
                    self.set_camera_orientation(PI / 3, -PI / 4)
                    ax = ThreeDAxes((-5, 5), (-5, 5), (-5, 5), 10, 10, 10)
                    line1 = Line3D(RIGHT * 2, UP + OUT, color=RED)
                    line2 = Line3D.parallel_to(line1, color=YELLOW)
                    self.add(ax, line1, line2)
        """
        point = np.array(point)
        vect = normalize(line.vect)
        return cls(point + vect * length / 2, point - vect * length / 2, **kwargs)

    @classmethod
    def perpendicular_to(cls, line: Line3D, point=ORIGIN, length: float = 5, **kwargs) -> Line3D:
        """Returns a line perpendicular to another line going through
        a given point.
        Parameters
        ----------
        line
            The line to be perpendicular to.
        point
            The point to pass through.
        length
            Length of the perpendicular line.
        kwargs
            Additional parameters to be passed to the class.
        Returns
        -------
        :class:`Line3D`
            Line perpendicular to ``line``.

        Examples
        --------
        .. manim:: PerpLineExample
            :save_last_frame:

            class PerpLineExample(ThreeDScene):
                def construct(self):
                    self.set_camera_orientation(PI / 3, -PI / 4)
                    ax = ThreeDAxes((-5, 5), (-5, 5), (-5, 5), 10, 10, 10)
                    line1 = Line3D(RIGHT * 2, UP + OUT, color=RED)
                    line2 = Line3D.perpendicular_to(line1, color=BLUE)
                    self.add(ax, line1, line2)
        """
        point = np.array(point)
        norm = np.cross(line.vect, point - line.start)
        if all(np.linalg.norm(norm) == np.zeros(3)):
            raise ValueError("Could not find the perpendicular.")

        start, end = perpendicular_bisector([line.start, line.end], norm)
        vect = normalize(end - start)
        return cls(point + vect * length / 2, point - vect * length / 2, **kwargs)


class ThreeDBond(OpenGLGroup):
    """
    Used to create a tridimensional bond.
    Uses an origin atom and a target atom to be drawn.
    """

    def __init__(self, from_atom, to_atom, bond_type, *mobjects, **kwargs):
        self.from_atom = from_atom
        self.to_atom = to_atom
        super().__init__(**kwargs)
        self.add(*mobjects)
        if bond_type in [1, ]:
            self.bonds = self.add_single_bond()
        elif bond_type in [2, 5, 7]:
            self.bonds = self.add_double_bond()
        elif bond_type in [3, ]:
            self.bonds = self.add_triple_bond()
        else:
            raise Exception(
                f"Unknown or unsupported bond type at bond with from atom {self.from_atom} "
                f"with index {self.from_atom.index}and to atom {self.to_atom} "
                f"with index {self.from_atom.index}"
            )

        self.add(self.bonds)

    def add_single_bond(self):
        bond = OpenGLGroup()
        midpoint = (self.to_atom.cords + self.from_atom.cords) / 2
        half_bond_1 = ThreeDLine(
            self.from_atom.cords, midpoint, color=self.from_atom.element.color
        )
        half_bond_2 = ThreeDLine(
            self.to_atom.cords, midpoint, color=self.to_atom.element.color
        )
        bond.add(half_bond_1, half_bond_2)
        return bond

    def add_double_bond(self):
        bond = OpenGLGroup()
        base_bond = self.add_single_bond()
        unit = self.get_perpendicular_unit_vector(self.from_atom.cords, self.to_atom.cords)
        second_bond = base_bond.copy()
        second_bond.shift(-0.12 * unit)
        base_bond.shift(0.12 * unit)
        bond.add(base_bond, second_bond)
        return bond

    def add_triple_bond(self):
        bond = OpenGLGroup()
        base_bond = self.add_single_bond()
        unit = self.get_perpendicular_unit_vector(self.from_atom.cords, self.to_atom.cords)
        second_bond = (base_bond.copy())
        third_bond = (base_bond.copy())
        second_bond.shift(-0.15 * unit)
        third_bond.shift(0.15 * unit)
        bond.add(base_bond, second_bond, third_bond)
        return bond

    def get_perpendicular_unit_vector(self, point_a, point_b):
        direction = point_b - point_a
        if direction[0] == 0 and direction[1] == 0:
            perpendicular_vector = np.cross(direction, np.array([0, 1, 0]))
        else:
            perpendicular_vector = np.cross(direction, np.array([0, 0, 1]))
        return perpendicular_vector / np.linalg.norm(perpendicular_vector)


class ThreeDMolecule(OpenGLGroup):
    def __init__(self, filename: str = None, add_bonds: bool = True, add_atoms: bool = True, **kwargs):
        super().__init__(**kwargs)
        file_extension = os.path.splitext(filename)[1]
        if file_extension == '.mol':
            atoms, bonds = mol_parser(file=filename)
        elif file_extension == '.pdb':
            atoms, bonds = pdb_parser(file=filename)
        else:
            atoms, bonds = None, None
        atoms_group = OpenGLGroup()
        bonds_group = OpenGLGroup()
        for _, atom in atoms.items():
            atoms_group.add(ThreeDAtom(Element(atom.get("element")), atom.get("cords")))

        for index, bonds_list in bonds.items():
            from_atom = atoms_group[index - 1]
            for bond in bonds_list:
                to_atom = atoms_group[bond.get("to") - 1]
                bond_type = bond.get("type")
                bonds_group.add(
                    ThreeDBond(
                        from_atom=from_atom, to_atom=to_atom, bond_type=int(bond_type)
                    )
                )
        if add_bonds:
            self.add(bonds_group)
        if add_atoms:
            self.add(atoms_group)
        self.move_to(ORIGIN)
