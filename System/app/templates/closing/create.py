import pdfkit
import jinja2
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(BASE_DIR, "index.html")

def createPDF(info, outputPath:str, pathHTML=html_path):
  try:
    print(html_path)
    nameHTML = os.path.basename(pathHTML)
    print(nameHTML)
    print(pathHTML)
    pathHTML = os.path.dirname(pathHTML)
    
    pathHTML = os.path.normpath(pathHTML)
    
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(pathHTML))
    template = env.get_template(nameHTML)
    html = template.render(info)
    
    options = {
      "page-size": "Letter",
      "margin-top": "0.05in",
      "margin-bottom": "0.05in",
      "margin-left": "0.05in",
      "margin-right": "0.05in",
      "encoding": "UTF-8",
      "enable-local-file-access": True,
      "quiet": False,
      "no-stop-slow-scripts": True,
      "disable-javascript": True
    }
    
    wkhtmltopdfPath = os.path.join(BASE_DIR, "../..", "bin", "wkhtmltopdf.exe")
    wkhtmltopdfPath = os.path.abspath(wkhtmltopdfPath)
    print(f"wkhtmltopdf.exe path: {wkhtmltopdfPath}")

    
    if not os.path.exists(wkhtmltopdfPath):
      print(f"Error: wkhtmltopdf not found in", {wkhtmltopdfPath})
      return 
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    pdfName = f"Cierre_{timestamp}.pdf"
    outputPath = os.path.join(outputPath, pdfName)
    print(outputPath)
    
    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdfPath)
    
    pdfkit.from_string(html, outputPath, options=options, configuration=config)
    print(f"PDF generado correctamente: {outputPath}")
    return True
  except:
    raise