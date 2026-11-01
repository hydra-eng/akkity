"""Bounded local text extraction. Files are data, never executable actions."""
from pathlib import Path
import zipfile
import xml.etree.ElementTree as ET

TEXT_TYPES={'.txt','.md','.csv','.tsv','.json','.log','.py','.js','.ts','.html','.css','.yaml','.yml','.xml'}
MAX_BYTES=2*1024*1024
MAX_CHARS=5000

def read_attachment(filename):
    path=Path(filename)
    if path.stat().st_size>MAX_BYTES:
        raise ValueError('Choose a file smaller than 2 MB.')
    suffix=path.suffix.lower()
    if suffix in TEXT_TYPES:
        text=path.read_text(encoding='utf-8-sig',errors='replace')
    elif suffix=='.docx':
        with zipfile.ZipFile(path) as archive:
            info=archive.getinfo('word/document.xml')
            if info.file_size>MAX_BYTES:raise ValueError('This document is too large to read.')
            root=ET.fromstring(archive.read(info))
        ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        text='\n'.join(''.join(p.itertext()) for p in root.findall('.//w:p',ns))
    elif suffix=='.pdf':
        from pypdf import PdfReader
        reader=PdfReader(path)
        if reader.is_encrypted:raise ValueError('Use an unlocked PDF.')
        parts=[]
        for page in reader.pages[:15]:
            parts.append(page.extract_text() or '')
            if sum(map(len,parts))>MAX_CHARS:break
        text='\n'.join(parts)
    else:
        raise ValueError('Supported: text, code, CSV, DOCX and text PDFs. This Gemma model cannot read images, audio or scanned PDFs.')
    if not text.strip():raise ValueError('No readable text found. Scanned PDFs need OCR first.')
    return {'name':path.name,'text':text[:MAX_CHARS],'truncated':len(text)>MAX_CHARS or suffix=='.pdf' and len(reader.pages)>15}
