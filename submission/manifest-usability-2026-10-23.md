# Current candidate manifest - COMP3211 Group 89

**Candidate:** `output/COMP3211_Group_Project-usability-2026-10-23.zip`

**Assembly:** `output/COMP3211_Group_Project-usability-2026-10-23/`

**ZIP SHA-256:** `9d0b243473e4dc565d40865b01318ee2b75f7515af55a4c3736e30dea1f4dd27`

**Payload:** 86 files; 1731308 ZIP bytes.

Current working-tree files, including uncommitted fixes, identify this release. Historical commit 4d3508d is not the complete delivery. Older archives are retained.

## Verification

Payload byte equality and ZIP CRC checked during assembly. Repository verification is recorded in `docs/reports/usability-release-2026-10-23.md` and the packaged evidence logs. Assembly alone does not establish that tests passed. Post-packaging clean-extraction verification must be recorded below before calling this candidate verified. Re-run after any subsequent change.

## Pending real deliverables

- `04_Demo/System_Demo.mp4`: actual recording, <=4 minutes.
- `05_Presentation/Presentation_Recording.mp4`: <=5 minutes, each member >=1 minute; real IDs/faces at each speaker's start and face visible throughout.
- `Honour_Declaration_for_Group_Project.pdf`: official form at ZIP root, with genuine details, agreed contributions and truthful AI disclosure.

NFR-01's exact disconnected/no-graphical-session check remains unverified. Human group review remains pending. This is not a submitted or complete assignment.

## Completed clean-extraction verification (2026-10-23)

Verified the exact ZIP SHA-256 `9d0b243473e4dc565d40865b01318ee2b75f7515af55a4c3736e30dea1f4dd27` in a new extraction directory. All 85 payload hashes and ZIP CRC passed; every source/test/tool file equals the current working-tree bytes. All 86 tests passed on Python 3.11.9, 3.12.3 and 3.13.5, including site-disabled runs. Full-suite model coverage is 431/436 (98.85%); 32 model unit methods alone cover 430/436 (98.62%) on all three versions. The packaged demo verifier, 1,000-record/five-run benchmark and compile checks passed on each version (21 recorded commands in total).

The six document PDFs plus six-slide presentation were rendered and visually checked: 40 pages/slides in total, with no text outside page bounds. PDF hashes match the ZIP. The editable PPTX passed package/layout/font checks and first-party reimport. All 54 FR and 5 NFR statements match the catalogue and have coverage rows; all 11 stories are mapped.

Full post-build log: `docs/reports/usability-clean-extraction-2026-10-23.txt`. This log is outside the immutable ZIP because it verifies that exact archive. No application code changed after these checks. Missing human deliverables remain as listed above.

## Per-file SHA-256

| Archive path | SHA-256 |
|---|---|
| `00_README.txt` | `f225613569537fc343bdfe9ed0552b758c042d6e46bc4c785edcf3555ffd4616` |
| `01_SRS/SRS.pdf` | `27f421444f8b22b49527b3ef7128099ee39e24bf1a74ec672f9d698d2584361c` |
| `02_Design/Design_Document.pdf` | `b9a541ef8c7a35e73d8df8a8424dfe403ec190f553f031e045c3db3076f28b47` |
| `03_Implementation/Developer_Manual.pdf` | `0baf9a58d6108a8b7529440bb20be012bc989c6d69d3c3a3d71836be1d1dd412` |
| `03_Implementation/evidence/usability-benchmark-2026-10-23-python311.txt` | `20e84e058802e6c61fb797433fd8181abcc30cd30d1112d27aeeb7c6ff1eed39` |
| `03_Implementation/evidence/usability-benchmark-2026-10-23-python312.txt` | `f733d6d588f452969a269915f06a0c5c4b7553f51f0dc1fcd4a5efb4c09adf30` |
| `03_Implementation/evidence/usability-benchmark-2026-10-23-python313.txt` | `4f0e2c168bd4e9d73445e1e386959794a17b6185084cd6b9a22fe3f189ed17b8` |
| `03_Implementation/evidence/usability-compile-2026-10-23-python311.txt` | `4b9cf68ad82b61269294558b3eaaa1fd41f668558fb44627974fd110a2ef8af3` |
| `03_Implementation/evidence/usability-compile-2026-10-23-python312.txt` | `929b590fb17966a6684f5fb32dcb64d3251875f5e26ef6d112cc25529609326d` |
| `03_Implementation/evidence/usability-compile-2026-10-23-python313.txt` | `85fd361905e94b6e5c659c7087cd2da32afdf4c206845ac097b85af9ac231b78` |
| `03_Implementation/evidence/usability-coverage-2026-10-23-python311.txt` | `bdc58af35b46dc4be4c0049630d3c400cfa4c6dc91daeab7fb2f5467d6385c76` |
| `03_Implementation/evidence/usability-coverage-2026-10-23-python312.txt` | `91edfb06a352192da101127af73c3437f5fa1aef4341d37b18ecd50e584a1ec8` |
| `03_Implementation/evidence/usability-coverage-2026-10-23-python313.txt` | `b9f8153b3e056ca392736d27f68a16471f30ed611371ef558ae26a4f23b2b2d4` |
| `03_Implementation/evidence/usability-demo-2026-10-23-python311.txt` | `ad0b6d691f525f5f0bf31eb2174b4baaf1727bf4193a54ca7c5c061490092228` |
| `03_Implementation/evidence/usability-demo-2026-10-23-python312.txt` | `54176dc88c2cce008f6bb399581e4a5558f450d0c0749f3486dd6fef3e87d897` |
| `03_Implementation/evidence/usability-demo-2026-10-23-python313.txt` | `1dc9d467a29feade9c2fccf01ab2354e1e54aefb9b5533230eb4db92c1461b53` |
| `03_Implementation/evidence/usability-import-audit-2026-10-23.txt` | `f088ae5272f5da5c84ae27b94e48eb5141d7462d6ead7c1ea1d9ba64f7a2964b` |
| `03_Implementation/evidence/usability-model-only-2026-10-23-python311.txt` | `bf21464e106d1144e68a8349dd44237723bff86ba1843522a51739988c580069` |
| `03_Implementation/evidence/usability-model-only-2026-10-23-python312.txt` | `8aeec87e6cf1aecc28cd9dcaff78d52c5c970e8e5565314b45ea48ce386e630a` |
| `03_Implementation/evidence/usability-model-only-2026-10-23-python313.txt` | `021eb05f5d854c3c656f8a345d3f7e6569e0e6ae418fe6987d6e03d0a1ffe91b` |
| `03_Implementation/evidence/usability-pdf-geometry-2026-10-23.json` | `bd667f57ed8b99c610f8c8cf2f66b49cdf6ea5e7ebd5cdf0ddab9c7fc42f43a8` |
| `03_Implementation/evidence/usability-release-2026-10-23.md` | `0b0aed8d67defe3d301fec30d2fac8cd7d3d76fab7c6769a88dd981295842cce` |
| `03_Implementation/evidence/usability-stdlib-2026-10-23-python311.txt` | `3a0d00a1c12733d31f90cb5dca245bdaa87557c27268c91ca49289eb20aeae17` |
| `03_Implementation/evidence/usability-stdlib-2026-10-23-python312.txt` | `6c9ba9351cfa982d7a7f7e5cd1c0fa3650fe6c1de2b86b1e2c729dd9c2eb258d` |
| `03_Implementation/evidence/usability-stdlib-2026-10-23-python313.txt` | `af8617bc659bc00eeab61946ec00d8d15d5ec71af0db79674f5a4f925c89a553` |
| `03_Implementation/evidence/usability-traceability-2026-10-23.json` | `7859600354a947c4aa277dbee87094ab87494ad18f833b671f70e23d581d3ce6` |
| `03_Implementation/evidence/usability-verification-2026-10-23-python311.txt` | `4903f6a377aa29f5fccc8e0ca176f630358414019c82979fff1d15c40db3c302` |
| `03_Implementation/evidence/usability-verification-2026-10-23-python312.txt` | `0e5d2201a8812f25ec077e2b4a0badad8073409791e0d6332e49681f39d5d7a9` |
| `03_Implementation/evidence/usability-verification-2026-10-23-python313.txt` | `d4faef5639451193f0cabe757256279e8ca10c677f48897c0faf34ba98e7cdf4` |
| `03_Implementation/media/demo/demo-commands.txt` | `3a80bc5836c415a481c8f390688430b4c8d8a2285eecad082d153a1b6d55de9a` |
| `03_Implementation/media/demo/demo-expected-output.txt` | `ac57c97090170b81f1c6e323119488e19a820309e814876604ec114e0f03d9da` |
| `03_Implementation/README.md` | `e37a3c6d5fbb1fcf5e3503ec6da03043a59c771bca2797654e5e401171cf7c38` |
| `03_Implementation/Requirements_Coverage.pdf` | `86f66159dd4562469a795345b8caa248b970140650d7242dae5c709bfef17615` |
| `03_Implementation/src/controller/__init__.py` | `b57a037a6a7f097fbc8d3f502d0c654f64c80d1ad85c847dd6ddcbb7436bb3c5` |
| `03_Implementation/src/controller/cli.py` | `04e0c7d0a56c25f813b93eef2649b26e2303f51a850bc1d7642be02d0bafec4e` |
| `03_Implementation/src/controller/help.py` | `5e9a1bf5318944054e5f7ef65d7c903334cbf13c71541821f47d3eb697f1acbb` |
| `03_Implementation/src/controller/output.py` | `d7fc0ba1bf0d7c23ab8b32b7a674d254539276170356eefd514bb933908ffb5f` |
| `03_Implementation/src/main.py` | `a32661ef03040693d88265376b6134244bea3cf41386a63dbcf265bc63659687` |
| `03_Implementation/src/model/__init__.py` | `81cc7a8d1f068d8bbdfbcab3aac34005649affa8ab5d08bf0467b829c382a341` |
| `03_Implementation/src/model/errors.py` | `5bd4f6ffef7f44e5ab2b35fcffb2d52e490d24d84084afea58c0a5c6644edd70` |
| `03_Implementation/src/model/manager.py` | `110c81878915abed4ae53f1b39e72a47d4c743de16a63e54ecfa5fcb41afb5cd` |
| `03_Implementation/src/model/records.py` | `5f1c2f75211330e263b4fe7352bfc693d84102b4944d72af43b425c2e3a991e4` |
| `03_Implementation/src/model/search.py` | `82c2647cce93a20e2bf6974f1dc9b1d84e05a709d9d9ee31608b729d6b2dd46b` |
| `03_Implementation/src/model/validation.py` | `8827cfeaf0e879df4dab616edb5f1f950c2ac67fb74e5d49bf8926cd59a338c3` |
| `03_Implementation/src/storage/__init__.py` | `972c5ae0bc93c80a7a2171ae0b39fed5b979e1ecc7939b178f0f71c0041fdc39` |
| `03_Implementation/src/storage/pim_file.py` | `5c0eebe8c8f8719387d7ee2980541dacd00595a443a7b651bd8ad8ad91953402` |
| `03_Implementation/Test_Coverage.pdf` | `290de56f37db3f9787ecad51328909f068e659e5c483ae69bee2211c5a7797b3` |
| `03_Implementation/tests/__init__.py` | `4566908709322660744dbe6e820b2afff9e16850e596c53915904dd82a2e25e4` |
| `03_Implementation/tests/controller/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `03_Implementation/tests/controller/test_cli.py` | `05de516fe3a006b4aba3f7d60ea61edcc4ada2a0d3deddd933087cb3064ea499` |
| `03_Implementation/tests/controller/test_independent_review.py` | `638df80179842cff96d57ae5f15c7beca685d6995a165a0391867ed543a562c1` |
| `03_Implementation/tests/controller/test_requirement_edges.py` | `437e4fc66574ea293fe8f8904480396a7ff6baa811ff6415f55715e8dd33c018` |
| `03_Implementation/tests/controller/test_terminal.py` | `b667892bf1b02ed6a01547ec90d510b3d09e59c66f11ec428e8a71ae87b9970b` |
| `03_Implementation/tests/controller/test_usability.py` | `e3ab5d5bdb4376d099bcb7e7e5c7c8adeddf2bc2b3a4ec3444e914059f6ee24c` |
| `03_Implementation/tests/model/__init__.py` | `65b20d4f0eeda97a8ee5825e54801364bebdf9a6f59ee6377ee43c4aed18349d` |
| `03_Implementation/tests/model/test_independent_review.py` | `c83e96c188f3e900441b22c6b9cd2b3f2c65c7ee4bd08e86bae8cff79c13d851` |
| `03_Implementation/tests/model/test_manager.py` | `b88f97a95433b157ebcf93cdd9ea1fd5a88fd5813efc3bda212ad54191fa61ef` |
| `03_Implementation/tests/model/test_records.py` | `2854f29ca772dd3900bc7cfc151f75568aa6de9ab0fdd2f002d04c73028bbd97` |
| `03_Implementation/tests/model/test_requirement_edges.py` | `7d4349b63dd60b814d4e9efae519b0965b885b2c16c7b22dbd1c65c2a5ae0569` |
| `03_Implementation/tests/model/test_search.py` | `3b84a8128198610052fb0d341c8caaa31f4c092abda2bc42a5d5e314f8a0dccd` |
| `03_Implementation/tests/model/test_search_integration.py` | `32e56ced206bca9b3003ac2b5f451830aeef9eccc394364ce3b3e53809bb0f95` |
| `03_Implementation/tests/model/test_search_positions.py` | `4f9b52e61c48b3fa7d9a63f110429d54734c92ec4484f3e170edc369bf4fe2d5` |
| `03_Implementation/tests/storage/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `03_Implementation/tests/storage/test_independent_review.py` | `4053e1e2c4a8fd0996148152effc9d09c7c73fb9d819bb41c76dade311df1517` |
| `03_Implementation/tests/storage/test_pim_file.py` | `673ae1b8bf72ec82e8992a06c620cf691af48b30ebe8bfb6e3489fab6a1b8998` |
| `03_Implementation/tests/storage/test_requirement_edges.py` | `8f7389ad827a70bc6be3843584ad7788b69ba158b672099247e6d2414aed2e27` |
| `03_Implementation/tests/test_acceptance.py` | `5293c0fecbd2d90d78e6396e3c5962b566a59758c66e29d204690e8cc2ad93fb` |
| `03_Implementation/tests/test_process_boundaries.py` | `37b89a199339dda996be1289ad0984662d2f02f49fe492980fc2516705673494` |
| `03_Implementation/tests/tools/__init__.py` | `4ce4f013e0fd9b0ea708c1b1b6a9ab63898490db9c29448de7684c0d70b41663` |
| `03_Implementation/tests/tools/test_evidence.py` | `e273f7791153a22226782cc25616b792cf806e003d026be7f9db9bc4a5b2e386` |
| `03_Implementation/tests/tools/test_model_coverage.py` | `f771b8c0158581a4c25b5a53b1d23428624494b12bbed6367135829b6b5deaed` |
| `03_Implementation/tools/benchmark.py` | `b1ea1cef85a72ad18ec069873c75360c9164e12f287d66f98d2c402e404b7d41` |
| `03_Implementation/tools/model_coverage.py` | `aff6a2efda0311235676307a7eb664afc4b1d1cf8ab819a11231aa94b863c042` |
| `03_Implementation/tools/verify_demo.py` | `4e23737313f74c3553a67c32c7c30dfce667c6903ba3df351010720989673aed` |
| `03_Implementation/User_Manual.pdf` | `3ee54c517186f968507d93fcf25a0b781d63322a2524577d3bfb03e5b648c90e` |
| `04_Demo/demo-checklist.md` | `bbea0eabc3462bf2b0ee9f1451bc0a02d635264586891a9ae25951a1a0c0e18c` |
| `04_Demo/demo-script.md` | `5158609125d8eee512ca96f1dba8362bbbda073eff44e550ad9f22ca2acde005` |
| `04_Demo/README.md` | `811495c7042c48764e96ae2baa321d184ccf68db747aee3d36518a8335bb6f9a` |
| `04_Demo/README.txt` | `cceecab085b3ff2f73f54461da6cb1e57e5478e7e47dee92c5501fccf9952db6` |
| `05_Presentation/presentation-script.md` | `e65d88e2bad6579ce7b1c16362856319969972010a6a1e105cc1e3523fb6ee29` |
| `05_Presentation/Presentation.pdf` | `9546f426ffcbadcccd7214fbca137460e5e526861aa8ae6e699d8e58331cce6e` |
| `05_Presentation/Presentation.pptx` | `951eba08b98b31f2a4c4eaeb32246082412eccaa27a5ecaebee0edfde11fc276` |
| `05_Presentation/README.md` | `7eab271282a3275485becc49e63f92bde707433c2c267a7bb7fbac0e1f047876` |
| `05_Presentation/recording-checklist.md` | `7ba82ea25ec50c08172ffc2ec965b3d2a36086120fc1cd79728255c85c1b4b42` |
| `AI_Assistance_Record.md` | `85c5adcf6660ce0a5c54f8872b068c5bb6924643b13e6308a4201bb94dd91f9b` |
| `SHA256SUMS.txt` | `7cdcbaca6b97afffc7f39be66f00585c1a19ef452e96c6175c66c5d2801afb7f` |
