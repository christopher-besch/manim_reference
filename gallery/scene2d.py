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
            previous_path = path.copy()
            previous_path.add_points_as_corners([dot.get_center()])
            path.become(previous_path)

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


# todo: understand this
class MovingZoomedSceneAround(ZoomedScene):
    def __init__(self, **kwargs):
        # setup zoomed camera
        ZoomedScene.__init__(
            self,
            zoom_factor=0.3,
            zoomed_display_height=1,
            zoomed_display_width=6,
            image_frame_stroke_width=20,
            zoomed_camera_config={"default_frame_stroke_width": 3},
            **kwargs
        )

    def construct(self):
        dot = Dot().shift(UL * 2)
        # background image
        image = ImageMobject(np.uint8([[0, 100, 30, 200],
                                       [255, 0, 5, 33]]))
        image.height = 7
        # text at original place
        frame_text = Text("Frame", color=PURPLE, font_size=67)
        # text at zoom
        zoomed_camera_text = Text("Zoomed camera", color=RED, font_size=67)

        self.add(image, dot)
        # get frame shown in zoomed camera and zoomed camera itself
        zoomed_camera = self.zoomed_camera
        zoomed_display = self.zoomed_display
        # get frames
        frame = zoomed_camera.frame
        zoomed_display_frame = zoomed_display.display_frame

        # input
        frame.move_to(dot)
        frame.set_color(PURPLE)
        # output
        zoomed_display_frame.set_color(RED)
        zoomed_display.shift(DOWN)

        zd_rect = BackgroundRectangle(zoomed_display, fill_opacity=0, buff=MED_SMALL_BUFF)
        # purpose unknown
        self.add_foreground_mobject(zd_rect)

        unfold_camera = UpdateFromFunc(zd_rect, lambda rect: rect.replace(zoomed_display))

        frame_text.next_to(frame, DOWN)

        # create camera frame and zoom
        self.play(Create(frame), FadeIn(frame_text, shift=UP))
        self.activate_zooming()

        self.play(self.get_zoomed_display_pop_out_animation(), unfold_camera)
        zoomed_camera_text.next_to(zoomed_display_frame, DOWN)
        self.play(FadeIn(zoomed_camera_text, shift=UP))
        scale_factor = [0.5, 1.5, 0]
        self.play(
            frame.animate.scale(scale_factor),
            zoomed_display.animate.scale(scale_factor),
            FadeOut(zoomed_camera_text),
            FadeOut(frame_text),
        )
        self.wait()
        self.play(ScaleInPlace(zoomed_display, 2))
        self.wait()
        self.play(frame.animate.shift(2.5 * DOWN))
        self.wait()
        self.play(self.get_zoomed_display_pop_out_animation(), unfold_camera, rate_func=lambda t: smooth(1 - t))
        self.play(Uncreate(zoomed_display_frame), FadeOut(frame))
        self.wait()


class OpeningManim(Scene):
    def construct(self):
        title = Tex(r"This is some \LaTeX")
        basel = MathTex(r"\sum_{n=1}^\infty \frac{1}{n^2} = \frac{\pi^2}{6}")
        VGroup(title, basel).arrange(DOWN)
        self.play(Write(title), FadeIn(basel, shift=DOWN))
        self.wait()

        # transform tex to top left and morph
        transform_title = Tex(r"That was a transform")
        transform_title.to_corner(UP + LEFT)
        self.play(Transform(title, transform_title), LaggedStart(*[FadeOut(obj, shift=DOWN) for obj in basel]))
        self.wait()

        grid = NumberPlane()
        grid_title = Tex(r"This is a grid", font_size=72)
        # shall replace other title
        grid_title.move_to(transform_title)

        # title has to be on top of grid
        self.add_foreground_mobject(grid_title)
        self.add(grid)
        self.play(
            # actually replace other title
            FadeOut(title),
            FadeIn(grid_title, shift=UP),
            # lag_ratio=0 -> everything gets added at the same time
            # default 1 -> no two things happen at the same time
            Create(grid, run_time=3, lag_ratio=0.1)
        )
        self.wait()

        # transform plane
        grid_transform_title = Tex(r"That was a non-linear function \\ applied to the grid")
        grid_transform_title.move_to(grid_title, UL)
        grid.prepare_for_nonlinear_transform()
        self.play(grid.animate.apply_function(
            lambda p: p + np.array([np.sin(p[1]),
                                    np.sin(p[0]),
                                    0])
        ), run_time=3)
        self.wait()
        self.play(Transform(grid_title, grid_transform_title))
        self.wait()


class SineCurveUnitCircle(Scene):
    def show_axis(self):
        x_start = np.array([-6, 0, 0])
        x_end = np.array([6, 0, 0])
        x_axis = Line(x_start, x_end)

        y_start = np.array([-4, -2, 0])
        y_end = np.array([-4, 2, 0])
        y_axis = Line(y_start, y_end)

        self.add(x_axis, y_axis)
        self.add_x_labels()

        self.origin_point = np.array([-4, 0, 0])
        self.curve_start = np.array([-3, 0, 0])

    def add_x_labels(self):
        x_labels = [
            MathTex(r"\pi"),
            MathTex(r"2 \pi"),
            MathTex(r"3 \pi"),
            MathTex(r"4 \pi"),
        ]

        for i in range(len(x_labels)):
            x_labels[i].next_to(np.array([-1 + 2*i, 0, 0]), DOWN)
            self.add(x_labels[i])

    def show_circle(self):
        circle = Circle(radius=1)
        circle.move_to(self.origin_point)
        self.add(circle)
        self.circle = circle

    def move_dot_and_draw_curve(self):
        orbit = self.circle
        origin_point = self.origin_point

        dot = Dot(radius=0.08, color=YELLOW)
        dot.move_to(orbit.point_from_proportion(0))
        self.t_offset = 0
        rate = 0.25

        def go_around_circle(mob, dt):
            self.t_offset += (dt * rate)
            mob.move_to(orbit.point_from_proportion(self.t_offset % 1))

        def get_line_to_circle():
            return Line(origin_point, dot.get_center(), color=BLUE)

        def get_line_to_curve():
            x = self.curve_start[0] + self.t_offset * 4
            y = dot.get_center()[1]
            return Line(dot.get_center(), np.array([x, y, 0]), color=YELLOW_A, stroke_width=2)

        # actual sin curve is made out of many lines
        self.curve = VGroup()
        self.curve.add(Line(self.curve_start, self.curve_start))

        def get_curve():
            last_line = self.curve[-1]
            x = self.curve_start[0] + self.t_offset * 4
            y = dot.get_center()[1]
            new_line = Line(last_line.get_end(), np.array([x, y, 0]), color=YELLOW_D)
            self.curve.add(new_line)

            return self.curve

        dot.add_updater(go_around_circle)

        # create mobject and constantly update/replace using same function
        origin_to_circle_line = always_redraw(get_line_to_circle)
        dot_to_curve_line = always_redraw(get_line_to_curve)
        sine_curve_line = always_redraw(get_curve)

        self.add(dot)
        self.add(orbit, origin_to_circle_line, dot_to_curve_line, sine_curve_line)
        self.wait(8.5)

        dot.remove_updater(go_around_circle)

    def construct(self):
        self.show_axis()
        self.show_circle()
        self.move_dot_and_draw_curve()
        self.wait()
