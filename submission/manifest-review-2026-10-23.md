# Group-review release manifest - 2026-10-23

**Status:** candidate for group review; two MP4s and the completed official Honour Declaration are still absent. Do not upload as a complete final submission.
**Directory:** `output/COMP3211_Group_Project/`
**Current ZIP:** `output/COMP3211_Group_Project-review-2026-10-23.zip`
**Application baseline:** `4d3508db0447a3ac6346a2a2789da89208f88fd5`; `src/` and the coverage tool are unchanged. Three added test files extend the suite from 33 to 45 methods. This is a local revision, not a new Git commit.
**Historical candidate:** the original pre-video ZIP is preserved. Its previous manifest is `submission/manifest-2026-09-30.md` and does not identify the current directory contents.

## Verification

The ZIP was extracted into a fresh directory with no Git metadata. All 45 tests passed on Python 3.11.9, 3.12.3 and 3.13.5, including actual CLI subprocess restart acceptance. The extracted Python 3.13.5 coverage run reported 416/430 (96.74%). Raw output: `docs/reports/release-check-2026-10-23.txt`.

All ZIP entry bytes were compared with the assembled directory. Both coverage PDFs are at the source-code root. The revised PDFs and slides were rendered and visually reviewed; text bounding boxes were checked against their page boundaries. The source does not contain new product behavior. NFR-01's exact network-disabled/no-graphical-session environment remains unverified.

**ZIP SHA-256:** `9e5c0a3875eaa803650334278437b90fb9a8dbac9aeff5115e3c6c16192e8e92`
**Files:** 35

| Relative ZIP path | SHA-256 |
|---|---|
| `01_SRS/SRS.pdf` | `c465a3d4627bdb55cd2c92dbab21db662eb13f47a2984129827f735b793b7ea5` |
| `02_Design/Design_Document.pdf` | `30e6d08a1ad43b1b551768a4f20e30e92afd06c1643a63dc8d65238bf2bed787` |
| `03_Implementation/Developer_Manual.pdf` | `6eb74dbb4a70da25c4a2e6b55dc78e40c21eb4d44ee2b1877a701836d09ae229` |
| `03_Implementation/README.md` | `b430b713815b13047f8d3fef534fc4b2a1969bbc04559abd3decce140bf11309` |
| `03_Implementation/Requirements_Coverage.pdf` | `3fd7e360190680364b7e4685ddaeea34063cd2b777706bfb7890a5286d415b91` |
| `03_Implementation/src/controller/__init__.py` | `b57a037a6a7f097fbc8d3f502d0c654f64c80d1ad85c847dd6ddcbb7436bb3c5` |
| `03_Implementation/src/controller/cli.py` | `b47f2b29476d22b185139dfceeb704359e91b8f71068327d17fce1183f934ba1` |
| `03_Implementation/src/main.py` | `c157135d3cee85e1fe45bef9ff37879042083d7ba00a002a752ddbeb68698095` |
| `03_Implementation/src/model/__init__.py` | `81cc7a8d1f068d8bbdfbcab3aac34005649affa8ab5d08bf0467b829c382a341` |
| `03_Implementation/src/model/errors.py` | `4bcecae48f3783efabb108e5b961d31aee23bfd79bcfce95f293d2afd296ff8f` |
| `03_Implementation/src/model/manager.py` | `110c81878915abed4ae53f1b39e72a47d4c743de16a63e54ecfa5fcb41afb5cd` |
| `03_Implementation/src/model/records.py` | `5f1c2f75211330e263b4fe7352bfc693d84102b4944d72af43b425c2e3a991e4` |
| `03_Implementation/src/model/search.py` | `1930a0c07c69b8e02b3d9fb1931b9c44e2bf756e559e03a73cd5b5e1ed97b5c8` |
| `03_Implementation/src/model/validation.py` | `8827cfeaf0e879df4dab616edb5f1f950c2ac67fb74e5d49bf8926cd59a338c3` |
| `03_Implementation/src/storage/__init__.py` | `972c5ae0bc93c80a7a2171ae0b39fed5b979e1ecc7939b178f0f71c0041fdc39` |
| `03_Implementation/src/storage/pim_file.py` | `abef69f231ca816c70997dd9ce5433ff2125a0275ecf061bc7ed1e3d92145c04` |
| `03_Implementation/Test_Coverage.pdf` | `e3d2568aa130169fcb5c79d277b9aaf111c4b798e504080606e3d2852a7fb3a9` |
| `03_Implementation/tests/__init__.py` | `4566908709322660744dbe6e820b2afff9e16850e596c53915904dd82a2e25e4` |
| `03_Implementation/tests/controller/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `03_Implementation/tests/controller/test_cli.py` | `5ff3d92dbe3d7e38753342578fb68a6b49f7bd18bfc981df543e1de045375802` |
| `03_Implementation/tests/controller/test_requirement_edges.py` | `99dbe6b82fceb1d50508571928232ceab3d4ccdca089edc52d22b11372fccd64` |
| `03_Implementation/tests/model/__init__.py` | `65b20d4f0eeda97a8ee5825e54801364bebdf9a6f59ee6377ee43c4aed18349d` |
| `03_Implementation/tests/model/test_manager.py` | `b88f97a95433b157ebcf93cdd9ea1fd5a88fd5813efc3bda212ad54191fa61ef` |
| `03_Implementation/tests/model/test_records.py` | `2854f29ca772dd3900bc7cfc151f75568aa6de9ab0fdd2f002d04c73028bbd97` |
| `03_Implementation/tests/model/test_requirement_edges.py` | `7d4349b63dd60b814d4e9efae519b0965b885b2c16c7b22dbd1c65c2a5ae0569` |
| `03_Implementation/tests/model/test_search.py` | `3b84a8128198610052fb0d341c8caaa31f4c092abda2bc42a5d5e314f8a0dccd` |
| `03_Implementation/tests/model/test_search_integration.py` | `32e56ced206bca9b3003ac2b5f451830aeef9eccc394364ce3b3e53809bb0f95` |
| `03_Implementation/tests/README.md` | `4c420235699d61db3592b053cbd4aa6b47fcc25d35b7930c5be072bed3a90616` |
| `03_Implementation/tests/storage/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `03_Implementation/tests/storage/test_pim_file.py` | `673ae1b8bf72ec82e8992a06c620cf691af48b30ebe8bfb6e3489fab6a1b8998` |
| `03_Implementation/tests/storage/test_requirement_edges.py` | `f1c2131d9e6c43ddc2e5769b1a27e1714d61fbc34f887cff407eff5b4a79d742` |
| `03_Implementation/tests/test_acceptance.py` | `aa8c2ee0752e0d2436da3066e45e2ecf369e8cff056fadc5021221ff5746a753` |
| `03_Implementation/tools/model_coverage.py` | `bf20277ad8c766a610c3ac99d9df72ab386e54e99994c1a98f84dcef6afb6080` |
| `03_Implementation/User_Manual.pdf` | `edac3089b338b2a8f8ce2a001993b49717cdbfa4c8ec429b3035b97b4531de96` |
| `05_Presentation/Presentation.pdf` | `07e12971868c168d0c2d63e7e7b14db1ea4e04c723ee9d5293128fbbb28b379e` |

## Outstanding human artifacts

- `04_Demo/System_Demo.mp4`: actual system demo, at most 4 minutes, review playback and measured duration.
- `05_Presentation/Presentation_Recording.mp4`: at most 5 minutes; each of four members speaks at least 1 minute, shows ID and face at their start, and keeps their face visible while speaking.
- `Honour_Declaration_for_Group_Project.pdf` at ZIP root: official form, accurate identities and AI disclosure, agreed contribution percentages and required signatures.

Group members must also review the content and replace relevant identity placeholders using verified information before the final export. The current PPTX, scripts, AI-use log and Chinese meeting note are maintained outside the submission ZIP for group editing. After adding real artifacts or modifying content, regenerate the final ZIP, manifest and extracted-folder checks.
