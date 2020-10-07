# This module is for easy plot styling consisting of 2 helper functions.
# palette_generator() helps with dynamic coloring of the bars in the chart.
# plot_styler() uses defined constant attributes within this module to set
# various properties to the chart. This eliminates the need to style
# indivicual plots manually.

palette = ['#50514f', '#f25f5c', '#ffe066', '#247ba0', '#70c1b3']

chart_font = 'Segoe UI'
chart_title_font_style = 'bold'
chart_title_font_size = '16pt'
chart_title_alignment = 'center'
axis_label_font_style = 'normal'
axis_label_size = '12pt'
axis_ticks_size = '12pt'
default_padding = 10
chart_inner_left_padding = 0.15


def palette_generator(length):

    int_div = length // len(palette)
    remainder = length % len(palette)
    return (palette * int_div) + palette[:remainder]


def plot_styler(plot):
    plot.x_range.range_padding = chart_inner_left_padding
    plot.xaxis.axis_label_text_font = chart_font
    plot.xaxis.major_label_text_font = chart_font
    plot.xaxis.axis_label_standoff = default_padding
    plot.xaxis.axis_label_text_font_size = axis_label_size
    plot.xaxis.axis_label_text_font_style = axis_label_font_style
    plot.xaxis.major_label_text_font_size = axis_label_size
    plot.yaxis.axis_label_text_font = chart_font
    plot.yaxis.axis_label_text_font_size = axis_label_size
    plot.yaxis.axis_label_text_font_style = axis_label_font_style
    plot.yaxis.axis_label_standoff = default_padding
    plot.yaxis.major_label_text_font = chart_font
    plot.yaxis.major_label_text_font_size = axis_label_size
    # "stretch_both" allows the plot elements to be completely responsive
    plot.sizing_mode = "stretch_both"
    # Hiding the logo and figure title so that the title may be generated and styled at front-end
    plot.toolbar.logo = None
    plot.title_location = None
