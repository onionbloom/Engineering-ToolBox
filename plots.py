# This module contains functions that will plot the given data

from bokeh.models import ColumnDataSource, HoverTool, PrintfTickFormatter, CategoricalColorMapper
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from plotStyle import plot_styler


def petal_sepal_scatter(dataframe):
    hover = HoverTool(tooltips=[('species name', '@species'),
                                ('petal length', '@petal_length'),
                                ('sepal legnth', '@sepal_length')
                                ])

    mapper = CategoricalColorMapper(factors=['setosa', 'virginica', 'versicolor'],
                                    palette=['#247ba0', '#f25f5c', '#ffe066'])

    source = ColumnDataSource(dataframe)
    plot = figure(title='Petal Length Against Sepal Length',
                  tools=[hover, 'pan', 'box_zoom', 'reset'],
                  x_axis_label='Petal Length', y_axis_label='Sepal Length')
    plot.circle('petal_length', 'sepal_length', source=source, size=10,
                color={'field': 'species', 'transform': mapper}, alpha=0.8)

    plot_styler(plot)

    return plot
