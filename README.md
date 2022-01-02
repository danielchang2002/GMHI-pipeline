# GMHI: Gut Microbiome Health Index

[![Anaconda-Server Badge](https://anaconda.org/danielchang2002/gmhi2/badges/version.svg)](https://anaconda.org/danielchang2002/gmhi2)
[![Anaconda-Server Badge](https://anaconda.org/danielchang2002/gmhi2/badges/platforms.svg)](https://anaconda.org/danielchang2002/gmhi2)
[![Anaconda-Server Badge](https://anaconda.org/danielchang2002/gmhi2/badges/license.svg)](https://anaconda.org/danielchang2002/gmhi2)
[![Anaconda-Server Badge](https://anaconda.org/danielchang2002/gmhi2/badges/downloads.svg)](https://anaconda.org/danielchang2002/gmhi2)
[![Anaconda-Server Badge](https://anaconda.org/danielchang2002/gmhi2/badges/installer/conda.svg)](https://conda.anaconda.org/danielchang2002)

### Description

Gut Microbiome Health Index (GMHI) is a robust index for evaluating
health status based on the species-level taxonomic profile of a stool
shotgun metagenome (gut microbiome) sample.

### Installation

To avoid dependency conflicts, create an isolated conda environment and
install gmhi

1. Install via conda

```sh
conda create --name gmhi_env -c danielchang2002 python=3.7 gmhi
```

2. Activate environment

```sh
conda activate gmhi_env
```

### Usage

```sh
usage: gmhi [-h] [-o OUTPUT] --fastq1 FASTQ1 --fastq2 FASTQ2

DESCRIPTION:
GMHI version 1.0
Gut Microbiome Health Index (GMHI) is a robust index for evaluating
health status based on the species-level taxonomic profile of a stool
shotgun metagenome (gut microbiome) sample.

AUTHORS:
Daniel Chang, Vinod Gupta, Jaeyun Sung

USAGE:
GMHI is a pipeline that takes as input two raw fastq files generated
from a paired end sequence, performs quality control, estimates microbial
abundances, and returns as output a health index score.

* Profiling a metagenome from raw reads:
$ gmhi --fastq1 metagenome1.fastq --fastq2 metagenome2.fastq

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file name

required named arguments:
  --fastq1 FASTQ1       first input fastq file
  --fastq2 FASTQ2       second input fastq file
```

### Example

Directory structure:

```sh
.
├── metagenome1.fastq
└── metagenome2.fastq
```

Command:

```sh
gmhi --fastq1 metagenome1.fastq --fastq2 metagenome2.fastq -o GMHI2.txt
```

Result:

```sh
.
├── GMHI.txt
├── abundance.txt
├── metagenome1.fastq
└── metagenome2.fastq
```

where GMHI.txt is a text file with a single line containing the health index
score of the metagenome, and abundance.txt is a tsv containing the estimated
microbial abundances.

### Runtime

Runtime depends on the size of the input metagenome and the system specs.

On a 2019 MacBook Pro with a 2.3 GHz 8-Core Intel Core i9 processor and
16GB of RAM, a single run of gmhi on an input metagenome
of 4 GB takes 29 minutes.

Note: the initial run on any machine will take extra time
because databases will need to be downloaded and installed before the actual
computation.
