#!/bin/bash
if [ $# -lt 1 ]; then 
   echo "USAGE $0 <filewithpath> (e.g. Oputput/SWMM5_EA-0.8.3.0.exe"
   exit 5
fi
python googlecode_upload.py  --labels="Featured,OpSys-Windows,Type-Installer" \
 --user="assela@pathirana.net" --project="swmm5-ea" --summary="windows installation (as a standalone program)" \
"$1" --password="`cat  ~/.googlecode.password`"
