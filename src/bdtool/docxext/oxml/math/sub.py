"""Custom element classes related to sub (CT_mSub)."""
from __future__ import annotations

from docx.oxml.parser import OxmlElement, register_element_cls
from bdtool.docxext.oxml.math.block import CT_mBlock

class CT_mSub(CT_mBlock):
    """`<m:sub>` element, containing the properties and element for a sub."""

register_element_cls("m:sub", CT_mSub)
