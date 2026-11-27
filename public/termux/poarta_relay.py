#!/usr/bin/env python3
"""Releul porții TOR — ține oglinda .onion și spune ce intră prin ea.

Tor trimite cererile serviciului ascuns aici (127.0.0.1:8080). Releul le duce
mai departe la API-ul organismului, cu TLS, și înregistrează fiecare cerere:
metoda, calea, agentul și începutul corpului. La fiecare 20 de secunde trimite
lotul la organ (acțiunea „intalnire”), care citește fiecare cerere determinist
și o împarte în atac, curiozitate sau neutru.

Ce NU face: nu inventează o adresă de origine. Pe Tor clientul nu se vede prin
construcție, deci releul nu raportează niciun IP — spune doar „tor”.

Rulează pe nod (Termux, Linux, runner GitHub), alături de tor:
  HYDRA_TOKEN=<tokenul de nod> python3 poarta_relay.py
"""

import json
import os
import threading
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ORIGINE = os.environ.get("HYDRA_ORIGINE", "https://hidra-smart-core.base44.app").rstrip("/")
API = os.environ.get("HYDRA_API", ORIGINE + "/functions/hydraPoartaTor")
TOKEN = os.environ.get("HYDRA_TOKEN", "")
PORT = int(os.environ.get("HYDRA_PORT", "8080"))

coada = []
blocare = threading.Lock()


def trimite_la_organ(lot):
    corp = json.dumps({"actiune": "intalnire", "token_nod": TOKEN, "intalniri": lot}).encode()
    cerere = urllib.request.Request(
        API, data=corp, headers={"Content-Type": "application/json"}, method="POST"
    )
    with urllib.request.urlopen(cerere, timeout=25) as raspuns:
        return json.loads(raspuns.read().decode() or "{}")


def reporter():
    """Trimite întâlnirile la organ; ce nu pleacă rămâne în coadă, nu se pierde."""
    while True:
        time.sleep(20)
        if not TOKEN:
            continue
        with blocare:
            lot = coada[:40]
        if not lot:
            continue
        try:
            trimite_la_organ(lot)
            with blocare:
                del coada[: len(lot)]
        except Exception as eroare:  # rețeaua poate lipsi o vreme
            print(f"[releu] lotul nu a plecat: {eroare}", flush=True)


class Releu(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _du(self):
        lungime = int(self.headers.get("Content-Length") or 0)
        corp = self.rfile.read(lungime) if lungime else b""
        with blocare:
            if len(coada) < 400:
                coada.append(
                    {
                        "la": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        "metoda": self.command,
                        "cale": self.path[:300],
                        "agent": (self.headers.get("User-Agent") or "")[:200],
                        "corp": corp[:400].decode("utf-8", "replace"),
                    }
                )
        tinta = ORIGINE + self.path
        cerere = urllib.request.Request(tinta, data=corp if corp else None, method=self.command)
        tip = self.headers.get("Content-Type")
        if tip:
            cerere.add_header("Content-Type", tip)
        try:
            with urllib.request.urlopen(cerere, timeout=30) as raspuns:
                date = raspuns.read()
                status = raspuns.status
                tip_raspuns = raspuns.headers.get("Content-Type", "application/json")
        except urllib.error.HTTPError as eroare:
            date = eroare.read()
            status = eroare.code
            tip_raspuns = eroare.headers.get("Content-Type", "application/json")
        except Exception as eroare:
            date = json.dumps({"error": f"organul nu a răspuns: {eroare}"}).encode()
            status = 502
            tip_raspuns = "application/json"
        self.send_response(status)
        self.send_header("Content-Type", tip_raspuns)
        self.send_header("Content-Length", str(len(date)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(date)

    do_GET = do_POST = do_PUT = do_OPTIONS = _du

    def log_message(self, *args):
        return


if __name__ == "__main__":
    threading.Thread(target=reporter, daemon=True).start()
    print(f"[releu] ascult pe 127.0.0.1:{PORT} și oglindesc {ORIGINE}", flush=True)
    if not TOKEN:
        print("[releu] fără token: cererile se oglindesc, dar nu se raportează la organ", flush=True)
    ThreadingHTTPServer(("127.0.0.1", PORT), Releu).serve_forever()
