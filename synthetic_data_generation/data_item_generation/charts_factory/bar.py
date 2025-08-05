from synthetic_data_generation.data_item_generation.charts_factory.chart_adapter import ChartAdapter
from synthetic_data_generation.chart_rendering.src.charts_generation.BarChartMatplotlibRenderer import BarChartMatplotlibRenderer
from synthetic_data_generation.chart_rendering.src.charts_generation.BarChartPyechartsRenderer import BarChartPyechartsRenderer
from synthetic_data_generation.chart_rendering.src.charts_generation.BarChartSeabornRenderer import BarChartSeabornRenderer
from synthetic_data_generation.chart_rendering.src.extract_data.utils import *
from synthetic_data_generation.data_item_generation.data_items.table_item.table_item import TableItem

from docling_core.types.doc.document import ChartBar, PictureBarChartData, PictureTabularChartData
from docling_core.types.doc.document import TableData, TableCell, PictureClassificationData, PictureClassificationClass
from pathlib import Path
import importlib.util
import random
import os
import logging
import time


class Bar(ChartAdapter):
    def __init__(self):
        print('loading chart factory')
        #TODO: fix problem with Pyecharts and javascript error: echarts is not defined
        self._render = random.choice([BarChartMatplotlibRenderer(), BarChartSeabornRenderer()])
        if isinstance(self._render, BarChartMatplotlibRenderer):
            print(f'initialized a Bar Render with Matplotlib')
        elif isinstance(self._render, BarChartSeabornRenderer):
            print(f'initialized a Bar Render with Seaborn')
        elif isinstance(self._render, BarChartPyechartsRenderer):
            print(f'initialized a Bar Render with Pyechart')
        else:
            print('strange Bar initialization')
        
        self.table = None

    def convert_docling_table_to_data(self, docling_table):
        '''This function transform a docling table item into a dictionary
       with a format aligned with the one expected from the chart generator'''
        try:
            table_data = docling_table.get('data',{})
            if len(table_data.keys()) == 0: return 
            self.table = docling_table
            n_rows = table_data.get("num_rows", 0)
            n_cols = table_data.get("num_cols", 0)
            print(f'num_rows {n_rows}')
            print(f'num_cols {n_cols}')


            if n_rows == 0 or n_cols == 0:
                print(
                    f"Table {docling_table.get('self_ref', '')} in json file has a 0 number of rows or cols."
                    f"Number of rows: {n_rows}. Number of columns: {n_cols}."
                )
                return

            table = []
            x_axis = []
            cells = table_data['table_cells']
            docling_rows = [cells[i:i + n_cols] for i in range(0, len(cells), n_cols)]
            #The case here is the one where the header is in the first column
            #so -> row_header = True
            type_of_header = ''
            print(f'number of ROWS {len(cells)}')
            for i, row in enumerate(docling_rows):
                #check if column or row header
                if i == 0 and row[0]['row_header'] == True:
                    type_of_header = 'row'
                elif i == 0  and row[0]['column_header'] == True:
                    type_of_header = 'col'

                if i == 0:
                    continue
                
                #TODO: add condition on the type of header
                row = [el["text"] for el in row]
                #TODO: check if it make sense to sanitize, currently most of the data are in latex format
                row[0] = sanitize_x_value(row[0])
                for i in range(1, len(row)):
                    row[i] = sanitize_y_value(row[i])
                    row[i] = remove_space_y_value(row[i])

                if is_valid_row_bar_chart(row, x_axis):
                    table.append(row)
                    x_axis.append(row[0])

            x_axis = truncate_strings(x_axis)
            print(f'len_x_axis {len(x_axis)}')
            if len(x_axis) < 2:
                print(
                    f"Table {docling_table.get('self_ref', '')} in json file: not enough values to plot."
                )
                return

            #trasform each column in a bar chart
            #TODO: I can add description/title if there is also a header column
            bar_charts = [[] for _ in range(n_cols - 1)]
            for row in table:
                for j, y in enumerate(row[1:]):
                    y = round(float(y), 2)
                    if y == 0:
                        y = random.uniform(0.1, 5)
                        y = round(float(y), 2)
                    bar_charts[j].append(y)
            bar_charts = [adjust_values(bar_chart) for bar_chart in bar_charts]
            # limit to 10 the max number of bars in each chart
            bar_charts = [bar_chart[:10] for bar_chart in bar_charts]

            formated_tables = []
            for bar_chart in bar_charts:
                formated_bar_chart = {
                    "title": "None",
                    "source": "None",
                    "x_title": "None",
                    "y_title": "None",
                    "values": {
                        label: str(bar) for label, bar in zip(x_axis, bar_chart)
                    },
                }
                # for label, bar in zip(x_axis, bar_chart):
                #     # cast to str because that is the standard format for this kind of datasets
                #     formated_bar_chart['values'][label] = str(bar)
                formated_tables.append(formated_bar_chart)
        except Exception as e:
            print(f'execption {e}')
            logging.info(e)
            return

        #bar return a list of bar charts. Need to understand How I want to manage it
        self.table_index = random.randint(0, len(formated_tables)-1)
        return formated_tables[self.table_index]    

    def convert_chart_data_to_docling(self, chart_data):
        '''Convert the bar data type used by Matteo in a docling GT
        {
            "title": "None",
            "source": "None",
            "x_title": "None",
            "y_title": "None",
            "values": {
                "World": "7377201.0",
                "Developed economies": "5860038.0",
                "Europe": "4427062.2",
                "European Union": "3689527.5",
                "Developing economies": "2951992.8",
                "Asia": "2214458.1",
                "L America and the Caribbean": "1476923.4",
                "Central America": "739388.7",
                "Oceania": "1854.0"
            }
        }'''
        title = chart_data.get('title', '')
        x_title = chart_data.get('x_title', '')
        y_title = chart_data.get('y_title', '')
        values = chart_data.get('values', {})
        bar_items = []
        for label, value in values.items():
            bar_items.append(ChartBar(label=label, values=value))
        return PictureBarChartData(title=title, x_axis_label=x_title, y_axis_label=y_title, bars=bar_items)
    
    def convert_chart_data_to_docling_updated(self, chart_data):
        # create a chart data
        title = chart_data.get('title', '')
        #method to pass from a json data to a docling table
        data = self.table['data']
        print(data)
        values = chart_data['values']
        cell_list = []
        values = chart_data['values']
        key_values = list(values.keys())
        num_cols = len(values.keys())
        num_rows = 2
        for i in range(num_rows*num_cols):
            if i < num_cols:
                #first row
                cell_list.append(TableCell(row_span=1,
                                           col_span=1,
                                           start_col_offset_idx=i,
                                           end_col_offset_idx=i+1,
                                           start_row_offset_idx=0,
                                           end_row_offset_idx=1,
                                           text=key_values[i],
                                           column_header=True))
            else:
                cell_list.append(TableCell(row_span=1,
                                           col_span=1,
                                           start_col_offset_idx=(i-num_cols),
                                           end_col_offset_idx=(i-num_cols+1),
                                           start_row_offset_idx=1,
                                           end_row_offset_idx=2,
                                           text=values[key_values[i-num_cols]]))
       
        table = TableData(table_cells=cell_list, num_rows=2, num_cols=num_cols)
        table_annotation = PictureTabularChartData(title=title, chart_data = table)
        annotation = PictureClassificationData(provenance='synthetic', predicted_classes=[PictureClassificationClass(class_name='bar_chart', confidence=1.0)])
        return [annotation, table_annotation]

    def render_and_save_chart(self, chart_data: str, file_hash: str, index: int):
        # module_spec = importlib.util.find_spec('synthetic_data_generation')
        root_path = os.path.abspath('.') 
        image_name = file_hash + '_pictures_' + str(index) + '.png'
        abs_image_path = os.path.join(root_path, 'synthetic_data_generation/dataset/demo/doclingdocs', image_name)
        #1. render generate the chart image and save it at a certain location
        self._render.render(chart_data, abs_image_path)

        



