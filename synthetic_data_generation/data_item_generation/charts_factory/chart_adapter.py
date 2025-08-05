from docling_core.types.doc.document import PictureChartData, PictureTabularChartData

class ChartAdapter:
    '''Base class describing a chart adapter'''
    
    def convert_docling_table_to_data(self, docling_table_item: str) -> str:
        #convert a docling item into the preferred data structure used by each chart
        pass

    def convert_chart_data_to_docling(self, chart_data: dict) -> PictureChartData:
        #convert the specific infos of the charts to Docling Document chart annotations
        #TODO: adapt to the new format
        pass

    def convert_chart_data_to_docling_updated(self, chart_data: dict) -> PictureTabularChartData:
        pass

    def render_and_save_chart(self, chart_data: dict, file_hash: str, index: int):
        #generate the chart image and save it
        pass


