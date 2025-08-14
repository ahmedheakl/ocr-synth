from data_loading.data_loader import DataLoader
from synthetic_data_generation.serializer.write_position_serializer.bbox_generator.doc_pages_col_bboxes_store import DocPagesColBboxesStore
from synthetic_data_generation.templates.template import Template
from .bbox_optimizer.document_bbox_optimizer import DocumentBboxOptimizer
from .bbox_optimizer.heading_bbox_optimizer import HeadingBboxOptimizer
from .data_structures.document_export_data import DocumentExportData
from .data_structures.ground_truth_data import GroundTruthData
from .data_structures.ground_truth_item import GroundTruthItem
from .pos_logs_corrector.pos_logs_corrector import PosLogsCorrector
from .pos_logging.items_position_stores_manager import ItemsPositionStoresManager

class WritePosLogsToJsonSerializer:

    def log_file_to_export_data(self, log_file_path: str, doc_file_path: str) -> DocumentExportData:
        print("hnksh")
        DocPagesColBboxesStore().clear()
        gt_data = self._log_file_data_to_gt_data(log_file_path)
        print('generated gt data')

        print('finding pos_store')
        pos_stores = ItemsPositionStoresManager(doc_file_path).get_paragraph_positions_store()
        self._optimize_latex_bboxes(gt_data, doc_file_path, pos_stores)
        print('optimize latent bbox')
        self._gen_gt_vis_data_file(gt_data, log_file_path, pos_stores)
        print('generate gt data file')
        doc_export_data = self._gen_gt_training_data_file(gt_data, doc_file_path)
        print("doc_export_data: ", doc_export_data)
        print('doc export data')
        return doc_export_data

    def _log_file_data_to_gt_data(self, log_file_path):
        log_data = DataLoader().load_file_as_lines(log_file_path)
        corrected_log_data = PosLogsCorrector().correct_pos_logs(log_data)
        return self._gen_gt_data(corrected_log_data)

    def _gen_gt_data(self, log_data):
        gt_data = GroundTruthData()
        for line_num in range(len(log_data)):
            try:
                #For every component, I add 2 lines (start and finish)
                # for this reason I only take the odd lines
                if (self._is_odd_line(line_num)):
                    gt_item = self._gen_gt_item(line_num, log_data)
                    gt_data.add_with_append_to_existing_item(gt_item)
            except:
                print(f'Artificial except problem with data {gt_data}')
        return gt_data

    def _is_odd_line(self, line_num):
        return ((line_num % 2) != 0)

    def _gen_gt_item(self, log_line_index, log_data):
        start_log_line = log_data[log_line_index-1]
        end_log_line = log_data[log_line_index]
        return GroundTruthItem(start_log_line, end_log_line)

    def _optimize_latex_bboxes(self, gt_data: GroundTruthData, doc_file_path, pos_stores):
        #Section are not included in the headings optimization
        self._optimize_heading_bboxes(gt_data)
        self._optimize_bboxes(gt_data, doc_file_path, pos_stores)

    def _optimize_heading_bboxes(self, gt_data: GroundTruthData):
        optimizer = HeadingBboxOptimizer(gt_data)
        optimizer.optimize_heading_bboxes()

    def _optimize_bboxes(self, gt_data: GroundTruthData, doc_file_path, pos_stores):
        page_images = self._load_page_images(doc_file_path)
        optimizer = DocumentBboxOptimizer(gt_data, page_images)
        optimizer.optimize_bboxes(pos_stores)

    def _load_page_images(self, doc_file_path):
        layout_settings = Template().get_layout_settings()
        size = layout_settings.get_page_size_px()
        return DataLoader().load_doc_page_images(doc_file_path, size=size)

    def _gen_gt_vis_data_file(self, gt_data: GroundTruthData, log_file_path: str, pos_store):
        split = log_file_path.split("/")
        dir_path = "/".join(split[0:-1]) + "/"
        file_name = split[-1]
        gt_data.gen_visualization_json_file(dir_path, file_name, pos_store)

    def _gen_gt_training_data_file(
        self, gt_data: GroundTruthData, doc_file_path: str
    ) -> DocumentExportData:
        pos_stores_manager = ItemsPositionStoresManager(doc_file_path)
        doc_export_data = DocumentExportData(doc_file_path)
        print(f'gt data {gt_data}')
        print(f'with positon {pos_stores_manager}')
        doc_export_data.add_segments(gt_data, pos_stores_manager)
        return doc_export_data
