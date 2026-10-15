#!/usr/bin/env bash
# =============================================================================
# HYDRA-UMC / URTC Ecosystem - starter-kit.sh
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
#
# Clones 13 core repositories (README.md's own "Core Ecosystem" table,
# plus HYDRA-UMC-UPDATER itself) as siblings under one workspace
# directory - the standard layout every cross-repo script in this
# ecosystem already assumes (HYDRA-UMC-SERVER's build-frontend.sh,
# HYDRA-UMC-SUITE's own discovery, HYDRA-UMC-UPDATER's own
# default_workspace_root()). Only these 13, not the full ~47-repo
# catalog - the request this answers ("Starter Kit que descargue los
# 12 repositorios core") asked specifically for a small core set, and
# that's also the smaller, faster, more focused starting point for
# someone new to the ecosystem. HYDRA-UMC-UPDATER is included precisely
# so the "next step" this script prints at the end - using it to check
# versions and build/update anything else - is something you can
# actually do immediately, without a second manual clone first.
#
# Idempotent: a directory that already exists here is left completely
# untouched (never pulled, never reset) - re-running this script after a
# partial run only clones what's still missing. Use HYDRA-UMC-UPDATER's
# own `update <name>` for pulling latest on something already cloned;
# this script's only job is the very first "get the source" step.
#
# Other sets (second argument) clone a whole ecosystem instead, discovered
# live exactly the way the dashboard and the updaters discover it - every
# public JuanenRac repository whose default branch carries that
# ecosystem's manifest - so the list never goes stale:
#   core       the 13 repositories above (default)
#   hydra-umc  every HYDRA-UMC repository  (hydra-umc.project.json)
#   urtc       every URTC repository       (urtc.project.json)
#   armor      every A.R.M.O.R. repository (armor.project.json)
#   all        the three ecosystems together
# Discovery needs curl; set GITHUB_TOKEN to raise GitHub's API rate limit.
#
# Usage:
#   ./starter-kit.sh [destination-directory] [core|hydra-umc|urtc|armor|all]
# =============================================================================
set -euo pipefail

DEST="${1:-.}"
SET="${2:-core}"
OWNER="JuanenRac"
case "$SET" in
  core|hydra-umc|urtc|armor|all) ;;
  *) echo "Unknown set '$SET' - use core, hydra-umc, urtc, armor or all" >&2; exit 2 ;;
esac
mkdir -p "$DEST"
cd "$DEST"

# Every public repository of $OWNER whose default branch has manifest $1.
discover() {
  local manifest="$1" page=1 auth=() listing names repo branch
  if [ -n "${GITHUB_TOKEN:-}" ]; then auth=(-H "Authorization: Bearer $GITHUB_TOKEN"); fi
  while :; do
    listing="$(curl -fsSL "${auth[@]}" "https://api.github.com/users/$OWNER/repos?type=owner&per_page=100&page=$page")" || {
      echo "FAIL  could not list $OWNER's repositories (network or rate limit)" >&2; return 1; }
    names="$(printf '%s' "$listing" | grep -o '"full_name": *"[^"]*"' | sed 's/.*"\([^"]*\)"$/\1/' | sed "s#^$OWNER/##")"
    [ -z "$names" ] && break
    for repo in $names; do
      branch="$(printf '%s' "$listing" | tr -d '\n' | grep -o "\"full_name\": *\"$OWNER/$repo\"[^}]*\"default_branch\": *\"[^\"]*\"" | sed 's/.*"default_branch": *"\([^"]*\)"/\1/' | head -1)"
      if curl -fsSL -o /dev/null "https://raw.githubusercontent.com/$OWNER/$repo/${branch:-main}/$manifest"; then
        echo "$repo"
      fi
    done
    [ "$(printf '%s\n' "$names" | wc -l)" -lt 100 ] && break
    page=$((page + 1))
  done
}

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
  HYDRA-UMC-UPDATER
)

case "$SET" in
  core)      REPOS=("${CORE_REPOS[@]}") ;;
  hydra-umc) mapfile -t REPOS < <(discover hydra-umc.project.json) ;;
  urtc)      mapfile -t REPOS < <(discover urtc.project.json) ;;
  armor)     mapfile -t REPOS < <(discover armor.project.json) ;;
  all)       mapfile -t REPOS < <(discover hydra-umc.project.json; discover urtc.project.json; discover armor.project.json) ;;
esac
if [ "${#REPOS[@]}" -eq 0 ]; then
  echo "No repositories found for set '$SET' - nothing to clone." >&2
  exit 1
fi

echo "============================================================"
echo " HYDRA-UMC / URTC / A.R.M.O.R. Starter Kit - set: $SET"
echo " Cloning ${#REPOS[@]} repositories into: $(pwd)"
echo "============================================================"

cloned=0
skipped=0
failed=0

for repo in "${REPOS[@]}"; do
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
echo "Next step: each ecosystem's own updater (HYDRA-UMC-UPDATER,"
echo "URTC-UPDATER, ARMOR-UPDATER - or ELECTRO-HOBBY-3D-UPDATER for all"
echo "three) can check versions, install/update any other project one at a"
echo "time, and build each project via its own build.sh/.bat. This script's"
echo "only job was step one: getting the source onto disk."

if [ "$failed" -gt 0 ]; then
  exit 1
fi
