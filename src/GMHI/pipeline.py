import subprocess
import pandas as pd
import os
from . import utils
from . import predict_health


def repair():
    # takes about 18s
    print("repairing sequences")
    subprocess.call(
        [
            "repair.sh",
            "in1=in1.fastq",
            "in2=in2.fastq",
            "out1=repaired1.fastq",
            "out2=repaired2.fastq",
            "outs=garbage",
        ]
    )


def quality_control():

    # takes about 2 mins
    subprocess.call(["fastqc", "repaired1.fastq"])
    subprocess.call(["fastqc", "repaired2.fastq"])

    subprocess.call(["unzip", "repaired1_fastqc.zip"])
    subprocess.call(["unzip", "repaired2_fastqc.zip"])


def extract_adapters():
    print("extracting adapter sequences")
    path = os.path.join(utils.DEFAULT_DB_FOLDER, "extract_adapter.sh")
    subprocess.call([path])


def remove_human():
    print("Removing human contaminants")
    subprocess.call(
        [
            "bowtie2",
            "-p",
            "16",
            "-x",
            os.path.join(utils.DEFAULT_DB_FOLDER, "GRCh38_noalt_as", "GRCh38_noalt_as"),
            "-1",
            "repaired1.fastq",
            "-2",
            "repaired2.fastq",
            "-S",
            "mapped.sam",
        ]
    )

    my_cmd = ["samtools", "view", "-bS", "mapped.sam"]
    with open("mapped.bam", "w") as outfile:
        subprocess.call(my_cmd, stdout=outfile)

    my_cmd = ["samtools", "view", "-b", "-f", "12", "-F", "256", "mapped.bam"]
    with open("human.bam", "w") as outfile:
        subprocess.call(my_cmd, stdout=outfile)

    my_cmd = [
        "samtools",
        "sort",
        "-n",
        "human.bam",
        "-o",
        "human_sorted.bam",
        "--threads",
        "16",
    ]
    subprocess.call(my_cmd)

    my_cmd = [
        "bedtools",
        "bamtofastq",
        "-i",
        "human_sorted.bam",
        "-fq",
        "human1.fastq",
        "-fq2",
        "human2.fastq",
    ]
    subprocess.call(my_cmd)


def remove_adapters_and_crap_reads():
    print("Removing adapter sequences and low quality reads")

    cmd = [
        "cat",
        "adapter1.txt",
        "adapter2.txt",
        os.path.join(utils.DEFAULT_DB_FOLDER, "TruSeq3-PE.fa"),
    ]
    with open("adapters.txt", "w") as outfile:
        subprocess.call(cmd, stdout=outfile)

    cmd = [
        "trimmomatic",
        "PE",
        "-threads",
        "16",
        "human1.fastq",
        "human2.fastq",
        "-baseout",
        "QC.fastq.gz",
        "ILLUMINACLIP:adapters.txt:2:30:10:2:keepBothReads",
        "LEADING:3",
        "TRAILING:3",
        "MINLEN:60",
    ]
    subprocess.call(cmd)

def profile_metagenome():
    print("Profiling metagenome")
    database_dir = os.path.join(utils.DEFAULT_DB_FOLDER, "clade_markers")
    cmd = [
        "metaphlan2.py",
        "QC_1P.fastq.gz,QC_2P.fastq.gz",
        "--bowtie2db", database_dir,
        "--bowtie2out", "bowtieout.bowtie2.bz2", 
        "--index", "mpa_v20_m200",
        "--nproc", "16", "--input_type", "fastq", 
        "-o", "metaphlan2.txt"
    ]
    subprocess.call(cmd)

    cmd = [
        "merge_metaphlan_tables.py", "metaphlan2.txt"
    ]
    with open('merged.txt', "w") as outfile:
        subprocess.run(cmd, stdout=outfile)

    path = os.path.join(utils.DEFAULT_DB_FOLDER, "species_only.sh")
    subprocess.call([path])

def health_index(args):
    print("calculating health index")
    score = predict_health.get_score()
    print("GMHI2 score:", score)
    try:
        f = args.output
        with open(f, 'w') as file:
            file.write(str(score) + "\n")
    except:
        pass

def remove_intermediate():
    to_remove = [
        # "GMHI2.txt",
        "QC_1P.fastq.gz",
        "QC_1U.fastq.gz",
        "QC_2P.fastq.gz",
        "QC_2U.fastq.gz",
        # "SRR6468520.srarp_1.fastq",
        # "SRR6468520.srarp_2.fastq",
        # "abundance.txt",
        "adapter1.txt",
        "adapter2.txt",
        "adapters.txt",
        "bowtieout.bowtie2.bz2",
        "garbage",
        "human.bam",
        "human1.fastq",
        "human2.fastq",
        "human_sorted.bam",
        "in1.fastq",
        "in2.fastq",
        "mapped.bam",
        "mapped.sam",
        "merged.txt",
        "metaphlan3.txt",
        "repaired1.fastq",
        "repaired1_fastqc",
        "repaired1_fastqc.html",
        "repaired1_fastqc.zip",
        "repaired2.fastq",
        "repaired2_fastqc",
        "repaired2_fastqc.html",
        "repaired2_fastqc.zip",
        # "test.ipynb",
        # "test.py",
    ]
    cmd = ["rm", "-rf"] + to_remove
    subprocess.call(cmd)


def run(args):

    # read inputs
    in1, in2 = args.fastq1, args.fastq2
    # print("Inputs:", in1, in2)

    # make a copy of input files with simpler name
    subprocess.call(["cp", in1, "in1.fastq"])
    subprocess.call(["cp", in2, "in2.fastq"])

    repair()
    quality_control()
    extract_adapters()
    remove_human()
    remove_adapters_and_crap_reads()
    profile_metagenome()
    health_index(args)
    remove_intermediate()