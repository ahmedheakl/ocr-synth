class FontStyle:

    def __init__(self, name: str, code: str, package: str):
        self._name = name
        self._code = code
        self._package = package

    def get_name(self) -> str:
        return self._name

    def get_latex_code(self) -> str:
        return self._code

    def get_latex_package_name(self) -> str:
        return self._package
