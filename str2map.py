#! /usr/bin/env python3
import pandas
import argparse

<<<<<<< HEAD
def parse_args():
=======
def parse_args()
>>>>>>> origin/master
    # Parse arguments
    parser = argparse.ArgumentParser(
            description="Produce csv files for importing into qGIS from structure files.")

    parser.add_argument('-p',
            type=argparse.FileType('r'),
            dest="popfile",
            required=True,
            help='Text file with population names, longitude and latitude, in this order')

    parser.add_argument('-f',
            type=argparse.FileType('r'),
            required=True,
            dest="strfile",
            help='The file that was used for the Structure run')

    parser.add_argument('-s',
            type=str,
            dest="sep",
            default="_",
            help='The separator in the sample name, the scripts assumes the format: POP[separator]SAMPLE')

    parser.add_argument('-i',
            type=argparse.FileType('r'),
            required=True,
            dest="structure",
            help='Structure output file')

    parser.add_argument('-o',
            type=argparse.FileType('w'),
            dest="outfile",
            default='-',
            help='Output file (default: STDOUT)')

    return parser.parse_args()

def main():
    args = parse_args()
    print(args)

    pops = pandas.read_table(args.popfile, header=None, delim_whitespace=True)
    pops.columns = ['pop','lon','lat']

    # Get sample and population name from the 1st column of the Structure input file
    strfile = pandas.read_table(args.strfile, header=None, delim_whitespace=True)
    samplenames = strfile.iloc[::2,0]
    samplenames = samplenames.reset_index()[0]
    popnames = samplenames.str.rpartition('_')[0]

    # Merge population name with Structure output
    structure = pandas.read_table(args.structure, header=None, delim_whitespace=True)
    structure = structure.round(0)
    structure = pandas.concat([popnames, structure], axis=1, ignore_index=True)

    # Get pivot table with populations as rows and haplotypes as columns
    # and merge with geographical coordinatesi
    pivottable = structure.groupby(0, as_index = False).sum()
    pivottable = pops.merge(pivottable, how='right', left_on='pop', right_on=0)
    pivottable = pivottable.drop(0, 1)

    # Write csv file for qGIS
    pivottable.to_csv(outfile) 

if __name__ == "__main__":
    main()

