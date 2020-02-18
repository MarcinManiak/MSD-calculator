from bokeh.plotting import figure, output_file, show
from bokeh.palettes import Dark2_5 as palette
import itertools



class Graph:
    """
    Cretas MSD grpah
    """
    def __init__(self, timestep, title):
        """
        :param timestep: duration of timestep or saving frames (if longer than timestep) in ps!
        :param title: Title of graph
        """
        self.timestep = timestep
        self.title = title
        self.colors = itertools.cycle(palette)


    def plot(self, *msd):
        """
        Builds msd graph
        :param msd: dictionary with keys = numer of step,values = MSD. Choose msd.msdX/Y/Y or msd.msd for sum of directions. You can plot many msd
        """
        print(f'---Creating plot---')

        p = figure(plot_width=1200, background_fill_color="honeydew", background_fill_alpha=0.2, tooltips=[
            ("Time [ps]", "$x"),
            ("MSD [A*A]", "$y)"),
        ])

        p.yaxis.axis_label = "MSD [A*A]"
        p.yaxis.axis_label_text_font_style = "italic"

        p.xaxis.axis_label = "Time [ps]"
        p.xaxis.axis_label_text_font_style = "italic"

        for pair in msd:
            self.x = []
            self.y = []
            dic = pair[0]
            legend = pair[1]
            for key, value in dic.items():
                self.x.append(key*self.timestep)
                self.y.append(value)

            p.line(self.x, self.y, legend_label=f"{legend}", line_width=2, color=next(self.colors))

        try:
            p.legend.location = "top_left"
            output_file(f"{self.title}.html", title=f"{self.title}")
            show(p)
        except Exception as e:
            print(f'\n\n{e}')
            print('!Plot Not created!')
        else:
            print(f'---Plot {self.title} created---')
