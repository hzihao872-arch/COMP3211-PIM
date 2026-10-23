# Current candidate manifest - COMP3211 Group 89

**Candidate:** `output/COMP3211_Group_Project-independent-review-2026-10-23-v2.zip`

**Assembly:** `output/COMP3211_Group_Project-independent-review-2026-10-23-v2/`

**ZIP SHA-256:** `a0a03e3eb5ae6672c7d4fe33a6ab6e564eb879e4d5f3c84127694e593cfae41e`

**Payload:** 55 files; 1688227 ZIP bytes.

Current working-tree files, including uncommitted fixes, identify this release. Historical commit 4d3508d is not the complete delivery. Older archives are retained.

## Verification

Payload byte equality and ZIP CRC checked during assembly. Repository runs: 51 tests passed on Python 3.11.9/3.12.3/3.13.5; full-suite model coverage 416/421 (98.81%); model-only 415/421 (98.57%). See `docs/reports/independent-review-2026-10-23.md` and the final clean-extraction log for post-packaging verification. Re-run after any subsequent change.

## Final clean-extraction result

PASS on 2026-10-23 for the exact ZIP SHA-256 above. A new extraction passed all 55 external file hashes, 54 internal payload hashes, ZIP CRC and current source byte equality. Python 3.11.9, 3.12.3 and 3.13.5 each passed all 51 tests and measured 416/421 model source lines (98.81%). Python 3.11 also passed all 51 tests with `-S`. Two independent CLI processes exactly matched the maintained demo transcript; a separate deep-JSON failure recovered with original data and the correct next ID.

Post-packaging log: `docs/reports/independent-clean-extraction-2026-10-23.txt`

Log SHA-256: `77be9b9174d796bb9254e05ccf276728cc6449fe0245b89939826bdc5da46139`

The post-packaging log and main review report are external review evidence; they are not recursively embedded in this already-verified ZIP.

## Pending real deliverables

- `04_Demo/System_Demo.mp4`: actual recording, <=4 minutes.
- `05_Presentation/Presentation_Recording.mp4`: <=5 minutes, each member >=1 minute; real IDs/faces at each speaker's start and face visible throughout.
- `Honour_Declaration_for_Group_Project.pdf`: official form at ZIP root, with genuine details, agreed contributions and truthful AI disclosure.

NFR-01's exact disconnected/no-graphical-session check remains unverified. Human group review remains pending. This is not a submitted or complete assignment.

## Per-file SHA-256

| Archive path | SHA-256 |
|---|---|
| `00_README.txt` | `894c2447b8cd5aae3aa7bc13a1522667dc7f09ad74d11cc8486d7f06e55ba654` |
| `01_SRS/SRS.pdf` | `939e85f84dcf57d68e03b9ef0d982df615b570a426f4d88e1f14e7827f8a48d1` |
| `02_Design/Design_Document.pdf` | `c0d056a22554f8a3cfe1a549a7afd107cc90d1653c460f981cbc1ca36a13dcd0` |
| `03_Implementation/Developer_Manual.pdf` | `5707da6841b82df6db62fb46aef3476e382c8dc1835c00d94d775b63dc7506ee` |
| `03_Implementation/evidence/independent-import-audit-2026-10-23.txt` | `d6fbfd469a103ad56cd8e1eb6117c278162d97288517873a9730d449aae04f28` |
| `03_Implementation/evidence/independent-model-coverage-2026-10-23-python311.txt` | `041271a77656980cbf2946472c5d12a9a232eaa3c3b6be695dbba38a403af1d6` |
| `03_Implementation/evidence/independent-model-coverage-2026-10-23-python312.txt` | `fb2867cfc9d997a0532e5783de3a615f859c5c46950b4ad8e1a179608cec40bb` |
| `03_Implementation/evidence/independent-model-coverage-2026-10-23-python313.txt` | `749ecc76e68aaefcc9eda8697bb405cdb21b69276ccf11b8e66343840c8103fa` |
| `03_Implementation/evidence/independent-model-units-only-2026-10-23.txt` | `9f7bb28a131a74b0ac80efa66a38712e14b650e53924ec28be494f655567f47a` |
| `03_Implementation/evidence/independent-pdf-geometry-2026-10-23.json` | `b7253c1ae603dcb8b65140196ea34ad67f2c0497e5ff7180c08915242450421b` |
| `03_Implementation/evidence/independent-stdlib-only-2026-10-23.txt` | `f29c4fdb6db82596f889c8fe658ef14a8f8ed0d5a61c2c6c3cc79077f2b93c0a` |
| `03_Implementation/evidence/independent-traceability-2026-10-23.json` | `bb82c2a1bea8f4df103b60a85f03e50f9648aa9d40e8c4d89cd5416dc7ef30c4` |
| `03_Implementation/evidence/independent-verification-2026-10-23-python311.txt` | `4c4459fe6580a5d836853fe12f8d38f25db5978e57d9b62224f49d818b33ab82` |
| `03_Implementation/evidence/independent-verification-2026-10-23-python312.txt` | `46984f75c3b0e6746cf243c3e1df5edd8f74861216d64a5fc505c6295917ff04` |
| `03_Implementation/evidence/independent-verification-2026-10-23-python313.txt` | `48cd37251ab5b553078a51abb0b766bbefe15504386eafad11ac571cb65f3306` |
| `03_Implementation/README.md` | `a80589f35fde560886c2276641f38015b7de0677aa0aafc5b5ba7c22001053d7` |
| `03_Implementation/Requirements_Coverage.pdf` | `8a2fbe3b34457e7322e1a47938d2e8c78f102c774829072f5d86fe1a50df5a92` |
| `03_Implementation/src/controller/__init__.py` | `b57a037a6a7f097fbc8d3f502d0c654f64c80d1ad85c847dd6ddcbb7436bb3c5` |
| `03_Implementation/src/controller/cli.py` | `fc1b1ce0537988e850e8c0cdbb22bcacd08578945ea24c255026b7f00643e21b` |
| `03_Implementation/src/main.py` | `c157135d3cee85e1fe45bef9ff37879042083d7ba00a002a752ddbeb68698095` |
| `03_Implementation/src/model/__init__.py` | `81cc7a8d1f068d8bbdfbcab3aac34005649affa8ab5d08bf0467b829c382a341` |
| `03_Implementation/src/model/errors.py` | `4bcecae48f3783efabb108e5b961d31aee23bfd79bcfce95f293d2afd296ff8f` |
| `03_Implementation/src/model/manager.py` | `110c81878915abed4ae53f1b39e72a47d4c743de16a63e54ecfa5fcb41afb5cd` |
| `03_Implementation/src/model/records.py` | `5f1c2f75211330e263b4fe7352bfc693d84102b4944d72af43b425c2e3a991e4` |
| `03_Implementation/src/model/search.py` | `1930a0c07c69b8e02b3d9fb1931b9c44e2bf756e559e03a73cd5b5e1ed97b5c8` |
| `03_Implementation/src/model/validation.py` | `8827cfeaf0e879df4dab616edb5f1f950c2ac67fb74e5d49bf8926cd59a338c3` |
| `03_Implementation/src/storage/__init__.py` | `972c5ae0bc93c80a7a2171ae0b39fed5b979e1ecc7939b178f0f71c0041fdc39` |
| `03_Implementation/src/storage/pim_file.py` | `5c0eebe8c8f8719387d7ee2980541dacd00595a443a7b651bd8ad8ad91953402` |
| `03_Implementation/Test_Coverage.pdf` | `70423511c7db9e677b858d7d58d9792bb29efa59898b0a9169eb86844180e2ce` |
| `03_Implementation/tests/__init__.py` | `4566908709322660744dbe6e820b2afff9e16850e596c53915904dd82a2e25e4` |
| `03_Implementation/tests/controller/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `03_Implementation/tests/controller/test_cli.py` | `5ff3d92dbe3d7e38753342578fb68a6b49f7bd18bfc981df543e1de045375802` |
| `03_Implementation/tests/controller/test_independent_review.py` | `638df80179842cff96d57ae5f15c7beca685d6995a165a0391867ed543a562c1` |
| `03_Implementation/tests/controller/test_requirement_edges.py` | `99dbe6b82fceb1d50508571928232ceab3d4ccdca089edc52d22b11372fccd64` |
| `03_Implementation/tests/model/__init__.py` | `65b20d4f0eeda97a8ee5825e54801364bebdf9a6f59ee6377ee43c4aed18349d` |
| `03_Implementation/tests/model/test_independent_review.py` | `c83e96c188f3e900441b22c6b9cd2b3f2c65c7ee4bd08e86bae8cff79c13d851` |
| `03_Implementation/tests/model/test_manager.py` | `b88f97a95433b157ebcf93cdd9ea1fd5a88fd5813efc3bda212ad54191fa61ef` |
| `03_Implementation/tests/model/test_records.py` | `2854f29ca772dd3900bc7cfc151f75568aa6de9ab0fdd2f002d04c73028bbd97` |
| `03_Implementation/tests/model/test_requirement_edges.py` | `7d4349b63dd60b814d4e9efae519b0965b885b2c16c7b22dbd1c65c2a5ae0569` |
| `03_Implementation/tests/model/test_search.py` | `3b84a8128198610052fb0d341c8caaa31f4c092abda2bc42a5d5e314f8a0dccd` |
| `03_Implementation/tests/model/test_search_integration.py` | `32e56ced206bca9b3003ac2b5f451830aeef9eccc394364ce3b3e53809bb0f95` |
| `03_Implementation/tests/storage/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `03_Implementation/tests/storage/test_independent_review.py` | `2d039a8c14aac02aa55a3b10f096fa0f550d38b6947674736b1d7ac9485709dc` |
| `03_Implementation/tests/storage/test_pim_file.py` | `673ae1b8bf72ec82e8992a06c620cf691af48b30ebe8bfb6e3489fab6a1b8998` |
| `03_Implementation/tests/storage/test_requirement_edges.py` | `f1c2131d9e6c43ddc2e5769b1a27e1714d61fbc34f887cff407eff5b4a79d742` |
| `03_Implementation/tests/test_acceptance.py` | `aa8c2ee0752e0d2436da3066e45e2ecf369e8cff056fadc5021221ff5746a753` |
| `03_Implementation/tests/tools/__init__.py` | `4ce4f013e0fd9b0ea708c1b1b6a9ab63898490db9c29448de7684c0d70b41663` |
| `03_Implementation/tests/tools/test_model_coverage.py` | `f771b8c0158581a4c25b5a53b1d23428624494b12bbed6367135829b6b5deaed` |
| `03_Implementation/tools/model_coverage.py` | `aff6a2efda0311235676307a7eb664afc4b1d1cf8ab819a11231aa94b863c042` |
| `03_Implementation/User_Manual.pdf` | `497b2f603b91db421c08bd3fe04fa2abfc098fa999e726d265c1a4a11f3b306a` |
| `04_Demo/README.txt` | `cceecab085b3ff2f73f54461da6cb1e57e5478e7e47dee92c5501fccf9952db6` |
| `05_Presentation/Presentation.pdf` | `0ab3c26730688ea5f0087cf04cf879e3ac330a726dc7ceb9539df4648e5787f9` |
| `05_Presentation/Presentation.pptx` | `a29790ddf3d2efc45e989ade5a7a2b161a96a753d68bd1c7260bb1036a507961` |
| `AI_Assistance_Record.md` | `f8e4b144fe8016690a5a93e482ddad5acb6208593411025137d9d14cee7e851d` |
| `SHA256SUMS.txt` | `12ee3a02a87fb45929ffabc64aa62c4884df73f6691c1627988d5212b8e8e02a` |
