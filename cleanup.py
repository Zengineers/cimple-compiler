# automates cleanup of the output files from the cimple compiler

# run command:
# python3 cleanup.py <cimple file> <optional arg>
#
# <cimple file>: the cimple program file path ending in .ci whose output files will be deleted
#       (the .ci file is not deleted)


import os, sys

def clean(fileExtension):
        if os.path.exists(inputFile + fileExtension):
            os.remove(inputFile + fileExtension)

inputFile = sys.argv[1].replace('.ci', '')

if len(inputFile) > 1:
    clean('.int')
    clean('.c')
    clean('.sym')
    clean('.asm')



