from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, PageBreak
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

pdfmetrics.registerFont(TTFont('SimSun', 'C:\Windows\Fonts\simsun.ttc'))
pdfmetrics.registerFont(TTFont('SimHei', 'C:\Windows\Fonts\simhei.ttf'))
pdfmetrics.registerFont(TTFont('SimKai', 'C:\Windows\Fonts\simkai.ttf'))

FONT_NAMES = [
    'SimSun',
    'SimHei',
    'SimKai',
]
FONT_NAME = 'SimSun'

# return ct
class FontStyles(object):

    @staticmethod
    def h1():
        style = getSampleStyleSheet()
        ct = style['Heading1']
        ct.fontName = FONT_NAME
        ct.fontSize = 20
        ct.textColor = colors.black
        ct.alignment = 1        # center alignment
        ct.leading = 40         # line interval
        return ct

    @staticmethod
    def h2():
        style = getSampleStyleSheet()
        ct = style['Heading2']
        ct.fontName = FONT_NAME
        ct.fontSize = 18
        ct.textColor = colors.black
        ct.alignment = 1        # center alignment
        ct.leading = 38         # line interval
        return ct

    @staticmethod
    def h3():
        style = getSampleStyleSheet()
        ct = style['Heading3']
        ct.fontName = FONT_NAME
        ct.fontSize = 16
        ct.textColor = colors.black
        ct.alignment = 1        # center alignment
        ct.leading = 35         # line interval
        return ct
    
    @staticmethod
    def h4():
        style = getSampleStyleSheet()
        ct = style['Heading4']
        ct.fontName = FONT_NAME
        ct.fontSize = 15
        ct.textColor = colors.black
        ct.alignment = 1        # center alignment
        ct.leading = 30         # line interval
        return ct

    @staticmethod
    def h5():
        style = getSampleStyleSheet()
        ct = style['Heading5']
        ct.fontName = FONT_NAME
        ct.fontSize = 14
        ct.textColor = colors.black
        ct.alignment = 1        # center alignment
        ct.leading = 25         # line interval
        return ct

    @staticmethod
    def h6():
        style = getSampleStyleSheet()
        ct = style['Heading6']
        ct.fontName = FONT_NAME
        ct.fontSize = 12
        ct.textColor = colors.black
        ct.alignment = 1        # center alignment
        ct.leading = 22         # line interval
        return ct

    @staticmethod
    def p():
        style = getSampleStyleSheet()
        ct = style['Normal']
        ct.fontName = FONT_NAME
        ct.fontSize = 12
        ct.textColor = colors.black
        ct.wordWrap = "CJK"     # auto new line
        ct.alignment = 0        # left alignment
        ct.firstLineIndent = 2 * 12
        ct.leading = 18         # line interval
        ct.spaceAfter = 8
        return ct


class PDFWriter(object):
    def __init__(self, font_name=None):
        self.list = []
        self.guides = []
        if font_name:
            assert font_name in FONT_NAMES, "{} not in {}!".format(font_name, FONT_NAMES)
            global FONT_NAME
            FONT_NAME = font_name

    def write(self, item):
        write_func = getattr(self, "write_{}".format(item['type']))
        write_func(item)

    def write_img(self, item):
        img = Image(item['value'])
        W, H = A4
        MAX_W = W * 0.5
        MAX_H = H * 0.5
        ratio_w = MAX_W / img.imageWidth
        ratio_h = MAX_H / img.imageHeight
        ratio = min(ratio_w, ratio_h)
        img.drawWidth = img.imageWidth * ratio
        img.drawHeight = img.imageHeight * ratio
        self.list.append(img)

    def write_text(self, item):
        ct = getattr(FontStyles, item['font'])()
        if item['href']:
            p = Paragraph("<a href=#{} color=blue>{}</a>".format(item['href'], item['value']), ct)
        else:
            p = Paragraph(item['value'], ct)
        self.list.append(p)

    def write_label(self, label):
        ct = getattr(FontStyles, 'h4')()
        p = Paragraph('<a name="{}"/>'.format(label), ct)
        self.list.append(p)

    def write_new_page(self):
        if len(self.list) > 0:
            self.list.append(PageBreak())

    def set_guides(self, guides):
        self.guides = guides

    def export_pdf(self, out_pdf_path):
        doc = SimpleDocTemplate(out_pdf_path, pagesize=A4)
        doc.build(self.list, onFirstPage=self.header_footer, onLaterPages=self.header_footer)

    def header_footer(self, canvas, doc):
        canvas.saveState()
        canvas.setFont(FONT_NAME, 10)
        W, H = A4
        canvas.drawString(W / 2, 30, "- %d -" % doc.page)
        # set OutlineEntry
        for title, key in self.guides:
            # print("Set OutlineEntry:", title, key)
            canvas.addOutlineEntry(title, key, level=0)
            canvas.showOutline()
        self.guides.clear()