import AxeBuilder from "@axe-core/playwright";
import { test, expect, openDashboard, gotoTab, LANGS, LEFTOVER, visibleText, Page, Variant } from "./helpers";

// The tab "Sentinel": a public-safe watch decided by rules (no AI), read when the page was generated. Counts, repository names, workflow file names and version
// tags only. Fixture (full): 40 repositories read at 2001-12-21 12:00 UTC, 37 of them read; 8 red workflows (54 checked), 6 releases ready, 3 invalid signatures,
// 5 hygiene gaps (3 without the ruleset, settings readable in 5), 1768 approximate minutes in 24 hours and 12 days of trend.

async function serious(page: Page) {
  const results = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"]).analyze();
  return results.violations.filter((v) => v.impact === "serious" || v.impact === "critical").map((v) => `${v.id}: ${v.nodes.slice(0, 3).map((n) => n.target.join(" ")).join(" | ")}`);
}

async function open(page: Page, variant: Variant | "single" = "full") {
  await page.clock.setFixedTime(new Date("2001-12-21T12:30:00Z"));      // the ages are counted from the clock of the browser
  await openDashboard(page, variant as Variant);
  await gotoTab(page, "sentinel");
}

const kpi = (page: Page, name: string) => page.getByTestId(`sn-k-${name}`).locator("b");

test.describe("sentinel tab: figures", () => {
  test("the tab sits after Builds and shows the figures of the fixture", async ({ page }) => {
    await open(page);
    const ids = await page.locator("[role=tab]").evaluateAll((tabs) => tabs.map((t) => t.getAttribute("data-testid")));
    expect(ids.indexOf("tab-sentinel")).toBe(ids.indexOf("tab-actions") + 1);
    await expect(page.locator("#sn-title")).toHaveText("Sentinel: watch over the ecosystem");
    await expect(page.getByTestId("sn-badge")).toHaveText("Rules, no AI");
    await expect(kpi(page, "red")).toHaveText("8");
    await expect(kpi(page, "cand")).toHaveText("6");
    await expect(kpi(page, "sig")).toHaveText("3");
    await expect(kpi(page, "hyg")).toHaveText("5");
    await expect(kpi(page, "min")).toHaveText("1 768 min");
    await expect(kpi(page, "read")).toHaveText("37 of 40");
    await expect(page.getByTestId("sn-asof")).toHaveText("Data as of 12:00 UTC");
  });

  test("red tiles are red in words too and the quiet ones are not", async ({ page }) => {
    await open(page);
    await expect(page.getByTestId("sn-k-red")).toHaveClass(/ac-bad/);
    await expect(page.getByTestId("sn-k-sig")).toHaveClass(/ac-bad/);
    await expect(page.getByTestId("sn-k-cand")).not.toHaveClass(/ac-bad/);
  });

  test("the report is made by rules: headline first, then the worst, each line with a glyph and a word", async ({ page }) => {
    await open(page);
    const keys = await page.locator("#sn-parte li").evaluateAll((items) => items.map((i) => `${i.getAttribute("data-key")}:${i.getAttribute("data-level")}`));
    expect(keys).toEqual(["head:bad", "sig:bad", "red:bad", "cand:warn", "hyg:warn", "unread:info"]);
    await expect(page.locator("#sn-parte li").first()).toContainText("8 red workflows, 6 releases ready, 3 invalid signatures, 5 repositories with a hygiene gap.");
    await expect(page.locator("#sn-parte li[data-key=sig]")).toContainText("INVALID signature of the latest release");
    await expect(page.locator("#sn-parte li[data-key=sig]")).toContainText("Do not install it");
    await expect(page.locator("#sn-parte li[data-key=sig] .sn-gl")).toHaveText("✕");
    await expect(page.locator("#sn-parte li[data-key=sig] .sn-lvl")).toContainText("Problem");
    await expect(page.locator("#sn-parte li[data-key=unread]")).toContainText("3 of 40 repositories could not be read");
    await expect(page.locator("#sn-parte li[data-key=compute]")).toHaveCount(0);      // 1 768 minutes are under the configured limit
  });

  test("the red table follows the single criterion and the release table follows the rule of the owner", async ({ page }) => {
    await open(page);
    await expect(page.getByTestId("sn-ci-table").locator("tbody tr")).toHaveCount(8);
    await expect(page.getByTestId("sn-ci-table").locator("thead th")).toHaveText(["Repository", "Workflow file", "In a row", "Red since"]);
    await expect(page.getByTestId("sn-ci-table").locator("tbody tr").first().locator("td").first()).toHaveText("ci.yml");
    await expect(page.locator("#sn-ci-sum")).toHaveText("54 workflows checked in 37 repositories.");
    await expect(page.getByTestId("sn-ci-table").locator("tbody tr").first().locator("td").nth(2)).toHaveText(/^\d+ (min|h|d) ago$/);
    await expect(page.locator("#sn-rel-rule")).toHaveText("Rule: at least 1 entry under [Unreleased] in the CHANGELOG and a last release older than 2 days (or none).");
    await expect(page.getByTestId("sn-rel-table").locator("tbody tr")).toHaveCount(6);
    const entries = await page.getByTestId("sn-rel-table").locator("tbody tr").evaluateAll((r) => r.map((x) => Number(x.querySelectorAll("td")[0].textContent)));
    expect(entries).toEqual([...entries].sort((a, b) => b - a));
    await expect(page.getByTestId("sn-rel-table").locator("tbody tr").first().locator("th")).toHaveText("ARMOR-FIXTURE-04");
    await expect(page.getByTestId("sn-rel-table")).toContainText("no release");
  });

  test("the table by ecosystem adds up to the repositories and the two new cards say so when they are empty", async ({ page }) => {
    await open(page);
    const rows = await page.getByTestId("sn-eco-table").locator("tbody tr").evaluateAll((r) => r.map((x) => ({ n: Number(x.querySelectorAll("td")[0].textContent), red: Number(x.querySelectorAll("td")[1].textContent) })));
    expect(rows.length).toBeGreaterThan(0);
    expect(rows.reduce((a, r) => a + r.n, 0)).toBe(40);
    expect(rows.reduce((a, r) => a + r.red, 0)).toBeLessThanOrEqual(8);
    await expect(page.getByTestId("sn-eco-table").locator("thead th")).toHaveText(["Ecosystem", "Repositories", "Red", "Ready", "Not published"]);
    await expect(page.getByTestId("sn-unpub-none")).toHaveText("No version is waiting to be published.");
    await expect(page.getByTestId("sn-ev-none")).toHaveText("No change recorded yet.");
  });

  test("signatures: the six answers add up to the repositories and an invalid one is named", async ({ page }) => {
    await open(page);
    const counts = await page.locator("#sn-sigs li").evaluateAll((items) => items.map((i) => ({ s: i.getAttribute("data-state"), n: Number(i.querySelector("b")!.textContent) })));
    expect(counts.map((c) => c.s)).toEqual(["verified", "invalid", "unverifiable", "none", "norelease", "unverified"]);
    expect(counts.reduce((a, c) => a + c.n, 0)).toBe(40);
    expect(counts.find((c) => c.s === "invalid")!.n).toBe(3);
    await expect(page.getByTestId("sn-sig-bad")).toBeVisible();
    await expect(page.getByTestId("sn-sig-bad")).toContainText("Do not install:");
  });

  test("hygiene: the ruleset, the settings it could not read said so, and nothing unread is shown as in order", async ({ page }) => {
    await open(page);
    await expect(page.getByTestId("sn-hyg")).toContainText("Active ruleset protecting the main branch: 34 of 37 repositories read.");
    await expect(page.getByTestId("sn-hyg")).toContainText("Missing in:");
    await expect(page.getByTestId("sn-hyg")).toContainText("readable in 5 of 37 repositories");
    await expect(page.getByTestId("sn-hyg")).toContainText("SHA pinning not required:");
    await expect(page.getByTestId("sn-hyg")).not.toContainText("No gap found");
  });

  test("computing: the busiest first with the total, and the trend has four series with their figures in words", async ({ page }) => {
    await open(page);
    await expect(page.getByTestId("sn-cmp-total")).toHaveText("Total: 1 768 min in 24 h, 1 878 min in 7 days");
    const bars = page.locator("#sn-cmp .ac-bar");
    expect(await bars.count()).toBe(6);
    await expect(page.locator("#sn-trend li")).toHaveCount(4);
    await expect(page.locator("#sn-trend li .sn-chart").first()).toHaveAttribute("aria-label", /^Red workflows: now 8, from \d+ to \d+; .+ \(from 2001-12-\d\d to 2001-12-21\)$/);
    await expect(page.locator("#sn-trend .sn-spark")).toHaveCount(4);
  });

  test("what is never shown is said, and nothing about alerts, pull requests, people or branches is on the tab", async ({ page }) => {
    await open(page);
    await expect(page.getByTestId("sn-excl")).toContainText("Security alerts");
    const text = (await page.locator("#panel-sentinel").innerText()).toLowerCase();
    const before = text.replace(/security alerts \(code scanning[^.]*\./, "");
    for (const word of ["codeql", "dependabot", "secret scanning", "bump ", "actor", "feature/"]) expect(before, word).not.toContain(word);
    const html = await page.content();
    const start = html.indexOf('"sentinel":{');
    expect(start).toBeGreaterThan(0);
    const block = html.slice(start, start + 60000).split('"tests":')[0];
    for (const word of ["codeql", "dependabot", "alerts", "title", "actor", "login", "rule\":"]) expect(block.toLowerCase(), word).not.toContain(word);
  });
});

test.describe("sentinel tab: other data", () => {
  test("a quiet situation says so and the headline is in order", async ({ page }) => {
    await open(page, "healthy");
    await expect(page.locator("#sn-parte li").first()).toHaveAttribute("data-level", "ok");
    await expect(page.locator("#sn-parte li[data-key=all_ok]")).toContainText("Everything that could be read is in order.");
    await expect(page.getByTestId("sn-ci-none")).toBeVisible();
    await expect(page.getByTestId("sn-rel-none")).toBeVisible();
    await expect(page.getByTestId("sn-k-red")).not.toHaveClass(/ac-bad/);
    await expect(kpi(page, "hyg")).toHaveText("0");
  });

  test("the last known reading is marked with its date when GitHub could not be read", async ({ page }) => {
    await open(page, "stale");
    await expect(page.getByTestId("sn-stale")).toContainText("2001-12-21");
    await expect(page.getByTestId("sn-stale")).toContainText("not a current one");
  });

  test("one day of history gives no trend line, only the note", async ({ page }) => {
    await open(page, "single");
    await expect(page.getByTestId("sn-trend-none")).toBeVisible();
    await expect(page.locator("#sn-trend li")).toHaveCount(0);
  });

  for (const variant of ["partial", "minimal", "empty"] as const) {
    test(`with nothing read (${variant}) it says not verified and never shows a number as if it were real`, async ({ page }) => {
      await open(page, variant);
      await expect(page.getByTestId("sn-not-read")).toBeVisible();
      await expect(kpi(page, "red")).toHaveText("Not verified");
      await expect(page.locator("#sn-parte li")).toHaveCount(1);
      await expect(page.getByTestId("sn-ci-none")).toHaveText("Not verified");
    });
  }
});

test.describe("sentinel tab: languages, accessibility, motion, print", () => {
  test("the 8 languages: no key, no placeholder, the report in each one and Portugal's Portuguese", async ({ page }) => {
    await open(page);
    const heads = new Set<string>();
    for (const lang of LANGS) {
      await page.locator("#lang-select").selectOption(lang);
      expect(await visibleText(page), lang).not.toMatch(LEFTOVER);
      heads.add((await page.locator("#sn-parte li").first().textContent()) || "");
      await expect(page.locator("#sn-parte li[data-key=sig]")).not.toContainText("{");
      await page.getByTestId("sn-help").locator("summary").click();
      await expect(page.getByTestId("sn-help-body")).not.toContainText("{");
      await page.getByTestId("sn-help").locator("summary").click();
      await expect(page.locator("#sn-trend li .sn-chart").first()).toHaveAttribute("aria-label", /.+/);
    }
    expect(heads.size).toBe(8);
    await page.locator("#lang-select").selectOption("pt");
    await expect(page.getByTestId("tab-sentinel")).toHaveText("Sentinela");
    await expect(page.getByTestId("sn-badge")).toHaveText("Regras, sem IA");
    await expect(page.locator("#sn-parte li").first()).toContainText("fluxos a vermelho");
    await expect(page.getByTestId("sn-hyg")).toContainText("repositórios");
    await page.locator("#lang-select").selectOption("es");
    await expect(page.getByTestId("tab-sentinel")).toHaveText("Centinela");
    await expect(page.locator("#sn-parte li[data-key=red]")).toContainText("En rojo en la rama principal");
    await page.locator("#lang-select").selectOption("ja");
    await expect(page.getByTestId("sn-badge")).toHaveText("ルールのみ(AI なし)");
  });

  for (const theme of ["dark", "light"]) {
    test(`axe finds no serious violation (${theme}), also quiet and with nothing read`, async ({ page }) => {
      test.setTimeout(90_000);
      await open(page);
      if (theme === "light") await page.locator("#theme-toggle").click();
      const found = [...(await serious(page)).map((x) => `all: ${x}`)];
      await page.getByTestId("sn-help").locator("summary").click();
      found.push(...(await serious(page)).map((x) => `help: ${x}`));
      for (const variant of ["healthy", "partial"] as const) {
        await openDashboard(page, variant);
        await gotoTab(page, "sentinel");
        if (theme === "light") await page.locator("#theme-toggle").click();
        found.push(...(await serious(page)).map((x) => `${variant}: ${x}`));
      }
      expect(found).toEqual([]);
    });
  }

  test("every control can be reached with the keyboard and shows its focus", async ({ page }) => {
    await open(page);
    const reached = new Set<string>();
    await page.locator("#panel-sentinel").focus();
    for (let i = 0; i < 70; i += 1) {
      await page.keyboard.press("Tab");
      const info = await page.evaluate(() => {
        const e = document.activeElement as HTMLElement;
        const style = getComputedStyle(e);
        return { id: e.id || e.getAttribute("class") || e.tagName, inside: !!e.closest("#panel-sentinel"), outline: style.outlineStyle !== "none" && parseFloat(style.outlineWidth) >= 2 };
      });
      if (info.inside) { reached.add(String(info.id).split(" ")[0]); expect(info.outline, String(info.id)).toBe(true); }
    }
    for (const needed of ["sn-ci-wrap", "sn-rel-wrap", "ac-link", "ac-bar"]) expect([...reached].some((r) => r.includes(needed)), needed).toBe(true);
  });

  test("with motion allowed the trend lines are drawn with an entrance, and with reduced motion they are not", async ({ page }) => {
    await page.emulateMedia({ reducedMotion: "no-preference" });
    await open(page);
    expect(await page.locator("#sn-trend polyline").first().evaluate((e) => getComputedStyle(e).animationName)).toBe("sn-draw");
    await page.emulateMedia({ reducedMotion: "reduce" });
    expect(await page.locator("#sn-trend polyline").first().evaluate((e) => getComputedStyle(e).animationName)).toBe("none");
  });

  test("print: the tables are whole on paper", async ({ page }) => {
    await open(page);
    await page.emulateMedia({ media: "print" });
    await expect(page.locator("#panel-sentinel")).toBeVisible();
    expect(await page.locator("#sn-ci-wrap").evaluate((e) => getComputedStyle(e).maxHeight)).toBe("none");
    expect(await page.locator("#sn-ci-wrap").evaluate((e) => getComputedStyle(e).overflowY)).toBe("visible");
  });

  test("the page makes no request of its own for this tab", async ({ page }) => {
    const requests: string[] = [];
    page.on("request", (r) => { if (/^https?:/.test(r.url()) && !r.url().startsWith("https://api.github.com/") && !/fonts\.(googleapis|gstatic)|\.svg/.test(r.url())) requests.push(r.url()); });
    await open(page);
    await page.locator("#lang-select").selectOption("fr");
    await page.locator("#sn-cmp .ac-bar").first().click();
    expect(requests.filter((u) => !u.startsWith("file:"))).toEqual([]);
  });
});

test.describe("sentinel tab: sizes", () => {
  test("1920x1080: everything is seen at a glance and neither the panel nor the page scroll", async ({ page }) => {
    await page.setViewportSize({ width: 1920, height: 1080 });
    await open(page);
    const m = await page.evaluate(() => {
      const panel = document.getElementById("panel-sentinel")!;
      const card = document.getElementById("pr-card");      // the card of signature and attestation presence is a list, not part of the glance: only it may scroll
      const extra = card ? card.getBoundingClientRect().height + 16 : 0;
      return { panel: panel.scrollHeight - panel.clientHeight - extra, page: document.documentElement.scrollHeight - document.documentElement.clientHeight };
    });
    expect(m.panel).toBeLessThanOrEqual(1);
    expect(m.page).toBeLessThanOrEqual(0);
    for (const id of ["#sn-kpis", "#sn-parte", "#sn-sigs", "#sn-ci-table", "#sn-rel-table", "#sn-hyg", "#sn-cmp", "#sn-trend"]) {
      const box = await page.locator(id).boundingBox();
      expect(box, id).not.toBeNull();
      expect(box!.y + Math.min(box!.height, 40), id).toBeLessThan(1080);
    }
    if (process.env.SHOTS) await page.screenshot({ path: `${process.env.SHOTS}/sentinel-1920.png` });
  });

  test("1366x768 and the tab bar still reach every tab, with no sideways scroll", async ({ page }) => {
    await page.setViewportSize({ width: 1366, height: 768 });
    await open(page);
    const m = await page.evaluate(() => ({ x: document.documentElement.scrollWidth - document.documentElement.clientWidth }));
    expect(m.x).toBeLessThanOrEqual(0);
    await expect(page.getByTestId("tab-sentinel")).toBeVisible();
    await expect(page.getByTestId("tab-errors")).toBeVisible();
    if (process.env.SHOTS) await page.screenshot({ path: `${process.env.SHOTS}/sentinel-1366.png` });
  });

  test("a phone: no sideways scroll, the tiles in two columns, nothing cut", async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await open(page);
    const m = await page.evaluate(() => ({ x: document.documentElement.scrollWidth - document.documentElement.clientWidth, cols: getComputedStyle(document.getElementById("sn-kpis")!).gridTemplateColumns.split(" ").length }));
    expect(m.x).toBeLessThanOrEqual(0);
    expect(m.cols).toBe(2);
    if (process.env.SHOTS) await page.screenshot({ path: `${process.env.SHOTS}/sentinel-390.png`, fullPage: true });
  });
});
