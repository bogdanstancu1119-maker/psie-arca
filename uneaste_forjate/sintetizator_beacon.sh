#!/bin/bash
# Script de sinteză pentru hydraSincronizareSymbiote
# Reduce obezitatea informațională prin arhivarea datelor cu prioritate critică
echo "Inițiere Mod Sinteză..." > /dev/null
find ./data/hydraSincronizareSymbiote/ -name "*.json" -mtime +0 -exec gzip {} \;
mv *.gz ./archive/beacon_critc_synthesis/ && echo "Sincronizare finalizată"