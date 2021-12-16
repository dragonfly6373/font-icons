import os

def intToHex(number):
    return "0x{:04x}".format(number)

def hexToInt(hexstr):
    return int(hexstr, 16)

def fromDir(inputdir, startnumber = 59648):
    files = os.listdir(inputdir)
    fnames = map(lambda f: os.path.splitext(os.path.basename(f))[0], files)
    index = 0
    for name in sorted(fnames):
        # print(intToHex(startnumber + index) + " " + name)
        yield (startnumber + index), name
        index += 1

def toFile(ddata, outputfile = "./namelist.nam"):
    with open(outputfile, "w", buffering=1024**2) as of:
        for code, name in dict(ddata).items():
            of.write(intToHex(code) + " " + name + os.linesep)
        of.close()
        print(">> write to file: " + outputfile)
        return outputfile

def generateNamelistFile(inputdir, startnumber = 59648, outputfile = "./namelist.nam"):
    return toFile(fromDir(inputdir, startnumber), outputfile)

def _converter(s):
    arr = s.replace("\r", "").replace("\n", "").split(" ")
    return (hexToInt(arr[0]), arr[1])

def fromFile(filepath):
    instream = open(filepath, "r")
    return dict(map(_converter, instream.readlines()))
