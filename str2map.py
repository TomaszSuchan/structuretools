#! /usr/bin/env python3
try:
    import pandas
except ImportError:
    raise ImportError("Pandas package not found, please install using: pip install pandas")
    

import argparse

def parse_args():
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
            dest="strinp",
            help='The file that was used for the Structure run')

    parser.add_argument('-s',
            type=str,
            dest="sep",
            default="_",
            help='The separator in the sample name, the scripts assumes the format: POP[separator]SAMPLE (default is underscore)')

    parser.add_argument('-i',
            type=argparse.FileType('r'),
            required=True,
            dest="strout",
            help='FastStructure output file')

    parser.add_argument('-o',
            type=argparse.FileType('w'),
            dest="output",
            default='-',
            help='Output file (default: STDOUT)')

    return parser.parse_args()

def main():
    args = parse_args()
    
    # Load populations file
    pops = pandas.read_table(args.popfile, header=None, delim_whitespace=True)
    pops.columns = ['pop','lon','lat']

    # Load Structure input file
    structureinp = pandas.read_table(args.strinp, header=None, delim_whitespace=True)
    # Get sample and population name from 1st column of the Structure input file
    samplenames = structureinp.iloc[::2,0]
    samplenames = samplenames.reset_index()[0]
    popnames = samplenames.str.rpartition('_')[0]

    # Load Structure output file
    structureout = pandas.read_table(args.strout, header=None, delim_whitespace=True)

    # Merge population name with Structure output
    structureout = structureout.round(0).astype(int) #round the likelihoods to 1 or 0
    structureout = pandas.concat([popnames, structureout], axis=1, ignore_index=True)

    # Get pivot table with populations as rows and haplotypes as columns
    # and merge with geographical coordinatesi
    pivottable = structureout.groupby(0, as_index = False).sum()
    pivottable = pops.merge(pivottable, how='right', left_on='pop', right_on=0)
    pivottable = pivottable.drop(0, 1) #remove second col with popnames in merged table

    # Write csv file for qGIS or to stdout
    if args.output:
    	args.output.write(pivottable.to_csv(sep='\t', index=False))
    else:
    	print(pivottable)
     
if __name__ == "__main__":
    main()

