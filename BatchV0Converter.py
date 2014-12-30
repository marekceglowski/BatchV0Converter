import os
import os.path
import sys
import subprocess
from mutagen.mp3 import MP3

# Quick and dirty script for batch conversion of 320 MP3 files to V0
# Marek Ceglowski

# This function finds all mp3s in a directory and its subdirectories with
# a bitrate of 320
def walk(dir):
    mp3s = []
    dir = os.path.abspath(dir)
    for file in [file for file in os.listdir(dir) if not file in [".",".."]]:
        nfile = os.path.join(dir,file)
        basename, extension = os.path.splitext(nfile)
        if (extension == '.mp3'):
            f = MP3(nfile)
            bitrate = f.info.bitrate / 1000
            if (bitrate == 320):
                mp3s.append(str(nfile))
        if os.path.isdir(nfile):
            sublist = walk(nfile)
            mp3s.extend(sublist)
    return mp3s

def main():
    program = 'lame.exe'
    print('Batch V0 Converter')
    print('------------------')
    print('This program takes a folder and recursively finds all mp3 files ' +
          'with a constant bitrate of 320kbps in it (and subfolders). ' +
          'Then it converts them all to variable bitrate of v0 and places them ' +
          'into <your folder>\converted\ in the same subfolder layout. Enjoy!' +
          '\nBy: Marek Ceglowski')
    path = input('\nPlease enter folder location of MP3 files:\n')
    outpath = path+'\\converted'
    
    filelist = walk(path)   # Get list of 320-mp3 files
    if not os.path.exists(outpath):
        os.makedirs(outpath)    # Create \converted\ folder
    
    for f in filelist:
        pathout = f.replace(path, outpath)
        if not os.path.exists(os.path.dirname(pathout)):
            os.makedirs(os.path.dirname(pathout))   # Create new subfolder
        arguments = [program,'-V0',f,pathout]   # LAME arguments
        subprocess.call(arguments)  # Run LAME with arguments
    print('Done!')
    return 0

if __name__ == '__main__':
    status = main()
    sys.exit(status)
