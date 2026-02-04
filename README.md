## LightTR: A Lightweight, High-Performance Tandem Repeat Clusterer

## <span id="Introduction">Introduction</span>
LightTR is a lightweight, high-performance tandem repeat clusterer. It is refactored from pyTanFinder with a shell-first architecture designed for minimal memory footprint and maximum stability.

## <span id="Dependencies">Dependencies</span>

**Software:**
- [Python >=3.7](https://www.python.org/)
  - `networkx` library
- [TRF (Tandem Repeats Finder)](https://github.com/Benson-Genomics-Lab/TRF)
- [BLAST](https://blast.ncbi.nlm.nih.gov/Blast.cgi)
- [seqkit](https://bioinf.shenwei.me/seqkit)
- [BEDTools](https://bedtools.readthedocs.io/en/latest/)
- [GNU Parallel](https://www.gnu.org/software/parallel)

## <span id="Installation">Installation</span>

LightTR has been tested and validated on Linux servers.
```bash
# Download LightTR from GitHub
$ git clone https://github.com/zskey-zn/LightTR.git
$ cd LightTR
$ chmod +x ./LightTR
# Use conda to install dependencies or point to already installed software.
```

## <span id="quick_start">Quick Start</span>

```bash
Usage: ./LightTR [OPTIONS]
Tandem Repeat Clustering Tool

Required Parameters:
  -f <FILE>, --fasta <FILE>    Input FASTA file

Optional Parameters:
  -h, --help                       Show this help message
  -m <INT>, --minM <INT>           Minimum tandem repeat length (default: 20)
  -M <INT>, --maxM <INT>           Maximum tandem repeat length (default: 2000)
  -n <INT>, --minMonNum <INT>      Minimum number of repeats (default: 5)
  -w <INT>, --window <INT>         Window size (bp) for merging adjacent regions (default: 400000)
  -t <PARAMS>, --trf_para <PARAMS> TRF parameters (default: "2 7 7 80 10 20 2000 -d -h -l6")
  -p <PREFIX>, --prefix <PREFIX>   Output file prefix (default: output)
  -T <INT>, --threads <INT>        Number of threads to use (default: 1)
  -b, --no_blast                   Skip the BLAST step
  -r, --no_runTRF                  Skip the TRF step
  -s, --split                      Enable split mode for acceleration

Examples:
# Run with default parameters (recommended with multiple threads)
LightTR -f genome.fasta -T 5

# Enable split mode to accelerate analysis of large genomes
LightTR --fasta genome.fasta --window 200000 --threads 10 --split
```

## <span id="comparison">Performance Comparison</span>
The following table summarizes a performance comparison between LightTR and pyTanFinder across various biological datasets, detailing metrics such as wall time, RSS peak memory usage, and disk memory consumption.

<table style="width: 100%; table-layout: fixed; border-collapse: collapse;">
<thead>
    <tr>
      <th style="padding: 8px; text-align: left; border-bottom: 2px solid #ddd;">Metric</th>
      <th style="padding: 8px; text-align: center; border-bottom: 2px solid #ddd;">LightTR</th>
      <th style="padding: 8px; text-align: center; border-bottom: 2px solid #ddd;">pyTanFinder</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px; text-align: left; white-space: nowrap;">Wall Time</td>
      <td style="padding: 8px; text-align: center;">5.7 min</td>
      <td style="padding: 8px; text-align: center;">55.2 min</td>
    </tr>
    <tr>
      <td style="padding: 8px; text-align: left; white-space: nowrap;">RSS Peak</td>
      <td style="padding: 8px; text-align: center;">5.3 GB</td>
      <td style="padding: 8px; text-align: center;">3.3 GB</td>
    </tr>
   <tr>
      <td style="padding: 8px; text-align: left; white-space: nowrap;">Disk Memory</td>
      <td style="padding: 8px; text-align: center;">956 MB</td>
      <td style="padding: 8px; text-align: center;">5.9 GB</td>
    </tr>
  </tbody>
</table>
