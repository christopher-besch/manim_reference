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
