from copy import deepcopy

from .config_keys import ConfigKeys

class ExportDataConfig:
    """
    Stores the config data for the parquet file export that cannot be generated
    by the program itself. The config data is received from config.json file.
    """

    def __init__(self, config_data: dict):
        self._config_data = self._gen_export_data_config_data(config_data)

    def get_dpi(self) -> int:
        return self._config_data[ConfigKeys.EXP_DPI]

    def get_config_data(self) -> dict:
        return deepcopy(self._config_data)

    def _gen_export_data_config_data(self, config_data: dict) -> dict:
        if (ConfigKeys.EXP_DATA not in config_data):
            raise KeyError("Key 'export-data' is missing in config.json!")
        data = config_data[ConfigKeys.EXP_DATA]
        return {
            ConfigKeys.EXP_DOMAIN: self._resolve_str_value(
                ConfigKeys.EXP_DOMAIN, data),
            ConfigKeys.EXP_DATASET: self._resolve_str_value(
                ConfigKeys.EXP_DATASET, data),
            ConfigKeys.EXP_URL: self._resolve_str_value(
                ConfigKeys.EXP_URL, data),
            ConfigKeys.EXP_TITLE: self._resolve_str_value(
                ConfigKeys.EXP_TITLE, data),
            ConfigKeys.EXP_DPI: self._resolve_dpi_value(data),
            ConfigKeys.EXP_LANGUAGE: self._resolve_str_value(
                ConfigKeys.EXP_LANGUAGE, data),
            ConfigKeys.EXP_CATEGORY: self._resolve_str_value(
                ConfigKeys.EXP_CATEGORY, data),
            ConfigKeys.EXP_HAP_CONFIDENCE: self._resolve_hap_confidence(data),
            ConfigKeys.EXP_NO_HAP_CONFIDENCE: self._resolve_no_hap_confidence(
                data)
        }

    def _resolve_dpi_value(self, exp_config_data: dict) -> int:
        dpi = self._resolve_int_value(ConfigKeys.EXP_DPI, exp_config_data)
        if ((dpi is None) or (dpi < 0)):
            return None
        return dpi

    def _resolve_hap_confidence(self, exp_config_data: dict) -> float:
        hap_confidence = self._resolve_float_value(
            ConfigKeys.EXP_HAP_CONFIDENCE, exp_config_data)
        if (hap_confidence is None):
            return None
        if ((hap_confidence < 0) or (hap_confidence > 1)):
            return None
        return hap_confidence

    def _resolve_no_hap_confidence(self, exp_config_data: dict) -> float:
        hap_confidence = self._resolve_hap_confidence(exp_config_data)
        if (hap_confidence is None):
            return None
        return 1 - hap_confidence

    def _resolve_str_value(self, key: str, exp_config_data: dict) -> str:
        return self._resolve_type_value(key, exp_config_data, str)

    def _resolve_int_value(self, key: str, exp_config_data: dict) -> int:
        return self._resolve_type_value(key, exp_config_data, int)

    def _resolve_float_value(self, key: str, exp_config_data: dict) -> float:
        return self._resolve_type_value(key, exp_config_data, float)

    def _resolve_type_value(self, key: str, exp_config_data: dict, dtype):
        if (key not in exp_config_data):
            return None
        value = exp_config_data[key]
        if (type(value) == dtype):
            return value
        return None
