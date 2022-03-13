from manim import *


class HelloLaTeX(Scene):
    def construct(self):
        tex = Tex(r"\LaTeX", color=BLUE, font_size=144)
        self.add(tex)


class MathTeXDemo(Scene):
    def construct(self):
        # same as Tex but within align*
        arrow0 = MathTex(r"\xrightarrow{x^6y^8}", font_size=96)
        arrow1 = Tex(r"\begin{align*}\xrightarrow{x^6y^8}\end{align*}", font_size=96)
        self.add(VGroup(arrow0, arrow1).arrange(DOWN))


class AddPackageLaTeX(Scene):
    def construct(self):
        template = TexTemplate()
        template.add_to_preamble(r"\usepackage{mathrsfs}")
        tex = MathTex(r"\mathscr{H} \rightarrow \mathbb{H}", tex_template=template, font_size=144)
        self.add(tex)


class LaTeXSubstrings(Scene):
    def construct(self):
        tex = Tex('Hello', r'$\bigstar$', r'\LaTeX', font_size=144)
        # color entire second substring red
        tex.set_color_by_tex('igsta', RED)
        self.add(tex)


class LaTeXSubstringColoring(Scene):
    def construct(self):
        equation = MathTex(
            r"e^x = x^0 + x^1 + \frac{1}{2} x^2 + \frac{1}{6} x^3 + \cdots + \frac{1}{n!} x^n + \cdots",
            substrings_to_isolate=["x", "+"]
        )
        # coloring entire substring -> x has to be isolated
        equation.set_color_by_tex("x", YELLOW)
        equation.set_color_by_tex("+", RED)
        self.add(equation)


class MatchingEquationParts(Scene):
    def construct(self):
        eq1 = MathTex("a^2 + b^2 = c^2")
        eq2 = MathTex("a^2 = c^2 - b^2")
        self.add(eq1)
        self.wait(0.5)
        self.play(TransformMatchingTex(eq1, eq2))
        self.wait(0.5)
        self.remove(eq2)

        # creating substrings
        eq3 = MathTex("{{a^2}} + {{b^2}} = {{c^2}}")
        eq4 = MathTex("{{a^2}} = {{c^2}} - {{b^2}}")
        self.add(eq3)
        self.wait(0.5)
        self.play(TransformMatchingTex(eq3, eq4))
        self.wait(0.5)


class LaTeXMathFonts(Scene):
    def construct(self):
        # using predefined TexFontTemplates
        tex = Tex(r"$x^2 + y^2 = z^2$", tex_template=TexFontTemplates.french_cursive, font_size=144)
        self.add(tex)


class LaTeXTemplateLibrary(Scene):
    def construct(self):
        # using TexTemplateLibrary for chinese text
        tex = Tex(r"Hello 你好 \LaTeX", tex_template=TexTemplateLibrary.ctex, font_size=144)
        self.add(tex)


class CircuitTikZ(Scene):
    def construct(self):
        latex_temp = TexTemplate()
        latex_temp.add_to_preamble(r"\usepackage{circuitikz}")

        circuit = Tex(r"""
        \begin{circuitikz}
            \draw (0,0)
            to[V,v=$U_q$] (0,1.5);
            \draw (0,1.5)
            to[nos] (2,1.5)
            to[C=$C$] (2,0)
            to[short] (0,0);
            \draw (2,1.5)
            to[short] (4,1.5)
            to[R=$R$] (4,0)
            to[short] (2,0);
            \draw (4,1.5)
            to[short] (6,1.5)
            to[voltmeter] (6,0)
            to[short] (4,0);
        \end{circuitikz}
        """, tex_template=latex_temp, color=WHITE, fill_opacity=0, stroke_width=3)
        self.add(circuit)
