#!/usr/bin/python

import os
import argparse
import json
import fontforge
import namelist
from demo import Demo

class Main:
    def __init__(self, sourcedir, prefix, outputdir):
        self.sourcedir = sourcedir
        self.prefix = prefix
        self.outputdir = outputdir

        self.validateFilePath(self.outputdir)
        self.ddata = dict(namelist.fromDir(self.sourcedir))

    def validateFilePath(self, filepath):
        if not os.path.exists(os.path.dirname(filepath)):
            try:
                os.makedirs(os.path.dirname(filepath))
            except OSError as exc:
                raise

    def loadConfig(self, font):
        config = json.loads(open('./font-config.json').read())
        font.fontname = config["fontname"]
        font.fullname = config["fullname"]
        font.familyname = config["familyname"]
        font.weight = config["weight"]
        font.version    = config["version"]
        font.encoding   = config["encoding"]
        font.copyright  = config["copyright"]
        font.em  = config["em"]
        font.ascent  = config["ascent"]
        font.descent  = config["descent"]

    def loadIcons(self, sourcedir):
        self.sourcedir = sourcedir

    def generateFont(self):
        f = namelist.toFile(self.ddata, os.path.join(self.outputdir, "namelist.nam"))
        fontforge.loadNamelist(f)
        font = fontforge.font()
        # self.loadConfig(font)

        # font = fontforge.open('blank.sfd')
        font.fontname = self.prefix + "-icons"
        font.familyname = self.prefix + "-icons"
        font.fullname = self.prefix + " icons"
        font.encoding = "UnicodeBmp"
        font.copyright = "Copyright VNPT © 2021"
        font.weight = "Regular"
        font.em = 2048
        font.ascent = 819
        font.descent = 205
        # font.addLookupSubtable('Anchors', 'DiacriticTop')
        # font.addAnchorClass('DiacriticTop', 'Top')
        # font.addLookupSubtable('Anchors', 'DiacriticBottom')
        # font.addAnchorClass('DiacriticBottom', 'Bottom')

        # glyph = font.createMappedChar('A')
        for code, name in self.ddata.items():
            print(". " + str(code) + " " + name)
            glyph = font.createChar(code, name)
            # glyph.glyphname = name
            glyph.importOutlines(os.path.join(self.sourcedir, '%s.svg' % name))
            # ymin = glyph.boundingBox()[1]
            glyph.transform([1, 0, 0, 1, 0, 0])

        font.round() # Needed to make simplify more reliable.
        font.simplify()
        font.removeOverlap()
        font.round()
        font.autoHint()
        font.generate(os.path.join(self.outputdir, self.prefix + "-icons.eot"))
        font.generate(os.path.join(self.outputdir, self.prefix + "-icons.ttf"))
        font.generate(os.path.join(self.outputdir, self.prefix + "-icons.woff"))
        font.generate(os.path.join(self.outputdir, self.prefix + "-icons.woff2"))
        # font.save(filepath)
        font.close()
        print(">>> export font: ", os.path.join(self.outputdir, self.prefix + "icons.woff"))

    def generateCss(self):
        print("generate css")

    def generateDemoHtml(self):
        demo = Demo(self.ddata, prefix="gomeet")
        demo.exportDemo(self.outputdir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Font Icon Generater')
    parser.add_argument("--projectname", default="font")
    parser.add_argument("--input")
    parser.add_argument("--output", default="./output")
    args = parser.parse_args()

    prefix    = args.projectname
    sourcedir = args.input
    outputdir = args.output

    app = Main(sourcedir, prefix, outputdir)
    app.generateFont()
    app.generateDemoHtml()
