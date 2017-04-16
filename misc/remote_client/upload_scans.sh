#!/usr/bin/env bash
echo "DEPRECATION WARNING: This file not updated for 2APR refactor"
# TODO Fix arg with an actual argument
scp arg dsb@cobalt.centurion.ai:/nvme/deployment/patient_scans.zip
upzip /nvme/deployment/patient_scans.zip /nvme/deployment/patient_scans
rm /nvme/deployment/patient_scans.zip