import pygal
from pygal import Config
from pygal.style import Style
from pygal.style import LightSolarizedStyle, RedBlueStyle

def pie(data, inner_radius=0):

    config = Config()
    #config.show_legend = False
    config.height=300
    config.width=300
    #config.print_values=True
    #config.print_labels=True
    #config.half_pie=True
    config.value_formatter = lambda x: f'{x}%'
    # config.style= RedBlueStyle(
    #     value_font_size=15,
    #     value_label_font_size=15,
    #     value_colors=())
    #config.legend_at_bottom=True
    #config.legend_at_bottom_columns=3
    config.dynamic_print_values=True
    config.inner_radius=inner_radius
    graph = pygal.Pie(config, title = "Number of Dogs Owned")
    for item in data:
        graph.add(item, data[item]) #[{'value': data[item], 'label':item}])
    graph_data = graph.render_data_uri()
    
    return graph_data