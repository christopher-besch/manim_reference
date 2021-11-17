from manim import *


class LenseExample(Scene):
    def construct(self):

        c1 = Circle(20).move_to(19.5*LEFT)
        c2 = Circle(20).move_to(19.5*RIGHT)
        lense = Intersection(c1, c2, color=BLUE, fill_opacity=1, stroke_width=0)
        self.add(lense)

        for i in np.arange(-4.5, 4.5, 0.01):
            self.shoot_ray(c1, c2, i, 1.0, 1.4, ORANGE)

    def intersect(self, circle_center, radius, ray_origin, inclination):
        """Intersection between circle and ray."""
        center_to_origin = ray_origin - circle_center

        a = inclination.dot(inclination)
        half_b = center_to_origin.dot(inclination)
        c = center_to_origin.dot(center_to_origin) - radius**2

        discriminant = half_b**2 - a*c
        assert discriminant >= 0

        # find nearest root
        t = (-half_b - np.sqrt(discriminant)) / a
        if (t < 0):
            t = (-half_b + np.sqrt(discriminant)) / a
        return ray_origin + t * inclination

    def refract(self, c: Circle, ray_origin, inclination, eta_air, eta_glass, into):
        inter = Point(self.intersect(c.get_center(), c.radius, ray_origin, inclination))
        ray = Line(ray_origin, inter)

        norm = inter.get_center() - c.get_center()
        theta = angle_between_vectors(ray.get_vector(), -norm)
        # get signed angle
        if ray.get_vector().dot(rotate_vector(norm, PI/2)) < 0:
            theta = -theta
        if into:
            theta_p = np.arcsin(eta_air/eta_glass*np.sin(theta))
            out_vec = rotate_vector(-norm, theta_p)
        else:
            theta_p = np.arcsin(eta_glass/eta_air*np.sin(theta))
            out_vec = rotate_vector(norm, theta_p)

        return inter, out_vec

    def shoot_ray(self, c1: Circle, c2: Circle, start_y, eta_air, eta_glass, color):
        start = Point((-8, start_y, 0))
        inter1, vec1 = self.refract(c2, start.get_center(), RIGHT, eta_air, eta_glass, True)
        ray1 = Line(start, inter1, color=color, stroke_width=1)
        self.add(ray1)

        inter2, vec2 = self.refract(c1, start.get_center(), vec1, eta_air, eta_glass, False)
        ray2 = Line(inter1, inter2, color=color, stroke_width=1)
        self.add(ray2)

        ray3 = Line(inter2, inter2.get_center() + 3*vec2, color=color, stroke_width=1)
        self.add(ray3)
