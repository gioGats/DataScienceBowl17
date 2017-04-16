#!/usr/bin/env bash

# Shell script that, when run on a Linux server, downloads additional datasets and uncompresses them in the correct
# arrangement to the appropriate locations as specified in deployment_file_structure.

# Will manually download and aggregate data onto fireball.cs.uni.edu;
# Sprint3 This script will provide mirroring between servers


echo "Not implemented pending large file hosting"

# Additional Data Sources

# Lung TIME annotated scans
# Main page at:
# http://cmp.felk.cvut.cz/LungTIME/index.html
# Ftp data at:
# http://ptak.felk.cvut.cz/Medical/Motol/LungTIME/TIME1.tar.gz          12G
# http://ptak.felk.cvut.cz/Medical/Motol/LungTIME/TIME2.tar.gz          199M
# http://ptak.felk.cvut.cz/Medical/Motol/LungTIME/annotations.tar.gz    62K

# Others
# LIDC-IDRI (Dicom versions of LUNA 16 data) ~ 150 GB (javaws download)
# https://wiki.cancerimagingarchive.net/display/Public/LIDC-IDRI

# NLST ~ 11.3 TB (javaws download)
# *** Must apply for access; not allowed for competition
# https://wiki.cancerimagingarchive.net/display/NLST/National+Lung+Screening+Trial
#
# SPIE-AAPM ~ 12.1 GB (javaws download)
# https://wiki.cancerimagingarchive.net/display/Public/SPIE-AAPM+Lung+CT+Challenge
#
# RIDER Lung CT ~ 7.55 GB (javaws download)
# https://wiki.cancerimagingarchive.net/display/Public/RIDER+Lung+CT#62ae708967f441a0ac07312d61047aeb

