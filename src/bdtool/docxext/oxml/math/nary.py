"""Custom element classes related to text runs (CT_mR)."""

from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Iterator, List

from docx.oxml.parser import OxmlElement, register_element_cls
from docx.oxml.ns import qn
from docx.oxml.text.font import CT_RPr
from docx.oxml.xmlchemy import BaseOxmlElement, OptionalAttribute, ZeroOrMore, ZeroOrOne

if TYPE_CHECKING:
    from bdtool.docxext.oxml.math.share import CT_ctrlPr, CT_mChar
from bdtool.docxext.oxml.math.block import CT_mBlock

class CT_mNary(CT_mBlock):
    """`<m:nary>` element, containing the properties and element for a nary."""

    get_or_add_naryPr: Callable[[], CT_naryPr]

    naryPr: CT_naryPr | None = ZeroOrOne("w:rPr")  # pyright: ignore[reportAssignmentType]


class CT_naryPr(BaseOxmlElement):
    """`<m:naryPr>` element, containing the properties and element for a naryPr."""

    get_or_add_chr: Callable[..., CT_mChar]
    get_or_add_limLoc: Callable[..., BaseOxmlElement]
    get_or_add_supHide: Callable[..., BaseOxmlElement]
    get_or_add_subHide: Callable[..., BaseOxmlElement]
    get_or_add_ctrlPr: Callable[..., CT_RPr]
    
    chr = ZeroOrOne("m:chr")
    limLoc = ZeroOrOne("m:limLoc")
    supHide = ZeroOrOne("m:supHide")
    subHide = ZeroOrOne("m:supHide")
    ctrlPr = ZeroOrOne("m:ctrlPr")

    def __init__(*key, **kwargs):
        super().__init__(*key, **kwargs)
        
    def add_chr(self, val=None) -> CT_mChar:
        """Add a `m:chr` child element and return it."""
        t = self.get_or_add_chr()
        if val:
            t.set(qn("m:val"), val)
        return t
    
    def add_limLoc(self, val="undOvr") -> BaseOxmlElement:
        """Add a `m:limLoc` child element and return it."""
        t = self.get_or_add_limLoc()
        if val:
            t.set(qn("m:val"), val)
        return t
    
    def add_supHide(self, val="0") -> BaseOxmlElement:
        """Add a `m:supHide` child element and return it."""
        t = self.get_or_add_supHide()
        if val:
            t.set(qn("m:val"), val)
        return t
    
    def add_subHide(self, val="0") -> BaseOxmlElement:
        """Add a `m:supHide` child element and return it."""
        t = self.get_or_add_subHide()
        if val:
            t.set(qn("m:val"), val)
        return t
    
register_element_cls("m:nary", CT_mNary)
register_element_cls("m:naryPr", CT_naryPr)

