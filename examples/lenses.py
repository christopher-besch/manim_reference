from manim import *


class LenseExample(Scene):
    def construct(self):
        c1 = Circle(3).move_to(2*LEFT)
        c2 = Circle(3).move_to(2*RIGHT)
        lense = Intersection(c1, c2, color=YELLOW, fill_opacity=1, stroke_width=0)
        self.add(lense)

        # self.shoot_ray(lense, 0.5)
        self.shoot_ray(lense, 0.6, 1.0, 1.4)
        # self.shoot_ray(lense, 0.7)

    def shoot_ray(self, lense, alpha, eta, eta_prime):
        tangent = TangentLine(lense, alpha=alpha)
        self.add(tangent)
        perpendicular = tangent.copy().rotate(PI/2)
        self.add(perpendicular)

        intersection = Point(lense.point_from_proportion(alpha))
        ray1 = Line(intersection.copy().shift(LEFT), intersection)
        self.add(ray1)

        ang1 = Angle(ray1, perpendicular)
        print(ang1.get_value() / DEGREES)

        ray2 = perpendicular.copy().rotate(np.arcsin(eta/eta_prime * np.sin(ang1.get_value())))
        self.add(ray2)
