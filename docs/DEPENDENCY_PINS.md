# Shared contract pins

The Sentinel tab has a card that shows, for every ecosystem, which version of its shared contracts each repository was last checked against, next to the current
version of those contracts. It only reports what the repositories write in their own files; it does not test compatibility.

## Where the pins come from

| Ecosystem | Pins | Current version |
|---|---|---|
| A.R.M.O.R. | `registry/contract_pins.json` of `ARMOR-COMMON` (consumer -> version) | `version` of `armor.project.json` of `ARMOR-COMMON` |
| URTC | `urtc_common_version` of `tools/urtc_common.lock.json` of every URTC repository that has one | `version` of `urtc.project.json` of `URTC-COMMON` |
| HYDRA-UMC | no machine readable source, so it is listed as such and never guessed | - |

The files are read once per page generation through the contents API with the read-only token of the workflow, and the result is embedded in the page.

## States

| State | Meaning |
|---|---|
| current | the pin equals the current version (missing trailing components count as zero) |
| behind | the pin is older than the current version |
| ahead | the pin is newer than the current version |
| unknown | the pin is not a version number |

If a source cannot be read the ecosystem is shown as "not verified"; if only some URTC repositories fail they are left out and the card says so. Nothing that could
not be read is ever shown as current.

## Signatures and attestations

The dashboard only checks that signatures and build attestations EXIST (see `SIGNATURE_PRESENCE.md`); the cryptographic verification of an attestation is done by the
owner's local monitor, not here.
