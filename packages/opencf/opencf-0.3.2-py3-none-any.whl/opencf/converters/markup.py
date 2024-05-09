"""
Conversion Handlers - Textual/Markup

This module provides classes for converting between different markup file formats. It includes concrete implementations of conversion classes for various file types (txt, md, html, ...).
"""

from typing import List

from opencf_core.base_converter import BaseConverter
from opencf_core.filetypes import FileType
from opencf_core.io_handler import StrToTxtWriter, TxtToStrReader


class TextToTextConverter(BaseConverter):
    """
    A converter class for converting text-based files to text format.
    """

    file_reader = TxtToStrReader()
    file_writer = StrToTxtWriter()

    @classmethod
    def _get_supported_input_types(cls) -> FileType:
        return [FileType.TEXT, FileType.MARKDOWN, FileType.JSON, FileType.XML]

    @classmethod
    def _get_supported_output_types(cls) -> FileType:
        return [FileType.TEXT, FileType.MARKDOWN, FileType.JSON, FileType.XML]

    # pylint: disable=W0221
    def _convert(self, input_contents: List[str]):
        md_content = "\n".join(input_contents)
        return md_content
