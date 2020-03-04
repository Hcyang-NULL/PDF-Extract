from io import StringIO
from io import open
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
import re


end_signal = ['.', ',', ';', '?', '!', ')']
email_re = r'(^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$)'


def add_div(data):
    new_data = ''
    for frag in data.split('\n'):
        if frag != '':
            frag = '<div contenteditable="true">\n' + frag + '\n</div>\n<br>\n'
            new_data += frag
    return new_data


def read_pdf(file_name):
    pdf = open(file_name, "rb")
    # resource manager
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    # device
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    process_pdf(rsrcmgr, device, pdf)
    device.close()
    content = retstr.getvalue()
    retstr.close()
    # 获取所有行
    lines = str(content).split("\n")

    data = ''
    frag = ''

    for line in lines:
        if line == '':
            if len(frag) <= 5:
                pass
            else:
                data += frag + '\n'
            frag = ''
        else:
            if re.match(email_re, line.strip()):
                continue
            if len(line) < 3:
                continue
            if line[-1] in end_signal:
                frag += line
            elif line[-1] == '-':
                frag += line[:-1]
            else:
                frag += line + ' '
    data = re.sub('\n\n*', '\n\n', data)
    data = add_div(data)
    with open('paper.txt', 'w', encoding='utf-8') as f:
        f.write(data)
    pdf.close()
    return data
