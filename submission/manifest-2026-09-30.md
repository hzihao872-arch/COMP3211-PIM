# WP08 Pre-Video Release Candidate Manifest

**Group:** 89. **Date:** 2026-09-30. **Status:** G8 candidate awaiting three real human artifacts; this is not a final submission.

**Directory:** output/COMP3211_Group_Project/
**Candidate ZIP:** output/COMP3211_Group_Project-pre-video-RC.zip
**Candidate ZIP SHA-256:** 9e26b1bf6aa07202fbb7fcdcee74e2a6d2b5139c1560155ed5014a066490b706
**Frozen product SHA:** 4d3508db0447a3ac6346a2a2789da89208f88fd5
**G7 merge commit:** 034bc02afe0326461228093c5cdd7952ea0e11c7

The ZIP contains the directory contents directly at archive root. Every ZIP entry matched the same relative path and SHA-256 in the assembled directory. There are no fabricated MP4 or declaration files. 03_Implementation is the submitted source-code root.

## Available artifacts

| Relative path in ZIP | Requirement | Source commit/version | SHA-256 | Verified by |
|---|---|---|---|---|
| 01_SRS/SRS.pdf | SRS-01–04; US1–US11 | 132be1b721c50591c34f5df65f9d9104459c32fc | 6c6a15574f2da141dae0d907e6b09aad1f8edeff04c86922525f07a15789b990 | 7 pages rendered; ZIP byte match |
| 02_Design/Design_Document.pdf | DES-01–04 | 132be1b721c50591c34f5df65f9d9104459c32fc | f7f492b62785c8f778cc34a438d19e7aeb2c1d1e68f31ed7425ff16b445d4577 | 8 pages rendered; ZIP byte match |
| 03_Implementation/Developer_Manual.pdf | IMP-03 | 678c981f4f274bea3b743e9b4b16a5e07e985c93 | bc9b2c321072a0c0ac9cecd8a2de5ef258fb93f8be406f3b966d180858dc592d | 2 pages rendered; extracted commands passed |
| 03_Implementation/README.md | IMP-03–04 | WP08 release README, 2026-09-30 | e9f2d620c2502c4ec145492e19177839a06aed8c07c95e4b1d77af04c5c58e58 | Extracted path and commands checked |
| 03_Implementation/Requirements_Coverage.pdf | IMP-06 | 132be1b721c50591c34f5df65f9d9104459c32fc | 93b781742f7935406f5cec9887462082bdb043d16ac025fbcdcb8e1d57298ee9 | 7 pages rendered; root location checked |
| 03_Implementation/src/controller/__init__.py | IMP-01–02; US1–US11 | 4d3508db0447a3ac6346a2a2789da89208f88fd5 | b57a037a6a7f097fbc8d3f502d0c654f64c80d1ad85c847dd6ddcbb7436bb3c5 | Freeze byte match; CLI workflow passed |
| 03_Implementation/src/controller/cli.py | IMP-01–02; US1–US11 | 4d3508db0447a3ac6346a2a2789da89208f88fd5 | b47f2b29476d22b185139dfceeb704359e91b8f71068327d17fce1183f934ba1 | Freeze byte match; CLI workflow passed |
| 03_Implementation/src/main.py | ADM-01; IMP-01–02 | 4d3508db0447a3ac6346a2a2789da89208f88fd5 | c157135d3cee85e1fe45bef9ff37879042083d7ba00a002a752ddbeb68698095 | Freeze byte match; CLI workflow passed |
| 03_Implementation/src/model/__init__.py | IMP-02; US1–US9 | 4d3508db0447a3ac6346a2a2789da89208f88fd5 | 81cc7a8d1f068d8bbdfbcab3aac34005649affa8ab5d08bf0467b829c382a341 | Freeze byte match; extracted suite 33 OK |
| 03_Implementation/src/model/errors.py | IMP-02; US1–US9 | 4d3508db0447a3ac6346a2a2789da89208f88fd5 | 4bcecae48f3783efabb108e5b961d31aee23bfd79bcfce95f293d2afd296ff8f | Freeze byte match; extracted suite 33 OK |
| 03_Implementation/src/model/manager.py | IMP-02; US1–US9 | 4d3508db0447a3ac6346a2a2789da89208f88fd5 | 110c81878915abed4ae53f1b39e72a47d4c743de16a63e54ecfa5fcb41afb5cd | Freeze byte match; extracted suite 33 OK |
| 03_Implementation/src/model/records.py | IMP-02; US1–US9 | 4d3508db0447a3ac6346a2a2789da89208f88fd5 | 5f1c2f75211330e263b4fe7352bfc693d84102b4944d72af43b425c2e3a991e4 | Freeze byte match; extracted suite 33 OK |
| 03_Implementation/src/model/search.py | IMP-02; US1–US9 | 4d3508db0447a3ac6346a2a2789da89208f88fd5 | 1930a0c07c69b8e02b3d9fb1931b9c44e2bf756e559e03a73cd5b5e1ed97b5c8 | Freeze byte match; extracted suite 33 OK |
| 03_Implementation/src/model/validation.py | IMP-02; US1–US9 | 4d3508db0447a3ac6346a2a2789da89208f88fd5 | 8827cfeaf0e879df4dab616edb5f1f950c2ac67fb74e5d49bf8926cd59a338c3 | Freeze byte match; extracted suite 33 OK |
| 03_Implementation/src/storage/__init__.py | IMP-01–02; US10–US11 | 4d3508db0447a3ac6346a2a2789da89208f88fd5 | 972c5ae0bc93c80a7a2171ae0b39fed5b979e1ecc7939b178f0f71c0041fdc39 | Freeze byte match; save/load workflow passed |
| 03_Implementation/src/storage/pim_file.py | IMP-01–02; US10–US11 | 4d3508db0447a3ac6346a2a2789da89208f88fd5 | abef69f231ca816c70997dd9ce5433ff2125a0275ecf061bc7ed1e3d92145c04 | Freeze byte match; save/load workflow passed |
| 03_Implementation/Test_Coverage.pdf | TST-02 | 132be1b721c50591c34f5df65f9d9104459c32fc | c771f6838a03232df21a2170d0ef3ea50ecc85c0634120ae4eead928e434019c | 2 pages rendered; 411/430 matched raw result |
| 03_Implementation/tests/__init__.py | TST-01; US1–US11 | 4d3508db0447a3ac6346a2a2789da89208f88fd5 | 4566908709322660744dbe6e820b2afff9e16850e596c53915904dd82a2e25e4 | ZIP byte match; extracted suite 33 OK |
| 03_Implementation/tests/controller/__init__.py | TST-01; US1–US11 | 4d3508db0447a3ac6346a2a2789da89208f88fd5 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | ZIP byte match; extracted suite 33 OK |
| 03_Implementation/tests/controller/test_cli.py | TST-01; US1–US11 | 4d3508db0447a3ac6346a2a2789da89208f88fd5 | 5ff3d92dbe3d7e38753342578fb68a6b49f7bd18bfc981df543e1de045375802 | ZIP byte match; extracted suite 33 OK |
| 03_Implementation/tests/model/__init__.py | TST-01; US1–US11 | 4d3508db0447a3ac6346a2a2789da89208f88fd5 | 65b20d4f0eeda97a8ee5825e54801364bebdf9a6f59ee6377ee43c4aed18349d | ZIP byte match; extracted suite 33 OK |
| 03_Implementation/tests/model/test_manager.py | TST-01; US1–US11 | 4d3508db0447a3ac6346a2a2789da89208f88fd5 | b88f97a95433b157ebcf93cdd9ea1fd5a88fd5813efc3bda212ad54191fa61ef | ZIP byte match; extracted suite 33 OK |
| 03_Implementation/tests/model/test_records.py | TST-01; US1–US11 | 4d3508db0447a3ac6346a2a2789da89208f88fd5 | 2854f29ca772dd3900bc7cfc151f75568aa6de9ab0fdd2f002d04c73028bbd97 | ZIP byte match; extracted suite 33 OK |
| 03_Implementation/tests/model/test_search_integration.py | TST-01; US1–US11 | 4d3508db0447a3ac6346a2a2789da89208f88fd5 | 32e56ced206bca9b3003ac2b5f451830aeef9eccc394364ce3b3e53809bb0f95 | ZIP byte match; extracted suite 33 OK |
| 03_Implementation/tests/model/test_search.py | TST-01; US1–US11 | 4d3508db0447a3ac6346a2a2789da89208f88fd5 | 3b84a8128198610052fb0d341c8caaa31f4c092abda2bc42a5d5e314f8a0dccd | ZIP byte match; extracted suite 33 OK |
| 03_Implementation/tests/README.md | TST-01; US1–US11 | 4d3508db0447a3ac6346a2a2789da89208f88fd5 | 4c420235699d61db3592b053cbd4aa6b47fcc25d35b7930c5be072bed3a90616 | ZIP byte match; extracted suite 33 OK |
| 03_Implementation/tests/storage/__init__.py | TST-01; US1–US11 | 4d3508db0447a3ac6346a2a2789da89208f88fd5 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | ZIP byte match; extracted suite 33 OK |
| 03_Implementation/tests/storage/test_pim_file.py | TST-01; US1–US11 | 4d3508db0447a3ac6346a2a2789da89208f88fd5 | 673ae1b8bf72ec82e8992a06c620cf691af48b30ebe8bfb6e3489fab6a1b8998 | ZIP byte match; extracted suite 33 OK |
| 03_Implementation/tests/test_acceptance.py | TST-01; US1–US11 | 4d3508db0447a3ac6346a2a2789da89208f88fd5 | aa8c2ee0752e0d2436da3066e45e2ecf369e8cff056fadc5021221ff5746a753 | ZIP byte match; extracted suite 33 OK |
| 03_Implementation/tools/model_coverage.py | TST-02 | 4d3508db0447a3ac6346a2a2789da89208f88fd5 | bf20277ad8c766a610c3ac99d9df72ab386e54e99994c1a98f84dcef6afb6080 | ZIP byte match; extracted coverage 411/430 |
| 03_Implementation/User_Manual.pdf | IMP-04 | 132be1b721c50591c34f5df65f9d9104459c32fc | edac3089b338b2a8f8ce2a001993b49717cdbfa4c8ec429b3035b97b4531de96 | 4 pages rendered; CLI workflow passed |
| 05_Presentation/Presentation.pdf | PRE-01; PRE-03 | 3969d7edb24a8e8289dc52763a64f55473ab2833 | 1ffcc8bb5ad91cab48cd20f10e518ebd7580ae48af3294c0fe20ef18cbc15b4b | 6 pages rendered; WP06 topics checked |

## Human artifacts absent from this candidate

| Required relative path | Requirement | Current status | Required final verification |
|---|---|---|---|
| 04_Demo/System_Demo.mp4 | IMP-05 | Missing: real recording not supplied | Real MP4; measured duration ≤240 seconds; playback/content check. |
| 05_Presentation/Presentation_Recording.mp4 | PRE-01–03 | Missing: real recording not supplied | Real MP4; measured duration ≤300 seconds; each member ≥60 seconds; ID card and face at start; current speaker visible throughout. |
| Honour_Declaration_for_Group_Project.pdf | DEC-01–02 | Missing: official signed form and member data not supplied | Official form at ZIP root; verified names/IDs, agreed contributions totaling 100%, truthful GenAI disclosure and signatures. |

## G8 candidate verification

- Official PDF requirements and docs/plans/deliverables-matrix.md were compared to the paths above. SRS/Design/manuals/reports/slides have the expected format and seven PDFs total 36 rendered pages.
- The two required coverage reports are directly in 03_Implementation/, the source-code root. No project-wrapper directory appears inside the candidate ZIP.
- A fresh extraction of the candidate ZIP on Windows 11 with Python 3.13.5 ran 33 tests successfully, model line coverage 411/430 (95.58%), compileall exit 0, and the User Manual two-process create/search/update/delete/save/load workflow ending at ID 5.
- The candidate ZIP has 32 entries. Every entry hash equals the corresponding assembled file. The tree contains no __pycache__, .pyc, virtual environment, .git, .env, .pem, .key, working .pim, TODO, TBD, PLACEHOLDER, member-code token, personal absolute path, or apparent credential string in the scanned text files.
- Frozen src/tests/tools remain byte-equivalent to commit 4d3508db0447a3ac6346a2a2789da89208f88fd5; WP07 only changed documents. Python 3.11 remains unverified.
- WP07 finding A-03 is closed: 03_Implementation/README.md is a release-specific guide, not a copy of the repository development README.

**G8 candidate decision:** passed for all Agent-producible artifacts. The final ZIP and upload remain blocked on the three real human artifacts and the checks in submission/human-closeout-checklist.md.
