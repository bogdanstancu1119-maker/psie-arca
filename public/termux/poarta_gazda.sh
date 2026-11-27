#!/usr/bin/env bash
# GAZDA PERMANENTĂ a porții TOR — separarea celor trei roluri (OM 27.11.2026):
#   · gazda (VPS sau dispozitiv propriu, pornit mereu) ține tor + releul + cheia;
#   · identitatea onion stă pe discul acestei gazde, cu permisiuni 700 și copie
#     de siguranță criptată — niciodată în cache, niciodată în git;
#   · GitHub Actions doar livrează versiunile (vezi poarta-tor.yml), nu găzduiește.
#
# Comenzi:
#   HYDRA_TOKEN=<tokenul nodului> [HYDRA_NONCE=<provocarea>] bash poarta_gazda.sh instalare
#   HYDRA_HS_PAROLA=<parola> bash poarta_gazda.sh backup
#   bash poarta_gazda.sh stare
#
# Ce NU face, prin construcție: nu regenerează identitatea onion, nu își rescrie
# tokenul ca „reparație” și nu se declară activă fără probe reușite.
set -u

DIR="${HYDRA_DIR:-$HOME/.hydra-tor}"
API="${HYDRA_API:-https://hidra-smart-core.base44.app/functions/hydraPoartaTor}"
AICI="$(cd "$(dirname "$0")" 2>/dev/null && pwd)"
UNIT="/etc/systemd/system/poarta-tor.service"
CMD="${1:-stare}"

spune() { echo "[gazdă] $*"; }

instalare() {
  if ! command -v tor >/dev/null 2>&1; then
    sudo apt-get update -qq >/dev/null 2>&1 && sudo apt-get install -y -qq tor socat curl python3 openssl >/dev/null 2>&1 \
      || pkg install -y tor socat curl python3 openssl >/dev/null 2>&1 \
      || { spune "instalează tor, socat, curl, python3, openssl"; return 1; }
  fi
  mkdir -p "$DIR/hs" "$DIR/backup"
  chmod 700 "$DIR" "$DIR/hs" "$DIR/backup"
  [ -n "${HYDRA_TOKEN:-}" ] && { printf '%s' "$HYDRA_TOKEN" > "$DIR/token"; chmod 600 "$DIR/token"; }
  [ -n "${HYDRA_NONCE:-}" ] && { printf '%s' "$HYDRA_NONCE" > "$DIR/nonce"; chmod 600 "$DIR/nonce"; }
  [ -s "$DIR/token" ] || { spune "lipsește tokenul: HYDRA_TOKEN=... bash poarta_gazda.sh instalare"; return 1; }
  if [ -f "$DIR/hs/hs_ed25519_secret_key" ]; then
    spune "identitate onion găsită pe disc — se păstrează, adresa rămâne aceeași"
  else
    spune "prima pornire: cheia onion se generează acum și rămâne pe acest disc"
  fi

  if command -v systemctl >/dev/null 2>&1; then
    sudo tee "$UNIT" >/dev/null <<EOF
[Unit]
Description=Poarta TOR a Hydra-PSIE (tor + releu + bataie + rotire token)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=$USER
Environment=HYDRA_DIR=$DIR
Environment=HYDRA_ORE_MAX=0
ExecStart=/bin/bash $AICI/poarta_tor.sh
Restart=always
RestartSec=20
ProtectSystem=full
ReadWritePaths=$DIR

[Install]
WantedBy=multi-user.target
EOF
    sudo systemctl daemon-reload
    sudo systemctl enable --now poarta-tor
    spune "serviciu systemd pornit: repornește singur tor, releul, bătaia la 6h și rotirea tokenului"
  else
    spune "fără systemd: termux-wake-lock && nohup bash $AICI/poarta_tor.sh >> $DIR/poarta.log 2>&1 &"
  fi
  spune "verifică apoi: bash poarta_gazda.sh stare"
}

backup() {
  [ -n "${HYDRA_HS_PAROLA:-}" ] || { spune "dă o parolă: HYDRA_HS_PAROLA=... bash poarta_gazda.sh backup"; return 1; }
  [ -d "$DIR/hs" ] || { spune "nu există $DIR/hs — nu e nimic de salvat"; return 1; }
  mkdir -p "$DIR/backup"
  local f="$DIR/backup/hs-$(date -u +%Y%m%dT%H%M%SZ).tar.gz.enc"
  tar -czf - -C "$DIR" hs | openssl enc -aes-256-cbc -pbkdf2 -salt -pass env:HYDRA_HS_PAROLA -out "$f" || return 1
  chmod 600 "$f"
  spune "copie criptată: $f"
  spune "ține-o în afara gazdei: fără ea, o gazdă nouă are altă adresă .onion"
}

stare() {
  local tor="jos" releu="jos" onion="lipsă" cod="000" bataie="-"
  pgrep -x tor >/dev/null 2>&1 && tor="viu"
  pgrep -f poarta_relay.py >/dev/null 2>&1 && releu="viu"
  [ -s "$DIR/hs/hostname" ] && onion="$(cat "$DIR/hs/hostname")"
  cod=$(curl -s -m 5 -o /dev/null -w '%{http_code}' "http://127.0.0.1:8080/functions/hydraPoartaTor?actiune=poarta" 2>/dev/null || echo 000)
  bataie=$(curl -s -m 20 "$API?actiune=permanent" | sed -n 's/.*"ultima_bataie_nod":"\([^"]*\)".*/\1/p')
  echo "tor: $tor · releu: $releu · onion: $onion · proba locală: $cod · ultima bătaie la organ: ${bataie:--}"
  if [ "$tor" = viu ] && [ "$releu" = viu ] && [ "$onion" != lipsă ] && [ "$cod" = "200" ]; then
    echo "verdict: activ — toate probele au trecut (proces, releu, adresă, endpoint local)"
  else
    echo "verdict: NU e activ — lipsește ce scrie mai sus; identitatea onion nu se schimbă și tokenul nu se rescrie"
  fi
}

case "$CMD" in
  instalare|backup|stare) "$CMD" ;;
  *) spune "comenzi: instalare | backup | stare"; exit 2 ;;
esac
