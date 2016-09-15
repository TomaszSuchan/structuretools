# structuretools
Tools for easy plotting fastStructure output

## str2map.py
Tool to parse fastStructure output, sample information in the structure input file, and population fileinto a csv file for qGIS.

Usage:

```
str2map.py [-h] -p POPFILE -f STRFILE [-s SEP] -i STRUCTURE
                  [-o OUTFILE]

arguments:
  -h, --help    show this help message and exit
  -p POPFILE    Text file with population names, longitude and latitude, in
                this order
  -f STRFILE    The file that was used for the Structure run
  -s SEP        The separator in the sample name, the scripts assumes the
                format: POP[separator]SAMPLE (default is underscore)
  -i STRUCTURE  Structure output file
  -o OUTFILE    Output file (default: STDOUT)
```

Example:

```
./str2map.py -p sampledata/populations-str.txt 
-f sampledata/samples-str.txt -i sampledata/k4-str -o out.csv
```

## plotmap.py
Tool for plotting a map from `str2map.py` output.

Usage:

```
plotmap.py [-h] -i INPUT [-o OUTPUT] [-c] [-p PIESIZE]

arguments:
  -h, --help  show this help message and exit
  -i INPUT    Input file or STDIN (default), with pop, lon, lat and population
              assigment columns; as produced by str2map.py script.
  -o OUTPUT   Output file name; supports png, pdf, ps, eps and svg.
  -c          Uses point coordinates to calculate map extent. If not used,
              the default extent is Europe.
  -p PIESIZE  Size of the piecharts; default = 300.
  -a ALPHA    Opacity of piecharts; 0.0 transparent through 1.0 opaque 
              (default).
```

Example:

```
./plotmap.py -i out.csv -o map.png
```

Important note - currently 10-colour palette is hardcoded in the script, you can use more by changing `Tableau_10` in the line 28 to `Tableau_20` if you structure file has K > 10.

## Piping the above scripts

You can skip saving the intermediate csv file and pipe `str2map.py` output directly to `plotmap.py`:

```
./str2map.py -p sampledata/populations-str.txt 
-f sampledata/samples-str.txt -i sampledata/k4-str | ./plotmap.py -o map.png
```
