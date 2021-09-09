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
        self.play(Transform(dot, dot2))
        # too short timing with this
        # dot.animate.shift(RIGHT)
        # move dot along circle
        self.play(MoveAlongPath(dot, circle), run_time=2, rate_func=linear)
        # rotate dot in mid-air
        self.play(Rotating(dot, about_point=[2, 0, 0]), run_time=1.5)
        self.wait()
