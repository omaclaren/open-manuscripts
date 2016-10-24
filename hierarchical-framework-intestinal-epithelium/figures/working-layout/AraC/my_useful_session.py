---

gs -dNOPAUSE -sDEVICE=pdfwrite -sOUTPUTFILE=stamp-test.pdf -dBATCH stamp.pdf prior-post-pro-vel-cropped.pdf
pdfnup stamp-test.pdf --nup 2x1 --landscape --outfile stamp-test-side.pdf

pdfjam --keepinfo --landscape --trim "100mm 0mm 0mm 0mm" --clip true stamp-test-side.pdf -o test-side-cropped.pdf
pdfjam --keepinfo --landscape --trim "0mm 0mm 100mm 0mm" --clip true stamp-test-side.pdf -o stamp-side-cropped.pdf

from pdfrw import PdfReader, PdfWriter, PageMerge
ipdf = PdfReader('test-side-cropped.pdf')
wpdf = PdfReader('stamp-side-cropped.pdf')
PageMerge(ipdf.pages[0]).add(wpdf.pages[0]).render()
PdfWriter().write('newfile.pdf', ipdf)

pdfcrop --margins '-120 5 -140 5' newfile.pdf newfile-cropped.pdf


---





# coding: utf-8
from PyPDF2 import PdfFileWriter, PdfFileReader
output = PdfFileWriter()
ipdf = PdfFileReader(open('prior-post-pro-vel-cropped.pdf', 'rb'))
wpdf = PdfFileReader(open('prior-posterior-stamp.pdf', 'rb'))
watermark = wpdf.getPage(0)
page = ipdf.getPage(0)
page.mergePage(watermark)
output.addPage(page)
with open('newfile.pdf', 'wb') as f:
    output.write(f)
    
from pdfrw import PdfReader, PdfWriter, PageMerge
ipdf = PdfReader('prior-post-pro-vel-cropped.pdf')
wpdf = PdfReader('prior-posterior-stamp.pdf')
#wmark = PageMerge().add(wpdf.pages[0])[0]

PageMerge(ipdf.pages[0]).add(wpdf.pages[0]).render()

#for page in ipdf.pages:
#    PageMerge(page).add(wmark).render()
PdfWriter().write('newfile.pdf', ipdf)

get_ipython().magic(u'histoty')
get_ipython().magic(u'history')

---

#gs -dNOPAUSE -sDEVICE=pdfwrite -sOUTPUTFILE=stamp-test.pdf -dBATCH stamp.pdf test.pdf

gs -dNOPAUSE -sDEVICE=pdfwrite -sOUTPUTFILE=stamp-test.pdf -dBATCH stamp.pdf prior-post-pro-vel-cropped.pdf
pdfnup stamp-test.pdf --nup 2x1 --landscape --outfile stamp-test-side.pdf

pdfjam --keepinfo --landscape --trim "100mm 0mm 0mm 0mm" --clip true stamp-test-side.pdf -o test-side-cropped.pdf
pdfjam --keepinfo --landscape --trim "0mm 0mm 100mm 0mm" --clip true stamp-test-side.pdf -o stamp-side-cropped.pdf







pdfjam --keepinfo --trim "10mm 15mm 10mm 15mm" --clip true --suffix "cropped" stamp-test-side.pdf
pdfcrop --margins '5 5 5 5' stamp-side-cropped.pdf stamp-side-cropped.pdf
pdfcrop --margins '5 5 5 5' test-side-cropped.pdf test-side-cropped.pdf
pdfcrop --margins '0 0 -470 0' stamp-test-side-cropped.pdf stamp-test-side-cropped-stamp.pdf
pdfcrop --margins '-200 0 0 0' stamp-test-side-cropped.pdf stamp-test-side-cropped-prof.pdf



---
gs -dNOPAUSE -sDEVICE=pdfwrite -sOUTPUTFILE=stamp-test.pdf -dBATCH stamp.pdf prior-post-pro-vel-cropped.pdf
pdfnup stamp-test.pdf --nup 2x1 --landscape --outfile stamp-test-side.pdf

pdfjam --keepinfo --landscape --trim "100mm 0mm 0mm 0mm" --clip true stamp-test-side.pdf -o test-side-cropped.pdf
pdfjam --keepinfo --landscape --trim "0mm 0mm 100mm 0mm" --clip true stamp-test-side.pdf -o stamp-side-cropped.pdf

from pdfrw import PdfReader, PdfWriter, PageMerge
ipdf = PdfReader('test-side-cropped.pdf')
wpdf = PdfReader('stamp-side-cropped.pdf')
PageMerge(ipdf.pages[0]).add(wpdf.pages[0]).render()
PdfWriter().write('newfile.pdf', ipdf)

pdfcrop --margins '5 5 5 5' newfile.pdf newfile-cropped.pdf





from pdfrw import PdfReader, PdfWriter, PageMerge
ipdf = PdfReader('stamp.pdf')
wpdf = PdfReader('test.pdf')
wmark = PageMerge().add(wpdf.pages[0])[0]

for page in ipdf.pages:
    PageMerge(page).add(wmark).render()
PdfWriter().write('newfile.pdf', ipdf)





from reportlab.pdfgen.canvas import Canvas
from pdfrw import PdfReader
from pdfrw.toreportlab import makerl
from pdfrw.buildxobj import pagexobj

input_file = "prior-post-pro-vel-cropped.pdf"
output_file = "prior-post-pro-vel-cropped_footer.pdf"

# Get pages
reader = PdfReader(input_file)
pages = [pagexobj(p) for p in reader.pages]


# Compose new pdf
canvas = Canvas(output_file)

for page_num, page in enumerate(pages, start=1):
    
    # Add page
    canvas.setPageSize((page.BBox[2], page.BBox[3]))
    canvas.doForm(makerl(canvas, page))
    
    # Draw footer
    footer_text = "Page %s of %s" % (page_num, len(pages))
    x = 128
    canvas.saveState()
    canvas.setStrokeColorRGB(0, 0, 0)
    canvas.setLineWidth(0.5)
    canvas.line(66, 78, page.BBox[2] - 66, 78)
    canvas.setFont('Times-Roman', 10)
    canvas.drawString(page.BBox[2]-x, 65, footer_text)
    canvas.restoreState()
    
    canvas.showPage()

canvas.save()
