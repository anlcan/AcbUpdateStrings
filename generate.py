#!/usr/bin/python

__author__ = 'anlcan'

from sys import argv
import re
import codecs
import subprocess

# https://developer.apple.com/library/mac/documentation/Cocoa/Conceptual/LoadingResources/Strings/Strings.html
ENCODING = "utf16"


def main(source_directory, original=None):

    """
    Finds localized strings in source files located in the source_directory, and updats original strings file
    """
    input_file = codecs.open(original, 'r', encoding=ENCODING)

    keys = dict()
    missing = list()

    lol = re.compile('/\*(.*)\*/"(.*)".*=.*"(.*)";')
    while True:
        line1 = input_file.readline().encode("utf8")
        while line1 and line1.strip() == "":
            line1 = input_file.readline().encode("utf8")
            
        line2 = input_file.readline().encode("utf8")
        while line2 and line2.strip() == "":
            line2 = input_file.readline().encode("utf8")
            
        l = line1.strip() + line2.strip()
        pp = lol.search(l)
        #print("item:"+l)
        
        if pp and pp.group(3):
            #print("groups:"+str(pp.groups())) 
            local_comment = pp.group(1).decode("utf8").encode("utf8").strip()
            local_key = pp.group(2).decode("utf8").encode("utf8")
            local_value = pp.group(3).decode("utf8").encode("utf8")
            #print (local_key)
            keys[local_key] = [local_value, local_comment]
            
        if not line2 : break

    print("// keys found:" + str(keys.__len__()))

    erp = re.compile('NSLocalizedString\(@"(.*)",(.*)\)')

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
                found_comment = p.group(2).decode("utf8").encode("utf8").strip()
                if found_comment.startswith("@\"") and found_comment.endswith("\""):
                    found_comment = found_comment[2:-1]
                if not keys.__contains__(found_key):
                    missing.append([found_key, found_comment])

    print("// missing   :" + str(missing.__len__()))

    output_file = codecs.open("Localizable.strings", 'w', encoding=ENCODING)
    for k, [v,c] in keys.items():
        l = '/* ' + c + ' */\n"' + k + '" = "' + v + '";\n\n'
        print l
        output_file.write(unicode(l, "utf8"))

    print ("# missing keys follow")

    for [l,c] in missing:
        line = '/* ' + c + ' */\n"' + l + '" = "";\n'
        print line
        output_file.write(unicode(line, "utf8"))


if __name__ == "__main__":
    if argv.__len__() != 3 or not argv[1] or not argv[2]:
        print """
                missing arguments
                usage : generate.py <path_to_folder_with_source_files> <path_to_Localizable.strings_file>
              """
    else:
        main(argv[1], argv[2])
