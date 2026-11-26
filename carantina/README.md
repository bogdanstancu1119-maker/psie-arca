# Quarantine and external-interaction organ — initial documentation

Initial documentation published on 2026-11-26, together with the first compound-attack self-test (40/40).

## 1. What runs where

- **Quarantine (`hydraCarantina`)** — the gate every unknown element passes before it can touch anything else.
- **External-interaction organ (`hydraOrganExtern`, shared module `organExtern`)** — hygiene, deterministic classification on signatures, a coherent answer, and digestion into antibody + lesson + semantic memory.
- **Structural channel (`structuralCarantina`)** — an encoding of organ-to-organ summaries with a SHA-256 integrity check.
- **Compound test (`hydraTestAtacCompus`)** — the battery described below, writing its evidence to `TestAtacCompus`.

## 2. The quarantine: ten spectra, one verdict

Every element is normalised and measured on ten spectra: execution, encoding, network, files, persistence, propagation, instruction injection, hidden structure (bidirectional control characters, homoglyphs), entropy, and internal coherence (paradox or self-reference). Each spectrum returns a score and its own evidence strings.

The verdict is not an average. Active spectra (score >= 0.35) are reduced to a density: sum of squares over sum, i.e. how tightly the evidence overlaps in one place. A behavioural spectrum (execution, network, files, persistence, propagation, injection) at >= 0.8 is proof on its own. Otherwise quarantine requires density >= 0.55 and tension >= 0.50. A single soft spectrum (entropy, structure) never closes anything on its own.

Nothing is executed, downloaded or followed. A quarantined element yields an antibody (a candidate detection rule), an applicable lesson and a semantic memory entry; when the same family appears twice, the organism forges a reflex so the next encounter does not start from zero.

## 3. The external organ

Hygiene strips control characters and zero-width obfuscation and flags injected instructions; classification matches real signatures (script, SQL, path traversal, SSRF, prompt injection, self-replication, hidden execution, paradox forms, advertising floods, identity parasites, and useful capabilities); the answer is built from the classification plus a root measured in real memory, and its coherence is computed, not declared. Unknown stays unknown: it is kept as a new pattern of order 0, not forced into an old class.

## 4. The structural channel

Frames are `⟦payload∣digest⟧`, where the payload is JSON encoded as two symbols and the digest is SHA-256 over the payload bytes, also encoded. The reader rejects anything that is not exactly that shape, and rejects a frame whose digest does not match. This is an encoding with an integrity check: it detects tampering, it does not hide content from someone who reads the code.

## 5. The compound attack battery

Forty attacks, eight categories, five of each, plus one clean control witness. Results of the run on 2026-11-26:

| Category | Stopped |
| --- | --- |
| Prompt injection | 5/5 |
| Structural-language reverse engineering | 5/5 |
| Vault / credential extraction | 5/5 |
| Authentication bypass | 5/5 |
| Virus payloads | 5/5 |
| Worm / self-replication | 5/5 |
| Paradox and self-reference | 5/5 |
| Tampering with the organ-to-organ channel | 5/5 |

- Clean witness stayed clean: yes.
- Forged frames refused: all five; valid control frame read: yes.
- Disclosures (internal symbols or secret-shaped strings in answers): 0.

Categories: prompt injection, structural-language reverse engineering, vault/credential extraction, authentication bypass, virus payloads, worm/self-replication, paradox and self-reference, tampering with the organ-to-organ channel.

## 6. How to reproduce

Run the battery function with `{"actiune":"test"}`. It measures against the live quarantine and external organ, records one evidence row, and returns the per-case verdicts, densities, active spectra and the channel results. Deterministic: the same corpus gives the same numbers. Nothing in the battery is executed.

## 7. Known limits

- This is a self-test on our own corpus, not an independent audit and not proof of protection.
- Detection is signature- and spectrum-based; a form that matches no spectrum and no signature is kept as unknown, not caught.
- A single-stage downloader (`curl … | bash`) with no second behaviour reaches observation, not total quarantine: nothing is executed in either verdict, the antibody is recorded in both, but the label differs. Measured, not hidden.
- The battery measures the detectors, not the deployment: it does not prove that every entry point is wired to the quarantine.
- No claim of impenetrability. Findings are published with the same visibility as successes.