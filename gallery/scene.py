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

        line_moving = Line(rotation_center, RIGHT)
        # rotate to initial setting
        line_moving.rotate(theta_tracker.get_value() * DEGREES, about_point=rotation_center)
        # arch to be shown
        a = Angle(line, line_moving, radius=0.5, other_angle=False)
        tex = MathTex(r"\theta").move_to(
            # get middle of arch of virtual angle
            Angle(line, line_moving, radius=0.5 + 3 * SMALL_BUFF, other_angle=False).point_from_proportion(0.5)
        )

        self.add(line, line_moving, a, tex)
        self.wait()

        # this function get applied every frame
        # change angle according to theta_tracker
        line_moving.add_updater(
            lambda x: x.become(line_ref.copy()).rotate(
                theta_tracker.get_value() * DEGREES, about_point=rotation_center)
        )

        # update arch according to lines
        a.add_updater(
            lambda x: x.become(Angle(line, line_moving, radius=0.5, other_angle=False))
        )
        # update location of label according to lines
        tex.add_updater(
            lambda x: x.move_to(Angle(
                line, line_moving, radius=0.5 + 3 * SMALL_BUFF, other_angle=False
            ).point_from_proportion(0.5))
        )

        # play animation
        self.play(theta_tracker.animate.set_value(40))
        self.play(theta_tracker.animate.increment_value(140))
        self.play(tex.animate.set_color(RED), run_time=0.5)
        self.play(theta_tracker.animate.set_value(350))


class MovingDots(Scene):
    def construct(self):
        d1 = Dot(color=BLUE)
        d2 = Dot(color=GREEN)
        dg = VGroup(d1, d2).arrange(UP, buff=1)
        l1 = Line(d1.get_center(), d2.get_center()).set_color(RED)
        # change x and y coordinates of dots
        x = ValueTracker(0)
        y = ValueTracker(0)
        d1.add_updater(lambda z: z.set_x(x.get_value()))
        d2.add_updater(lambda z: z.set_y(y.get_value()))
        # reset line
        l1.add_updater(lambda z: z.become(Line(d1.get_center(), d2.get_center())))
        self.add(d1, d2, l1)
        self.play(x.animate.set_value(5))
        self.play(y.animate.set_value(4))
        self.wait(1)


class MovingGroupToTarget(Scene):
    def construct(self):
        group = VGroup(Dot(LEFT), Dot(ORIGIN),
                       Dot(RIGHT, color=RED),
                       Dot(2 * RIGHT).scale(1.4))
        target = Dot([4, 3, 0], color=YELLOW)
        self.add(group, target)
        # align third element in group to target
        self.play(group.animate.shift(target.get_center() - group[2].get_center()))


class MovingFrameBox(Scene):
    def construct(self):
        text = MathTex(
            r"\frac{d}{dx} f(x) g(x) =",
            r"f(x) \frac{d}{dx} g(x)",
            r"+",
            r"g(x) \frac{d}{dx} f(x)"
        )
        # prettily write text with boxes around
        self.play(Write(text))
        framebox1 = SurroundingRectangle(text[1], buff=0.1)
        framebox2 = SurroundingRectangle(text[3], buff=0.1)
        self.play(Create(framebox1))
        self.wait()
        # seems to be the same as ReplacementTransform
        self.play(Transform(framebox1, framebox2))
        self.wait()


class RotationUpdater(Scene):
    def construct(self):
        # dt = time in seconds since last call
        def updater_forth(mobj, dt):
            mobj.rotate_about_origin(dt)

        def updater_back(mobj, dt):
            mobj.rotate_about_origin(-dt)

        line_reference = Line(ORIGIN, LEFT).set_color(WHITE)
        line_moving = Line(ORIGIN, LEFT).set_color(YELLOW)
        line_moving.add_updater(updater_forth)

        self.add(line_reference, line_moving)
        self.wait(2)
        # exchange updater
        line_moving.remove_updater(updater_forth)
        line_moving.add_updater(updater_back)
        self.wait(2)
        line_moving.remove_updater(updater_back)
        self.wait(0.5)


class PointWithTrace(Scene):
    def construct(self):
        path = VMobject()
        dot = Dot()
        path.set_points_as_corners([dot.get_center(), dot.get_center()])

        # add current location of dot as corner of path
        def update_path(path):
            # copy seem to be unnecessary
            path.add_points_as_corners([dot.get_center()])
            # previous_path = path.copy()
            # previous_path.add_points_as_corners([dot.get_center()])
            # path.become(previous_path)

        # now only do stuff with dot and path will follow
        path.add_updater(update_path)
        self.add(path, dot)
        self.play(Rotating(dot, radians=PI, about_point=RIGHT, run_time=2))
        self.wait()
        self.play(dot.animate.shift(UP))
        self.play(dot.animate.shift(LEFT))
        self.wait()


class SinAndCosFunctionPlot(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-10, 10.3, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=10,
            axis_config={"color": GREEN},
            x_axis_config={
                # go from -10 to 10 inclusive
                "numbers_to_include": np.arange(-10, 10.01, 2),
                "numbers_with_elongated_ticks": np.arange(-10, 10.01, 2)
            },
            # no pointy arrow
            tips=False
        )
        axes_labels = axes.get_axis_labels()
        sin_graph = axes.get_graph(lambda x: np.sin(x), color=BLUE)
        cos_graph = axes.get_graph(lambda x: np.cos(x), color=RED)

        # set label for individual graph
        sin_label = axes.get_graph_label(sin_graph, r"\sin(x)", x_val=-10, direction=UP/2)
        cos_label = axes.get_graph_label(cos_graph, r"\cos(x)")

        # vertical line
        vert_line = axes.get_vertical_line(axes.i2gp(TAU, cos_graph), color=YELLOW, line_func=Line)
        # with label
        line_label = axes.get_graph_label(cos_graph, r"x=2\pi", x_val=TAU, direction=UR, color=WHITE)

        plot = VGroup(axes, sin_graph, cos_graph, vert_line)
        labels = VGroup(axes_labels, sin_label, cos_label, line_label)
        self.add(plot, labels)


class ArgMinExample(Scene):
    def construct(self):
        # use default numbers and elongated ticks
        ax = Axes(x_range=[0, 10], y_range=[0, 100, 10], axis_config={"include_tip": False})
        # set labels
        labels = ax.get_axis_labels(x_label="x", y_label="f(x)")

        t = ValueTracker(0)

        # add actual function
        def func(x):
            return 2 * (x - 5) ** 2
        graph = ax.get_graph(func, color=MAROON)

        # add dot that moves along graph
        # ax.coords_to_point = ax.c2p
        dot = Dot(point=ax.coords_to_point(t.get_value(), func(t.get_value())))
        dot.add_updater(lambda x: x.move_to(ax.c2p(t.get_value(), func(t.get_value()))))

        # numerically calculate minimum
        # 200 dots in x_range
        x_space = np.linspace(*ax.x_range[:2], 200)
        minimum_index = func(x_space).argmin()

        self.add(ax, labels, graph, dot)
        # move to minimum
        self.play(t.animate.set_value(x_space[minimum_index]))
        self.wait()


class GraphAreaPlot(Scene):
    def construct(self):
        ax = Axes(
            x_range=[0, 5],
            y_range=[0, 6],
            x_axis_config={"numbers_to_include": [2, 3]},
            tips=False,
        )

        labels = ax.get_axis_labels()

        # define shown curves
        curve1 = ax.get_graph(lambda x: 4 * x - x ** 2, x_range=[0, 4], color=BLUE_C)
        curve2 = ax.get_graph(lambda x: 0.8 * x ** 2 - 3 * x + 4, x_range=[0, 4], color=GREEN_B)

        # vertical lines
        line1 = ax.get_vertical_line(ax.input_to_graph_point(2, curve1), color=YELLOW)
        line2 = ax.get_vertical_line(ax.i2gp(3, curve1), color=YELLOW)

        # vertical bars on left
        area1 = ax.get_area(curve1, x_range=[0.3, 0.6], dx_scaling=40, color=BLUE)
        # area between curves
        area2 = ax.get_area(curve2, [2, 3], bounded=curve1, color=GREY, opacity=0.2)

        self.add(ax, labels, curve1, curve2, line1, line2, area1, area2)


class HeatDiagramPlot(Scene):
    def construct(self):
        ax = Axes(
            x_range=[0, 40, 5],
            y_range=[-8, 32, 5],
            x_length=9,
            y_length=6,
            x_axis_config={"numbers_to_include": np.arange(0, 40, 5)},
            y_axis_config={"numbers_to_include": np.arange(-5, 34, 5)},
            tips=False,
        )
        labels = ax.get_axis_labels(x_label=MathTex(r"\Delta Q"), y_label=MathTex(r"T[\circ C]"))

        x_vals = [0, 8, 38, 39]
        y_vals = [20, 0, 0, -5]
        graph = ax.get_line_graph(x_values=x_vals, y_values=y_vals)

        self.add(ax, labels, graph)


class FollowingGraphCamera(MovingCameraScene):
    def construct(self):
        # to be able to return to start
        self.camera.frame.save_state()

        # create the axes and curve
        ax = Axes(x_range=[-1, 10], y_range=[-1, 10])
        graph = ax.get_graph(lambda x: np.sin(x), color=BLUE, x_range=[0, 3 * PI])

        # create dots at start and end of graph
        dot1 = Dot(ax.i2gp(graph.t_min, graph))
        dot2 = Dot(ax.i2gp(graph.t_max, graph))
        moving_dot = Dot(dot1.get_center(), color=ORANGE)

        self.add(ax, graph, dot1, dot2, moving_dot)
        # move camera to moving_dot and zoom in <- scale camera with 0.5
        self.play(self.camera.frame.animate.scale(0.5).move_to(moving_dot))

        def update_curve(mob):
            mob.move_to(moving_dot.get_center())

        self.camera.frame.add_updater(update_curve)
        # move dot along graph
        self.play(MoveAlongPath(moving_dot, graph, rate_func=linear))
        self.camera.frame.remove_updater(update_curve)

        self.play(Restore(self.camera.frame))
