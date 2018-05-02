#!/gpfs/data01/sjroth/software/anaconda3/bin/python3.6
'''
Script for performing a modified fastq-dump. Can do this for batches of files.
'''
from Helpers import *
import argparse

def main():

    #Get command line arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument("-s","--sra",help="SRA ID",action="append")
    parser.add_argument("-n","--num-cpu",help="Number of CPUs",type=int,default=1)
    parser.add_argument('-o',"--outdir",help="Output Directory",default=".")
    parser.add_argument("--paired_end",help="Paired End Experiment",action="store_true")
    parser.add_argument("-c","--compression",help="Compression Method",default=None)
    parser.add_argument("--scratch",help="Scratch Location",default=None)

    args = parser.parse_known_args()[0]

    #Run the fastq-dump.
    if args.sra:

        for sra in args.sra:

            #Get metadata.
            num_spots = get_num_spots(sra)
            intervals = divide_spots(num_spots,args.num_cpu)

            #Run the fastq-dump.
            parallel_dump(sra,intervals,args.paired_end,args.outdir,args.compression)

        #Clear the scratch if specified.
        if args.scratch:
            shutil.rmtree(args.scratch)

    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()