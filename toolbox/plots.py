# This module contains functions that will plot the given data
from bokeh.models import ColumnDataSource, HoverTool, PrintfTickFormatter, CategoricalColorMapper, BoxAnnotation
from bokeh.plotting import figure, show
from bokeh.transform import factor_cmap
from toolbox.plotStyle import plot_styler


def stabTrimPlot(dataframe):
    """ Description text here """
    hover = HoverTool(tooltips=[('altitude', '@ALTITUDE'),
                                ('time', '@DATETIME{%H:%M:%S}')],
                      # format time to H:M:S without the date. details: DatetimeTickFormatter
                      formatters={'@DATETIME': 'datetime'},
                      # display a tooltip whenever the cursor is vertically in line with a glyph
                      mode='vline')

    mapper = CategoricalColorMapper(factors=['setosa', 'virginica', 'versicolor'],
                                    palette=['#247ba0', '#f25f5c', '#ffe066'])

    source = ColumnDataSource(dataframe)
    plot = figure(title='Aircraft Flight Envelope', tools=[hover, 'pan', 'box_zoom', 'reset'],
                  x_axis_label='UTC Time (hh:mm:ss)', y_axis_label='Aircraft Altitude (ft)', x_axis_type='datetime')

    plot_styler(plot)

    plot.line(x='DATETIME', y='ALTITUDE', source=source,
              line_width=2, color="blue")

    return plot


def flapAsymPlot(dataframe):
    """ Function to plot Flap Asymmetry parameters """
    hover = HoverTool(tooltips=[('Altitude', '@ALTITUDE ft'),
                                ('Time', '@DATETIME{%H:%M:%S}')],
                      formatters={'@DATETIME': 'datetime'},
                      mode='vline')

    source = ColumnDataSource(dataframe)
    dataframe['TE_FLPSK1TO8_VAL'] = (
        dataframe['TE_FLAPSKW_1'] - dataframe['TE_FLAPSKW_8']).abs()
    dataframe['TE_FLPSK2TO7_VAL'] = (
        dataframe['TE_FLAPSKW_2'] - dataframe['TE_FLAPSKW_7']).abs()
    dataframe['TE_FLPSK3TO6_VAL'] = (
        dataframe['TE_FLAPSKW_3'] - dataframe['TE_FLAPSKW_6']).abs()
    dataframe['TE_FLPSK4TO5_VAL'] = (
        dataframe['TE_FLAPSKW_4'] - dataframe['TE_FLAPSKW_5']).abs()
    source2 = ColumnDataSource(dataframe)

    # Create the figures to house the plots
    plot = figure(title='Aircraft Flight Envelope', tools=[hover, 'pan', 'box_zoom', 'wheel_zoom', 'save', 'reset'],
                  x_axis_label='UTC Time (hh:mm:ss)', y_axis_label='Aircraft Altitude (ft)', x_axis_type='datetime')

    plot2 = figure(title='Flap Angle Deltas', tools=['pan', 'box_zoom', 'wheel_zoom', 'save', 'reset'],
                   x_axis_label='UTC Time (hh:mm:ss)', y_axis_label='Deltas (Degrees)', x_axis_type='datetime')

    # Adding line glyphs to the plots and assign them to a variable for the hovertool definition later
    plot.line(x='DATETIME', y='ALTITUDE', source=source,
              line_width=2, color="#63B1EC")
    l1 = plot2.line(x='DATETIME', y='TE_FLPSK1TO8_VAL',
               source=source2, line_width=2, color='#3040c4')
    l2 = plot2.line(x='DATETIME', y='TE_FLPSK2TO7_VAL',
               source=source2, line_width=2, color='#70c1b3')
    l3 = plot2.line(x='DATETIME', y='TE_FLPSK3TO6_VAL',
               source=source2, line_width=2, color='#81b3a3')
    l4 = plot2.line(x='DATETIME', y='TE_FLPSK4TO5_VAL',
               source=source2, line_width=2, color='#f36b7f')

    # Define the individual hover tools for each lines and then add them to the plot
    hover2_1 = HoverTool(tooltips=[('Skew 1-8', '@TE_FLPSK1TO8_VAL'),
                                   ('Time', '@DATETIME{%H:%M:%S}')],
                         formatters={'@DATETIME': 'datetime'},
                         mode='vline',
                         renderers=[l1])

    hover2_2 = HoverTool(tooltips=[('Skew 2-7', '@TE_FLPSK2TO7_VAL'),
                                   ('Time', '@DATETIME{%H:%M:%S}')],
                         formatters={'@DATETIME': 'datetime'},
                         mode='vline',
                         renderers=[l2])

    hover2_3 = HoverTool(tooltips=[('Skew 3-6', '@TE_FLPSK3TO6_VAL'),
                                   ('Time', '@DATETIME{%H:%M:%S}')],
                         formatters={'@DATETIME': 'datetime'},
                         mode='vline',
                         renderers=[l3])

    hover2_4 = HoverTool(tooltips=[('Skew 4-5', '@TE_FLPSK4TO5_VAL'),
                                   ('Time', '@DATETIME{%H:%M:%S}')],
                         formatters={'@DATETIME': 'datetime'},
                         mode='vline',
                         renderers=[l4])

    plot2.add_tools(hover2_1, hover2_2, hover2_3, hover2_4)

    # Adding some styles
    plot_styler(plot)
    plot_styler(plot2)

    # Adding box annotation
    low_box = BoxAnnotation(top=80, fill_alpha=0.1, fill_color='#b8f2e6')
    high_box = BoxAnnotation(bottom=80, fill_alpha=0.1, fill_color='#ffa5ab')

    plot2.add_layout(low_box)
    plot2.add_layout(high_box)

    return plot, plot2
