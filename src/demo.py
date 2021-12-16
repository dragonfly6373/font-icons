import os
import re
import json

class Demo:
    def __init__(self, ddata, prefix = "vnpt") -> None:
        self.ddata = ddata
        self.prefix = prefix

    def exportCss(self, outputdir = "./"):
        filename = os.path.join(outputdir, self.prefix + "-icons.css")
        with open(filename, "w", buffering=1024*2) as of:
            headerStr = '''@font-face {{
                font-family: '{prefix}-icons';
                src: url('./{prefix}-icons.eot');
                src: url('./{prefix}-icons.eot?#iefix') format('embedded-opentype'),
                    url('./{prefix}-icons.woff2') format('woff2'), 
                    url('./{prefix}-icons.woff') format('woff'),
                    url('./{prefix}-icons.ttf') format('truetype');
                font-weight: normal;
                font-style: normal;
            }}

            [class^="icon-{prefix}-"], [class*=" icon-{prefix}-"] {{
                font-family: '{prefix}-icons' !important;
                speak: none;
                position: relative;
                display: inline-block;
                font-style: normal;
                font-weight: 400;
                line-height: 1;
                -webkit-font-smoothing: antialiased;
                width: 1em;
                text-align: center;
                vertical-align: middle;

                -webkit-font-smoothing: antialiased;
                -moz-osx-font-smoothing: grayscale;
            }}
            '''.format(prefix = self.prefix)

            of.write(headerStr)

            print("# generate css:")
            for code, name in self.ddata.items():
                of.write(
                    '''.icon-{prefix}-{name}:before {{
                        content: "\{code}";
                    }}
                    '''.format(prefix = self.prefix, name = name , code = "{:04x}".format(code))
                )
            of.close()
            print(">>> output file: " + filename)
            return filename

    def _generateJsonData(self):
        return json.dumps(self.ddata, indent=4)

    def _replacement(self, matchobj):
        if matchobj.group() is not None:
            group = matchobj.group()
            print(group)
            if "title" in group: return self.prefix.upper() + " - Font Icons"
            if "prefix" in group: return self.prefix.lower()
            if "css_path" in group: return self.prefix + "-icons.css"
            if "jsondata" in group: return self._generateJsonData()

    def exportHtml(self, outputdir = "./"):
        filename = os.path.join(outputdir, "index.html")
        template = open(os.path.join(os.path.dirname(__file__), "template.html"), "rt")
        with open(filename, "w", buffering=1024*2) as of:
            for line in template.readlines():
                of.write(re.sub("\$\{([^}]+)\}", self._replacement, line))
            of.close()
        template.close()
        print(">>> output file: " + filename)

    def exportDemo(self, outputdir = "./"):
        self.exportCss(outputdir)
        self.exportHtml(outputdir)

