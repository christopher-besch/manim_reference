from manim import *


class BraceAnnotation(Scene):
    def construct(self):
        # line with dots at ends
        dot = Dot([-2, -1, 0])
        dot2 = Dot([2, 1, 0])
        line = Line(dot.get_center(), dot2.get_center()).set_color(ORANGE)
        # create horiaontal brace at line
        b1 = Brace(line)
        b1text = b1.get_text("Horizontal distance")
        # create brace at line <- get orthogonal vector to line for direction
        b2 = Brace(line, direction=line.copy().rotate(PI/2).get_unit_vector())
        b2text = b2.get_tex("x-x_1")
        self.add(line, dot, dot2, b1, b2, b1text, b2text)


class VectorArrow(Scene):
    def construct(self):
        dot = Dot(ORIGIN)
        arrow = Arrow(dot.get_center(), [2, 2, 0], buff=0)
        numberplane = NumberPlane()
        # set texts
        origin_text = Text("(0, 0)").next_to(dot, DOWN)
        tip_text = Text("(2, 2)").next_to(arrow.get_end(), RIGHT)
        self.add(numberplane, dot, arrow, origin_text, tip_text)


class GradientImageFromArray(Scene):
    def construct(self):
        n = 256
        # create n*n image
        image_array = np.uint8(
            [[i * 256 / n for i in range(0, n)] for _ in range(0, n)]
        )
        image = ImageMobject(image_array).scale(2)
        image.background_rectangle = SurroundingRectangle(image, GREEN)
        self.add(image, image.background_rectangle)


class PointMovingOnShapes(Scene):
    def construct(self):
        circle = Circle(radius=1, color=BLUE)
        dot = Dot()
        dot2 = dot.copy().shift(RIGHT)
        self.add(dot)

        line = Line([3, 0, 0], [5, 0, 0])
        self.add(line)

        self.play(GrowFromCenter(circle))
        # both work
        # self.play(Transform(dot, dot2))
        self.play(dot.animate.shift(RIGHT))
        # move dot along circle
        self.play(MoveAlongPath(dot, circle), run_time=2, rate_func=linear)
        # rotate dot in mid-air
        self.play(Rotating(dot, about_point=[2, 0, 0]), run_time=1.5)
        self.wait()


class MovingAround(Scene):
    def construct(self):
        square = Square(color=BLUE, fill_opacity=1)

        self.play(square.animate.shift(LEFT))
        self.play(square.animate.set_fill(ORANGE))
        self.play(square.animate.scale(0.3))
        self.play(square.animate.rotate(0.4))


class MovingAngle(Scene):
    def construct(self):
        rotation_center = LEFT
        theta_tracker = ValueTracker(110)
        # unmoving horizontal line
        line = Line(LEFT, RIGHT)
        line_ref = line.copy()

        line_moving = Line(LEFT, RIGHT)
        # rotate to initial setting
        line_moving.rotate(theta_tracker.get_value() * DEGREES, about_point=rotation_center)
        a = Angle(line, line_moving, radius=0.5, other_angle=False)
        tex = MathTex(r"\theta").move_to(
            # get middle of arch of virtual angle
            Angle(line, line_moving, radius=0.5 + 3 * SMALL_BUFF, other_angle=False).point_from_proportion(0.5)
        )

        self.add(line, line_moving, a, tex)
        self.wait()

        line_moving.add_updater(
            lambda x: x.become(line_ref.copy()).rotate(
                theta_tracker.get_value() * DEGREES, about_point=rotation_center
            )
        )

        a.add_updater(
            lambda x: x.become(Angle(line, line_moving, radius=0.5, other_angle=False))
        )
        tex.add_updater(
            lambda x: x.move_to(
                Angle(
                    line, line_moving, radius=0.5 + 3 * SMALL_BUFF, other_angle=False
                ).point_from_proportion(0.5)
            )
        )

        self.play(theta_tracker.animate.set_value(40))
        self.play(theta_tracker.animate.increment_value(140))
        self.play(tex.animate.set_color(RED), run_time=0.5)
        self.play(theta_tracker.animate.set_value(350))
