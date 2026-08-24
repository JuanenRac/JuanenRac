#!/usr/bin/env bash
# =============================================================================
# HYDRA-UMC / URTC Ecosystem - starter-kit.sh
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
#
# Clones the 12 original/core repositories (README.md's own "Core
# Ecosystem" table) as siblings under one workspace directory - the
# standard layout every cross-repo script in this ecosystem already
# assumes (HYDRA-UMC-SERVER's build-frontend.sh, HYDRA-UMC-SUITE's own
# discovery, HYDRA-UMC-UPDATER's own default_workspace_root()). Only
# the 12 core repos, not all 44/45 - the audit idea this answers
# ("Starter Kit que descargue los 12 repositorios core") asked
# specifically for the core set, and that's also the smaller, faster,
# more focused starting point for someone new to the ecosystem; run
# HYDRA-UMC-UPDATER afterward (see the summary this script prints at the
# end) for the rest, or to build/update anything cloned here.
#
# Idempotent: a directory that already exists here is left completely
# untouched (never pulled, never reset) - re-running this script after a
# partial run only clones what's still missing. Use HYDRA-UMC-UPDATER's
# own `update <name>` for pulling latest on something already cloned;
# this script's only job is the very first "get the source" step.
#
# Usage:
#   ./starter-kit.sh [destination-directory]   (default: current directory)
# =============================================================================
set -euo pipefail

DEST="${1:-.}"
mkdir -p "$DEST"
cd "$DEST"

CORE_REPOS=(
  HYDRA-UMC
  HYDRA-UMC-SERVER
  HYDRA-UMC-STUDIO
  HYDRA-UMC-SUITE
  HYDRA-UMC-DSI
  HYDRA-UMC-ANDROID-CONTROL
  HYDRA-UMC-IOS-CONTROL
  HYDRA-UMC-EDITOR-URDF
  URTC
  URTC-FLASHER
  URTC-TESTER
  URTC-WEB-STUDIO
)

echo "============================================================"
echo " HYDRA-UMC / URTC Starter Kit"
echo " Cloning the 12 core repositories into: $(pwd)"
echo "============================================================"

cloned=0
skipped=0
failed=0

for repo in "${CORE_REPOS[@]}"; do
  if [ -d "$repo" ]; then
    echo "SKIP  $repo (already exists here - untouched)"
    skipped=$((skipped + 1))
    continue
  fi
  echo "CLONE $repo ..."
  if git clone --quiet "https://github.com/JuanenRac/$repo.git" "$repo"; then
    cloned=$((cloned + 1))
  else
    echo "FAIL  $repo - see git's own error above"
    failed=$((failed + 1))
  fi
done

echo "============================================================"
echo " Done: $cloned cloned, $skipped already present, $failed failed"
echo "============================================================"
echo
echo "Next step: HYDRA-UMC-UPDATER (one of the repos just cloned above)"
echo "can check versions, install/update any of the other projects one"
echo "at a time, and build each project via its own build.sh/.bat - see"
echo "HYDRA-UMC-UPDATER/README.md. This script's only job was step one:"
echo "getting the source onto disk."

if [ "$failed" -gt 0 ]; then
  exit 1
fi
