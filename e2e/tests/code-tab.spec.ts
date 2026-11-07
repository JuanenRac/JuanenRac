import { test, expect, openDashboard, gotoTab, LANGS, LEFTOVER, visibleText, Variant } from "./helpers";
import type { Page } from "@playwright/test";

// The tab "Code": lines of code, tests and documentation per repository, ecosystem and type, counted once a day (data/code-stats.json) and embedded in the page.
// Fixture (full): 40 repositories in 4 ecosystems and 5 types, 39 measured (3 of them last known figures) and 1 not measured, two languages in each repository
// (5 main ones plus Shell), a history of 46 days and tests declared by 14 repositories.

async function open(page: Page, variant: Variant = "full") {
  await openDashboard(page, variant);
  await gotoTab(page, "code");
}

const number = (text: string | null) => Number((text || "").replace(/[^\d]/g, ""));

test.describe("code tab: figures", () => {
  test("the tab sits after Tests and shows the title, the badge and ten figures", async ({ page }) => {
    await open(page);
    const ids = await page.locator("[role=tab]").evaluateAll((tabs) => tabs.map((t) => t.getAttribute("data-testid")));
    expect(ids.indexOf("tab-code")).toBe(ids.indexOf("tab-tests") + 1);
    await expect(page.getByTestId("tab-code")).toHaveText("Code");
    await expect(page.locator("#cd-title")).toHaveText("Code statistics");
    await expect(page.getByTestId("cd-badge")).toHaveText("Counted on shallow clones");
    await expect(page.getByTestId("cd-kpis").locator("li")).toHaveCount(10);
    await expect(page.getByTestId("cd-k-repos").locator("b")).toHaveText("39 / 40");
    await expect(page.getByTestId("cd-note")).toContainText("3 repositories");
    await expect(page.getByTestId("cd-note")).toContainText("Not measured");
    await expect(page.getByTestId("cd-stale")).toBeHidden();
  });

  test("the totals of the figures are the totals of the table", async ({ page }) => {
    await open(page);
    const total = page.getByTestId("cd-total").locator("td");
    const heads = await page.locator("#cd-table thead th").allInnerTexts();
    const at = (name: string) => heads.findIndex((h) => h.replace(/[↑↓]/g, "").trim() === name) - 1;
    const code = number(await total.nth(at("Code")).textContent());
    expect(code).toBeGreaterThan(0);
    expect(number(await page.getByTestId("cd-k-code").locator("b").textContent())).toBe(code);
    expect(number(await page.getByTestId("cd-k-tests").locator("b").textContent())).toBe(number(await total.nth(at("Test lines")).textContent()));
    expect(number(await page.getByTestId("cd-k-docs").locator("b").textContent())).toBe(number(await total.nth(at("Documentation")).textContent()));
  });

  test("the help says what is counted and what is left out", async ({ page }) => {
    await open(page);
    await page.getByTestId("cd-help").locator("summary").click();
    await expect(page.getByTestId("cd-help-body")).toContainText("depth 1");
    await expect(page.getByTestId("cd-help-body")).toContainText("linguist-generated");
    await expect(page.getByTestId("cd-help-body")).toContainText("code-stats-config.json");
    await expect(page.getByTestId("cd-help-body")).not.toContainText("{");
  });
});

test.describe("code tab: charts", () => {
  test("stacked bars of code, tests and documentation: the whole, each ecosystem and each type", async ({ page }) => {
    await open(page);
    const rows = page.getByTestId("cd-prop-svg").locator("g[data-row]");
    await expect(rows).toHaveCount(1 + 4 + 5);
    await expect(rows.first().locator(".cd-seg")).toHaveCount(3);
    for (const kind of ["code", "tests", "docs"]) await expect(rows.first().locator(`.cd-seg[data-kind=${kind}]`)).toHaveCount(1);
    const values = await rows.first().locator(".cd-seg").evaluateAll((els) => els.map((e) => Number(e.getAttribute("data-value"))));
    expect(values.every((v) => v > 0)).toBe(true);
    const widths = await rows.first().locator(".cd-seg rect").evaluateAll((els) => els.map((e) => e.getBoundingClientRect().width));
    expect(widths[0]).toBeGreaterThan(widths[2]);
    expect(await page.getByTestId("cd-prop-legend").locator("li").allInnerTexts()).toEqual(["Code", "Tests", "Documentation"]);
    await expect(page.getByTestId("cd-prop-table").locator("tbody tr")).toHaveCount(10);
  });

  test("the value is in a tooltip on hover and on keyboard focus, and in the name of the element", async ({ page }) => {
    await open(page);
    const seg = page.getByTestId("cd-prop-svg").locator(".cd-seg[data-kind=code]").first();
    const label = (await seg.getAttribute("aria-label")) || "";
    expect(label).toMatch(/lines of code .*of tests .*of documentation/);
    await seg.hover();
    await expect(page.getByTestId("cd-tip")).toBeVisible();
    await expect(page.getByTestId("cd-tip")).toHaveText(label);
    await page.mouse.move(2, 2);
    await expect(page.getByTestId("cd-tip")).toBeHidden();
    await seg.focus();
    await expect(page.getByTestId("cd-tip")).toHaveText(label);
    await page.keyboard.press("Escape");
    await expect(page.getByTestId("cd-tip")).toBeHidden();
  });

  test("languages: global bars, one stacked bar per ecosystem and a legend with the same names", async ({ page }) => {
    await open(page);
    const names = await page.getByTestId("cd-lang-global-svg").locator(".cd-seg").evaluateAll((els) => els.map((e) => e.getAttribute("data-lang")));
    expect([...names].sort()).toEqual(["C++", "Kotlin", "Python", "Rust", "Shell", "TypeScript"]);
    expect((await page.getByTestId("cd-lang-legend").locator("li").allInnerTexts()).sort()).toEqual([...names].sort());
    const ecoRows = await page.getByTestId("cd-lang-eco-svg").locator(".cd-seg").evaluateAll((els) => new Set(els.map((e) => e.getAttribute("data-eco"))).size);
    expect(ecoRows).toBe(4);
    await expect(page.getByTestId("cd-lang-table").locator("tbody tr")).toHaveCount(6);
    const first = await page.getByTestId("cd-lang-global-svg").locator(".cd-seg").evaluateAll((els) => els.map((e) => Number(e.getAttribute("data-value"))));
    expect(first).toEqual([...first].sort((a, b) => b - a));
  });

  test("evolution: three lines for the whole and one per ecosystem, with the kind of line chosen by buttons", async ({ page }) => {
    await open(page);
    await expect(page.getByTestId("cd-evo-wrap")).toBeVisible();
    await expect(page.getByTestId("cd-evo-total-svg").locator("path.cd-line")).toHaveCount(3);
    await expect(page.getByTestId("cd-evo-eco-svg").locator("path.cd-line")).toHaveCount(4);
    await expect(page.getByTestId("cd-evo-total-svg")).toHaveAttribute("aria-label", /from 2001-11-06 to 2001-12-21/);
    await expect(page.getByTestId("cd-metric-code")).toHaveAttribute("aria-pressed", "true");
    await page.getByTestId("cd-metric-tests").click();
    await expect(page.getByTestId("cd-metric-tests")).toHaveAttribute("aria-pressed", "true");
    await expect(page.getByTestId("cd-evo-eco-svg")).toHaveAttribute("aria-label", /Line chart of Tests/);
    await expect(page.getByTestId("cd-evo-table").locator("tbody tr")).toHaveCount(46);
    const last = page.getByTestId("cd-evo-total-svg").locator(".cd-mark[data-series=code]").last();
    await last.focus();
    await expect(page.getByTestId("cd-tip")).toContainText("Code on 2001-12-21");
    const path = await page.getByTestId("cd-evo-total-svg").locator("path.cd-line[data-series=code]").getAttribute("d");
    expect((path || "").split("L").length).toBeGreaterThan(40);
  });

  test("the largest repositories: stacked bars, sorted, with the number chosen", async ({ page }) => {
    await open(page);
    await expect(page.getByTestId("cd-top-svg").locator("g[data-repo]")).toHaveCount(20);
    await page.getByTestId("cd-top-n").selectOption("10");
    const rows = page.getByTestId("cd-top-svg").locator("g[data-repo]");
    await expect(rows).toHaveCount(10);
    const sums = await rows.evaluateAll((els) => els.map((g) => Array.from(g.querySelectorAll(".cd-seg")).reduce((a, s) => a + Number(s.getAttribute("data-value")), 0)));
    expect(sums).toEqual([...sums].sort((a, b) => b - a));
    await expect(page.getByTestId("cd-top-table").locator("tbody tr")).toHaveCount(10);
    await expect(page.getByTestId("cd-top-svg")).toHaveAttribute("aria-label", /10 repositories/);
  });

  test("every chart is drawn with data, has size on the screen and can be captured", async ({ page }, info) => {
    await open(page);
    for (const id of ["cd-prop-chart", "cd-lang-global", "cd-lang-eco", "cd-evo-total", "cd-evo-eco", "cd-top-chart"]) {
      const chart = page.getByTestId(id);
      await chart.scrollIntoViewIfNeeded();
      const box = await chart.boundingBox();
      expect(box, id).not.toBeNull();
      expect(box!.width, id).toBeGreaterThan(200);
      expect(box!.height, id).toBeGreaterThan(80);
      expect(await chart.locator("rect, path, circle, polygon").count(), id).toBeGreaterThan(3);
      const picture = await chart.screenshot();
      expect(picture.length, id).toBeGreaterThan(2500);
      await info.attach(`code-${id}.png`, { body: picture, contentType: "image/png" });
    }
  });
});

test.describe("code tab: the table", () => {
  test("one row per repository, the biggest code first, and the not measured one says so", async ({ page }) => {
    await open(page);
    await expect(page.locator("#cd-table tbody tr")).toHaveCount(40);
    const codes = await page.locator("#cd-table tbody tr:not([data-state=unread])").evaluateAll((els) => els.map((e) => Number(e.getAttribute("data-code"))));
    expect(codes).toEqual([...codes].sort((a, b) => b - a));
    await expect(page.locator("#cd-table tbody tr[data-state=unread]")).toHaveCount(1);
    await expect(page.locator("#cd-table tbody tr[data-state=unread]")).toContainText("Not measured");
    await expect(page.locator("#cd-table tbody tr[data-state=lastknown]").first()).toContainText("Last known");
    await expect(page.getByTestId("cd-matches")).toHaveAttribute("data-shown", "40");
  });

  test("a column heading sorts and says so, and a second click reverses it", async ({ page }) => {
    await open(page);
    await page.getByTestId("cd-sort-name").click();
    await expect(page.locator("#cd-table th[aria-sort=ascending]")).toHaveCount(1);
    const names = await page.locator("#cd-table tbody tr:not([data-state=unread]) .cd-name-btn").allInnerTexts();
    expect(names).toEqual([...names].sort((a, b) => a.toLowerCase().localeCompare(b.toLowerCase())));
    await expect(page.getByTestId("cd-live")).toContainText("Sorted by Repository, ascending");
    await page.getByTestId("cd-sort-name").click();
    await expect(page.locator("#cd-table th[aria-sort=descending]")).toHaveCount(1);
    await expect(page.getByTestId("cd-sort-name")).toBeFocused();
  });

  test("filters by ecosystem and type, search by name, and the total follows the rows", async ({ page }) => {
    await open(page);
    await page.getByTestId("cd-eco-urtc").click();
    await expect(page.getByTestId("cd-matches")).toHaveAttribute("data-shown", "10");
    await expect(page.getByTestId("cd-eco-urtc")).toHaveAttribute("aria-pressed", "true");
    await page.getByTestId("cd-type-firmware").click();
    await expect(page.getByTestId("cd-matches")).toHaveAttribute("data-shown", "2");
    await page.getByTestId("cd-eco-all").click();
    await page.getByTestId("cd-type-all").click();
    const allCode = number(await page.getByTestId("cd-k-code").locator("b").textContent());
    await page.getByTestId("cd-search").fill("fixture-03");
    await expect(page.getByTestId("cd-matches")).toHaveAttribute("data-shown", "4");
    await expect(page.locator("#cd-table tbody tr")).toHaveCount(4);
    const rowCodes = await page.locator("#cd-table tbody tr").evaluateAll((els) => els.map((e) => Number(e.getAttribute("data-code"))));
    const sum = rowCodes.reduce((a, b) => a + b, 0);
    expect(sum).toBeGreaterThan(0);
    expect(sum).toBeLessThan(allCode);
    expect(number(await page.getByTestId("cd-k-code").locator("b").textContent())).toBe(allCode);
    await page.getByTestId("cd-search").fill("zzzz-nothing");
    await expect(page.getByTestId("cd-none")).toBeVisible();
    await expect(page.getByTestId("cd-none")).toHaveText("No row matches the filters.");
  });

  test("the rows can be grouped by ecosystem and by type, and the groups add up to the total", async ({ page }) => {
    await open(page);
    await page.getByTestId("cd-group").selectOption("eco");
    await expect(page.locator("#cd-table tbody tr")).toHaveCount(4);
    await expect(page.locator("#cd-table thead th").first()).toContainText("Ecosystem");
    const groups = await page.locator("#cd-table tbody tr").evaluateAll((els) => els.map((e) => Number(e.getAttribute("data-code"))));
    expect(groups.reduce((a, b) => a + b, 0)).toBe(number(await page.getByTestId("cd-k-code").locator("b").textContent()));
    await page.getByTestId("cd-group").selectOption("type");
    await expect(page.locator("#cd-table tbody tr")).toHaveCount(5);
  });

  test("the name of a repository opens its panel", async ({ page }) => {
    await open(page);
    await page.locator("#cd-table .cd-name-btn").first().click();
    await expect(page.locator("#repo-panel")).toBeVisible();
  });
});

test.describe("code tab: languages and states", () => {
  for (const lang of LANGS) {
    test(`${lang}: the tab, its charts and its table are translated and show no leftovers`, async ({ page }) => {
      await open(page);
      await page.locator("#lang-select").selectOption(lang);
      const title = await page.locator("#cd-title").innerText();
      if (lang !== "en") expect(title).not.toBe("Code statistics");
      if (lang === "es") expect(title).toBe("Estadísticas de código");
      if (lang === "pt") expect(title).toBe("Estatísticas de código");
      for (const id of ["cd-prop-svg", "cd-lang-global-svg", "cd-evo-total-svg", "cd-top-svg"]) {
        const label = (await page.getByTestId(id).getAttribute("aria-label")) || "";
        expect(label, `${lang} ${id}`).not.toMatch(/\{|\}|undefined/);
        if (lang !== "en") expect(label, `${lang} ${id}`).not.toMatch(/the table below has the same figures/);
      }
      const tip = (await page.getByTestId("cd-prop-svg").locator(".cd-seg").first().getAttribute("aria-label")) || "";
      expect(tip).not.toMatch(/\{|\}|undefined/);
      const heads = await page.locator("#cd-table thead th").allInnerTexts();
      expect(heads.length).toBeGreaterThan(10);
      if (["es", "fr", "ja", "zh", "pt"].includes(lang)) expect(heads.join(" ")).not.toContain("Repository");
      expect(await visibleText(page)).not.toMatch(/\{[a-z]+\}/);
      expect(await page.locator("#panel-code").innerText()).not.toMatch(LEFTOVER);
    });
  }

  test("the charts follow the theme", async ({ page }) => {
    await open(page);
    const fill = () => page.getByTestId("cd-prop-svg").locator(".cd-seg[data-kind=code] rect").first().evaluate((e) => getComputedStyle(e).fill);
    const dark = await fill();
    await page.locator("#theme-toggle").click();
    await expect(page.locator("html")).toHaveAttribute("data-theme", "light");
    expect(await fill()).not.toBe(dark);
    await expect(page.getByTestId("cd-table")).toBeVisible();
  });

  test("a stale document says how old it is", async ({ page }) => {
    await open(page, "stale");
    await expect(page.getByTestId("cd-stale")).toBeVisible();
    await expect(page.getByTestId("cd-stale")).toHaveText("These figures are 4 days old (counted on 2001-12-17).");
  });

  test("one day of history cannot draw a line and says so", async ({ page }) => {
    await open(page, "single");
    await expect(page.getByTestId("cd-evo-msg")).toBeVisible();
    await expect(page.getByTestId("cd-evo-msg")).toContainText("Only one day is recorded so far (2001-12-21)");
    await expect(page.getByTestId("cd-evo-wrap")).toBeHidden();
    await expect(page.getByTestId("cd-prop-svg")).toBeVisible();
  });

  for (const variant of ["minimal", "partial", "empty"] as const) {
    test(`${variant}: no figures means "not verified", never zeros`, async ({ page }) => {
      await open(page, variant);
      await expect(page.getByTestId("cd-not-read")).toBeVisible();
      await expect(page.getByTestId("cd-not-read")).toHaveText("No code statistics could be read in this build, so nothing is verified.");
      await expect(page.getByTestId("cd-body")).toBeHidden();
    });
  }

  test("the healthy variant shows the tab without a note about old figures", async ({ page }) => {
    await open(page, "healthy");
    await expect(page.getByTestId("cd-stale")).toBeHidden();
    await expect(page.getByTestId("cd-prop-svg")).toBeVisible();
  });
});
