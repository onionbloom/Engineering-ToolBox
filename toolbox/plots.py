# This module contains functions that will plot the given data
from bokeh.models import ColumnDataSource, HoverTool, PrintfTickFormatter, CategoricalColorMapper
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from toolbox.plotStyle import plot_styler


def stabTrimPlot(dataframe):
    hover = HoverTool(tooltips=[('altitude', '@ALTITUDE'),
                                ('time', '@DATETIME{%H:%M:%S}')],
                                # format time to H:M:S without the date. details: DatetimeTickFormatter
                                formatters = {'@DATETIME': 'datetime'},
                                # display a tooltip whenever the cursor is vertically in line with a glyph
                                mode='vline')

    mapper = CategoricalColorMapper(factors=['setosa', 'virginica', 'versicolor'],
                                    palette=['#247ba0', '#f25f5c', '#ffe066'])

    source = ColumnDataSource(dataframe)
    plot = figure(title='Aircraft Flight Envelope', tools=[hover, 'pan', 'box_zoom', 'reset'],
                  x_axis_label='UTC Time (hh:mm:ss)', y_axis_label='Aircraft Altitude (ft)', x_axis_type='datetime')

    plot.line('DATETIME', 'ALTITUDE', source=source , line_width=2, color="blue")

    plot_styler(plot)

    return plot
