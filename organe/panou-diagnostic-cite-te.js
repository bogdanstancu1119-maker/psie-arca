// ORGAN AUTO-DEPLOYAT de Hydra — Panou diagnostic citește stare stale/cache, nu live — contrazis direct de AuditHidra/GenPSIE
// Generat autonom la 2026-11-19T19:45:26.878Z
// Scop: Repară sursa de date a panoului de monitorizare ca să reflecte starea live, nu un cache stale — evită diagnostice false care ar putea duce la acțiuni drastice greșite (stingere organe funcționale)
// Plan: 1) Identifică funcția/organul care generează panoul "suflu informațional / organe hrănite / reflexe macro probate" (probabil hydraSalaSport sau hydraRoiSuperCreiere pacing sau hydraAutoEvaluare). 2) Verifică dacă citește din ConfigHidra cache vechi în loc de query live pe BeaconOrganic/GenPSIE/AuditHidra. 3) Corelează cu bug-ul deja raportat (Lege.aggregate vs Lege.filter discrepanță, id 6aff0befae5fb1edd5405430) — posibil aceeași cauză structurală (agregare stale). 4) NU reduce organe active bazat pe acest panou până nu e confirmat că citește date proaspete.

// (script negenerat — vezi plan_actiune)

// _Hydra·J712·A1.0_