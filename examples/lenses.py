from manim import *


class LenseExample(Scene):
    def construct(self):
        c1 = Circle(2).move_to(1*LEFT)
        c2 = Circle(2).move_to(1*RIGHT)
        lense = Intersection(c1, c2, color=YELLOW, fill_opacity=1, stroke_width=0)
        self.add(lense, c2)

        # self.shoot_ray(c1, c2, 1, 1.0, 1.4)
        # self.shoot_ray(c1, c2, 0.5, 1.0, 1.4)
        # self.shoot_ray(c1, c2, 0, 1.0, 1.4)
        # self.shoot_ray(c1, c2, -0.5, 1.0, 1.4)
        # self.shoot_ray(c1, c2, -1, 1.0, 1.4)

        start = Point((-2, 0, 0))
        end = Point(self.intersect(c2.get_center(), c2.radius, start.get_center(), 2*RIGHT + UP))
        line = Line(start, end)
        self.add(start, end, line)

    def intersect(self, circle_center, radius, ray_origin, inclination):
        """Intersection between circle and ray."""
        center_to_origin = ray_origin - circle_center
        # inclination = normalize(inclination)

        a = inclination.dot(inclination)
        half_b = center_to_origin.dot(inclination)
        c = center_to_origin.dot(center_to_origin) - radius**2

        discriminant = half_b**2 - a*c
        assert discriminant >= 0

        # find nearest root
        t = (-half_b - np.sqrt(discriminant) / a)
        # if (t < 0):
        # t = (-b + np.sqrt(discriminant) / 2*a)
        return ray_origin + t * inclination

    def shoot_ray(self, c1: Circle, c2: Circle, start_y, eta_air, eta_glass):
        start = Point((-4, start_y, 0))
        inter1 = Point(self.intersect(c2.get_center(), c2.radius, start.get_center(), UR, True))
        self.add(inter1)
        ray1 = Line(start, inter1)
        self.add(ray1)

        norm1_vec = inter1.get_center() - c2.get_center()
        norm1 = Line(c2.get_center(), inter1)
        theta = angle_between_vectors(ray1.get_vector(), -norm1_vec)
        # get signed angle
        if ray1.get_vector().dot(rotate_vector(norm1_vec, PI/2)) < 0:
            theta = -theta

        r = Line(inter1, inter1.get_center() + rotate_vector(-norm1_vec, theta))
        # self.add(r)

        inter2 = Point(self.intersect(c1.get_center(), c1.radius, inter1.get_center(), DL, False))
        ray2 = Line(inter1, inter2)
        self.add(ray2)
