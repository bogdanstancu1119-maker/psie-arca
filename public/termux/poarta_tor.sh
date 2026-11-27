#!/usr/bin/env bash
# POARTA TOR a Hydra-PSIE — nodul care ține oglinda .onion.
# Gratuit, fără VPS: merge pe Termux (telefon), pe orice Linux, sau pe un
# runner GitHub Actions (workflow-ul poarta-tor.yml, la 6h, fără bani).
#
# Ce face: pornește tor + socat, citește adresa .onion, o atestă la organ,
# apoi dă bătaie la 6h și reatestă zilnic. Dacă tor sau socat mor, le repornește.
# Cheia serviciului ascuns rămâne în $HYDRA_DIR/hs — cu ea, adresa rămâne aceeași.
#
# Necesită tokenul de nod și provocarea, citite din panoul /tor al organismului.
set -u

DIR="${HYDRA_DIR:-$HOME/.hydra-tor}"
API="${HYDRA_API:-https://hidra-smart-core.base44.app/functions/hydraPoartaTor}"
GAZDA="${HYDRA_GAZDA:-hidra-smart-core.base44.app}"
ORE_MAX="${HYDRA_ORE_MAX:-0}"   # 0 = cât ține dispozitivul; peste 0 = se oprește singur (CI)
ORIGINE="${API%%/functions/*}"
RELEU="$(cd "$(dirname "$0")" 2>/dev/null && pwd)/poarta_relay.py"

mkdir -p "$DIR/hs"
[ -n "${HYDRA_TOKEN:-}" ] && printf '%s' "$HYDRA_TOKEN" > "$DIR/token"
[ -n "${HYDRA_NONCE:-}" ] && printf '%s' "$HYDRA_NONCE" > "$DIR/nonce"
[ -s "$DIR/token" ] || { echo "lipsește tokenul de nod (HYDRA_TOKEN sau $DIR/token)"; exit 1; }

if ! command -v tor >/dev/null 2>&1; then
  pkg install -y tor socat curl python >/dev/null 2>&1 \
    || sudo apt-get install -y tor socat curl python3 >/dev/null 2>&1 \
    || sudo apk add tor socat curl python3 >/dev/null 2>&1 || true
fi
command -v tor >/dev/null 2>&1 || { echo "tor lipsește: instalează tor și socat"; exit 1; }
command -v socat >/dev/null 2>&1 || { echo "socat lipsește: instalează-l"; exit 1; }

cat > "$DIR/torrc" <<EOF
SocksPort 9050
HiddenServiceDir $DIR/hs
HiddenServiceVersion 3
HiddenServicePort 80 127.0.0.1:8080
EOF

start_all() {
  # Releul (python3) ține oglinda și spune organului ce intră prin ea: fără el,
  # traficul merge, dar întâlnirile nu se pot citi — și atunci poarta nu ar putea
  # spune dacă a atras un atac sau o curiozitate. Fără python3, socat duce
  # traficul mai departe, iar poarta recunoaște că nu numără.
  if command -v python3 >/dev/null 2>&1 && [ -f "$RELEU" ]; then
    pgrep -f "poarta_relay.py" >/dev/null 2>&1 \
      || HYDRA_TOKEN="${HYDRA_TOKEN:-$(cat "$DIR/token" 2>/dev/null)}" HYDRA_ORIGINE="$ORIGINE" HYDRA_API="$API" \
         nohup python3 "$RELEU" >>"$DIR/releu.log" 2>&1 &
  else
    pgrep -f "OPENSSL:$GAZDA:443" >/dev/null 2>&1 \
      || nohup socat TCP-LISTEN:8080,fork,reuseaddr OPENSSL:$GAZDA:443,verify=1 >>"$DIR/socat.log" 2>&1 &
  fi
  pgrep -f "tor -f $DIR/torrc" >/dev/null 2>&1 \
    || nohup tor -f "$DIR/torrc" >>"$DIR/tor.log" 2>&1 &
}

onion() { cat "$DIR/hs/hostname" 2>/dev/null || true; }

post() {
  curl -s -m 25 -X POST "$API" -H 'Content-Type: application/json' -d "$1"
}

atest() {
  local o; o="$(onion)"; [ -z "$o" ] && return 0
  echo "[poartă] atest adresa $o"
  post "{\"actiune\":\"revendica\",\"resupra\":true,\"adresa_onion\":\"$o\",\"nonce\":\"$(cat "$DIR/nonce" 2>/dev/null)\",\"token_nod\":\"$(cat "$DIR/token" 2>/dev/null)\"}" | head -c 400
  echo
}

# ROTIREA TOKENULUI: organul spune câte zile mai are tokenul; când coboară sub
# 30, nodul cere el unul nou — nu așteaptă să expire și nu îl rescrie singur.
roteste() {
  R=$(post "{\"actiune\":\"rotire\",\"token_nod\":\"$(cat "$DIR/token" 2>/dev/null)\"}")
  NOU=$(printf '%s' "$R" | sed -n 's/.*"token_nod":"\([^"]*\)".*/\1/p')
  if [ -n "$NOU" ]; then
    printf '%s' "$NOU" > "$DIR/token"; chmod 600 "$DIR/token"
    echo "[poartă] token rotit; expiră la $(printf '%s' "$R" | sed -n 's/.*"expira_la":"\([^"]*\)".*/\1/p')"
  else
    echo "[poartă] rotirea nu a reușit: $(printf '%s' "$R" | head -c 200)"
  fi
}

bate() {
  local o; o="$(onion)"; [ -z "$o" ] && return 0
  R=$(post "{\"actiune\":\"bate\",\"adresa_onion\":\"$o\",\"token_nod\":\"$(cat "$DIR/token" 2>/dev/null)\"}")
  echo "[poartă] bătaie trimisă"
  Z=$(printf '%s' "$R" | sed -n 's/.*"zile_ramase_token":\([0-9]*\).*/\1/p')
  if [ -n "$Z" ] && [ "$Z" -le 30 ]; then roteste; fi
}

start_all
sleep 30
echo "adresa .onion: $(onion)"
atest

T=0
while :; do
  start_all
  sleep 60
  T=$((T + 60))
  if [ $((T % 21600)) -lt 60 ]; then bate; fi
  if [ $((T % 86400)) -lt 60 ]; then atest; fi
  if [ "$ORE_MAX" != "0" ] && [ "$T" -ge $((ORE_MAX * 3600)) ]; then
    echo "[poartă] tura s-a încheiat după ${ORE_MAX}h; următoarea pornire o reia pe aceeași cheie"
    exit 0
  fi
done
