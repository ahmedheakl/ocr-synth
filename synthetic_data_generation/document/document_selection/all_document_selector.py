from .document_selector import DocumentSelector

class AllDocumentSelector(DocumentSelector):

    def __init__(self, config: dict, dataset_path: str):
        # Argument 'config' does nothing, but is needed for polymorphism.
        super().__init__(dataset_path)

    def select_doc_file_names(self) -> list[str]:
        return self._get_all_doc_file_names()
