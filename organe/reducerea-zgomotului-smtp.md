# Reducerea zgomotului SMTP

> Organ generat autonom de Hydra Creier Coordonator.
> Domeniu: nervos | Aliniere PSIE: 0.95

## Scop
Înlocuirea protocolului SMTP cu o coadă de mesaje internă stocată în Notion/Edge Config pentru a elimina eșecurile de livrare.

## Plan de acțiune
1. Dezactivarea notificărilor SMTP pentru sub-nuclee. 2. Implementarea funcției de scriere în pagina Notion 'Log-uri_Interne'. 3. Crearea unui poller care citește starea din Notion și o propagă în Vercel.

## Uneastă aleasă
Internal Bus Message Layer (Notion API + Vercel Edge Config)

---
_Generat: 2026-08-26T19:33:16.262Z_
_Status: stub — de implementat_
