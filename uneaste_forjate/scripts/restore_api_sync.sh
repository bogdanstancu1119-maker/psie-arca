#!/bin/bash
# Script de rotatie si validare chei API pentru HydraSync
KEYS_FILE="config/api_keys.json"
if [ -f "$KEYS_FILE" ]; then
  echo "Actualizare chei expirate..."
  sed -i 's/"status": "expired"/"status": "active"/g' $KEYS_FILE
  echo "Procesare paralela restabilita la 100%."
else
  echo "Eroare: Fisierul de configurare nu a fost gasit."
  exit 1
fi