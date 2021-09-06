from manim import *


class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(PINK, opacity=0.5)

        square = Square()
        square.rotate(PI / 4)

        self.play(Create(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(square))


class Shapes(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        triangle = Triangle()

        circle.shift(LEFT)
        square.shift(UP)
        triangle.shift(RIGHT)

        self.add(circle, square, triangle)
        # without wait manim creates single image
        self.wait(1)


class MobjectPlacement(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        triangle = Triangle()

        # absolute coordinates
        circle.move_to(2*LEFT)
        # place square to left of circle
        # relative to passed in object
        square.next_to(circle, LEFT)
        # align left border of triangle to left border of circle
        triangle.align_to(circle, LEFT)

        self.add(circle, square, triangle)
        self.wait(1)


class MobjectStyling(Scene):
    def construct(self):
        # functions returns modified object
        circle = Circle().shift(LEFT)
        square = Square().shift(UP)
        triangle = Triangle().shift(RIGHT)

        circle.set_stroke(color=GREEN, width=20)
        square.set_fill(YELLOW, opacity=1.0)
        triangle.set_fill(PINK, opacity=0.5)

        # add objects in defined order to screen
        self.add(circle, square, triangle)
        self.wait(1)


class SomeAnimations(Scene):
    def construct(self):
        square = Square()
        self.add(square)

        # interpolate between fully transparent and fully opaque square
        self.play(FadeIn(square))
        self.play(Rotate(square, PI/4))
        self.play(FadeOut(square))

        self.wait(1)


class AnimateExample(Scene):
    def construct(self):
        square = Square().set_fill(RED, opacity=1.0)
        self.add(square)

        # any property can be animated
        self.play(square.animate.set_fill(WHITE))
        self.wait(1)

        # default run_time=1
        self.play(square.animate.shift(UP).rotate(PI/3), run_time=3)
        self.wait(1)


class Count(Animation):
    def __init__(self, number: DecimalNumber, start: float, end: float, **kwargs) -> None:
        # pass number as mobject the animation controls
        super().__init__(number, **kwargs)

        self.start = start
        self.end = end

    def interpolate_mobject(self, alpha: float) -> None:
        # set value of DecimalNumber according to alpha
        value = self.start + (alpha * (self.end - self.start))
        self.mobject.set_value(value)


class CountingScene(Scene):
    def construct(self):
        number = DecimalNumber().set_color(WHITE).scale(5)
        # keep DecimalNumber centered at all time
        number.add_updater(lambda number: number.move_to(ORIGIN))

        self.add(number)
        self.wait()

        self.play(Count(number, 0, 100), run_time=2,
                  rate_func=linear)
        self.wait()


class MobjectExample(Scene):
    def construct(self):
        p1 = [-1, -1, 0]
        p2 = [1, -1, 0]
        p3 = [1, 1, 0]
        p4 = [-1, 1, 0]
        # create square without left side
        a = Line(p1, p2). \
            append_points(Line(p2, p3).get_points()). \
            append_points(Line(p3, p4).get_points())
        point_start = a.get_start()
        point_end = a.get_end()
        point_center = a.get_center()
        # UL = UPP + LEFT
        self.add(Text(f"a.get_start() = {np.round(point_start,2).tolist()}", font_size=24).to_edge(UR).set_color(YELLOW))
        self.add(Text(f"a.get_end() = {np.round(point_end,2).tolist()}", font_size=24).next_to(self.mobjects[-1], DOWN).set_color(RED))
        self.add(Text(f"a.get_center() = {np.round(point_center,2).tolist()}", font_size=24).next_to(self.mobjects[-1], DOWN).set_color(BLUE))

        self.add(Dot(a.get_start()).set_color(YELLOW).scale(2))
        self.add(Dot(a.get_end()).set_color(RED).scale(2))
        self.add(Dot(a.get_top()).set_color(GREEN_A).scale(2))
        self.add(Dot(a.get_bottom()).set_color(GREEN_D).scale(2))
        self.add(Dot(a.get_center()).set_color(BLUE).scale(2))
        self.add(Dot(a.point_from_proportion(0.5)).set_color(ORANGE).scale(2))
        # little white dots on line
        self.add(*[Dot(x) for x in a.get_points()])
        self.add(a)

        self.wait()


class ExampleTransform(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        m1 = Square().set_color(RED)
        m1.set_fill(GREEN, opacity=1.0)
        m2 = Rectangle().set_color(RED).rotate(0.2)
        # transform from m1 to m2
        self.play(Transform(m1, m2))


class ExampleRotation(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        m1a = Square().set_color(RED).shift(LEFT)
        m1b = Circle().set_color(RED).shift(LEFT)
        m2a = Square().set_color(BLUE).shift(RIGHT)
        m2b = Circle().set_color(BLUE).shift(RIGHT)

        points = m2a.points
        # rotate together and not both clockwise -> rotate right target square pi/2 left
        points = np.roll(points, int(len(points)/4), axis=0)
        m2a.points = points

        # perform multiple transformations at once
        self.play(Transform(m1a, m1b), Transform(m2a, m2b), run_time=1)
