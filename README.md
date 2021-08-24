## Cimple Compiler


#### SUMMARY

Cimple is a simplified version of the C programming language with educational purposes.\
Its capabilities are limited, however, it contains many well-known control flow statements. \
Cimple program files have a .ci extension. A full language description can be found in the report\
files (ENG or GR). The compiler was developed for the Compilers course [@cse.uoi.gr](https://www.cs.uoi.gr/) and\
the final code produced is in MIPS32 assembly.
<br><br>


#### CONTENTS

* `cimple.py`: the compiler
* `cimple-test-files`: various Cimple programs used for testing purposes
* `compilation-output`: examples of the files created from the compilation
* `report`: thorough project reports in both English and Greek.
* `cleanup.py`: used to clean any unwanted files created from the compilation
<br><br>


#### EXECUTION

* Run command: `python3 cimple.py <cimple file> <optional arg>`\
    &emsp;`<cimple file>`: the cimple program file path to be compiled ending in .ci\
    &emsp;`<optional arg>`: can be one of the following\
    &emsp;&emsp;    -lex: print lex tokens on screen\
    &emsp;&emsp;    -ic: print intermediate code quad on screen\
    &emsp;&emsp;    -st: print symbol table on screen\
    &emsp;&emsp;    -asm: print final assembly code on screen

* By default the compiler creates 3 files:\
    &emsp;   .int file with the intermediate code\
    &emsp;   .sym file with the symbol table\
    &emsp;   .asm file with the final MIPS assembly code
   
* If the cimple program has no function or procedure an extra C file equivalent is created\
    which contains the intermediate code quads as low level C code. (can be compiled with any C compiler)

* The produced final code can be assembled and executed with MARS 4.5:\
[MIPS Assembler and Runtime Simulator](http://courses.missouristate.edu/KenVollmar/mars/) 
<br><br>


#### LANGUAGE

Python 3.8.5