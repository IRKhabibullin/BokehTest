import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource, TableColumn
from bokeh.models.widgets import TextInput, Button, DataTable, Div
from bokeh.plotting import figure


# calculates row sum by clicking on row. Multiple selection supported
def row_selected(attr, old, new):
    row_sum = 0
    for value in source.data.values():
        for table_row in new['1d']['indices']:
            row_sum += value[table_row]
    div.text = 'Sum by row #{}: {}'.format(
        ', '.join([str(i) for i in new['1d']['indices']]), row_sum)


# creates figure for passed column data
def get_figure(column_data, column_index):
    p = figure(name='plot1', plot_height=300, plot_width=500,
               title="Column #{} figure".format(column_index),
               toolbar_location=None,
               tools="crosshair")
    p.vbar(x=range(len(column_data)), top=column_data, width=0.7)
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    return p


# adds plot for selected column
def column_button_clicked():
    column_index = curdoc().get_model_by_name('column_index').value
    try:
        data = source.data['column' + column_index]
        plots = main_layout.children
        plot1 = curdoc().get_model_by_name('plot1')
        if plot1 is not None:
            plots.remove(plot1)
        plots.append(get_figure(data, column_index))
    except KeyError as e:
        print('KeyError:', e)


# calculates sum of a row from 'row_index' TextInput.
def row_button_clicked():
    try:
        selected_index = int(curdoc().get_model_by_name('row_index').value)
        if selected_index in range(10):
            row_sum = 0
            for value in source.data.values():
                row_sum += value[selected_index]
            print(selected_index, row_sum)
            div.text = 'Sum by row #{}: {}'.format(selected_index, row_sum)
        else:
            div.text = 'Wrong row number!'
    except ValueError as e:
        div.text = 'Wrong row number!'
        print(e)


def row_input_changed(attrname, old, new):
    row_button_clicked()


def column_input_changed(attrname, old, new):
    column_button_clicked()


data = dict(
    column0=np.random.randint(100, size=10),
    column1=np.random.randint(100, size=10),
    column2=np.random.randint(100, size=10)
)
source = ColumnDataSource(data)
source.on_change('selected', row_selected)
columns = [
    TableColumn(field="column0", title="Column 0"),
    TableColumn(field="column1", title="Column 1"),
    TableColumn(field="column2", title="Column 2")
]
data_table = DataTable(source=source, columns=columns, width=400, height=300)

row_index_input = TextInput(name='row_index', title="Row number", value='0')
row_index_input.on_change('value', row_input_changed)

row_button = Button(label='Get row sum', button_type='primary')
row_button.on_click(row_button_clicked)

div = Div(height=70)

text = TextInput(name='column_index', title="Column number", value='0')
text.on_change('value', column_input_changed)

column_button = Button(label='Show column figure', button_type='primary')
column_button.on_click(column_button_clicked)

inputs = widgetbox(row_index_input, row_button, div, text, column_button)
main_layout = row(inputs, data_table, width=800)
curdoc().add_root(main_layout)
curdoc().title = "Table analysis"
