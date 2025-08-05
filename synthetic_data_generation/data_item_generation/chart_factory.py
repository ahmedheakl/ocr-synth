from synthetic_data_generation.data_item_generation.charts_factory.chart_adapter import ChartAdapter
# from synthetic_data_generation.data_item_generation.charts_factory.bar import Bar
# from synthetic_data_generation.data_item_generation.charts_factory.pie import Pie
# from synthetic_data_generation.data_item_generation.charts_factory.stacked_bar import StackedBar

class ChartFactory:
    '''In order to mantain one interface, a Factory of charts is developed
       This factor is also a wrapper to the code written by Matteo Omenetti
       that takes a standard json format and convert it to different style of charts.
       All the product of the factory will inherit from ChartAdapter '''
    
    @staticmethod
    def get_chart(type_of_chart: str) -> ChartAdapter:
        if type_of_chart == 'bar':
            return None
        elif type_of_chart == 'pie':
            return None
        elif type_of_chart == 'stackedbar':
            return None