from manim import *


class Path_mapper(VMobject):
    def __init__(self, path_source: VMobject, num_of_path_points=100, **kwargs):
        super().__init__(**kwargs)
        self.num_of_path_points = num_of_path_points
        self.path = path_source
        self.generate_length_map()

    def generate_length_map(self):
        norms = np.array(0)
        for k in range(self.path.get_num_curves()):
            norms = np.append(norms, self.path.get_nth_curve_length_pieces(k, sample_points=11))
        # add up length-pieces in array form
        self.pathdata_lengths = np.cumsum(norms)
        self.pathdata_alpha = np.linspace(0, 1, self.pathdata_lengths.size)

    def cubic_to_quads(self, cubic_points):
        # based on https://ttnghia.github.io/pdf/QuadraticApproximation.pdf
        q_points = np.empty((0, 3))
        gamma = 0.5
        q1 = cubic_points[0, :] + 3 / 2 * gamma * (cubic_points[1, :] - cubic_points[0, :])
        q3 = cubic_points[3, :] + 3 / 2 * (1 - gamma) * (cubic_points[2, :] - cubic_points[3, :])
        q2 = (1 - gamma) * q1 + gamma * q3
        q0 = cubic_points[0, :]
        q4 = cubic_points[3, :]
        q_points = np.append(q_points, (q0, q1, q2, q2, q3, q4), axis=0)
        return q_points

    def calc_len_bezier_quad(self, points):
        a = points[0, :]
        b = points[1, :]
        c = points[2, :]

        B = b - a
        F = c - b
        A = F - B
        nF = np.linalg.norm(F)
        nA = np.linalg.norm(A)
        nB = np.linalg.norm(B)
        if nA > 1e-8:
            L = (nF * np.dot(A, F) - nB * np.dot(A, B)) / (nA ** 2) + (nA ** 2 * nB ** 2 - np.dot(A, B) ** 2) / \
                (nA ** 3) * (np.log(nA * nF + np.dot(A, F)) - np.log(nA * nB + np.dot(A, B)))
            return L
        else:
            return np.linalg.norm(a - c)

    def calc_len_with_quads(self):
        L = 0
        for k in range(self.path.get_num_curves()):
            points = self.path.get_nth_curve_points(k)
            quads = self.cubic_to_quads(points)
            L0 = self.calc_len_bezier_quad(quads[:3, :])
            L1 = self.calc_len_bezier_quad(quads[3:, :])
            L += L0 + L1
        return L

    def get_path_length(self):
        return self.pathdata_lengths[-1]

    def alpha_from_length(self, s):
        if hasattr(s, '__iter__'):
            return [np.interp(t, self.pathdata_lengths, self.pathdata_alpha) for t in s]
        else:
            return np.interp(s, self.pathdata_lengths, self.pathdata_alpha)

    def length_from_alpha(self, a):
        if hasattr(a, '__iter__'):
            return [np.interp(t, self.pathdata_alpha, self.pathdata_lengths) for t in a]
        else:
            return np.interp(a, self.pathdata_alpha, self.pathdata_lengths)

    def equalize_alpha(self, a):
        'used for inverting the alpha behavior'
        return self.alpha_from_length(a * self.get_path_length())

    def equalize_rate_func(self, rate_func):
        '''
        Specifically made to be used with Create() animation.
        :param rate_func: rate function to be equalized
        :return: callable new rate function
        Example:
        class test_path_mapper_anim(Scene):
            def construct(self):
                mob1 = round_corners(Triangle(fill_color=TEAL,fill_opacity=0).scale(3),0.5)
                PM = Path_mapper(mob1)
                mob2 = mob1.copy()
                mob1.shift(LEFT * 2.5)
                mob2.shift(RIGHT * 2.5)

                self.play(Create(mob1,rate_func=PM.equalize_rate_func(smooth)),Create(mob2),run_time=5)
                self.wait()
        '''

        def eq_func(t: float):
            return self.equalize_alpha(rate_func(t))

        return eq_func

    def point_from_proportion(self, alpha: float) -> np.ndarray:
        '''
         Override original implementation.
         Should be the same, except it uses pre calculated length table and should be faster a bit.
        '''
        if hasattr(alpha, '__iter__'):
            values = self.alpha_from_length(alpha * self.get_path_length())
            ret = np.empty((0, 3))
            for a in values:
                if a == 1:
                    index = self.path.get_num_curves() - 1
                    remainder = 1
                else:
                    index = int(a * self.path.get_num_curves() // 1)
                    remainder = (a * self.path.get_num_curves()) % 1
                p = self.path.get_nth_curve_function(index)(remainder)
                ret = np.concatenate([ret, np.reshape(p, (1, 3))], axis=0)
            return ret
        else:
            a = self.alpha_from_length(alpha * self.get_path_length())
            if a == 1:
                index = self.path.get_num_curves() - 1
                remainder = 1
            else:
                index = int(a * self.path.get_num_curves() // 1)
                remainder = (a * self.path.get_num_curves()) % 1
            return self.path.get_nth_curve_function(index)(remainder)

    def get_length_between_points(self, b, a):
        '''
        Signed arc length between to points.
        :param b: second point
        :param a: first point
        :return: length (b-a)
        '''
        return self.length_from_alpha(b) - self.length_from_alpha(a)

    def get_length_between_points_wrapped(self, b, a):
        ''' This function wraps around the length between two points similar to atan2 method.
        Useful for closed mobjects.
        Returns distance value between -L/2...L/2 '''
        AB = self.get_length_between_points(b, a)
        L = self.get_path_length()
        return (AB % L - L / 2) % L - L / 2

    def get_length_between_points_tuple(self, b, a):
        ''' Function to get the 2 absolute lengths between 2 parameters on closed mobjects.
        Useful for closed mobjects.
        :returns tuple (shorter, longer)'''

        AB = abs(self.get_length_between_points(b, a))
        L = self.get_path_length()
        if AB > L / 2:
            return (L - AB), AB
        else:
            return AB, (L - AB)

    def get_bezier_index_from_length(self, s):
        a = self.alpha_from_length(s)
        nc = self.path.get_num_curves()
        indx = int(a * nc // 1)
        bz_a = a * nc % 1
        if indx == nc:
            indx = nc - 1
            bz_a = 1
        return (indx, bz_a)

    def get_tangent_unit_vector(self, s):
        # diff_bez_points = 1/3*(self.path.points[1:,:]-self.path.points[:-1,:])
        indx, bz_a = self.get_bezier_index_from_length(s)
        points = self.path.get_nth_curve_points(indx)
        dpoints = (points[1:, :] - points[:-1, :]) / 3
        bzf = bezier(dpoints)
        point = bzf(bz_a)
        return normalize(point)

    def get_tangent_angle(self, s):
        tv = self.get_tangent_unit_vector(s)
        return angle_of_vector(tv)

    def get_normal_unit_vector(self, s):
        tv = self.get_tangent_unit_vector(s)
        return rotate_vector(tv, PI / 2)

    def get_curvature_vector(self, s):
        indx, bz_a = self.get_bezier_index_from_length(s)
        points = self.path.get_nth_curve_points(indx)
        dpoints = (points[1:, :] - points[:-1, :]) * 3
        ddpoints = (dpoints[1:, :] - dpoints[:-1, :]) * 2
        deriv = bezier(dpoints)(bz_a)
        dderiv = bezier(ddpoints)(bz_a)
        curv = np.cross(deriv, dderiv) / (np.linalg.norm(deriv) ** 3)
        return curv

    def get_curvature(self, s):
        return np.linalg.norm(self.get_curvature_vector(s))


class Dashed_line_mobject(VDict):
    def __init__(self, target_mobject: VMobject,
                 num_dashes=15,
                 dashed_ratio=0.5,
                 dash_offset=0.0,
                 **kwargs):
        super().__init__(**kwargs)
        self.path = Path_mapper(target_mobject, num_of_path_points=10 * target_mobject.get_num_curves())
        # self.path.add_updater(lambda mob: mob.generate_length_map())

        dshgrp = self.generate_dash_mobjects(
            **self.generate_dash_pattern_dash_distributed(num_dashes, dash_ratio=dashed_ratio, offset=dash_offset)
        )
        self.add({'dashes': dshgrp})
        self['dashes'].match_style(target_mobject)

    def generate_dash_pattern_metric(self, dash_len, space_len, num_dashes, offset=0):
        ''' generate dash pattern in metric curve-length space'''
        period = dash_len + space_len
        n = num_dashes
        full_len = self.path.get_path_length()
        dash_starts = [(i * period + offset) for i in range(n)]
        dash_ends = [(i * period + dash_len + offset) for i in range(n)]
        k = 0
        while k < len(dash_ends):
            if dash_ends[k] < 0:
                dash_ends.pop(k)
                dash_starts.pop(k)
            k += 1

        k = 0
        while k < len(dash_ends):
            if dash_starts[k] > full_len:
                dash_ends.pop(k)
                dash_starts.pop(k)
            k += 1
        return {'dash_starts': dash_starts, 'dash_ends': dash_ends}

    def generate_dash_pattern_dash_distributed(self, num_dashes, dash_ratio=0.5, offset=0.0):
        full_len = self.path.get_path_length()
        period = full_len / num_dashes
        dash_len = period * dash_ratio
        space_len = period * (1 - dash_ratio)
        n = num_dashes + 2

        return self.generate_dash_pattern_metric(dash_len, space_len, n, offset=(offset - 1) * period)

    def generate_dash_mobjects(self, dash_starts=[0], dash_ends=[1]):
        ref_mob = self.path.path
        a_list = self.path.alpha_from_length(dash_starts)
        b_list = self.path.alpha_from_length(dash_ends)
        ret = []
        for i in range(len(dash_starts)):
            mobcopy = VMobject().match_points(ref_mob)
            ret.append(mobcopy.pointwise_become_partial(mobcopy, a_list[i], b_list[i]))
        return VGroup(*ret)
