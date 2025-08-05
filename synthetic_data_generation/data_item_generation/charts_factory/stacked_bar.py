from synthetic_data_generation.data_item_generation.charts_factory.chart_adapter import ChartAdapter
from synthetic_data_generation.chart_rendering.src.charts_generation.StackedBarChartMatplotlibRenderer import StackedBarChartMatplotlibRenderer
from synthetic_data_generation.chart_rendering.src.charts_generation.StackedBarChartPyechartsRenderer import StackedBarChartPyechartsRenderer
from synthetic_data_generation.chart_rendering.src.charts_generation.StackedBarChartSeabornRenderer import StackedBarChartSeabornRenderer
from synthetic_data_generation.chart_rendering.src.extract_data.utils import *

from docling_core.types.doc.document import ChartStackedBar, PictureStackedBarChartData, PictureTabularChartData
from docling_core.types.doc.document import TableData, TableCell, PictureClassificationClass, PictureClassificationData
from pathlib import Path
import importlib.util
import random
import os
import logging
import time
import math


class StackedBar(ChartAdapter):
    def __init__(self):
        print('loading chart factory')
        #TODO: fix problem with Pyecharts and javascript error: echarts is not defined
        self._render = random.choice([StackedBarChartMatplotlibRenderer(), StackedBarChartMatplotlibRenderer()])
        if isinstance(self._render, StackedBarChartMatplotlibRenderer):
            print(f'initialized a Stacked Bar Render with Matplotlib')
        elif isinstance(self._render, StackedBarChartSeabornRenderer):
            print(f'initialized a Stacked Bar Render with Seaborn')
        elif isinstance(self._render, StackedBarChartPyechartsRenderer):
            print(f'initialized a Stacked Bar Render with Pyechart')
        else:
            print('strange Stacked Bar initialization')
        
        self.table = None

    def convert_docling_table_to_data(self, docling_table):
        '''This function transform a docling table item into a dictionary
       with a format aligned with the one expected from the chart generator'''
        try:
            print('stacked bar')
            table_data = docling_table.get('data',{})
            if len(table_data.keys()) == 0: return 
            self.table = docling_table
            n_rows = table_data.get("num_rows", 0)
            n_cols = table_data.get("num_cols", 0)
            print(f'num_rows {n_rows}')
            print(f'num_rows {n_cols}')


            if n_rows == 0 or n_cols == 0:
                print(
                    f"Table {docling_table.get('self_ref', '')} in json file has a 0 number of rows or cols."
                    f"Number of rows: {n_rows}. Number of columns: {n_cols}."
                )
                return

            table = []
            x_axis = []
            units_index = None
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

                #TODO: add condition on the type of header
                row = [el["text"] for el in row]
                #TODO: check if it make sense to sanitize, currently most of the data are in latex format
                row[0] = sanitize_x_value(row[0])
                for i in range(1, len(row)):
                    row[i] = sanitize_y_value(row[i])
                    row[i] = remove_space_y_value(row[i])
                is_valid_row = is_valid_row_bar_chart(row, x_axis)
                if is_valid_row:
                    for i in range(1, len(row)):
                        row[i] = float(row[i])

                #there's the case where the first row is valid and still is a unit
                if units_index is None and is_valid_row:
                    units_index = min(0,i - 1)
                    print(units_index)

                if is_valid_row and (units_index != i):
                    table.append(row[1:])
                    x_axis.append(row[0])

            x_axis = truncate_strings(x_axis)
            print(f'len_x_axis {len(x_axis)}')
            if len(x_axis) < 2:
                print(
                    f"Table {docling_table.get('self_ref', '')} in json file: not enough values to plot."
                )
                return
            
            units = [doc_cell['text'] for doc_cell in docling_rows[units_index]][1:]
            while units_index > 0 and any([unit == "" for unit in units]):
                units_index = units_index - 1
                units = [doc_cell['text'] for doc_cell in docling_rows[units_index]][1:]

            unique_units_indexes = first_occurrence_indexes(units)
            units = list(set(units))
            if len(units) < 2:
                print(
                    f"Table {docling_table.get('self_ref', '')} in json file: not enough units to plot."
                )
                return
            
            # Take into consideration only the first 8 bars
            bars = table[:8]
            labels = x_axis[:8]
            # Take into consideration only the first 4 units
            units = units[:4]
            # take into consideration only the first 4 units and filter for different units
            bars = [filter_by_first_occurrences(unique_units_indexes, bar)[:4] for bar in bars]
            bars = adjust_outliers_zscore(bars)
            bar_chart = {
                "title": "None",
                "source": "None",
                "x_title": "None",
                "y_title": "None",
                "values": {
                    label: {unit: str(value) for unit, value in zip(units, bar)}
                    for label, bar in zip(labels, bars)
                },
            }
            
        except Exception as e:
            print(f'execption {e}')
            logging.info(e)
            return None

        #bar return a list of bar charts. Need to understand How I want to manage it

        return bar_chart   

    def convert_chart_data_to_docling(self, chart_data):
        '''Convert the bar data type used by Matteo in a docling GT
        {
            "title": "None",
            "source": "None",
            "x_title": "None",
            "y_title": "None",
            "values": {
                "World": {"unit1": "7377201.0", "unit2": "50"},
                "Developed economies": {"unit1": "7377201.0", "unit2": "50"},
                "Europe": {"unit1": "7377201.0", "unit2": "50"},
            }
        }'''
        title = chart_data.get('title', '')
        x_title = chart_data.get('x_title', '')
        y_title = chart_data.get('y_title', '')
        values = chart_data.get('values', {})
        stackedbars = []
        for label, value_dict in values.items():
            #TODO: expect a int value and not a float for some reason
            tuple_list = [(key, int(float(value))) for key, value in value_dict.items()]
            stackedbars.append(ChartStackedBar(label=[label], values=tuple_list))
                
        return PictureStackedBarChartData(title=title, x_axis_label=x_title, y_axis_label=y_title, stacked_bars=stackedbars)

    def convert_chart_data_to_docling_updated(self, chart_data):
        print('converting stacked')
        # create a chart data
        title = chart_data.get('title', '')
        #method to pass from a json data to a docling table
        data = self.table['data']
        values = chart_data['values']
        cell_list = []
        values = chart_data['values']
        labels = list(values.keys())
        units = list(values[labels[0]].keys())
        num_cols = len(units) + 1
        num_rows = len(labels) + 1
        for i in range(num_rows*num_cols):
            if i == 0:
                #special case, empty
                cell_list.append(TableCell(row_span=1,
                                        col_span=1,
                                        start_col_offset_idx=i,
                                        end_col_offset_idx=i+1,
                                        start_row_offset_idx=0,
                                        end_row_offset_idx=1,
                                        text='',
                                        column_header=True))
            elif i < num_cols:
                #first row
                cell_list.append(TableCell(row_span=1,
                                        col_span=1,
                                        start_col_offset_idx=i,
                                        end_col_offset_idx=i+1,
                                        start_row_offset_idx=0,
                                        end_row_offset_idx=1,
                                        text=units[i-1],
                                        column_header=True))
            elif (i - num_cols) == 0:
                #case first column
                row = int(math.floor(i/num_cols))
                row_key = labels[row-1]
                cell_list.append(TableCell(row_span=1,
                                        col_span=1,
                                        start_col_offset_idx=0,
                                        end_col_offset_idx=1,
                                        start_row_offset_idx=row,
                                        end_row_offset_idx=row+1,
                                        text=row_key,
                                        row_header=True))

            else:
                #case first column
                row = int(math.floor(i/num_cols))
                cell_list.append(TableCell(row_span=1,
                                        col_span=1,
                                        start_col_offset_idx=(i-num_cols*row),
                                        end_col_offset_idx=(i-num_cols*row +1),
                                        start_row_offset_idx=row,
                                        end_row_offset_idx=row+1,
                                        text=values[row_key][units[i-num_cols*row-1]]))
    
        table = TableData(table_cells=cell_list, num_rows=2, num_cols=num_cols)
        table_annotation = PictureTabularChartData(title=title, chart_data = table)
        annotation = PictureClassificationData(provenance='synthetic', predicted_classes=[PictureClassificationClass(class_name='stacked_bar_chart', confidence=1.0)])
        return [annotation, table_annotation]
    
    def render_and_save_chart(self, chart_data: str, file_hash: str, index: int):
        # module_spec = importlib.util.find_spec('synthetic_data_generation')
        root_path = os.path.abspath('.') 
        image_name = file_hash + '_pictures_' + str(index) + '.png'
        abs_image_path = os.path.join(root_path, 'synthetic_data_generation/dataset/demo/doclingdocs', image_name)
        #1. render generate the chart image and save it at a certain location
        self._render.render(chart_data, abs_image_path)

        



