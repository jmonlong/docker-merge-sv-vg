FROM ubuntu:18.04
MAINTAINER jmonlong@ucsc.edu

# Prevent dpkg from trying to ask any questions, ever
ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true

## python, snakemake and awscli
RUN apt-get update \
        && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        git screen time less nano wget gcc make bzip2 \
        python3 \
        python3-pip \
        python3-setuptools \
        tabix \
        libncurses5-dev libncursesw5-dev \
        zlib1g-dev libbz2-dev liblzma-dev \
        && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip

RUN pip3 install --no-cache-dir biopython pyfaidx pyvcf

## bcftools
RUN wget --no-check-certificate https://github.com/samtools/bcftools/releases/download/1.10.2/bcftools-1.10.2.tar.bz2 && \
        tar -xjf bcftools-1.10.2.tar.bz2 && \
        cd bcftools-1.10.2 && \
        ./configure && make && make install && \
        cd .. && rm -rf bcftools-1.10.2 bcftools-1.10.2.tar.bz2

WORKDIR /scripts

ADD align_variants.py .
ADD merge_exact_hets.py .

WORKDIR /home
