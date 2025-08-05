import re

class UrlToLatexUrlSerializer:

    def urls_to_latex_urls(self, string: str) -> str:
        s = self._clean_spaces_from_urls(string)
        s = self._separate_urls_by_spaces(s)
        s = self._add_latex_url_identifiers_and_split_tokens(s)
        return self._merge_wrong_url_splits(s)

    def _clean_spaces_from_urls(self, string: str) -> str:
        matches = self._find_urls_in_string(string)
        token_string = self._substitute_urls_in_string_with_token(string)
        return self._replace_tokens_with_space_free_urls(token_string, matches)

    def _find_urls_in_string(self, string: str) -> list[str]:
        pattern = r"\(h[ ]?t[ ]?t[ ]?p[^\)]*\)"
        matches = re.findall(pattern, string)
        return matches

    def _substitute_urls_in_string_with_token(self, string: str) -> str:
        pattern = r"\(h[ ]?t[ ]?t[ ]?p[^\)]*\)"
        token_string = re.sub(pattern, "<sub>", string)
        return token_string

    def _replace_tokens_with_space_free_urls(
        self, string: str, matches: list
    ) -> str:
        for item in matches:
            string = string.replace("<sub>", item.replace(" ", ""))
        return string

    def _separate_urls_by_spaces(self, string: str) -> str:
        pattern = r'([^( ])http'
        return re.sub(pattern, r"\1 http", string)

    def _add_latex_url_identifiers_and_split_tokens(self, string: str) -> str:
        string_pre_processed = self._pre_process_url_string(string)
        pattern = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        return re.sub(pattern, r'<split>\\url{\1}<split>', string_pre_processed)

    def _pre_process_url_string(self, string: str) -> str:
        """
        Processing steps to avoid a hang-up of the html pattern. Processing in
        this function is really only for handling hang-ups due to unfortunate
        character combinations the url pattern cannot deal with.
        """
        s = self._remove_open_parenthesis_between_non_empty_chars(string)
        return s

    def _remove_open_parenthesis_between_non_empty_chars(
        self, string: str
    ) -> str:
        pattern = r"([^ ]{1})\(([^ ]{1})"
        return re.sub(pattern, r"\1\2", string)

    def _merge_wrong_url_splits(self, string: str) -> str:
        pattern = r"}<split> <split>\\url{([^h]{1}[^t]{2}[^p]{1})"
        return re.sub(pattern, r"\1", string)
