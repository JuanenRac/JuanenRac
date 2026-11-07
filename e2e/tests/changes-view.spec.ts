import * as fs from "fs";
import AxeBuilder from "@axe-core/playwright";
import type { Page } from "@playwright/test";
import { test, expect, openDashboard, gotoTab, LANGS, LEFTOVER, visibleText, Variant } from "./helpers";

// The "Changelog" tab: statistics of the CHANGELOG of every repository (versions, entries, the kind of each entry decided by words) and the pace of
// the tags. Fixture (full): 40 repositories, 36 of them with a changelog that was measured (one has no changelog in each twelve, one was not measured), a history
// of 46 days, the text of the entries kept for the newest five versions, and tags for nine in ten repositories.

async function open(page: Page, variant: Variant = "full") {
  await openDashboard(page, variant);
  await gotoTab(page, "changelog");
}

const number = (text: string | null) => Number((text || "").replace(/[^\d]/g, ""));
const kpi = (page: Page, name: string) => page.getByTestId(`ch-k-${name}`).locator("b");

test.describe("changes view: switching and figures", () => {
  test("the changelog statistics are a tab of their own, next to the code one", async ({ page }) => {
    await openDashboard(page);
    const ids = await page.locator('[role="tab"]').evaluateAll((els) => els.map((e) => e.id));
    expect(ids.indexOf("tab-changelog")).toBe(ids.indexOf("tab-code") + 1);
    await gotoTab(page, "code");
    await expect(page.getByTestId("cd-body")).toBeVisible();
    await expect(page.getByTestId("ch-body")).toBeHidden();
    await expect(page.getByTestId("cd-views")).toHaveCount(0);
    await gotoTab(page, "changelog");
    await expect(page.getByTestId("ch-body")).toBeVisible();
    await expect(page.getByTestId("cd-body")).toBeHidden();
    await expect(page.locator("#ch-title")).toHaveText("Changelog statistics");
  });

  test("nine figures, with the repositories that have a changelog and the share of what could not be classified", async ({ page }) => {
    await open(page);
    await expect(page.getByTestId("ch-kpis").locator("li")).toHaveCount(9);
    await expect(kpi(page, "repos")).toHaveText("36");
    expect(number(await kpi(page, "versions").textContent())).toBeGreaterThan(0);
    expect(number(await kpi(page, "entries").textContent())).toBeGreaterThan(number(await kpi(page, "unreleased").textContent()));
    await expect(kpi(page, "fix")).toContainText("%");
    await expect(kpi(page, "unclassified")).toContainText("%");
    const entries = number(await kpi(page, "entries").textContent());
    const versions = number(await kpi(page, "versions").textContent());
    const avg = Number((await kpi(page, "avg").textContent())!.replace(",", "."));
    expect(Math.abs(avg - entries / versions)).toBeLessThan(0.06);
    expect(number(await kpi(page, "d90").textContent())).toBeGreaterThanOrEqual(number(await kpi(page, "d30").textContent()));
  });

  test("the help says how entries are classified and how many stay unclassified", async ({ page }) => {
    await open(page);
    await page.getByTestId("ch-help").locator("summary").click();
    await expect(page.getByTestId("ch-help-body")).toContainText("[Unreleased]");
    await expect(page.getByTestId("ch-help-body")).toContainText("unclassified");
    await expect(page.getByTestId("ch-help-body")).toContainText("tags of GitHub");
    await expect(page.getByTestId("ch-help-body")).not.toContainText("{");
  });
});

test.describe("changes view: charts", () => {
  test("the donut has one slice and one legend line per kind, and its figures are the entries of the kpis", async ({ page }) => {
    await open(page);
    const legend = page.getByTestId("ch-donut-legend").locator("li");
    await expect(legend).toHaveCount(11);
    const values = await legend.evaluateAll((els) => els.map((e) => Number(e.getAttribute("data-value"))));
    const published = number(await kpi(page, "entries").textContent());
    const waiting = number(await kpi(page, "unreleased").textContent());
    expect(values.reduce((a, b) => a + b, 0)).toBe(published + waiting);
    const slices = await page.getByTestId("ch-donut-svg").locator(".cd-seg").evaluateAll((els) => els.map((e) => Number(e.getAttribute("data-value"))));
    expect(slices).toEqual(values.filter((v) => v > 0));
    await expect(page.getByTestId("ch-donut-svg").locator("text.ch-donut-total")).toHaveText(String(published + waiting).replace(/\B(?=(\d{3})+$)/g, ","));
    await expect(page.getByTestId("ch-donut-table").locator("tbody tr")).toHaveCount(11);
    await expect(legend.last()).toContainText("Unclassified");
  });

  test("a slice shows its value on hover and on focus and is named for assistive technology", async ({ page }) => {
    await open(page);
    const slice = page.getByTestId("ch-donut-svg").locator(".cd-seg").first();
    const label = (await slice.getAttribute("aria-label")) || "";
    expect(label).toMatch(/entries \(.*%\)/);
    await slice.hover();
    await expect(page.getByTestId("cd-tip")).toHaveText(label);
    await page.mouse.move(2, 2);
    await slice.focus();
    await expect(page.getByTestId("cd-tip")).toHaveText(label);
  });

  test("stacked bars of the kinds for the whole, each ecosystem and each type, with the same numbers in a table", async ({ page }) => {
    await open(page);
    const rows = page.getByTestId("ch-stack-svg").locator("g[data-row]");
    await expect(rows).toHaveCount(1 + 4 + 5);
    await expect(page.getByTestId("ch-stack-table").locator("tbody tr")).toHaveCount(10);
    const first = await rows.first().locator(".cd-seg").evaluateAll((els) => els.reduce((a, e) => a + Number(e.getAttribute("data-value")), 0));
    expect(first).toBe(number(await kpi(page, "entries").textContent()) + number(await kpi(page, "unreleased").textContent()));
    expect(await page.getByTestId("ch-stack-legend").locator("li").count()).toBe(11);
    const seg = rows.nth(1).locator(".cd-seg").first();
    expect(await seg.getAttribute("aria-label")).toMatch(/entries \(.*%\)/);
  });

  test("evolution: three lines for the whole and one per ecosystem from the daily history", async ({ page }) => {
    await open(page);
    await expect(page.getByTestId("ch-evo-wrap")).toBeVisible();
    await expect(page.getByTestId("ch-evo-total-svg").locator("path.cd-line")).toHaveCount(3);
    await expect(page.getByTestId("ch-evo-eco-svg").locator("path.cd-line")).toHaveCount(4);
    await expect(page.getByTestId("ch-evo-table").locator("tbody tr")).toHaveCount(46);
    await page.getByTestId("ch-evo-total-svg").locator(".cd-mark[data-series=entries]").last().focus();
    await expect(page.getByTestId("cd-tip")).toContainText("Published entries on 2001-12-21");
  });

  test("ranking: the repositories with most changes, stacked by kind, and the highest share of fixes", async ({ page }) => {
    await open(page);
    const rows = page.getByTestId("ch-rank-vol-svg").locator("g[data-row]");
    await expect(rows).toHaveCount(15);
    const sums = await rows.evaluateAll((els) => els.map((g) => Array.from(g.querySelectorAll(".cd-seg")).reduce((a, s) => a + Number(s.getAttribute("data-value")), 0)));
    expect(sums).toEqual([...sums].sort((a, b) => b - a));
    await page.getByTestId("ch-top-n").selectOption("10");
    await expect(rows).toHaveCount(10);
    await expect(page.getByTestId("ch-rank-vol-table").locator("tbody tr")).toHaveCount(10);
    const shares = await page.getByTestId("ch-rank-fix-svg").locator(".cd-seg").evaluateAll((els) => els.map((e) => Number(e.getAttribute("data-value"))));
    expect(shares.length).toBeGreaterThan(0);
    expect(shares.length).toBeLessThanOrEqual(10);
    expect(shares).toEqual([...shares].sort((a, b) => b - a));
    await expect(page.locator("#ch-rank-fix-hint")).toContainText("at least 10 entries");
  });

  test("every chart is drawn with data, has size and can be captured", async ({ page }, info) => {
    await open(page);
    for (const id of ["ch-donut-chart", "ch-stack-chart", "ch-evo-total", "ch-evo-eco", "ch-rank-vol", "ch-rank-fix", "ch-det-chart"]) {
      const chart = page.getByTestId(id);
      await chart.scrollIntoViewIfNeeded();
      const box = await chart.boundingBox();
      expect(box, id).not.toBeNull();
      expect(box!.width, id).toBeGreaterThan(150);
      expect(box!.height, id).toBeGreaterThan(80);
      expect(await chart.locator("rect, path, circle, polygon").count(), id).toBeGreaterThan(3);
      const picture = await chart.screenshot();
      expect(picture.length, id).toBeGreaterThan(2500);
      await info.attach(`changes-${id}.png`, { body: picture, contentType: "image/png" });
    }
  });
});

test.describe("changes view: the detail of a repository", () => {
  test("the versions of a repository are drawn and listed with their entries by kind", async ({ page }) => {
    await open(page);
    const repo = await page.getByTestId("ch-repo").inputValue();
    expect(repo).toMatch(/FIXTURE/);
    const rows = page.getByTestId("ch-det-table").locator("tbody tr");
    const count = await rows.count();
    expect(count).toBeGreaterThan(5);
    await expect(page.getByTestId("ch-det-svg").locator("g[data-row]")).toHaveCount(count);
    await expect(page.getByTestId("ch-det-svg")).toHaveAttribute("aria-label", new RegExp(repo));
    const header = (await page.getByTestId("ch-det-table").locator("thead th").allTextContents()).map((h) => h.toLowerCase());
    expect(header.slice(0, 2)).toEqual(["version", "entries"]);
    expect(header).toContain("bug fix");
    const entries = await rows.first().locator("td").nth(1).textContent();
    const parts = await rows.first().locator("td").evaluateAll((tds) => tds.slice(1, 11).map((t) => Number(t.textContent)));
    expect(parts[0]).toBe(Number(entries));
    expect(parts.slice(1).reduce((a, b) => a + b, 0)).toBe(Number(entries));
  });

  test("the range of versions limits the rows", async ({ page }) => {
    await open(page);
    await page.getByTestId("ch-range").selectOption("5");
    const rows = page.getByTestId("ch-det-table").locator("tbody tr");
    const published = await rows.evaluateAll((els) => els.filter((e) => e.getAttribute("data-version") !== "unreleased").length);
    expect(published).toBe(5);
    await page.getByTestId("ch-range").selectOption("0");
    expect(await rows.count()).toBeGreaterThan(published);
  });

  test("opening a version lists its entries, searchable and filterable by kind", async ({ page }) => {
    await open(page);
    await page.locator("#ch-det-table tbody tr:not([data-version=unreleased]) .ch-open").first().click();
    await expect(page.getByTestId("ch-entries")).toBeVisible();
    await expect(page.getByTestId("ch-entries-title")).toContainText("Entries of ");
    const items = page.getByTestId("ch-entry-list").locator("li");
    const total = await items.count();
    expect(total).toBeGreaterThan(0);
    await expect(page.getByTestId("ch-entry-count")).toHaveAttribute("data-total", String(total));
    const kinds = await items.evaluateAll((els) => els.map((e) => e.getAttribute("data-kind")));
    const some = kinds[0]!;
    await page.getByTestId(`ch-entry-kind-${some}`).click();
    await expect(items).toHaveCount(kinds.filter((k) => k === some).length);
    await page.getByTestId("ch-entry-kind-all").click();
    await expect(items).toHaveCount(total);
    const word = ((await items.first().locator("span").last().textContent()) || "").split(" ")[0]!.slice(0, 3).toLowerCase();
    await page.getByTestId("ch-entry-search").fill(word);
    const shown = await items.count();
    expect(shown).toBeGreaterThan(0);
    expect(shown).toBeLessThanOrEqual(total);
    await page.getByTestId("ch-entry-search").fill("zzzz-nothing");
    await expect(items).toHaveCount(0);
    await expect(page.getByTestId("ch-entry-count")).toHaveText("No entry matches.");
  });

  test("the entries waiting to be published can be read too, and an old version says its text is not kept", async ({ page }) => {
    await open(page);
    await page.getByTestId("ch-range").selectOption("0");
    await page.getByTestId("ch-open-unreleased").click();
    await expect(page.getByTestId("ch-entries-title")).toHaveText("Entries of Unreleased");
    expect(await page.getByTestId("ch-entry-list").locator("li").count()).toBeGreaterThan(0);
    const last = page.locator("#ch-det-table tbody tr:not([data-version=unreleased]) .ch-open").last();
    await last.click();
    await expect(page.getByTestId("ch-entries-note")).toBeVisible();
    await expect(page.getByTestId("ch-entries-note")).toContainText("newest 5 versions");
    await expect(page.getByTestId("ch-entry-list").locator("li")).toHaveCount(0);
  });

  test("another repository can be chosen", async ({ page }) => {
    await open(page);
    const options = await page.getByTestId("ch-repo").locator("option").evaluateAll((os) => os.map((o) => (o as HTMLOptionElement).value));
    expect(options.length).toBe(36);
    await page.getByTestId("ch-repo").selectOption(options[3]!);
    await expect(page.getByTestId("ch-det-svg")).toHaveAttribute("aria-label", new RegExp(options[3]!));
  });
});

test.describe("changes view: the table, the filters and the export", () => {
  test("one row per repository with a changelog, most entries first, and a total", async ({ page }) => {
    await open(page);
    const rows = page.locator("#ch-table tbody tr");
    await expect(rows).toHaveCount(36);
    const entries = await rows.evaluateAll((els) => els.map((e) => Number(e.getAttribute("data-entries"))));
    expect(entries).toEqual([...entries].sort((a, b) => b - a));
    const heads = await page.locator("#ch-table thead th").allInnerTexts();
    expect(heads.map((h) => h.replace(/[↑↓]/g, "").trim())).toEqual(expect.arrayContaining(["Repository", "Ecosystem", "Type", "Versions", "Entries", "Waiting", "Per version", "Bug fix", "Unclassified", "Tags", "Last tag", "30 days", "90 days", "Days between tags"]));
    expect(number(await page.getByTestId("ch-total").locator("td").nth(3).textContent())).toBe(entries.reduce((a, b) => a + b, 0));
    await expect(page.getByTestId("ch-matches")).toHaveAttribute("data-shown", "36");
  });

  test("a repository without tags says not available instead of zero", async ({ page }) => {
    await open(page);
    await page.getByTestId("ch-sort-tags").click();
    await expect(page.locator("#ch-table tbody tr").last()).toContainText("n/a");
  });

  test("sorting says so and a second click reverses it", async ({ page }) => {
    await open(page);
    await page.getByTestId("ch-sort-versions").click();
    await expect(page.locator("#ch-table th[aria-sort=descending]")).toHaveCount(1);
    await page.getByTestId("ch-sort-versions").click();
    await expect(page.locator("#ch-table th[aria-sort=ascending]")).toHaveCount(1);
    await expect(page.getByTestId("ch-live")).toContainText("Sorted by Versions, ascending");
    await expect(page.getByTestId("ch-sort-versions")).toBeFocused();
  });

  test("the filters apply to the table, the figures, the donut and the ranking", async ({ page }) => {
    await open(page);
    await page.getByTestId("ch-eco-urtc").click();
    const shown = Number(await page.getByTestId("ch-matches").getAttribute("data-shown"));
    expect(shown).toBeGreaterThan(0);
    expect(shown).toBeLessThan(36);
    await expect(kpi(page, "repos")).toHaveText(String(shown));
    await expect(page.locator("#ch-table tbody tr")).toHaveCount(shown);
    const published = number(await kpi(page, "entries").textContent());
    const waiting = number(await kpi(page, "unreleased").textContent());
    const slices = await page.getByTestId("ch-donut-svg").locator(".cd-seg").evaluateAll((els) => els.reduce((a, e) => a + Number(e.getAttribute("data-value")), 0));
    expect(slices).toBe(published + waiting);
    await expect(page.getByTestId("ch-rank-vol-svg").locator("g[data-row]")).toHaveCount(Math.min(15, shown));
    await page.getByTestId("ch-type-firmware").click();
    expect(Number(await page.getByTestId("ch-matches").getAttribute("data-shown"))).toBeLessThan(shown);
    await page.getByTestId("ch-eco-all").click();
    await page.getByTestId("ch-type-all").click();
    await page.getByTestId("ch-search").fill("zzzz-nothing");
    await expect(page.getByTestId("ch-none")).toBeVisible();
    await expect(page.getByTestId("ch-none")).toHaveText("No row matches the filters.");
    await expect(kpi(page, "repos")).toHaveText("0");
  });

  test("the rows can be grouped by ecosystem and by type and the groups add up", async ({ page }) => {
    await open(page);
    await page.getByTestId("ch-group").selectOption("eco");
    const rows = page.locator("#ch-table tbody tr");
    await expect(rows).toHaveCount(4);
    const sum = (await rows.evaluateAll((els) => els.map((e) => Number(e.getAttribute("data-entries"))))).reduce((a, b) => a + b, 0);
    expect(sum).toBe(number(await kpi(page, "entries").textContent()));
    await page.getByTestId("ch-group").selectOption("type");
    await expect(rows).toHaveCount(5);
  });

  test("the table is exported as CSV with the rows that are shown", async ({ page }) => {
    await open(page);
    await page.getByTestId("ch-eco-armor").click();
    const shown = Number(await page.getByTestId("ch-matches").getAttribute("data-shown"));
    const [download] = await Promise.all([page.waitForEvent("download"), page.getByTestId("ch-export-csv").click()]);
    expect(download.suggestedFilename()).toBe("changelog-statistics.csv");
    const text = fs.readFileSync((await download.path())!, "utf8");
    expect(text.charCodeAt(0)).toBe(0xfeff);
    const lines = text.trim().split("\r\n");
    expect(lines.length).toBe(1 + shown + 1);
    expect(lines[0]).toContain("Repository");
    expect(lines[0]).toContain("Entries");
    expect(lines[1]).toMatch(/^ARMOR-FIXTURE-\d\d,A\.R\.M\.O\.R\.,/);
    expect(lines[lines.length - 1].startsWith("Total")).toBe(true);
    await expect(page.getByTestId("ch-live")).toHaveText(`Exported ${shown + 1} rows.`);
  });

  test("the table is exported as JSON with stable keys", async ({ page }) => {
    await open(page);
    await page.getByTestId("ch-group").selectOption("eco");
    const [download] = await Promise.all([page.waitForEvent("download"), page.getByTestId("ch-export-json").click()]);
    expect(download.suggestedFilename()).toBe("changelog-statistics.json");
    const data = JSON.parse(fs.readFileSync((await download.path())!, "utf8"));
    expect(data.length).toBe(4 + 1);
    expect(Object.keys(data[0])).toEqual(expect.arrayContaining(["name", "versions", "entries", "unreleased", "avg", "fix", "unclassified", "tags", "last", "d30", "d90", "gap"]));
    expect(data[data.length - 1].name).toBe("Total");
    expect(data.slice(0, -1).reduce((a: number, r: { entries: number }) => a + r.entries, 0)).toBe(data[data.length - 1].entries);
  });

  test("the name of a repository opens its panel", async ({ page }) => {
    await open(page);
    await page.locator("#ch-table .cd-name-btn").first().click();
    await expect(page.locator("#repo-panel")).toBeVisible();
  });
});

test.describe("changes view: languages and states", () => {
  for (const lang of LANGS) {
    test(`${lang}: the view, its charts, its detail and its table are translated`, async ({ page }) => {
      await open(page);
      await page.locator("#lang-select").selectOption(lang);
      const title = await page.locator("#ch-title").innerText();
      if (lang !== "en") expect(title).not.toBe("Changelog statistics");
      if (lang === "es") expect(title).toBe("Estadísticas de los changelog");
      if (lang === "pt") expect(title).toBe("Estatísticas dos changelogs");
      if (lang === "en") expect(await page.locator("#tab-changelog").innerText()).toBe("Changelog");
      await page.locator("#ch-det-table tbody tr:not([data-version=unreleased]) .ch-open").first().click();
      for (const id of ["ch-donut-svg", "ch-stack-svg", "ch-evo-total-svg", "ch-rank-vol-svg", "ch-rank-fix-svg", "ch-det-svg"]) {
        const label = (await page.getByTestId(id).getAttribute("aria-label")) || "";
        expect(label, `${lang} ${id}`).not.toMatch(/\{|\}|undefined/);
        if (lang !== "en") expect(label, `${lang} ${id}`).not.toMatch(/the table below has the same figures/);
      }
      const legend = await page.getByTestId("ch-donut-legend").innerText();
      expect(legend).not.toMatch(LEFTOVER);
      if (lang !== "en") expect(legend).not.toContain("Bug fix");
      expect(await page.locator("#ch-body").innerText()).not.toMatch(LEFTOVER);
      expect(await visibleText(page)).not.toMatch(/\{[a-z]+\}/);
      const heads = await page.locator("#ch-table thead th").allInnerTexts();
      expect(heads.length).toBeGreaterThan(15);
      if (["es", "fr", "ja", "zh", "pt"].includes(lang)) expect(heads.join(" ")).not.toContain("Repository");
    });
  }

  test("the charts follow the theme", async ({ page }) => {
    await open(page);
    const fill = () => page.getByTestId("ch-donut-svg").locator(".cd-seg path").first().evaluate((e) => getComputedStyle(e).fill);
    const dark = await fill();
    await page.locator("#theme-toggle").click();
    await expect(page.locator("html")).toHaveAttribute("data-theme", "light");
    expect(await fill()).not.toBe(dark);
  });

  test("one day of history cannot draw a line and says so", async ({ page }) => {
    await open(page, "single");
    await expect(page.getByTestId("ch-evo-msg")).toBeVisible();
    await expect(page.getByTestId("ch-evo-msg")).toContainText("Only one day is recorded so far");
    await expect(page.getByTestId("ch-donut-svg")).toBeVisible();
  });

  for (const variant of ["minimal", "partial", "empty"] as const) {
    test(`${variant}: no figures means "not verified", never zeros`, async ({ page }) => {
      await open(page, variant);
      await expect(page.getByTestId("ch-not-read")).toBeVisible();
      await expect(page.getByTestId("ch-not-read")).toHaveText("No changelog statistics could be read in this build, so nothing is verified.");
      await expect(page.getByTestId("ch-main")).toBeHidden();
    });
  }
});

test.describe("changes view: accessibility", () => {
  for (const theme of ["dark", "light"]) {
    for (const lang of ["en", "ja"]) {
      test(`axe, ${theme}, ${lang}: no serious or critical violations, with a version opened`, async ({ page }) => {
        await open(page);
        if (theme === "light") await page.locator("#theme-toggle").click();
        await page.locator("#lang-select").selectOption(lang);
        await page.locator("#ch-det-table tbody tr:not([data-version=unreleased]) .ch-open").first().click();
        const results = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"]).analyze();
        const found = results.violations.filter((v) => v.impact === "serious" || v.impact === "critical")
          .map((v) => `${v.id}: ${v.nodes.slice(0, 3).map((n) => n.target.join(" ")).join(" | ")}`);
        expect(found).toEqual([]);
      });
    }
  }
});

test.describe("changes view: screen sizes", () => {
  for (const [name, width, height] of [["phone", 390, 800], ["tablet", 768, 1024], ["laptop", 1280, 800]] as const) {
    test(`${name}: nothing makes the page wider than the screen and the table scrolls by itself`, async ({ page }) => {
      await page.setViewportSize({ width, height });
      await open(page);
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      expect(overflow).toBeLessThanOrEqual(1);
      const wrap = page.getByTestId("ch-table-wrap");
      await wrap.scrollIntoViewIfNeeded();
      expect(await wrap.evaluate((e) => e.scrollWidth > e.clientWidth)).toBe(true);
      const box = await page.getByTestId("ch-donut-chart").boundingBox();
      expect(box!.width).toBeLessThanOrEqual(width);
    });
  }
});

