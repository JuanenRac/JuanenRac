import AxeBuilder from "@axe-core/playwright";
import { test, expect, openDashboard, gotoTab, LANGS, LEFTOVER, visibleText, Page } from "./helpers";

// Evidence checklist, history of the progress, "since your last visit" and the display modes.
// The fixture page carries the day 2001-12-21; the history holds one snapshot a day before it, with two days missing.

const ITEMS = ["tests", "ci", "release", "signed", "docs", "sim", "hw"];

async function serious(page: Page) {
  const results = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"]).analyze();
  return results.violations.filter((v) => v.impact === "serious" || v.impact === "critical").map((v) => `${v.id}: ${v.nodes.slice(0, 3).map((n) => n.target.join(" ")).join(" | ")}`);
}

test.describe("evidence checklist", () => {
  test("shows a row per repository with a verified, missing, not verified or not applicable state in text and glyph", async ({ page }) => {
    await openDashboard(page);
    await gotoTab(page, "evidence");
    const rows = page.locator("#ev-table tbody tr");
    await expect(rows).toHaveCount(40);
    await expect(page.locator("#ev-matches")).toHaveAttribute("data-shown", "40");
    const first = rows.first().locator("td.ev-cell");
    await expect(first).toHaveCount(ITEMS.length);
    const states = new Set<string>();
    for (const cell of await page.locator("#ev-table td.ev-cell").all()) {
      states.add((await cell.getAttribute("data-status")) || "");
      // never colour alone: a visible glyph and a text for screen readers
      expect((await cell.locator("[aria-hidden=true]").textContent())?.trim()).toMatch(/^[✓✕?–◐]$/);
      expect((await cell.locator(".sr-only").textContent())?.length).toBeGreaterThan(3);
    }
    expect(states.has("yes") && states.has("no") && states.has("unverified")).toBe(true);
  });

  test("a signed release is never shown as verified", async ({ page }) => {
    await openDashboard(page);
    await gotoTab(page, "evidence");
    const signed = await page.locator('#ev-table td[data-item="signed"]').evaluateAll((cells) => cells.map((c) => c.getAttribute("data-status")));
    expect(signed.length).toBe(40);
    expect(signed).not.toContain("yes");
  });

  test("the counters per ecosystem add up to the rows of the table", async ({ page }) => {
    await openDashboard(page);
    await gotoTab(page, "evidence");
    for (const eco of ["hydra-umc", "urtc", "armor", "eh3d"]) {
      const total = await page.locator("#ev-table tbody tr").evaluateAll((trs, e) => trs.filter((tr) => tr.querySelector("td.ev-eco-cell")?.textContent && tr.getAttribute("data-repo")!.toLowerCase().startsWith(e === "hydra-umc" ? "hydra-umc" : e)).length, eco);
      const cell = page.locator(`#ev-counts tr[data-eco="${eco}"] td[data-item="tests"]`);
      const text = (await cell.locator("span").first().textContent()) || "";
      expect(text).toMatch(new RegExp(`^\\d+/${total}$`));
    }
  });

  test("filters by ecosystem and by what is missing, combine, and reset", async ({ page }) => {
    await openDashboard(page);
    await gotoTab(page, "evidence");
    await page.getByTestId("ev-eco-urtc").click();
    await expect(page.locator("#ev-table tbody tr")).toHaveCount(10);
    await expect(page.getByTestId("ev-eco-urtc")).toHaveAttribute("aria-pressed", "true");
    await page.getByTestId("ev-missing-tests").click();
    const n = await page.locator("#ev-table tbody tr").count();
    expect(n).toBeLessThan(10);
    for (const status of await page.locator('#ev-table td[data-item="tests"]').evaluateAll((c) => c.map((x) => x.getAttribute("data-status")))) expect(status).toBe("no");
    await page.getByTestId("ev-missing-ci").click();
    expect(await page.locator("#ev-table tbody tr").count()).toBeLessThanOrEqual(n);
    await page.getByTestId("ev-unverified").click();
    await expect(page.getByTestId("ev-unverified")).toHaveAttribute("aria-pressed", "true");
    await page.getByTestId("ev-reset").click();
    await expect(page.locator("#ev-table tbody tr")).toHaveCount(40);
    await expect(page.getByTestId("ev-eco-all")).toHaveAttribute("aria-pressed", "true");
  });

  test("filters that match nothing say so", async ({ page }) => {
    await openDashboard(page);
    await gotoTab(page, "evidence");
    await page.getByTestId("ev-eco-electro-hobby-3d").click();
    await expect(page.getByTestId("ev-none")).toBeVisible();
    await expect(page.locator("#ev-table tbody tr")).toHaveCount(0);
  });

  test("a repository name opens its side panel with the same checklist", async ({ page }) => {
    await openDashboard(page);
    await gotoTab(page, "evidence");
    const name = (await page.locator("#ev-table tbody tr").first().getAttribute("data-repo"))!;
    const status = await page.locator("#ev-table tbody tr").first().locator('td[data-item="tests"]').getAttribute("data-status");
    await page.locator("#ev-table tbody tr").first().locator("th button").click();
    await expect(page.getByTestId("repo-panel")).toBeVisible();
    await expect(page.getByTestId("repo-panel-title")).toHaveText(name);
    await expect(page.locator("#rp-ev li")).toHaveCount(ITEMS.length);
    await expect(page.locator('#rp-ev li[data-item="tests"] .ev-st')).toHaveClass(new RegExp(`ev-${status}`));
  });

  test("the keyboard reaches the filters and the repository buttons", async ({ page }) => {
    await openDashboard(page);
    await gotoTab(page, "evidence");
    await page.getByTestId("ev-missing-docs").focus();
    await page.keyboard.press("Enter");
    await expect(page.getByTestId("ev-missing-docs")).toHaveAttribute("aria-pressed", "true");
    await page.keyboard.press("Space");
    await expect(page.getByTestId("ev-missing-docs")).toHaveAttribute("aria-pressed", "false");
    await page.locator("#ev-table tbody tr button").first().focus();
    await page.keyboard.press("Enter");
    await expect(page.getByTestId("repo-panel")).toBeVisible();
  });

  test("with no repository data it says so instead of an empty table", async ({ page }) => {
    await openDashboard(page, "empty");
    await gotoTab(page, "evidence");
    await expect(page.getByTestId("ev-no-checks")).toBeVisible();
    await expect(page.locator("#ev-table")).toBeHidden();
  });

  test("no untranslated key in any language", async ({ page }) => {
    await openDashboard(page);
    for (const lang of LANGS) {
      await page.locator("#lang-select").selectOption(lang);
      await gotoTab(page, "evidence");
      expect(await visibleText(page), lang).not.toMatch(LEFTOVER);
    }
    await page.locator("#lang-select").selectOption("pt");
    await expect(page.locator("#ev-title")).toHaveText("Lista de evidências por repositório");
    await page.locator("#lang-select").selectOption("ja");
    await expect(page.locator("#ev-title")).toHaveText("リポジトリ別エビデンスチェックリスト");
  });
});

test.describe("history of the progress", () => {
  test("draws one line per ecosystem, with a table for screen readers and the two periods", async ({ page }) => {
    await openDashboard(page);
    await expect(page.locator("#evo-svg")).toBeVisible();
    await expect(page.locator("#evo-svg path.evo-line")).toHaveCount(4 * 2);       // two days are missing: each line has a gap, so two segments
    await expect(page.locator("#evo-svg")).toHaveAttribute("aria-label", /2001-12-21/);
    const rows = page.locator("#evo-table tbody tr");
    expect(await rows.count()).toBe(44);
    await expect(page.getByTestId("evo-count")).toContainText("44");
    await page.getByTestId("evo-30").click();
    await expect(page.getByTestId("evo-30")).toHaveAttribute("aria-pressed", "true");
    expect(await page.locator("#evo-table tbody tr").count()).toBeLessThan(44);
    await expect(page.locator("#evo-table tbody tr").last().locator("th")).toHaveText("2001-12-21");
  });

  test("a day without snapshot is not filled in", async ({ page }) => {
    await openDashboard(page);
    const dates = await page.locator("#evo-table tbody th").allTextContents();
    expect(dates).not.toContain("2001-11-30");     // 21 days before the fixture day
    expect(dates).not.toContain("2001-12-01");
    expect(dates).toContain("2001-11-29");
  });

  test("a measure of one area changes the lines and an unknown value is not drawn as a number", async ({ page }) => {
    await openDashboard(page);
    await page.getByTestId("evo-metric").selectOption("ci");
    await expect(page.locator("#evo-table tbody")).toContainText("not verified");
    await expect(page.locator("#evo-svg")).toBeVisible();
  });

  test("with a single snapshot no line is drawn and the page says why", async ({ page }) => {
    await openDashboard(page, "single");
    await expect(page.locator("#evo-svg")).toBeHidden();
    await expect(page.getByTestId("evo-msg")).toContainText("2001-12-21");
    await expect(page.getByTestId("evo-msg")).toContainText("two are needed");
  });

  test("with no history at all it says so", async ({ page }) => {
    await openDashboard(page, "minimal");
    await expect(page.locator("#evo-svg")).toBeHidden();
    await expect(page.getByTestId("evo-msg")).toContainText("No history has been saved yet");
  });

  test("the lines are drawn with motion only when it is allowed", async ({ page }) => {
    await openDashboard(page);
    const reduced = await page.locator("#evo-svg path.evo-line").first().evaluate((el) => getComputedStyle(el).animationName);
    expect(reduced).toBe("none");
    await page.emulateMedia({ reducedMotion: "no-preference" });
    const allowed = await page.locator("#evo-svg path.evo-line").first().evaluate((el) => getComputedStyle(el).animationName);
    expect(allowed).toBe("evo-draw");
  });

  test("texts in every language", async ({ page }) => {
    await openDashboard(page);
    for (const lang of LANGS) {
      await page.locator("#lang-select").selectOption(lang);
      expect(await visibleText(page), lang).not.toMatch(LEFTOVER);
      expect(await page.locator("#evo-svg").getAttribute("aria-label"), lang).not.toMatch(/\{[a-z]+\}/);
    }
  });
});

test.describe("since your last visit", () => {
  const previous = (value: number) => ({ visited: "2001-12-01", values: { "urtc|overall": value, "armor|overall": 54 } });

  test("lists what changed with the old and the new value", async ({ page }) => {
    await page.addInitScript((data) => { try { if (!sessionStorage.getItem("seeded")) { localStorage.setItem("hydra-dashboard-visit", JSON.stringify(data)); sessionStorage.setItem("seeded", "1"); } } catch (e) { /* none */ } }, previous(40));
    await openDashboard(page);
    await expect(page.getByTestId("visit-card")).toBeVisible();
    await expect(page.getByTestId("visit-since")).toContainText("2001-12-01");
    await expect(page.getByTestId("visit-list")).toContainText("URTC");
    await expect(page.getByTestId("visit-list")).toContainText("40% → 47% (+7)");
    await expect(page.getByTestId("visit-list")).not.toContainText("A.R.M.O.R.");
    // it stays for the whole session, also after a reload
    await page.reload();
    await expect(page.getByTestId("visit-list")).toContainText("40% → 47%");
    await page.getByTestId("visit-dismiss").click();
    await expect(page.getByTestId("visit-card")).toBeHidden();
  });

  test("says nothing changed when nothing did", async ({ page }) => {
    await page.addInitScript((data) => { localStorage.setItem("hydra-dashboard-visit", JSON.stringify(data)); }, previous(47));
    await openDashboard(page);
    await expect(page.getByTestId("visit-card")).toBeVisible();
    await expect(page.getByTestId("visit-none")).toBeVisible();
    await expect(page.getByTestId("visit-list")).toBeEmpty();
  });

  test("is not shown on a first visit, and the visit is remembered for the next one", async ({ page }) => {
    await openDashboard(page);
    await expect(page.getByTestId("visit-card")).toBeHidden();
    const stored = await page.evaluate(() => JSON.parse(localStorage.getItem("hydra-dashboard-visit") || "null"));
    expect(stored.values["urtc|overall"]).toBe(47);
  });

  test("is not shown, and nothing breaks, when the browser blocks the storage", async ({ page }) => {
    await page.addInitScript(() => {
      const fail = () => { throw new Error("blocked"); };
      Object.defineProperty(window, "localStorage", { get: fail });
      Object.defineProperty(window, "sessionStorage", { get: fail });
    });
    await openDashboard(page);
    await expect(page.getByTestId("visit-card")).toBeHidden();
    await expect(page.locator("#evo-svg")).toBeVisible();
  });

  test("a damaged stored visit is ignored", async ({ page }) => {
    await page.addInitScript(() => { localStorage.setItem("hydra-dashboard-visit", "{broken"); });
    await openDashboard(page);
    await expect(page.getByTestId("visit-card")).toBeHidden();
  });
});

test.describe("display modes", () => {
  test("compact mode is a denser layout of the same content, kept in the address and in the storage", async ({ page }) => {
    await openDashboard(page);
    const before = await page.locator(".card").first().evaluate((el) => el.getBoundingClientRect().height);
    await page.getByTestId("mode-compact").click();
    await expect(page.locator("html")).toHaveAttribute("data-density", "compact");
    await expect(page.getByTestId("mode-compact")).toHaveAttribute("aria-pressed", "true");
    expect(await page.locator(".card").first().evaluate((el) => el.getBoundingClientRect().height)).toBeLessThanOrEqual(before);
    expect(page.url()).toContain("view=compact");
    await page.reload();
    await expect(page.locator("html")).toHaveAttribute("data-density", "compact");
    await page.keyboard.press("c");
    await expect(page.locator("html")).not.toHaveAttribute("data-density", "compact");
  });

  test("presentation mode hides the side panel, enlarges the text, has a shortcut and Escape leaves it", async ({ page }) => {
    await openDashboard(page);
    await expect(page.locator(".sidebar")).toBeVisible();
    await page.getByTestId("mode-present").click();
    await expect(page.locator("html")).toHaveAttribute("data-mode", "present");
    await expect(page.locator(".sidebar")).toBeHidden();
    await expect(page.getByTestId("mode-present")).toContainText("Exit presentation");
    expect(page.url()).toContain("mode=present");
    expect(await page.locator("main.content").evaluate((el) => getComputedStyle(el).zoom)).not.toBe("1");
    await page.keyboard.press("Escape");
    await expect(page.locator("html")).not.toHaveAttribute("data-mode", "present");
    await expect(page.locator(".sidebar")).toBeVisible();
    await page.keyboard.press("p");
    await expect(page.locator("html")).toHaveAttribute("data-mode", "present");
    await page.keyboard.press("p");
    await expect(page.locator("html")).not.toHaveAttribute("data-mode", "present");
  });

  test("the address opens the page in presentation mode", async ({ page }) => {
    await openDashboard(page, "full", "#summary?mode=present");
    await expect(page.locator("html")).toHaveAttribute("data-mode", "present");
  });

  test("the shortcuts are ignored while typing", async ({ page }) => {
    await openDashboard(page);
    await page.getByTestId("project-search").focus();
    await page.keyboard.type("cp");
    await expect(page.locator("html")).not.toHaveAttribute("data-density", "compact");
    await expect(page.locator("html")).not.toHaveAttribute("data-mode", "present");
    await expect(page.getByTestId("project-search")).toHaveValue("cp");
  });

  test("the modes work with the storage blocked", async ({ page }) => {
    await page.addInitScript(() => { Object.defineProperty(window, "localStorage", { get() { throw new Error("blocked"); } }); });
    await openDashboard(page);
    await page.getByTestId("mode-compact").click();
    await expect(page.locator("html")).toHaveAttribute("data-density", "compact");
  });

  test("print media shows a clean report: no controls, a title, the data date and every report tab", async ({ page }) => {
    await openDashboard(page);
    await page.emulateMedia({ media: "print" });
    await expect(page.getByTestId("print-head")).toBeVisible();
    await expect(page.locator("#print-data")).toHaveText("Data of 2001-12-21");
    await expect(page.locator("#print-when")).toContainText("Printed on");
    for (const hidden of [".sidebar", ".tabs", ".top-actions", ".app-footer", "#panel-projects"]) await expect(page.locator(hidden).first()).toBeHidden();
    for (const shown of ["summary", "hydra-umc", "urtc", "armor", "eh3d", "evidence", "errors"]) await expect(page.locator(`#panel-${shown}`)).toBeVisible();
    expect(await page.evaluate(() => getComputedStyle(document.body).backgroundColor)).toBe("rgb(255, 255, 255)");
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    expect(overflow).toBeLessThanOrEqual(1);
  });

  test("print date says not verified when the data have no date", async ({ page }) => {
    await openDashboard(page, "minimal");
    await page.emulateMedia({ media: "print" });
    await expect(page.locator("#print-data")).toHaveText("Date of the data: not verified");
  });

  test("the print button asks the browser to print", async ({ page }) => {
    await openDashboard(page);
    await page.evaluate(() => { (window as any).__printed = 0; window.print = () => { (window as any).__printed += 1; }; });
    await page.getByTestId("mode-print").click();
    expect(await page.evaluate(() => (window as any).__printed)).toBe(1);
  });

  test("the mode buttons are in every language", async ({ page }) => {
    await openDashboard(page);
    for (const lang of LANGS) {
      await page.locator("#lang-select").selectOption(lang);
      expect(await visibleText(page), lang).not.toMatch(LEFTOVER);
    }
    await page.locator("#lang-select").selectOption("pt");
    await expect(page.getByTestId("mode-present")).toHaveText("Apresentação");
  });
});

test.describe("page metadata", () => {
  test("has its own icon and the Open Graph and Twitter cards", async ({ page }) => {
    await openDashboard(page);
    expect(await page.locator('link[rel="icon"]').getAttribute("href")).toMatch(/^data:image\/svg\+xml,/);
    for (const property of ["og:title", "og:description", "og:image", "og:url", "og:type"]) expect(await page.locator(`meta[property="${property}"]`).getAttribute("content"), property).toBeTruthy();
    expect(await page.locator('meta[property="og:image"]').getAttribute("content")).toMatch(/^https:\/\/juanenrac\.github\.io\/JuanenRac\/og-image\.png$/);
    expect(await page.locator('meta[name="twitter:card"]').getAttribute("content")).toBe("summary_large_image");
  });
});

for (const theme of ["dark", "light"]) {
  test(`axe finds no serious violation in the new views (${theme})`, async ({ page }) => {
    test.setTimeout(120_000);
    await openDashboard(page);
    if (theme === "light") await page.locator("#theme-toggle").click();
    const found: string[] = [];
    found.push(...(await serious(page)).map((x) => `summary: ${x}`));
    await gotoTab(page, "evidence");
    found.push(...(await serious(page)).map((x) => `evidence: ${x}`));
    await page.getByTestId("ev-missing-tests").click();
    found.push(...(await serious(page)).map((x) => `filtered: ${x}`));
    await page.locator("#ev-table tbody tr button").first().click();
    found.push(...(await serious(page)).map((x) => `panel: ${x}`));
    await page.keyboard.press("Escape");
    await page.getByTestId("mode-compact").click();
    found.push(...(await serious(page)).map((x) => `compact: ${x}`));
    await page.getByTestId("mode-compact").click();
    await page.getByTestId("mode-present").click();
    found.push(...(await serious(page)).map((x) => `present: ${x}`));
    expect(found).toEqual([]);
  });
}

test.describe("screen sizes", () => {
  for (const [name, width, height] of [["1920x1080", 1920, 1080], ["1366x768", 1366, 768], ["mobile", 390, 844]] as const) {
    test(`${name}: nothing overflows the page and the new views fit`, async ({ page }) => {
      await page.setViewportSize({ width, height });
      await openDashboard(page);
      await gotoTab(page, "evidence");
      expect(await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth), "horizontal scroll").toBeLessThanOrEqual(1);
      if (width > 800) expect(await page.evaluate(() => document.documentElement.scrollHeight - document.documentElement.clientHeight), "page scroll").toBeLessThanOrEqual(1);
      await expect(page.locator("#evidence-view")).toBeVisible();
      await gotoTab(page, "summary");
      await expect(page.locator("#evo-card")).toBeAttached();
      expect(await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth)).toBeLessThanOrEqual(1);
      await page.getByTestId("mode-present").isVisible().then(async (visible) => {
        if (!visible) return;
        await page.keyboard.press("p");
        expect(await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth), "present").toBeLessThanOrEqual(1);
      });
    });
  }
});
