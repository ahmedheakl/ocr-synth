from PIL import Image
from pylatex import Figure, NewLine, NoEscape, SubFigure
import random
import logging
from typing_extensions import Annotated, Self, deprecated
from docling_core.types.doc.document import PictureItem
from docling_core.types.doc.labels import DocItemLabel
from synthetic_data_generation.serializer.write_position_serializer.data_structures.ground_truth_data import GroundTruthData
from synthetic_data_generation.data_item_generation.data_items.main_text_item import MainTextItem
from synthetic_data_generation.data_item_generation import data_item_map
from synthetic_data_generation.data_item_generation.chart_factory import ChartFactory
from synthetic_data_generation.document_generation.data_stores_manager import DataStoresManager
from synthetic_data_generation.data_item_generation.data_items.util.prov_item import ProvItem
from synthetic_data_generation.data_item_generation.data_items.figure_item import figure_item_image_saver as figure_saver
from synthetic_data_generation.data_stores.wrap_items_store import WrapItemsStore
from synthetic_data_generation.data_stores.wrap_item_store_item import WrapItemStoreItem
from synthetic_data_generation.document_extension.environments.figure_environments.wrapfigure_env import WrapfigureEnv
from synthetic_data_generation.templates.available_options.available_items import AvailableItems
from synthetic_data_generation.templates.template import Template
from synthetic_data_generation.data_item_generation.data_items.util.lang import is_latin_text, _wrap_latin_segments

from util.data_stores.docling_data_store import DoclingDataStore
from util.data_stores.document_page_images_store import DocumentPageImagesStore
from util.geometry_transformation import bbox_coordinate_transformer as bbox_transformer
from util.latex_item_type_names import LatexItemTypeNames
from util.retrieve_index_from_reference import retrieve_component_from_index_and_type, retrieve_index_type_from_reference_string
from pathlib import Path
from .figure_item_env_width_calculator import FigureItemEnvWidthCalculator
import base64
import mimetypes
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class FigureItem(MainTextItem):

    _CHART_LABEL = 0
 
    def __init__(self, index, data: dict):
        # normalise charspan     (unchanged) -------------------------------
        for i, prov in enumerate(data['prov']):
            data['prov'][i]['charspan'] = (0, 0)
        super().__init__(index, self._get_figure_data(data))

        # -------------------------------------------------------------------
        # 1. determine a deterministic file name prefix
        temp_store    = DoclingDataStore()
        file_hash     = temp_store.get_file_hash()
        ref_parts     = data['self_ref'].split('/')
        ref_type      = ref_parts[1]
        ref_index     = ref_parts[2]
        default_root  = Path('synthetic_data_generation/dataset/demo/doclingdocs')
        default_root.mkdir(parents=True, exist_ok=True)
        # -------------------------------------------------------------------

        # 2. resolve the image source
        uri: str | None = data.get('image', {}).get('uri')
        if uri:
            if uri.startswith("data:"):
                # ------------ handle data-URI -----------------------------
                self.image_path = self._store_data_uri(
                    uri,
                    default_root / f"{file_hash}_{ref_type}_{ref_index}"
                )
            else:
                # ------------ regular file path --------------------------
                self.image_path = Path(uri).expanduser().resolve()
        else:
            # ------------ legacy fallback -------------------------------
            self.image_path = default_root / f"{file_hash}_{ref_type}_{ref_index}.png"

        self.caption     = data['captions']
        self.width       = 0
        self.height      = 0
        self.annotations = data['annotations']
        self._is_chart   = len(self.annotations) > 0

       
    def get_text(self):
        return super().get_text()

    def get_segment_text(self, *args) -> str:
        return None
    
    def get_annotations(self) -> dict:
        return self.annotations
    
    def get_image_size(self) -> dict:
        return {
          "width": self.width,
          "height": self.height
        }

    def has_text(self):
        return super().has_text()

    def add_as_latex_to_doc(self, doc, main_text_item):
        if (self._is_subfigure()):
            self._add_subfigures_as_latex_to_doc(doc)
        else:
            self._add_figure_as_latex_to_doc(doc, main_text_item)

    def _is_subfigure(self):
        return self._prov.get_num_items() > 1

    def _add_subfigures_as_latex_to_doc(self, doc, main_text_item):
        with doc.create(Figure(position="h")) as figure:
            for index, item in enumerate(self._prov.get_items()):
                self._add_subfigure_as_latex_to_doc(doc, item, index)
            self._add_figure_caption_to_doc(figure, doc, main_text_item)

    def _add_subfigure_as_latex_to_doc(self, doc, prov_item, subfigure_index):
        image_path = str(self.image_path)
        image = Image.open(image_path)
        width, height = image.size
        self.width = width
        self.height = height
        figure_saver.save_subfigure_image(image, self._index, subfigure_index)
        self._create_subfigure_in_doc(doc)
        
    def _create_subfigure_in_doc(self, doc, subfigure_index):
        with doc.create(SubFigure(position="h")) as subfigure:
            self._add_subimage_to_doc(subfigure, subfigure_index)

    def _add_subimage_to_doc(self, subfigure, subfigure_index):
        path = figure_saver.gen_subfigure_path(self._index, subfigure_index)
        subfigure.add_image(path, width=NoEscape("\\linewidth"))

    def _add_figure_as_latex_to_doc(self, doc, main_text_item):
        image_path = str(self.image_path)
        image = Image.open(image_path)
        width, height = image.size
        self.width = width
        self.height = height
        figure_saver.save_figure_image(image, self._index)
        self._create_figure_in_doc(doc, main_text_item)

    def _create_figure_in_doc(self, doc, main_text_item):
        #TODO: understand when to use the wrappable environment
        env = Template().get_figure_item_settings().get_figure_env()
        self._set_figure_env_line_width(env)
        if (self._is_wrapable_env(env)):
            self._store_item_data_to_wrapable_item_store(env)
        with doc.create(env) as figure:
            self._add_figure_image_to_doc(figure, doc)
            self._add_figure_caption_to_doc(figure, doc, main_text_item)

    def _set_figure_env_line_width(self, env):
        calculator = FigureItemEnvWidthCalculator()
        line_width = calculator.calc_figure_env_line_width(env, self._index)
        env.set_line_width(line_width)

    def _is_wrapable_env(self, env) -> bool:
        return type(env) == WrapfigureEnv

    def _store_item_data_to_wrapable_item_store(self, env: WrapfigureEnv):
        self._add_figure_item_to_wrap_items_store(env)
        self._add_caption_item_to_wrap_items_store(env)

    def _add_figure_item_to_wrap_items_store(self, env: WrapfigureEnv):
        figure_item = WrapItemStoreItem(LatexItemTypeNames.FIGURE, self._index,
            env.get_float_position(), env.get_line_width())
        WrapItemsStore().add_item(figure_item)

    def _add_caption_item_to_wrap_items_store(self, env: WrapfigureEnv):
        if (self.has_text()):
            caption_item = WrapItemStoreItem(
                LatexItemTypeNames.CAPTION, self._get_caption_item_index(),
                env.get_float_position(), env.get_line_width())
            WrapItemsStore().add_item(caption_item)

    def _add_figure_image_to_doc(self, figure, doc):
        self._add_figure_spacing(doc)
        doc.log_write_position(self._index)
        self._add_figure_spacing(doc)

        image_path = figure_saver.gen_figure_path(self._index)
        width = round(random.uniform(0.2, 0.9), 2)  # random width between 0.2 and 0.9

        if self._is_chart:
            logger.info("Adding chart image")
            try:
                figure.add_image(image_path, width=width)
            except Exception:
                logger.exception("Problem adding chart image")
        else:
            # Use raw LaTeX for \centerline and image with dynamic width
            doc.append(NoEscape(r"\centerline{"))
            doc.append(NoEscape(r"\includegraphics[width=%.2f\linewidth]{%s}" % (width, image_path)))
            doc.append(NoEscape(r"}"))
            doc.log_write_position(self._index)

    def _add_figure_spacing(self, doc):
        """
        Spacing before and after the first position log is required for single
        col env only. Without this spacing, the position logs are not correct
        and screw the bbox GT values.
        """
        layout_settings = Template().get_layout_settings()
        if (layout_settings.has_one_col()):
            doc.append(NewLine())

    def _add_figure_caption_to_doc(self, figure, doc, main_text_item):
        """Take the captions key from the image dictionary and retrieve
        the corresponding text data from the DoclingDataStore """
        if self._has_active_caption():
            caption_index, caption_type = self._get_caption_item_index()
            caption_item = retrieve_component_from_index_and_type(caption_index, caption_type)
            item_instance = data_item_map.data_to_instance(self._index + 1, caption_item)
            item_instance.set_caption()
            gt_store = GroundTruthData()
            gt_store.add_with_overwrite_existing_item(item_instance)
            doc.log_write_position(self._get_caption_document_index())
            # main_text_item.add_item(item_instance)

            # 🔁 Detect language and wrap if Latin
            raw_text = item_instance.get_text()
            wrapped = _wrap_latin_segments(raw_text)
            latex_caption_text = rf"\textarabic{{{wrapped}}}"
            figure.add_caption(NoEscape(latex_caption_text))
            doc.log_write_position(self._get_caption_document_index())
        else:
            doc.append(NewLine())
    
    def _has_active_caption(self):
        return len(self.caption) > 0
        
    def _get_figure_data(self, data: dict):
        return data

    def _get_caption_item_index(self):
        '''retrieved the docling reference index
            (Used in Docling Documents and the Docling Database)'''
        caption_ref = self.caption[0]['$ref']
        caption_number, caption_type = retrieve_index_type_from_reference_string(caption_ref)
        return caption_number, caption_type
    
    def _get_caption_document_index(self):
        '''Retrieved the index of the element in the Document.
        This index is important to position the element in the Document'''
        return self._index + 1
    
    @classmethod
    def from_table(cls, docling_table: dict, parent = None) -> Self:
        '''Generate and Construct a picture item from a DoclingDocs
           table, with the corresponding annotations element'''
        chart_string = random.choice(['bar', 'pie', 'stackedbar'])
        logger.debug("Chart string: %s", chart_string)
        chart_adapter = ChartFactory.get_chart(chart_string)
        chart_values = chart_adapter.convert_docling_table_to_data(docling_table)
        logger.debug("Generated chart values: %s", chart_values)
        if chart_values is None:
            chart_string = random.choice(['bar', 'pie'])
            logger.debug("Fallback chart string: %s", chart_string)
            chart_adapter = ChartFactory.get_chart(chart_string)
            chart_values = chart_adapter.convert_docling_table_to_data(docling_table)
            if chart_values is None:
                return None
        annotations = chart_adapter.convert_chart_data_to_docling_updated(chart_values)
        logger.debug("Converted chart to docling annotations")
        docling_temp_store = DoclingDataStore()
        number_of_images_in_DockDoc = len(docling_temp_store.get_pictures())
        file_hash = docling_temp_store.get_file_hash()
        index = number_of_images_in_DockDoc + FigureItem._CHART_LABEL
        chart_adapter.render_and_save_chart(chart_values, file_hash, index)
        logger.debug("Rendered and saved chart with index: %d", index)
        FigureItem._CHART_LABEL += 1
        cref = f"#/pictures/{index}"
        logger.debug("Created chart from table with ref: %s", cref)
        fig_item = PictureItem(
            label=DocItemLabel.PICTURE,
            annotations=annotations,
            image=None,
            self_ref=cref,
            parent=parent,
        )
        return fig_item

    @staticmethod
    def _store_data_uri(data_uri: str, stem: Path) -> Path:
        """
        Decode a data-URI and write it to <stem>.<ext>.
        Returns the resulting Path.
        """
        header, b64 = data_uri.split(",", 1)
        # header example: "data:image/png;base64"
        mime_part   = header.split(";")[0]            # "data:image/png"
        mime_type   = mime_part.split(":", 1)[1]      # "image/png"
        ext         = mimetypes.guess_extension(mime_type) or ".bin"

        target_path = stem.with_suffix(ext)
        target_path.parent.mkdir(parents=True, exist_ok=True)

        with target_path.open("wb") as fh:
            fh.write(base64.b64decode(b64))

        return target_path
