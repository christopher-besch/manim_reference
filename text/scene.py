from manim import *
import manimpango


class HelloWorld(Scene):
    def construct(self):
        text = Text("Hello World", font_size=144)
        self.add(text)


class SingleLineColor(Scene):
    def construct(self):
        text = MarkupText(f'all in red <span fgcolor="{YELLOW}">except this</span>', color=RED)
        self.add(text)


class FontsExample(Scene):
    def construct(self):
        ft = Text("JetBrains Mono NL", font="JetBrains Mono NL")
        self.add(ft)


class SlantsExample(Scene):
    def construct(self):
        a = Text("Normal", slant=NORMAL)
        b = Text("Italic", slant=ITALIC)
        c = Text("Oblique", slant=OBLIQUE)
        a.next_to(b, UP)
        c.next_to(b, DOWN)
        self.add(a, b, c)


class DifferentWeight(Scene):
    def construct(self):
        g = VGroup()
        # show all different weights
        weight_list = dict(sorted({weight: manimpango.Weight(weight).value for weight in manimpango.Weight}.items(), key=lambda x: x[1]))
        for weight in weight_list:
            g += Text(weight.name, weight=weight.name, font="Open Sans")
        self.add(g.arrange(DOWN).scale(0.5))


class Textt2cExample(Scene):
    def construct(self):
        # make second to penultimate char blue
        t2cindices = Text("Hello", t2c={"[1:-1]": BLUE}).move_to(LEFT)
        # make "rl" word red
        t2cwords = Text("World", t2c={"rl": RED}).next_to(t2cindices, RIGHT)
        # problems with ligatures -> entire ligature gets red (only < should be red)
        brokenligatures = Text("Broken<=", font="JetBrains Mono", t2c={"[-2:-1]": RED, "Broken": YELLOW}).next_to(t2cindices, DOWN)
        self.add(t2cindices, t2cwords, brokenligatures)


class GradientExample(Scene):
    def construct(self):
        t = Text("Hello World!", gradient=(RED, BLUE, GREEN), font_size=96)
        self.add(t)


class t2gExample(Scene):
    def construct(self):
        t2gindices = Text(
            "Hello",
            t2g={
                "[1:-1]": (RED, GREEN),
            },
        ).move_to(LEFT)
        t2gwords = Text(
            "World",
            t2g={
                "World": (RED, BLUE),
            },
        ).next_to(t2gindices, RIGHT)
        self.add(t2gindices, t2gwords)


class LineSpacing(Scene):
    def construct(self):
        a = Text("Hello\nWorld", line_spacing=1)
        b = Text("Hello\nWorld", line_spacing=4)
        self.add(Group(a, b).arrange(LEFT, buff=5))


class DisableLigatures(Scene):
    def construct(self):
        li = Text("fl ligature", font_size=96)
        nli = Text("fl ligature", disable_ligatures=True, font_size=96)
        self.add(Group(li, nli).arrange(DOWN, buff=0.8))


class IterateColor(Scene):
    def construct(self):
        text = Text("Colors", font_size=96)
        # Text behaves like VGroups
        # ligatures broken
        for letter in text:
            letter.set_color(random_color())
        self.add(text)


class MarkupTest(Scene):
    def construct(self):
        text = MarkupText(
            f'<span underline="double" underline_color="{GREEN}">double green underline</span> in red text<span fgcolor="{YELLOW}"> except this</span>',
            color=RED,
            font_size=34
        )
        self.add(text)
