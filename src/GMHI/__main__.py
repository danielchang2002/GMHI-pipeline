from . import prerun
from . import pipeline
import os
import argparse
from argparse import RawTextHelpFormatter

__author__ = "Daniel Chang, Vinod Gupta, Jaeyun Sung"
__version__ = "1.0"


def main():
    parser = argparse.ArgumentParser(
        description="DESCRIPTION:\n"
        "GMHI2 version " + __version__ + " \n"
        "Gut Microbiome Health Index (GMHI) is a robust index "
        "for evaluating health status based on the species-level taxonomic "
        "profile of a stool shotgun metagenome (gut microbiome) sample.\n\n"
        "AUTHORS: \n" + __author__ + "\n\n"
        "USAGE: \n"
        "GMHI is a pipeline that takes as input two raw fastq files generated "
        "from a paired end sequence, performs quality control, "
        "estimates microbial abundances, "
        "and returns as output a health index score.\n\n"
        "* Profiling a metagenome from raw reads:\n"
        "$ gmhi --fastq1 metagenome1.fastq --fastq2 metagenome2.fastq\n\n",
        formatter_class=RawTextHelpFormatter,
    )

    parser.add_argument("-o", "--output", help="Output file name") #, default="stdout")
    requiredNamed = parser.add_argument_group("required named arguments")
    requiredNamed.add_argument(
        "--fastq1", required=True, help="first input fastq file", type=str
    )
    requiredNamed.add_argument(
        "--fastq2", required=True, help="second input fastq file", type=str
    )
    args = parser.parse_args()

    in1, in2 = args.fastq1, args.fastq2

    print("Inputs:", in1, in2)
    if not os.path.exists(in1) or not os.path.exists(in2):
        print("file(s) do not exist")
        return
    if in1.split(".")[-1] != "fastq" or in2.split(".")[-1] != "fastq":
        print("invalid file extensions")
        return

    up_to_date = prerun.check_versions()
    if not up_to_date:
        return
    prerun.check_and_install_databases()
    pipeline.run(args)


if __name__ == "__main__":
    main()
