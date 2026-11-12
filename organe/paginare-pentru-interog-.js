// ORGAN AUTO-DEPLOYAT de Hydra — Paginare pentru interogări GenPSIE (anti-trunchiere)
// Generat autonom la 2026-11-12T22:41:10.335Z
// Scop: Evitarea raportării false de "curățare completă" când de fapt doar prima pagină de rezultate a fost procesată.
// Plan: La orice curățare viitoare de duplicate pe entități mari (GenPSIE, MemorieHidra etc.): interoghează cu skip crescător în pași de 50, procesează fiecare pagină explicit, continuă până rezultatul e sub limita paginii (semn că s-a ajuns la final). Nu declara "curățare completă" fără a confirma că ultima pagină a fost goală/parțială.

// (script negenerat — vezi plan_actiune)

// _Hydra·J712·A1.0_