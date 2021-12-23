#!/usr/bin/env python3

# adjusted from https://gist.github.com/chriscasola/4700426
# change: ignores section between ```....``` - markdown shows them without formatting.

import sys
import re


def processFile(in_file, out_file):

    with open (in_file, "r") as in_file:
        in_file_data = in_file.read()

    with open(out_file, "w") as newFile:
        toc = []
        levels = [0,0,0,0,0]
        tempFile = []
        tocLoc = 0
        partOfToc = False

        is_text = True

        section_start = 0

        while True:
            section_end = in_file_data.find("```", section_start)
            if section_end == -1:
                section_end = len(in_file_data)
            text_section = in_file_data[  section_start : section_end ]
            section_start = section_end + 3

            #print( f"is_text: {is_text} section_end: {section_end} text_section: {text_section}")

            if is_text:
                is_text = False

                for line in text_section.split('\n'):
                    line = line + '\n'

                    if partOfToc and line != '\n':
                        continue
                    else:
                        partOfToc = False
                    if 'Table of Contents' in line:
                        tocLoc = len(tempFile) + 1
                        partOfToc = True
                    elif line[0] == '#':
                        secId = buildToc(line, toc, levels)
                        line = addSectionTag(cleanLine(line), secId) + '\n'
                    tempFile.append(line)

            else:
                is_text = True
                tempFile.append("```")
                tempFile.append(text_section)
                tempFile.append("```")

            if section_start >= len(in_file_data):
                break

        for line in toc:
            tempFile.insert(tocLoc, line)
            tocLoc += 1
        tempFile.insert(tocLoc, "\n")

        #don't know, if that is of benefit.
        #tempFile.insert(0, '" Set text width as 72.' + "\n")

        for line in tempFile:
            newFile.write(line)


def addSectionTag(line, secId):
    startIndex = line.find(' ')
    line = line[:startIndex + 1] + '<a id=\'' + secId + '\' />' + line[startIndex + 1:]
    return line

def buildToc(line, toc, levels):
    line = cleanLine(line)
    secId = 's'
    if line[:5] == '#####':
        raise UserWarning('Header levels greater than 4 not supported')
    elif line[:4] == '####':
        levels[4] += 1
        secId += str(levels[1]) + '-' + str(levels[2]) + '-' + str(levels[3]) + '-' + str(levels[4])
        toc.append('        * [' + line[5:] + '](#' + secId + ')\n')
    elif line[:3] == '###':
        levels[3] += 1
        secId += str(levels[1]) + '-' + str(levels[2]) + '-' + str(levels[3])
        toc.append('      * [' + line[4:] + '](#' + secId + ')\n')
    elif line[:2] == '##':
        levels[2] += 1
        levels[3] = 0
        secId += str(levels[1]) + '-' + str(levels[2])
        toc.append('  * [' + line[3:] + '](#' + secId + ')\n')
    elif line[:1] == '#':
        levels[1] += 1
        levels[3] = levels[2] = 0
        secId += str(levels[1])
        toc.append('* [' + line[2:] + '](#' + secId + ')\n')
    return secId

def cleanLine(text):
    text = stripNewline(text)
    text = removeAnchors(text)
    return text

def stripNewline(text):
    return text.replace('\n', '')

def removeAnchors(text):
    while ('<' in text and '>' in text):
        leftTag = text.index('<')
        rightTag = text.index('>')
        text = text[0:leftTag] + text[rightTag + 1:]
    return text

if __name__ == "__main__":
    processFile(sys.argv[1], sys.argv[2])

