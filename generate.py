__author__ = 'anlcan'

from sys import argv
import re
import codecs
import subprocess

# https://developer.apple.com/library/mac/documentation/Cocoa/Conceptual/LoadingResources/Strings/Strings.html
ENCODING = "utf16"

"""
The first time you run the genstrings tool, it creates a set of new strings files
for you. Subsequent runs replace the contents of those strings files with the
current string entries found in your source code. For subsequent runs, it is a
good idea to save a copy of your current strings files before running genstrings.
You can then diff the new and old versions to determine which strings were
added to (or changed in) your project. You can then use this information to
update any already localized versions of your strings files, rather than replacing
those files and localizing them again
"""
def main(source_directory, original=None):

    input_file = codecs.open(original, 'r', encoding=ENCODING)

    keys = dict()
    missing = set()

    lol = re.compile('"(.*)".*=.*"(.*)";')
    for l in input_file.readlines():
        l = l.encode("utf8")
        pp = lol.search(l.strip())
        # print l

        if pp and pp.group(2):
            local_key = pp.group(1).decode("utf8").encode("utf8")
            local_value = pp.group(2).decode("utf8").encode("utf8")
            #print (local_key)
            keys[local_key] = local_value

    print("// keys found:" + str(keys.__len__()))

    erp = re.compile('NSLocalizedString\(@"(.*)",.*\)')

    findoutput = subprocess.check_output(["find", source_directory, "-name", '*.m'])
    source_files = findoutput.splitlines()
    for s in source_files:
        if s.find("conflicted") > 0:
            continue

        m = open(s.strip(), 'r')

        for line in m.readlines():
            if line.find("NSLocalizedString") > 0:
                p = erp.search(line)
                if not p:
                    continue

                found_key = p.group(1).decode("utf8").encode("utf8")
                if not keys.__contains__(found_key):
                    missing.add(found_key)

    print("// missing   :" + str(missing.__len__()))

    output_file = codecs.open("Localizable.strings", 'w', encoding=ENCODING)
    for k, v in keys.items():
        l = '"' + k + '"="' + v + '";\n'
        print l
        output_file.write(unicode(l, "utf8"))

    print ("# missing keys follow")

    for l in missing:
        line = '"' + l + '"="";\n'
        print line
        output_file.write(unicode(line, "utf8"))


if __name__ == "__main__":
    main(argv[1], argv[2])
