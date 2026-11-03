#!/usr/bin/env python3
# =============================================================================
# JuanenRac profile - scripts/dashboard_nav_ui.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0 - see LICENSE.md
# =============================================================================
"""Keyboard shortcuts with their help, and the breadcrumb ("where am I") of the status dashboard.

The markup, the style sheet and the script are plain strings placed into the page by dashboard_app. The script is inserted into the shell's own scope (it
uses `activateTab`, `currentTab`, `state`, `openPanel`, `navRepo`, `parseHash` and `currentDict`), so it must stay in step with dashboard_app.JS.

Single-key shortcuts follow the rules of WCAG 2.1.4: they are off while a field has the focus, they never use a modifier of the browser or of the system,
and the help dialog has a switch that turns them all off (remembered in the browser when it can be). Stdlib only.
"""
from __future__ import annotations

import dashboard_robust_texts
from dashboard_charts import esc

EN = dashboard_robust_texts.TEXTS["en"]

# (keys as shown, i18n key of the action)
SHORTCUTS: tuple[tuple[tuple[str, ...], str], ...] = (
    (("/",), "help_k_search"),
    (("1", "2", "3", "4"), "help_k_eco"),
    (("0",), "help_k_summary"),
    (("?",), "help_k_help"),
    (("C",), "help_k_compact"),
    (("P",), "help_k_present"),
    (("←", "→", "Home", "End"), "help_k_tabs"),
    (("Esc",), "help_k_esc"),
)


def help_button() -> str:
    return (f'<button type="button" class="btn btn-ghost btn-help" id="help-open" data-testid="help-open" aria-haspopup="dialog" aria-label="{esc(EN["help_open"])}" '
            f'title="{esc(EN["help_open_title"])}" data-i18n-aria-label="help_open" data-i18n-title="help_open_title"><span aria-hidden="true">?</span></button>')


def help_dialog() -> str:
    rows = "".join(
        f'<tr><th scope="row">{" ".join(f"<kbd>{esc(k)}</kbd>" for k in keys)}</th><td data-i18n="{key}">{esc(EN[key])}</td></tr>' for keys, key in SHORTCUTS)
    return (
        '<dialog class="help-dialog" id="help-dialog" aria-labelledby="help-title" data-testid="help-dialog">'
        f'<h2 id="help-title" data-i18n="help_open">{esc(EN["help_open"])}</h2>'
        f'<p class="muted" data-i18n="help_intro">{esc(EN["help_intro"])}</p>'
        f'<table class="help-table" data-testid="help-table"><thead><tr><th scope="col" data-i18n="help_col_key">{esc(EN["help_col_key"])}</th>'
        f'<th scope="col" data-i18n="help_col_action">{esc(EN["help_col_action"])}</th></tr></thead><tbody>{rows}</tbody></table>'
        f'<div class="help-toggle"><input type="checkbox" id="help-keys-on" data-testid="help-keys-on" checked> <label for="help-keys-on" data-i18n="help_toggle">{esc(EN["help_toggle"])}</label></div>'
        f'<div class="help-actions"><button type="button" class="btn" id="help-close" data-testid="help-close" data-i18n="help_close">{esc(EN["help_close"])}</button></div>'
        '</dialog>'
    )


def crumbs() -> str:
    return (f'<nav class="crumbs" aria-label="{esc(EN["crumb_label"])}" data-i18n-aria-label="crumb_label" data-testid="crumbs">'
            f'<ol id="crumb-list"><li aria-current="page"><span data-i18n="crumb_home">{esc(EN["crumb_home"])}</span></li></ol></nav>')


CSS = r"""
  /* ======================= Keyboard help and breadcrumb ======================= */
  .btn-help { min-width: 32px; padding: 4px 9px; font-weight: 800; border-color: var(--border-strong); background: var(--panel-2); color: var(--text); }
  :root[data-theme="dark"] .btn-help, :root:not([data-theme="light"]) .btn-help { color: var(--text); }
  .help-dialog { max-width: min(640px, 92vw); border: 1px solid var(--border-strong); border-radius: var(--radius); background: var(--panel); color: var(--text); padding: 18px 20px; }
  .help-dialog::backdrop { background: rgba(0, 0, 0, .55); }
  .help-dialog h2 { margin: 0 0 8px; font-size: 18px; }
  .help-table { width: 100%; border-collapse: collapse; margin: 10px 0; font-size: 13px; }
  .help-table th, .help-table td { text-align: left; padding: 6px 8px; border-bottom: 1px solid var(--border); vertical-align: top; }
  .help-table thead th { color: var(--dim); font-size: 11px; letter-spacing: .08em; text-transform: uppercase; }
  .help-table tbody th { white-space: nowrap; font-weight: 400; width: 1%; }
  kbd { display: inline-block; min-width: 1.6em; text-align: center; padding: 1px 6px; margin-right: 3px; border: 1px solid var(--border-strong); border-bottom-width: 2px; border-radius: 6px; background: var(--panel-2); color: var(--text); font: 600 12px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }
  .help-toggle { display: flex; gap: 8px; align-items: center; margin: 10px 0; font-size: 13px; }
  .help-actions { display: flex; justify-content: flex-end; }
  .crumbs { margin-top: 0; font-size: 11px; max-width: 420px; }
  .crumbs ol { list-style: none; margin: 0; padding: 0; display: flex; flex-wrap: nowrap; gap: 0; overflow: hidden; white-space: nowrap; }
  .crumbs li { display: inline-flex; align-items: center; min-height: 24px; min-width: 0; color: var(--dim); }
  .crumbs li + li::before { content: "›"; margin: 0 6px; color: var(--dim); }
  .crumbs li:last-child { color: var(--text); font-weight: 600; min-width: 0; overflow: hidden; text-overflow: ellipsis; }
  .crumbs a { display: inline-flex; align-items: center; min-height: 24px; color: var(--accent); text-decoration: underline; text-underline-offset: 2px; }
  @media (max-width: 760px) { .crumbs { max-width: 100%; } }
  @media print { .crumbs, .help-dialog, #help-open { display: none !important; } }
"""

JS = r"""
  // ---------------- Keyboard shortcuts, their help and the breadcrumb ----------------
  const KEYS_KEY = "hydra-dashboard-keys";
  const helpDialog = document.getElementById("help-dialog");
  const helpOpen = document.getElementById("help-open");
  const helpKeysOn = document.getElementById("help-keys-on");
  const crumbList = document.getElementById("crumb-list");
  const ECO_KEYS = { "1": "hydra-umc", "2": "urtc", "3": "armor", "4": "eh3d" };
  var helpOpener = null;

  shortcutsOn = safeGet(KEYS_KEY) !== "off";
  if (helpKeysOn) {
    helpKeysOn.checked = shortcutsOn;
    helpKeysOn.addEventListener("change", function () { shortcutsOn = helpKeysOn.checked; safeSet(KEYS_KEY, shortcutsOn ? "on" : "off"); });
  }
  function helpIsOpen() { return !!(helpDialog && helpDialog.hasAttribute("open")); }
  function openHelp(opener) {
    if (!helpDialog || helpIsOpen()) { return; }
    helpOpener = opener || document.activeElement;
    if (helpKeysOn) { helpKeysOn.checked = shortcutsOn; }
    try { helpDialog.showModal(); } catch (e) { helpDialog.setAttribute("open", ""); }
    const close = document.getElementById("help-close");
    if (close) { close.focus(); }
  }
  function closeHelp() {
    if (!helpIsOpen()) { return; }
    try { helpDialog.close(); } catch (e) { helpDialog.removeAttribute("open"); }
    if (helpOpener && document.contains(helpOpener) && helpOpener.focus) { helpOpener.focus(); }
    helpOpener = null;
  }
  if (helpOpen) { helpOpen.addEventListener("click", function () { openHelp(helpOpen); }); }
  const helpCloseBtn = document.getElementById("help-close");
  if (helpCloseBtn) { helpCloseBtn.addEventListener("click", closeHelp); }
  if (helpDialog) { helpDialog.addEventListener("cancel", function (event) { event.preventDefault(); closeHelp(); }); }

  // Capture phase: Escape closes the help first, and the other Escape handlers (panel, presentation mode) do not also react to the same key press.
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && helpIsOpen()) { event.preventDefault(); event.stopPropagation(); closeHelp(); }
  }, true);

  function focusSearch() {
    const input = document.getElementById("project-search");
    if (!input || rootEl.getAttribute("data-mode") === "present") { return false; }
    const toggle = document.getElementById("filters-toggle");
    if (toggle && toggle.offsetParent !== null && toggle.getAttribute("aria-expanded") === "false") { toggle.click(); }
    input.focus();
    input.select();
    return true;
  }

  document.addEventListener("keydown", function (event) {
    if (event.defaultPrevented || event.ctrlKey || event.altKey || event.metaKey || event.isComposing) { return; }
    const target = event.target;
    if (target && target.closest && target.closest("input, select, textarea, [contenteditable='true'], dialog:not(.help-dialog)")) { return; }
    if (!shortcutsOn || (helpIsOpen() && event.key !== "?")) { return; }
    const key = event.key;
    if (key === "?") { event.preventDefault(); if (helpIsOpen()) { closeHelp(); } else { openHelp(null); } }
    else if (key === "/") { if (focusSearch()) { event.preventDefault(); } }
    else if (key === "0") { event.preventDefault(); activateTab("summary"); }
    else if (Object.prototype.hasOwnProperty.call(ECO_KEYS, key)) { event.preventDefault(); activateTab(ECO_KEYS[key]); }
  });

  // ---- Breadcrumb: tab > scope > repository, mirrored in the address ----
  function crumbText(selector, fallback) {
    const el = document.querySelector(selector);
    return el ? el.textContent.trim() : fallback;
  }
  function crumbHash(tab, scope, repo) {
    let hash = "#" + tab;
    const query = [];
    if (tab === "projects" && scope && scope !== "all") { query.push("scope=" + encodeURIComponent(scope)); }
    if (repo) { query.push("repo=" + encodeURIComponent(repo)); }
    return query.length ? hash + "?" + query.join("&") : hash;
  }
  function crumbRender(dict) {
    if (!crumbList) { return; }
    dict = dict || currentDict();
    const items = [{ label: dict.crumb_home, hash: "#summary", key: "home" }];
    const tabButton = document.querySelector("[role='tab'][data-tab='" + currentTab + "']");
    items.push({ label: tabButton ? tabButton.textContent.trim() : currentTab, hash: crumbHash(currentTab, "all", null), key: "tab" });
    if (currentTab === "projects") {
      const scopeLabel = crumbText("[data-scope='" + state.eco + "'] span", state.eco);
      items.push({ label: scopeLabel, hash: crumbHash("projects", state.eco, null), key: "scope" });
    }
    if (navRepo) { items.push({ label: navRepo, hash: crumbHash(currentTab, state.eco, navRepo), key: "repo" }); }
    crumbList.textContent = "";
    items.forEach(function (item, index) {
      const li = document.createElement("li");
      li.setAttribute("data-crumb", item.key);
      if (index === items.length - 1) {
        li.setAttribute("aria-current", "page");
        li.textContent = item.label;
      } else {
        const a = document.createElement("a");
        a.href = item.hash;
        a.textContent = item.label;
        li.appendChild(a);
      }
      crumbList.appendChild(li);
    });
  }
  crumbRefresh = crumbRender;
  crumbRender(currentDict());

  // The repository named in the address is opened once the whole script is ready; the address is read again when it changes.
  function openRepoFromHash(parsed) {
    const name = parsed && parsed.params ? parsed.params.repo : "";
    if (name && DATA.repos[name] && name !== navRepo) { openPanel(name, null); }
  }
  openRepoFromHash(startHash);
  window.addEventListener("hashchange", function () { openRepoFromHash(parseHash()); });
"""
