"""Run with python scripts/test_files.py; no model or GUI needed."""
import sys,tempfile,zipfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'app'))
from local_files import read_attachment
from pypdf import PdfWriter
from pypdf.generic import DictionaryObject,NameObject,DecodedStreamObject

with tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp)
    text=root/'notes.txt';text.write_text('Moonberry is the project name.\n'*300)
    result=read_attachment(text)
    assert result['truncated'] and len(result['text'])==5000
    doc=root/'notes.docx'
    with zipfile.ZipFile(doc,'w') as archive:
        archive.writestr('word/document.xml','<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body><w:p><w:r><w:t>Moonberry project</w:t></w:r></w:p></w:body></w:document>')
    assert 'Moonberry' in read_attachment(doc)['text']
    writer=PdfWriter();page=writer.add_blank_page(width=300,height=300)
    font=DictionaryObject({NameObject('/Type'):NameObject('/Font'),NameObject('/Subtype'):NameObject('/Type1'),NameObject('/BaseFont'):NameObject('/Helvetica')})
    page[NameObject('/Resources')]=DictionaryObject({NameObject('/Font'):DictionaryObject({NameObject('/F1'):writer._add_object(font)})})
    stream=DecodedStreamObject();stream.set_data(b'BT /F1 12 Tf 20 250 Td (Moonberry project) Tj ET')
    page[NameObject('/Contents')]=writer._add_object(stream)
    pdf=root/'notes.pdf';writer.write(pdf)
    assert 'Moonberry' in read_attachment(pdf)['text']
    large=root/'large.txt';large.write_bytes(b'x'*(2*1024*1024+1))
    try:read_attachment(large);raise AssertionError('Oversized file accepted')
    except ValueError:pass
    picture=root/'cat.png';picture.write_bytes(b'not an image')
    try:read_attachment(picture);raise AssertionError('Unsupported file accepted')
    except ValueError:pass
print('PASS: text truncation, DOCX, PDF, size limit and unsupported format')
