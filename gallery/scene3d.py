from manim import *


class FixedInFrameMObjectTest(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        # position camera
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        text3d = Text("This is a 3D text")
        # text not impacted by camera movement
        self.add_fixed_in_frame_mobjects(text3d)
        text3d.to_corner(UL)
        self.add(axes)
        self.wait()


class ThreeDLightSourcePosition(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        sphere = Surface(
            lambda u, v: np.array([1.5 * np.cos(u) * np.cos(v),
                                   1.5 * np.cos(u) * np.sin(v),
                                   1.5 * np.sin(u)]),
            v_range=[0, TAU], u_range=[-PI / 2, PI / 2],
            # define texture of surface
            checkerboard_colors=[RED_D, RED_E], resolution=(15, 32)
        )
        # set source of light
        self.renderer.camera.light_source.move_to(3*IN)
        self.set_camera_orientation(phi=75*DEGREES, theta=30*DEGREES)
        self.add(axes, sphere)


class ThreeDCameraRotation(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        circle = Circle()
        self.set_camera_orientation(phi=75*DEGREES, theta=30*DEGREES)
        self.add(circle, axes)
        # ambience good
        # anti-clockwise
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait()
        self.stop_ambient_camera_rotation()
        # move back
        self.move_camera(phi=75*DEGREES, theta=30*DEGREES)
        self.wait()

        # illusion good?
        # todo: why orientation flip?
        self.begin_3dillusion_camera_rotation(rate=2)
        self.wait(PI/2)
        self.stop_3dillusion_camera_rotation()
        self.move_camera(phi=75*DEGREES, theta=30*DEGREES)


class ThreeDSurfacePlot(ThreeDScene):
    def construct(self):
        resolution_fa = 42
        self.set_camera_orientation(phi=75*DEGREES, theta=-30*DEGREES)

        def param_gauss(u, v):
            x = u
            y = v
            sigma = 0.4
            mu = [0, 0]
            d = np.linalg.norm(np.array([x - mu[0], y - mu[1]]))
            z = np.exp(-(d ** 2 / (2 * sigma ** 2)))
            return np.array([x, y, z])

        gauss_plane = Surface(
            param_gauss,
            resolution=(resolution_fa, resolution_fa),
            v_range=[-2, 2],
            u_range=[-2, 2],
        )

        gauss_plane.scale_about_point(2, ORIGIN)
        gauss_plane.set_style(fill_opacity=1, stroke_color=GREEN)
        gauss_plane.set_fill_by_checkerboard(ORANGE, BLUE, opacity=0.5)
        axes = ThreeDAxes()
        self.add(axes, gauss_plane)
