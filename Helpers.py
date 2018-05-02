'''
Helper functions for modified fastq-dump.
'''
import subprocess
import sys
import os
import shutil

'''
Define a function that can get the number of spots in a given SRA. This helps with parallelizing runs.
'''
def get_num_spots(sra_id):

    p = subprocess.Popen(["sra-stat", "--meta", "--quick", sra_id], stdout=subprocess.PIPE)
    stdout, stderr = p.communicate()
    txt = stdout.decode().rstrip().split("\n")
    total = 0
    for l in txt:
        total += int(l.split("|")[2].split(":")[0])

    return total

'''
Define a function that can divide the spots into intervals.
'''
def divide_spots(num_spots,num_threads):

    step = int(num_spots/num_threads)
    intervals = list(range(0,num_spots+1,step))
    intervals[-1] = num_spots

    return [[intervals[i]+1,intervals[i+1]] for i in range(len(intervals)-1)]

'''
Define a function that can execute a parallelized fastq-dump. This is essentially a wrapper for fastq-dump that takes 
advantage of the ability for fastq-dump to dump specific portions of the fastq file.
'''
def parallel_dump(sra_id,intervals,paired_end=False,out_dir="",compression="gzip"):

    #Format split and compression command.
    if paired_end:
        split_cmd = ["--split-files"]
    else:
        split_cmd = []
    if compression:
        compression_cmd = [f"--{compression}"]
    else: compression_cmd = []

    #Begin fastq-dump.
    if os.path.exists(f"temp_{sra_id}"):
        shutil.rmtree(f"temp_{sra_id}")
    processes = []
    for i in range(len(intervals)):

        curr_temp_folder = f"temp_{sra_id}/{i}"
        cmd = ["fastq-dump","-N",str(intervals[i][0]),"-X",str(intervals[i][1]),"-O",
               curr_temp_folder]+split_cmd+compression_cmd+[sra_id]
        p = subprocess.Popen(cmd)
        processes.append(p)

    for i in range(len(intervals)):

        exit_code = processes[i].wait()
        if exit_code != 0:
            sys.stderr.write(f"fastq-dump error! exit code: {exit_code}\n")
            sys.exit(exit_code)

    #Join files and remove temporary files.
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    if out_dir == ".":
        out_dir = ""
    if compression == "gzip":
        extension = ".gz"
    elif compression == 'bzip2':
        extension = ".bz2"
    else:
        extension = ""

    if paired_end: 
        subprocess.call(f"cat temp_{sra_id}/*/{sra_id}_1.* > {out_dir}{sra_id}_1.fastq{extension}",shell=True)
        subprocess.call(f"cat temp_{sra_id}/*/{sra_id}_2.* > {out_dir}{sra_id}_2.fastq{extension}", shell=True)

    else:
        subprocess.call(f"cat temp_{sra_id}/*/{sra_id}.* > {out_dir}{sra_id}.fastq{extension}",shell=True)

    shutil.rmtree(f"temp_{sra_id}")