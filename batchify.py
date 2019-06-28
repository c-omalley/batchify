#!/usr/bin/env python
#--------------------------------------------------------------------------
# File: batchify.py
#
# Create a CMD.EXE batch file to run Python scripts as commands
#--------------------------------------------------------------------------

import os, sys

# Settings ----------------------------------------------------------------
# Set SCRIPTS to the folder where batch files will be places. This folder
# should be named in the PATH environment variable. If None, the batchify 
# will check for a "Script" folder in "%USERPROFILE%\Documents"
SCRIPTS = None

# batchify ----------------------------------------------------------------
# Create a Windows Batch File that will call the given script. Returns
# the name of the batch file created.
def batchify(script, python=None, args=None):

    '''Create a Windows Batch File that will call the given script.
    Returns the name of the batch file created.
    
    Arguments:

        -script     Path to python script file (required)
        -python     Path to alternate python interpreter     
        -args       Arguments to add to the script call in the batch file
    '''

    # Change a filename's suffix (e.g. "hello.py" --> "hello.bat")
    def suffix(filename, s):
        name, _ = os.path.splitext(filename)
        return name + s
 
    # Python
    python = sys.executable if not python else python
    
    # Additional arguments for the script command line
    args = [] if not args else args

    # Full path to the script
    script = os.path.abspath(script)

    # Write batch file
    batchfile = suffix(os.path.basename(script), '.bat')
    template = f'''@echo off
REM
REM {batchfile}
REM
REM Synopsis

REM Settings ----------------------------------------------------------

set PYTHON="{sys.executable}"

set SCRIPT="{script}"

REM -------------------------------------------------------------------

%PYTHON% %SCRIPT% {" ".join(args)} %*
'''
    with open(batchfile, 'w') as f:
        f.write(template)

    return batchfile


if __name__ == '__main__':

    import shutil

    # Find installation folder
    # Assume $HOME/Documents/Scripts/
    folder = SCRIPTS
    if not(SCRIPTS):
        for v in ('HOME', 'USERPROFILE'):
            try:
                folder = os.path.join(os.environ[v], 'Documents', 'Scripts')
                break
            except KeyError:
                pass
    if not folder:
        folder = os.getcwd()
    elif not os.path.exists(folder):
        os.makedirs(folder)
    
    # Process scripts
    for filename in sys.argv[1:]:
        batchfile = batchify(filename)
        if not folder == os.getcwd():
            destination = os.path.join(folder, batchfile)
            if os.path.exists(destination):
                os.remove(destination)
            shutil.move(batchfile, folder)
        print(f"{batchfile} --> {folder}")