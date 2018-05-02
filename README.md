# GEO_Download
Program for harnessing multithreading in order to piggy back off of the SRA toolkit function called fastq-dump for faster downloads as well as batch downloads. This is the first version.

## Getting Started
These are instructions for how to get off the ground with this project.

### Prerequisites
The SRA toolkit software suite has a program called fastq-dump that will be used here so that is the only requirement for external software. The easiest way to install is via anaconda's bioconda channel.
```
conda install sra-tools
```

### Optional Tips
fastq-dump has a weird default setting where it writes to your scratch automatically to cache the SRA files. This is a good function as fetching the SRA file is more time costly than dumping the SRA to a fastq directly. However, despite the speed gain, there is an issue. By writing to your default scratch, it can mess up your local memory. Thus, I suggest creating your own temporary scratch to avoid this. Here is how you do this: [SRA Toolkit Configuration Wiki](https://github.com/ncbi/sra-tools/wiki/Toolkit-Configuration)

This is completely optional but suggested heavily. Remember this new scratch because you want to delete this after each batch download. This program actually has an option to do this automatically.

To make this script executable (i.e., you don't have to type python /path_to_script/modified_fastq_dump.py), add a shebang command at the top of the modified_fastq_dump.py file like so:
```
#!/gpfs/data01/sjroth/software/anaconda3/bin/python3.6
```
Then, run the following command:
```
chmod +x /path_to_script/modified_fastq_dump.py
```
Finally, edit your .bashrc:
```
export PATH=/gpfs/data01/sjroth/Pipelines/GEO_Download:$PATH
```

## Running the program
Once you have the prequisites, this program is very simple to run. If you have this installed as an executable, omit the python step as it is redundant.
```
python modified_fastq_dump.py -s SRA_IDs -n NUM_CPU -o OUTDIR -c COMPRESSION_METHOD --scratch SCRATCH_LOCATION
```
An optional flag is --paired_end for paired end files. This flag requires that you separate batches of single end files and paired end files. Future versions may include autodetection of these properties. Available compression methods are gzip and bzip2. These are suggested.
