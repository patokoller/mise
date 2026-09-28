# Recovery of August 2026 files — done 2026-09-28

On 2026-09-28 the Project knowledge was found to be missing files produced in August chat sessions.
They were recompiled from the chat transcripts. This folder holds the scripts and notes that did it,
so the recovery can be audited. The recovered files themselves live where they belong in the repo.

## What was missing, and where it is now

| File | How recovered | Now at |
|---|---|---|
| `cph-route-a1-frame.xlsx` | Session build scripts re-run (`early/rebuild/`). Cross-checked 2026-09-28: the 68 F1-passing place IDs, tiers and names match the union file exactly (0 differences) | `data/` |
| `cph-route-a2-frame.xlsx` | Same. 109 F1-passing place IDs, tiers and names match the union file exactly (0 differences) | `data/` |
| `f2-test-fixture-copenhagen.xlsx` | Same. **Not frame data** — press-sourced test fixture from 2026-07-30 | `archive/` |
| D-056 addendum + `D-057`–`D-060` | Verbatim from the 2026-08-12 transcript | inserted in `12-decision-log.md` after D-056 |
| `BUILD-STATUS.md` 2026-08-12 version | The session's own edit script re-run on the 2026-08-10 base | `BUILD-STATUS.md` |
| Lost 2026-08-01 edit (schema row, D-047 wording) | Verbatim from transcript, see `early/session-e2953710-turn19-lost-edits.md` | `BUILD-STATUS.md`, `12-decision-log.md` |
| `phase1-menu-capture-template.xlsx` | Session build script re-run | `data/phase1/` |
| `next-session-brief.md` (2026-08-12) | Verbatim. Historical — superseded by BUILD-STATUS | `archive/2026-08-12/` |
| Phase 1 fetched pages (8) and proposed venues (40) | Compiled from the transcript's fetch log. **Partial**, not a data file the session wrote | `data/phase1/` |

## What could not be recovered

- The operator's upload `list_and_menus.xlsx` (39 rows with URLs). Its contents were never shown in the transcript.
- Exact per-page fetch times for the 8 pages fetched on 2026-08-12. Only the date is known.
- Dish lines for Enigma and Prodigi's lunch menu, which were never logged.

## Deliberately not in this public repository

The dish lines logged on 2026-08-12 (91 lines from 8 venues). They are machine-extracted, condensed,
flagged unreliable by `D-059`, and are menu content that `10-legal-and-ethics.md` §5 says is held
internally and not republished. The operator holds a copy.

## Limits on fidelity

Documents were copied from Project knowledge by transcription, not by file copy — the Project tool
returns text, not files. There is no byte-level proof the copies are identical. Spreadsheets were
regenerated from code, so file-level metadata (creation dates) differs from the originals; cell
contents were checked, file bytes were not.
