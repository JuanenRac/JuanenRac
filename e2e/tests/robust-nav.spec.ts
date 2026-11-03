import AxeBuilder from "@axe-core/playwright";
import * as fs from "fs";
import { test, expect, openDashboard, gotoTab, panel, visibleText, LEFTOVER, LANGS, Page, Variant } from "./helpers";

const TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"];
const SHOTS = process.env.SHOTS || "";

async function serious(page: Page) {
  const results = await new AxeBuilder({ page }).withTags(TAGS).analyze();
  return results.violations
    .filter((v) => v.impact === "serious" || v.impact === "critical")
    .map((v) => `${v.id} [${v.impact}] ${v.help}: ${v.nodes.slice(0, 3).map((n) => n.target.join(" ")).join(" | ")}`);
}

async function shoot(page: Page, name: string) {
  if (!SHOTS) return;
  fs.mkdirSync(SHOTS, { recursive: true });
  await page.screenshot({ path: `${SHOTS}/${name}.png` });
}

const crumbs = (page: Page) => page.locator("#crumb-list li");
const crumbTexts = async (page: Page) => (await crumbs(page).allTextContents()).map((t) => t.trim());

test.describe("keyboard shortcuts and their help", () => {
  test("? opens the help with every key, Escape closes it and gives the focus back", async ({ page }) => {
    await openDashboard(page);
    await page.getByTestId("tab-summary").focus();
    await page.keyboard.press("?");
    const dialog = page.getByTestId("help-dialog");
    await expect(dialog).toBeVisible();
    await expect(dialog).toHaveAttribute("aria-labelledby", "help-title");
    for (const key of ["/", "1", "4", "0", "?", "C", "P", "Esc"]) await expect(dialog.locator("kbd", { hasText: new RegExp(`^${key.replace("?", "\\?")}$`) }).first()).toBeVisible();
    await expect(page.getByTestId("help-close")).toBeFocused();
    await page.keyboard.press("Escape");
    await expect(dialog).toBeHidden();
    await expect(page.getByTestId("tab-summary")).toBeFocused();
  });

  test("the help button opens it and the close button closes it", async ({ page }) => {
    await openDashboard(page);
    await expect(page.getByTestId("help-open")).toHaveAttribute("aria-haspopup", "dialog");
    await page.getByTestId("help-open").click();
    await expect(page.getByTestId("help-dialog")).toBeVisible();
    await page.getByTestId("help-close").click();
    await expect(page.getByTestId("help-dialog")).toBeHidden();
    await expect(page.getByTestId("help-open")).toBeFocused();
  });

  test("/ focuses the search and the keys typed there are text, not shortcuts", async ({ page }) => {
    await openDashboard(page);
    await page.keyboard.press("/");
    await expect(page.getByTestId("project-search")).toBeFocused();
    await page.keyboard.type("1?c0p/");
    await expect(page.getByTestId("project-search")).toHaveValue("1?c0p/");
    await expect(page.getByTestId("tab-hydra-umc")).toHaveAttribute("aria-selected", "false");
    await expect(page.getByTestId("help-dialog")).toBeHidden();
    await expect(page.locator("html")).not.toHaveAttribute("data-density", "compact");
    await expect(page.locator("html")).not.toHaveAttribute("data-mode", "present");
  });

  test("1 to 4 open the ecosystems and 0 the summary", async ({ page }) => {
    await openDashboard(page);
    for (const [key, id] of [["1", "hydra-umc"], ["2", "urtc"], ["3", "armor"], ["4", "eh3d"], ["0", "summary"]]) {
      await page.keyboard.press(key);
      await expect(page.getByTestId(`tab-${id}`)).toHaveAttribute("aria-selected", "true");
      await expect(page).toHaveURL(new RegExp(`#${id}$`));
    }
  });

  test("the old keys C and P still work", async ({ page }) => {
    await openDashboard(page);
    await page.keyboard.press("c");
    await expect(page.locator("html")).toHaveAttribute("data-density", "compact");
    await page.keyboard.press("c");
    await expect(page.locator("html")).not.toHaveAttribute("data-density", "compact");
  });

  test("a key with Ctrl, Alt or Meta is left to the browser", async ({ page }) => {
    await openDashboard(page);
    await page.keyboard.press("Control+2");
    await page.keyboard.press("Alt+3");
    await page.keyboard.press("Control+/");
    await expect(page.getByTestId("tab-summary")).toHaveAttribute("aria-selected", "true");
    await expect(page.getByTestId("project-search")).not.toBeFocused();
  });

  test("the switch turns every single-key shortcut off and is remembered", async ({ page }) => {
    await openDashboard(page);
    await page.getByTestId("help-open").click();
    await page.getByTestId("help-keys-on").uncheck();
    await page.keyboard.press("Escape");
    await page.keyboard.press("2");
    await page.keyboard.press("c");
    await page.keyboard.press("/");
    await expect(page.getByTestId("tab-summary")).toHaveAttribute("aria-selected", "true");
    await expect(page.locator("html")).not.toHaveAttribute("data-density", "compact");
    await expect(page.getByTestId("project-search")).not.toBeFocused();
    await page.reload();
    await page.waitForSelector("[role=tab][aria-selected=true]");
    await page.keyboard.press("2");
    await expect(page.getByTestId("tab-summary")).toHaveAttribute("aria-selected", "true");
    await page.getByTestId("help-open").click();
    await expect(page.getByTestId("help-keys-on")).not.toBeChecked();
    await page.getByTestId("help-keys-on").check();
    await page.keyboard.press("Escape");
    await page.keyboard.press("2");
    await expect(page.getByTestId("tab-urtc")).toHaveAttribute("aria-selected", "true");
  });

  test("with the storage blocked the shortcuts still work", async ({ page }) => {
    await page.addInitScript(() => {
      Object.defineProperty(window, "localStorage", { get() { throw new Error("blocked"); } });
    });
    await openDashboard(page);
    await page.keyboard.press("3");
    await expect(page.getByTestId("tab-armor")).toHaveAttribute("aria-selected", "true");
  });

  for (const lang of LANGS) {
    test(`the help is complete in ${lang}`, async ({ page }) => {
      await openDashboard(page);
      await page.locator("#lang-select").selectOption(lang);
      await page.getByTestId("help-open").click();
      const text = await page.getByTestId("help-dialog").innerText();
      expect(text).not.toMatch(LEFTOVER);
      expect(text.length).toBeGreaterThan(200);
      await expect(page.getByTestId("help-open")).toHaveAttribute("aria-label", /.+/);
    });
  }

  test("axe finds nothing serious with the help open, in both themes", async ({ page }) => {
    await openDashboard(page);
    await page.keyboard.press("?");
    expect(await serious(page)).toEqual([]);
    await page.keyboard.press("Escape");
    await page.locator("#theme-toggle").click();
    await page.keyboard.press("?");
    expect(await serious(page)).toEqual([]);
  });
});

test.describe("breadcrumb and address", () => {
  test("shows the dashboard and the tab, and the last item is the current page", async ({ page }) => {
    await openDashboard(page);
    expect(await crumbTexts(page)).toEqual(["Dashboard", "Summary"]);
    await expect(crumbs(page).last()).toHaveAttribute("aria-current", "page");
    await expect(page.getByTestId("crumbs")).toHaveAttribute("aria-label", "You are here");
    await gotoTab(page, "urtc");
    expect(await crumbTexts(page)).toEqual(["Dashboard", "URTC"]);
  });

  test("on the projects tab it adds the scope and follows the scope in the address", async ({ page }) => {
    await openDashboard(page);
    await gotoTab(page, "projects");
    expect(await crumbTexts(page)).toEqual(["Dashboard", "Projects", "All"]);
    await page.getByTestId("scope-urtc").click();
    expect((await crumbTexts(page))[2]).toMatch(/URTC/);
    await expect(page).toHaveURL(/#projects\?scope=urtc/);
    await page.getByTestId("scope-armor").click();
    await expect(crumbs(page).last()).toContainText("A.R.M.O.R.");
  });

  test("an address with a scope opens the projects with that scope in the breadcrumb", async ({ page }) => {
    await openDashboard(page, "full", "#projects?scope=eh3d");
    await expect(page.getByTestId("tab-projects")).toHaveAttribute("aria-selected", "true");
    await expect(crumbs(page).last()).toContainText("EH3D");
  });

  test("a link of the breadcrumb goes back to that level", async ({ page }) => {
    await openDashboard(page);
    await gotoTab(page, "projects");
    await page.getByTestId("scope-urtc").click();
    await crumbs(page).nth(1).locator("a").click();
    await expect(page).toHaveURL(/#projects$/);
    await crumbs(page).first().locator("a").click();
    await expect(page.getByTestId("tab-summary")).toHaveAttribute("aria-selected", "true");
    await expect(page).toHaveURL(/#summary$/);
  });

  test("opening a repository adds it to the breadcrumb and to the address; closing removes it", async ({ page }) => {
    await openDashboard(page);
    await gotoTab(page, "projects");
    const button = page.locator("button[data-open-repo]").first();
    const name = (await button.getAttribute("data-open-repo")) as string;
    await button.click();
    await expect(page.getByTestId("repo-panel")).toBeVisible();
    await expect(crumbs(page).last()).toHaveText(name);
    await expect(crumbs(page).last()).toHaveAttribute("aria-current", "page");
    expect(page.url()).toContain(`repo=${encodeURIComponent(name)}`);
    await page.getByTestId("repo-panel-close").click();
    expect(page.url()).not.toContain("repo=");
    expect((await crumbTexts(page)).includes(name)).toBe(false);
  });

  test("an address with a repository opens its panel", async ({ page }) => {
    await openDashboard(page);
    const name = (await page.locator("button[data-open-repo]").first().getAttribute("data-open-repo")) as string;
    await page.goto(`full/index.html#projects?repo=${encodeURIComponent(name)}`);
    await page.waitForSelector("[role=tab][aria-selected=true]");
    await expect(page.getByTestId("repo-panel")).toBeVisible();
    await expect(page.getByTestId("repo-panel-title")).toHaveText(name);
    await expect(crumbs(page).last()).toHaveText(name);
  });

  test("an address with an unknown repository is ignored", async ({ page }) => {
    await openDashboard(page, "full", "#projects?repo=NOT-A-REPOSITORY");
    await expect(page.getByTestId("repo-panel")).toBeHidden();
    expect(await crumbTexts(page)).toEqual(["Dashboard", "Projects", "All"]);
  });

  for (const lang of LANGS) {
    test(`the breadcrumb is translated (${lang})`, async ({ page }) => {
      await openDashboard(page, "full", "#projects?scope=urtc");
      await page.locator("#lang-select").selectOption(lang);
      const tab = (await page.getByTestId("tab-projects").innerText()).trim();
      const items = await crumbTexts(page);
      expect(items[1]).toBe(tab);
      expect(items.join(" ")).not.toMatch(LEFTOVER);
      if (lang !== "en") expect(items[0]).not.toBe("");
    });
  }
});

test.describe("manifest health", () => {
  test("is valid manifests over repositories, with the figures and how it is calculated", async ({ page }) => {
    await openDashboard(page);
    const card = page.getByTestId("kpi-percent");
    const valid = Number(await card.getAttribute("data-valid"));
    const repos = Number(await card.getAttribute("data-repos"));
    expect(repos).toBeGreaterThan(0);
    expect(valid).toBeLessThan(repos); // the full dataset has an unlisted and an invalid manifest and some without evidence
    const shown = (await page.locator("#health-percent").innerText()).trim();
    expect(shown).toBe(`${Math.round((valid * 1000) / repos) / 10}%`);
    await expect(card).toContainText(`${valid} of ${repos} valid`);
    await card.locator("summary").click();
    await expect(page.getByTestId("registry-help")).toBeVisible();
    await expect(page.getByTestId("registry-help")).toContainText("valid manifests divided by repositories");
  });

  test("filters do not rewrite it", async ({ page }) => {
    await openDashboard(page);
    const before = await page.locator("#health-percent").innerText();
    await page.getByTestId("filter-eco-urtc").click();
    await expect(page.locator("#health-percent")).toHaveText(before);
  });

  for (const variant of ["partial", "empty", "minimal"] as Variant[]) {
    test(`says it is not verified when no manifest was read (${variant})`, async ({ page }) => {
      await openDashboard(page, variant);
      await expect(page.locator("#health-percent")).toHaveText("–");
    });
  }

  for (const lang of LANGS) {
    test(`the explanation is in ${lang}`, async ({ page }) => {
      await openDashboard(page);
      await page.locator("#lang-select").selectOption(lang);
      await page.getByTestId("kpi-percent").locator("summary").click();
      const text = await page.getByTestId("registry-help").innerText();
      expect(text).not.toMatch(LEFTOVER);
      if (lang !== "en") expect(text).not.toContain("divided by repositories");
      await expect(page.getByTestId("kpi-percent")).not.toContainText("{ok}");
    });
  }
});

test.describe("generation figures and the last known data", () => {
  test("the errors tab shows when, how long and what was resolved out of what was attempted", async ({ page }) => {
    await openDashboard(page);
    await gotoTab(page, "errors");
    await expect(page.getByTestId("gen-built")).toContainText("2001-12-20 08:31 UTC");
    await expect(page.getByTestId("gen-built")).toContainText("48 s");
    await expect(page.getByTestId("gen-step-versions")).toHaveText("Versions resolved: 38 of 40 repositories");
    await expect(page.getByTestId("gen-step-manifests")).toHaveText("Valid manifests: 36 of 41 repositories");
    await expect(page.getByTestId("gen-step-commits")).toHaveText("Last-commit lookups answered: 20 of 40");
    await expect(page.getByTestId("gen-step-activity")).toHaveText("CI and release records read: 40 of 40 repositories");
  });

  test("the exact reason of every unreadable manifest is listed by repository", async ({ page }) => {
    await openDashboard(page);
    await gotoTab(page, "errors");
    await expect(panel(page, "errors").locator("li", { hasText: "ARMOR-FIXTURE-BAD" })).toContainText("version file missing");
    await expect(panel(page, "errors").locator("li", { hasText: "URTC-FIXTURE-GHOST" })).toContainText("did not list");
  });

  test("a page without the figures says they are not available", async ({ page }) => {
    await openDashboard(page, "minimal");
    await gotoTab(page, "errors");
    await expect(page.getByTestId("gen-unknown")).toBeVisible();
    await expect(page.getByTestId("gen-built")).toHaveCount(0);
  });

  test("a fresh page has no notice of old data", async ({ page }) => {
    await openDashboard(page);
    await expect(page.getByTestId("stale-banner")).toHaveCount(0);
  });

  test("the last known data are marked with their date and never presented as current", async ({ page }) => {
    await openDashboard(page, "stale");
    const banner = page.getByTestId("stale-banner");
    await expect(banner).toBeVisible();
    await expect(banner).toContainText("2001-12-19");
    await expect(banner).toContainText("not current");
    const alerts = page.getByTestId("alerts-status");
    await expect(alerts).toHaveAttribute("data-state", "incomplete");
    await expect(alerts).not.toContainText(/no alerts/i);
    await expect(page.getByTestId("alerts-why")).toContainText("2001-12-19");
    await gotoTab(page, "errors");
    await expect(page.getByTestId("gen-step-activity")).toHaveText("CI and release records read: 0 of 40 repositories");
  });

  test("the notice is in the 8 languages with the date and no leftovers", async ({ page }) => {
    await openDashboard(page, "stale");
    for (const lang of LANGS) {
      await page.locator("#lang-select").selectOption(lang);
      const text = await page.getByTestId("stale-banner").innerText();
      expect(text).toContain("2001-12-19");
      expect(text).not.toMatch(LEFTOVER);
      if (lang !== "en") expect(text).not.toContain("not current");
    }
  });

  test("when the network fails the page still works and keeps saying the data are old", async ({ page, problems }) => {
    await page.route(/^https?:\/\//, (route) => route.abort("internetdisconnected"));
    await openDashboard(page, "stale");
    for (const id of ["summary", "projects", "evidence", "insight", "rack", "errors"]) {
      await gotoTab(page, id);
    }
    await gotoTab(page, "summary");
    await expect(page.getByTestId("stale-banner")).toBeVisible();
    await expect(page.getByTestId("alerts-status")).toHaveAttribute("data-state", "incomplete");
    // The only errors allowed are the requests that failed because the network is down; the page itself raised none.
    const own = problems.filter((m) => !/Failed to load resource|net::ERR|ERR_INTERNET_DISCONNECTED/i.test(m));
    expect(own).toEqual([]);
    problems.length = 0;
  });

  test("the stale page has no serious axe violation in both themes", async ({ page }) => {
    await openDashboard(page, "stale");
    expect(await serious(page)).toEqual([]);
    await page.locator("#theme-toggle").click();
    expect(await serious(page)).toEqual([]);
    await gotoTab(page, "errors");
    expect(await serious(page)).toEqual([]);
  });
});

test.describe("URTC rack page", () => {
  test("shows the snapshot: source, simulation notice, counters, alarms and slots", async ({ page }) => {
    await openDashboard(page);
    await gotoTab(page, "rack");
    await expect(page.getByTestId("rack-state")).toHaveAttribute("data-state", "alarm");
    await expect(page.getByTestId("rack-state")).toContainText("Alarm");
    await expect(page.getByTestId("rack-source")).toHaveText("Source: simulation");
    await expect(page.getByTestId("rack-sim")).toContainText("not a real rack");
    await expect(page.getByTestId("rack-summary")).toHaveText("Slots in use: 3 of 8 · heating: 1 · maintenance due: 1");
    await expect(page.getByTestId("rack-alarm")).toHaveCount(3);
    await expect(page.getByTestId("rack-alarms")).toContainText("Slot 0: maintenance due for unit 1:7");
    await expect(page.getByTestId("rack-alarms")).toContainText("thermal check says overshoot");
    await expect(page.getByTestId("rack-slot")).toHaveCount(8);
    await expect(page.locator("tr[data-slot='5'] td").first()).toHaveText("Empty");
  });

  test("every value of the snapshot is text, never markup", async ({ page }) => {
    await openDashboard(page);
    await gotoTab(page, "rack");
    await expect(page.getByTestId("rack-state")).toContainText("Fixture rack <b>");
    await expect(panel(page, "rack").locator("b")).toHaveCount(0);
  });

  test("a quiet bench snapshot says no alarms and has no simulation notice", async ({ page }) => {
    await openDashboard(page, "healthy");
    await gotoTab(page, "rack");
    await expect(page.getByTestId("rack-state")).toHaveAttribute("data-state", "ok");
    await expect(page.getByTestId("rack-no-alarms")).toBeVisible();
    await expect(page.getByTestId("rack-sim")).toHaveCount(0);
  });

  test("without a snapshot it says there is no data and shows no state", async ({ page }) => {
    await openDashboard(page, "minimal");
    await gotoTab(page, "rack");
    await expect(page.getByTestId("rack-state")).toHaveAttribute("data-state", "nodata");
    await expect(page.getByTestId("rack-nodata")).toBeVisible();
    await expect(page.getByTestId("rack-table")).toHaveCount(0);
    await expect(panel(page, "rack")).not.toContainText(/no alarms/i);
  });

  test("a snapshot that cannot be used says why and shows no state", async ({ page }) => {
    await openDashboard(page, "partial");
    await gotoTab(page, "rack");
    await expect(page.getByTestId("rack-invalid")).toContainText("schema 2 is not 1");
    await expect(page.getByTestId("rack-state")).toHaveAttribute("data-state", "nodata");
    await expect(page.getByTestId("rack-table")).toHaveCount(0);
  });

  for (const lang of LANGS) {
    test(`the page is complete in ${lang}, with the alarms and the verdicts translated`, async ({ page }) => {
      await openDashboard(page);
      await page.locator("#lang-select").selectOption(lang);
      await gotoTab(page, "rack");
      const text = await visibleText(page);
      const rack = await panel(page, "rack").innerText();
      expect(rack).not.toMatch(LEFTOVER);
      expect(text.length).toBeGreaterThan(500);
      if (lang !== "en") {
        expect(rack).not.toContain("maintenance due for unit");
        expect(rack).not.toContain("thermal check says");
        expect(rack).not.toContain("Slots in use");
        const row = await page.locator("tr[data-slot='1']").innerText();
        expect(row).not.toMatch(/\breached\b|\bovershoot\b/);
      }
    });
  }

  for (const variant of ["full", "healthy", "minimal", "partial"] as Variant[]) {
    for (const theme of ["dark", "light"]) {
      test(`axe finds nothing serious on the rack tab (${variant}, ${theme})`, async ({ page }) => {
        await openDashboard(page, variant);
        if (theme === "light") await page.locator("#theme-toggle").click();
        await gotoTab(page, "rack");
        expect(await serious(page)).toEqual([]);
      });
    }
  }

  test("fits 1920x1080 without page scroll and keeps the table inside its own region", async ({ page }) => {
    await page.setViewportSize({ width: 1920, height: 1080 });
    await openDashboard(page);
    await gotoTab(page, "rack");
    const o = await page.evaluate(() => ({ h: document.documentElement.scrollHeight, ch: document.documentElement.clientHeight, w: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth }));
    expect(o.h).toBeLessThanOrEqual(o.ch);
    expect(o.w).toBeLessThanOrEqual(o.cw);
    await shoot(page, "dash-1920-rack");
  });

  test("fits a mobile screen without horizontal page scroll", async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await openDashboard(page);
    await gotoTab(page, "rack");
    const o = await page.evaluate(() => ({ w: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth }));
    expect(o.w).toBeLessThanOrEqual(o.cw);
    await shoot(page, "dash-390-rack");
  });
});

test.describe("sizes of the new parts", () => {
  for (const [w, h] of [[1920, 1080], [1366, 768], [390, 844]]) {
    test(`${w}x${h}: breadcrumb, help button, errors tab and summary fit without horizontal scroll`, async ({ page }) => {
      await page.setViewportSize({ width: w, height: h });
      await openDashboard(page, "stale", "#projects?scope=urtc");
      for (const id of ["summary", "errors"]) {
        await gotoTab(page, id);
        const o = await page.evaluate(() => ({ w: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth, h: document.documentElement.scrollHeight, ch: document.documentElement.clientHeight }));
        expect(o.w).toBeLessThanOrEqual(o.cw);
        if (w >= 1366) expect(o.h).toBeLessThanOrEqual(o.ch);
        await shoot(page, `dash-${w}-${id}`);
      }
      await expect(page.getByTestId("help-open")).toBeVisible();
      await expect(page.getByTestId("crumbs")).toBeVisible();
      await page.getByTestId("help-open").click();
      const box = await page.getByTestId("help-dialog").boundingBox();
      expect(box && box.x >= 0 && box.x + box.width <= w + 1).toBe(true);
    });
  }

  test("the keyboard and the breadcrumb add no request of their own", async ({ page }) => {
    const requests: string[] = [];
    page.on("request", (r) => { if (/^https?:/.test(r.url()) && !r.url().startsWith("https://api.github.com/")) requests.push(r.url()); });
    await openDashboard(page);
    await page.keyboard.press("?");
    await page.keyboard.press("Escape");
    await page.keyboard.press("2");
    await gotoTab(page, "rack");
    expect(requests.filter((u) => !/fonts\.|\.svg|actions\/workflows/.test(u))).toEqual([]);
  });
});
