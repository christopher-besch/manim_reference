from manim import *


class LenseExample(Scene):
    def construct(self):
        c1 = Circle(10).move_to(9*LEFT)
        c2 = Circle(10).move_to(9*RIGHT)
        lense = Intersection(c1, c2, color=YELLOW, fill_opacity=1, stroke_width=0)
        self.add(lense)

        self.shoot_ray(c1, c2, 1, 1.0, 1.4)
        self.shoot_ray(c1, c2, 0.5, 1.0, 1.4)
        self.shoot_ray(c1, c2, 0, 1.0, 1.4)
        self.shoot_ray(c1, c2, -0.5, 1.0, 1.4)
        self.shoot_ray(c1, c2, -1, 1.0, 1.4)

    def intersect(self, circle_origin, radius, ray_origin, inclination, outer=True):
        """Intersection between circle and ray."""
        center_to_origin = ray_origin - circle_origin

        a = np.linalg.norm(inclination)**2
        half_b = center_to_origin.dot(inclination)
        c = np.linalg.norm(center_to_origin)**2 - radius**2

        discriminant = half_b * half_b - a * c
        assert discriminant > 0

        if outer:
            t = (-half_b - np.sqrt(discriminant) / a)
        else:
            t = (-half_b + np.sqrt(discriminant) / a)
        return ray_origin + t * inclination

    def shoot_ray(self, c1: Circle, c2: Circle, start_y, eta_air, eta_glass):
        start = Point((-4, start_y, 0))
        inter1 = Point(self.intersect(c2.get_center(), c2.radius, start.get_center(), RIGHT, True))
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
