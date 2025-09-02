from __future__ import annotations

from docx.oxml.text.paragraph import CT_P
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from lxml import etree
import re


def add_endnote(ct_p: CT_P, instrText: str = None, index=1) -> CT_P:

    r = ct_p.add_r() 
    fld = OxmlElement("w:fldChar") 
    fld.set(qn("w:fldCharType"), "begin") 
    r.append(fld)
    
    r = ct_p.add_r()
    fld = OxmlElement("w:instrText")
    fld.set(qn("xml:space"), "preserve") 
    fld.text = instrText.replace("\n", "")
    r.append(fld)
    
    r = ct_p.add_r()
    fld = OxmlElement("w:fldChar")
    fld.set(qn("w:fldCharType"), "separate")
    r.append(fld)
    
    r = ct_p.add_r()
    rPr = OxmlElement("w:rPr")
    noProof = OxmlElement("w:noProof")
    rPr.append(noProof)
    vertAlign = OxmlElement("w:vertAlign")
    vertAlign.set(qn("w:val"), "superscript") 
    rPr.append(vertAlign)
    r.append(rPr)
    t = OxmlElement("w:t")
    t.text = f"[{str(index)}]"
    r.append(t)
    
    r = ct_p.add_r()
    fld = OxmlElement("w:fldChar")
    fld.set(qn("w:fldCharType"), "end")
    r.append(fld)
    
    return ct_p
