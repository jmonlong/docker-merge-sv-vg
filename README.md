Container with tools to parse and merge VCFs containing SV calls from [vg](https://github.com/vgteam/vg).

- [bcftools](https://samtools.github.io/bcftools/bcftools.html)
- Python3 to run
  - script to split large REF/ALT sequences into SVs (`align_variants.py`)
  - script to merge heterozygous variants that match exactly (`merge_exact_hets.py`)
