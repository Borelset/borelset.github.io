# Publication refresh — 2026-11-18

The homepage bibliography contains **65 records**, including **18 additions** to the 47 records in `docs/legacy-about.html`.

## Coverage and identity

The requested [Google Scholar profile](https://scholar.google.com/citations?user=nF6Que0AAAAJ&hl=zh-CN) returned HTTP 429; the official `.com.hk` endpoint was also unavailable. This refresh therefore **does not claim an exhaustive comparison with the Scholar profile**.

Candidates were discovered through [DBLP](https://dblp.org/pid/240/2218.html), then checked against official proceedings, publisher-deposited Crossref metadata, or Harbin Institute of Technology Shenzhen news. The DBLP page contains an ORCID conflict and unrelated namesakes, so it was not imported wholesale. Identity checks used HIT Shenzhen affiliation, known collaborators and ORCID **0000-0001-5104-8301**. The [Crossref ORCID query](https://api.crossref.org/works?filter=orcid:0000-0001-5104-8301&rows=100) returned 26 records; records without ORCID metadata were checked individually.

## Added works

| Bibliographic year | Work | Venue / evidence |
| --- | --- | --- |
| 2027 | Improving Compression Ratio of Lossy Compression for HPC via Modeling-Based Arithmetic Coding | [APPT 2026, Springer](https://link.springer.com/chapter/10.1007/978-981-92-4805-6_35); already online August 24, 2026, but recommended citation year is 2027 |
| 2026 | Deduplication can Make File Systems Faster | [TOS](https://doi.org/10.1145/3806054) |
| 2026 | Improving the Restore Performance of Fine-Grained Deduplication on Docker Container Image Storage | [TPDS](https://doi.org/10.1109/TPDS.2026.3678624) |
| 2026 | ZipFloat | [DAC](https://doi.org/10.1145/3770743.3804017) |
| 2026 | Improving Compression Ratio of Lossy Compression on HPC Datasets via Modeling-Based Arithmetic Coding | [DCC](https://doi.org/10.1109/DCC66757.2026.00107), one-page abstract, distinct from the APPT long paper |
| 2026 | CuCM | [DCC](https://doi.org/10.1109/DCC66757.2026.00108), one-page record |
| 2026 | Once Rolling Hashing is Enough | [EuroSys](https://doi.org/10.1145/3767295.3803596) |
| 2026 | A High-Performance Persistent Transactional Memory System via Cooperative Concurrency Control | [HPDC](https://doi.org/10.1145/3806645.3807586) |
| 2026 | The Enduring Potential of Locality | [IWQoS](https://doi.org/10.1109/IWQoS70441.2026.11661042) |
| 2026 | SuperDelta: Improving the Compression Ratio in the Fine-grained Deduplication Storage Systems | [TOS](https://doi.org/10.1145/3859484), online November 6; no volume/issue yet |
| 2026 | NF2FS | [TCAD](https://doi.org/10.1109/TCAD.2026.3744529), early access; placeholder `1–1` page range omitted |
| 2026 | Towards Condensed and Efficient Read-Only File System via Sort-Enhanced Compression | [FAST](https://www.usenix.org/conference/fast26/presentation/huang) |
| 2026 | RESA | [ICLR official proceedings](https://proceedings.iclr.cc/paper_files/paper/2026/hash/89bd6217280d1417370c89ee493ba3c7-Abstract-Conference.html) |
| 2026 | ProphetKV | [ICML / PMLR](https://proceedings.mlr.press/v306/wang26y.html); final author order, no separate arXiv duplicate |
| 2026 | BoundSim | [NAS award announcement](https://www.hitsz.edu.cn/news/2026/1103/c6a18832/page.htm); full authors checked on the attached IEEE award certificate; no DOI/PDF fabricated |
| 2025 | The Logic of Fingerprint Upgrade in Deduplicated Storage | [ICCD](https://doi.org/10.1109/ICCD65941.2025.00073) |
| 2025 | The Design of an Efficient Lossy Compressor for Time Series Databases | [TACO](https://doi.org/10.1145/3767158) |
| 2025 | Towards Efficient Extendible Perfect Hashing for Hybrid PM-DRAM Memory | [TACO](https://doi.org/10.1145/3770859) |

## Corrections and exclusions

- Updated Argus from the old 2025 in-press entry to its final TOS 22(1), 2026 publication; it remains one record. Updated the 2025 first-author TPDS paper from in press to its final volume and pages.
- Added missing 2025 publisher links and used final publisher author lists and citations. Corrected the GogetaFS author list against USENIX.
- Fixed the QD-Compressor journal link, which previously pointed to NetSync, using the [IEEE record](https://ieeexplore.ieee.org/abstract/document/10018182).
- Used the final 2024 journal year for FedComp and the publisher's recommended [2025 citation year for MiDedup](https://link.springer.com/chapter/10.1007/978-981-96-2830-8_20), whose conference name remains NPC 2024.
- Excluded RCMoE because its official author list does not include Xiangyu Zou. Excluded the Shenzhen University CEA author and two power-system namesakes. Omitted SWE-Game because identity could not be established.
- Did not add *Wisdom From File Systems*: its publisher metadata lists online publication on April 10, 2027, after this audit date. Its metadata creation date is not proof of publication or acceptance.

Older bibliography text was otherwise retained; this was not a full line-by-line bibliographic audit of every older paper. Per-record sources and the structured change log are stored in `_data/publication_audit.json`.

## Maintenance

Edit `_data/publications.json` for normal updates and use topic IDs from `_data/publication_topics.yml`. `source_url` and `evidence_note` are optional provenance fields. `year` is numeric, `links` contains `{ "label", "url" }` objects, and `bibtex` is an optional complete citation string. Keep a stable `id` when updating an existing work, even when its final publication year changes.

`scripts/import-publications.py` only recreates the **legacy 47-paper export**, defaulting to `docs/legacy-about.html`. It requires an explicit `--output` and must not be used to replace the current researched bibliography. For comparison:

```sh
python3 scripts/import-publications.py --output /tmp/legacy-publications.json
```
