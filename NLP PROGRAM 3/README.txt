How to compile:
->For the ner program: python ner.py
->For the eval program: python eval.py

(Further instructions will be given in the command prompt itself when the program is run)
All the input files for both the programs should be in the same folder as the source code. It might work if they're put in a subfolder and the path is given correctly, but I haven't checked that.

One weird thing I noticed is that for the prediction file, I had to split the lines by '\r' and for the gold file, by '\n' (which is what we normally 
do.) Both files look the same, but programatically, it didn't work when I split the prediction file by '\n'. So I've added a small fix for that by first trying to split using '\n' and if that doesn't work, split by '\r'.

I haven't tried this on a cade machine.
