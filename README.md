# structuretools
Tools for easy plotting fastStructure output

## str2map.py
Tool to parse fastStructure output, sample information in the structure input file, and population fileinto a csv file for qGIS.

```
usage: str2map.py [-h] -p POPFILE -f STRFILE [-s SEP] -i STRUCTURE
                  [-o OUTFILE]

Produce csv files for importing into qGIS from structure files.

optional arguments:
  -h, --help    show this help message and exit
  -p POPFILE    Text file with population names, longitude and latitude, in
                this order
  -f STRFILE    The file that was used for the Structure run
  -s SEP        The separator in the sample name, the scripts assumes the
                format: POP[separator]SAMPLE
  -i STRUCTURE  Structure output file
  -o OUTFILE    Output file (default: STDOUT)
```
