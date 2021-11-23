import subprocess
import os
from . import utils
from . import install_databases
import traceback


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def print_check_message(boolean):
    print(
        bcolors.OKGREEN + "passed" + bcolors.ENDC
        if boolean
        else bcolors.FAIL + "failed" + bcolors.ENDC
    )


version_dict = {
    "repair.sh": "38.90",
    "fastqc": "0.11.8",
    "bowtie2": "2.4.4",
    "samtools": "1.9",
    "bedtools": "2.27.1",
    "trimmomatic": "0.39",
    "metaphlan": "3.0.13",
}


def check_tool(tool):
    gt = version_dict[tool]
    print(tool, "version:", gt)
    flag = "--version" if not tool == "trimmomatic" else "-version"

    try:
        proc = subprocess.Popen(
            [tool, flag], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        if not tool == "repair.sh":
            output = proc.stdout.read().decode("ASCII")
        else:
            output = proc.stderr.read().decode("ASCII")
        correct = gt in output
    except:
        correct = False
    print_check_message(correct)
    if not correct:
        if tool == "repair.sh":
            tool = "bbmap"
        print(bcolors.WARNING + tool, "not found on path or wrong version")
        print(
            'please run: "conda install -c bioconda',
            tool + "=" + gt + '"',
            bcolors.ENDC,
        )
    print()
    return correct


def check_versions():
    print(
        "-" * 5,
        "Version checks",
        "-" * 5,
    )
    any_failed = False
    for tool in version_dict:
        if not check_tool(tool):
            any_failed = True
    if any_failed:
        print(
            bcolors.FAIL,
            "Please (re)install dependencies with above instructions and rerun",
            bcolors.ENDC,
        )
    else:
        print(
            bcolors.OKGREEN,
            "All dependencies up to date",
            bcolors.ENDC,
        )
    print("-" * 5, "Version checks done", "-" * 5, "\n")
    return not any_failed


import hashlib

hashes = {
    "GRCh38_noalt_as.1.bt2": "a4841a0b52b76812ab5a00b7d390111d",
    "GRCh38_noalt_as.2.bt2": "56c4081853880066a4de5d74e559434c",
    "GRCh38_noalt_as.3.bt2": "b2d325b6836d0e957c349d3557b5a743",
    "GRCh38_noalt_as.4.bt2": "aee1363daba2b49637417b9213281591",
    "GRCh38_noalt_as.rev.1.bt2": "190f2ba81e148b298fb00129f6653a8a",
    "GRCh38_noalt_as.rev.2.bt2": "57080fad22f8ff849639433b20f45ec3",
}


def check_GRCh38_noalt_as():
    database = "GRCh38_noalt_as"
    print(database)
    correct = True
    try:
        for file in hashes:
            h = hashlib.md5(
                open(os.path.join(utils.DEFAULT_DB_FOLDER, database, file), "rb").read()
            ).hexdigest()
            gt = hashes[file]
            if h != gt:
                correct = False
    except Exception:
        # print(traceback.format_exc())
        correct = False
    print_check_message(correct)
    if not correct:
        print(
            bcolors.WARNING + database, "database not found or corrupted", bcolors.ENDC
        )
    return correct


def check_clade_markers():
    print("clade markers")
    subprocess.call(
        [
            "metaphlan",
            "--install",
            "--index",
            "mpa_v30_CHOCOPhlAn_201901",
            "--bowtie2db",
            os.path.join(utils.DEFAULT_DB_FOLDER, "clade_markers"),
        ]
    )
    print_check_message(True)


def check_and_install_databases():
    print("-" * 5, "Database checks and/or installation", "-" * 5)
    g_good = check_GRCh38_noalt_as()
    # if not g_good:
    #     install_databases.install_GRCh38_noalt_as()
    #     check_GRCh38_noalt_as()
    # check_clade_markers()
    print("-" * 5, "Database checks done", "-" * 5, "\n")
