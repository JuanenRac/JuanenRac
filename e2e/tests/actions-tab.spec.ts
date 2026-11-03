import AxeBuilder from "@axe-core/playwright";
import { test, expect, openDashboard, gotoTab, LANGS, LEFTOVER, visibleText, Page, Variant } from "./helpers";

// The tab "Builds" (Actions / Builds): the state of the GitHub Actions runs read when the page was generated. State and numbers only.
// Fixture (full): 40 repositories, read at 2001-12-21 12:00 UTC: 36 with builds read (4 have no workflows, 2... see below), 248 runs in 24 hours
// (201 successful, 28 failed, 16 cancelled, 3 running), 18 open build-failed and 3 open build-stuck issues, 38 of 40 repositories read (2 could not be),
// and 12 days of daily summaries (11 of the history plus today).

const ECOS = ["hydra-umc", "urtc", "armor", "eh3d"] as const;

async function serious(page: Page) {
  const results = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"]).analyze();
  return results.violations.filter((v) => v.impact === "serious" || v.impact === "critical").map((v) => `${v.id}: ${v.nodes.slice(0, 3).map((n) => n.target.join(" ")).join(" | ")}`);
}

async function open(page: Page, variant: Variant | "single" = "full") {
  await openDashboard(page, variant as Variant);
  await gotoTab(page, "actions");
}

const kpi = (page: Page, name: string) => page.getByTestId(`ac-k-${name}`).locator("b");
const rows = (page: Page) => page.locator("#ac-table tbody tr");

test.describe("builds tab: figures", () => {
  test("the tab sits after Tests and shows the figures of the fixture", async ({ page }) => {
    await open(page);
    const ids = await page.locator("[role=tab]").evaluateAll((tabs) => tabs.map((t) => t.getAttribute("data-testid")));
    expect(ids.indexOf("tab-actions")).toBe(ids.indexOf("tab-tests") + 1);
    await expect(page.locator("#ac-title")).toHaveText("Actions / Builds");
    await expect(kpi(page, "runs")).toHaveText("248");
    await expect(kpi(page, "rate")).toHaveText("88 %");
    await expect(kpi(page, "min")).toHaveText(/^~\d+ h$/);
    await expect(kpi(page, "failed")).toHaveText("18");
    await expect(kpi(page, "stuck")).toHaveText("3");
    await expect(kpi(page, "read")).toHaveText("38 of 40");
    await expect(page.getByTestId("ac-asof")).toHaveText("Data as of 12:00 UTC");
    await expect(page.getByTestId("ac-unverified")).toContainText("2 repositories could not be read");
  });

  test("the red figures are red in words too: a build-failed issue count above zero marks the tile", async ({ page }) => {
    await open(page);
    await expect(page.getByTestId("ac-k-failed")).toHaveClass(/ac-bad/);
    await expect(page.getByTestId("ac-k-runs")).not.toHaveClass(/ac-bad/);
  });

  test("the ring adds up to the runs of the last 24 hours and has a name that says it", async ({ page }) => {
    await open(page);
    const counts = await page.locator("#ac-legend li").evaluateAll((items) => items.map((i) => ({ code: i.getAttribute("data-code"), n: Number(i.querySelector("b")!.textContent) })));
    expect(counts).toEqual([{ code: "s", n: 201 }, { code: "f", n: 28 }, { code: "c", n: 16 }, { code: "k", n: 0 }, { code: "p", n: 3 }]);
    expect(counts.reduce((a, c) => a + c.n, 0)).toBe(248);
    await expect(page.locator("#ac-ring svg")).toHaveAttribute("aria-label", "Results of the runs of the last 24 hours: Success 201, Failure 28, Cancelled 16, Running 3");
    await expect(page.locator("#ac-ring .ac-ring-seg")).toHaveCount(4);
    await expect(page.locator("#ac-legend li .ac-sw").first()).toHaveText("✓");
  });

  test("success rate per repository: the lowest first, six at most, each with its figures in words", async ({ page }) => {
    await open(page);
    const bars = page.locator("#ac-rate .ac-bar");
    expect(await bars.count()).toBeLessThanOrEqual(6);
    const percents = await bars.evaluateAll((b) => b.map((x) => Number(x.querySelector(".ac-bar-val")!.textContent!.replace(/\D/g, ""))));
    expect(percents.length).toBeGreaterThan(3);
    expect(percents).toEqual([...percents].sort((a, b) => a - b));
    await expect(bars.first()).toHaveAttribute("aria-label", /^[A-Z0-9-]+: \d+ % \(\d+ of \d+\)$/);
  });

  test("duration of the last run: the longest first, in minutes or seconds", async ({ page }) => {
    await open(page);
    const names = await page.locator("#ac-dur .ac-bar").count();
    expect(names).toBeGreaterThan(3);
    await expect(page.locator("#ac-dur .ac-bar").first().locator(".ac-bar-val")).toHaveText(/^\d+ (min|s)$/);
    const secs = await page.locator("#ac-dur .ac-bar").evaluateAll((b) => b.map((x) => (x.querySelector(".ac-fill") as HTMLElement).style.getPropertyValue("--w")));
    const widths = secs.map((w) => parseFloat(w));
    expect(widths).toEqual([...widths].sort((a, b) => b - a));
  });

  test("the timeline has one row per busy repository (five at most) and every dot is named", async ({ page }) => {
    await open(page);
    await expect(page.getByTestId("ac-tl")).toHaveAttribute("aria-label", /Timeline of the runs of the last 24 hours in 5 repositories/);
    await expect(page.locator("#ac-tl .ac-tl-name")).toHaveCount(5);
    const dots = await page.locator("#ac-tl .evo-mark title").allTextContents();
    expect(dots.length).toBeGreaterThan(20);
    for (const t of dots.slice(0, 10)) expect(t).toMatch(/^[A-Z0-9-]+: (Success|Failure|Cancelled|Other|Running), .+ ago$/);
  });

  test("the runs per day come from the history plus today", async ({ page }) => {
    await open(page);
    await expect(page.locator("#ac-trend .ac-col")).toHaveCount(12);
    await expect(page.locator("#ac-trend .ac-col").last()).toHaveAttribute("aria-label", "2001-12-21: 248 runs, 201 successful, 28 failed");
    await expect(page.getByTestId("ac-trend-none")).toBeHidden();
  });
});

test.describe("builds tab: the table", () => {
  test("one row per repository, failures first, and what was not read is not green", async ({ page }) => {
    await open(page);
    await expect(rows(page)).toHaveCount(40);
    await expect(page.getByTestId("ac-matches")).toHaveText("40 of 40 repositories");
    const states = await rows(page).evaluateAll((r) => r.map((x) => `${x.getAttribute("data-state")}:${x.getAttribute("data-last") || ""}`));
    const okRows = states.filter((s) => s.startsWith("ok:"));
    const firstOk = okRows.findIndex((s) => s !== "ok:f");
    expect(okRows.slice(0, firstOk).every((s) => s === "ok:f")).toBe(true);
    expect(okRows.slice(firstOk).some((s) => s === "ok:f")).toBe(false);
    expect(states.filter((s) => s === "ok:f").length).toBeGreaterThan(5);
    const unread = page.locator('#ac-table tbody tr[data-state="unread"]');
    await expect(unread).toHaveCount(2);
    await expect(unread.first()).toContainText(/not verified/i);
    await expect(unread.first().locator(".ac-res .ac-sw")).toHaveCount(0);
    await expect(page.locator('#ac-table tbody tr[data-state="none"]').first()).toContainText("No workflows");
  });

  test("a failing row says it with a glyph and a word", async ({ page }) => {
    await open(page);
    const first = rows(page).first();
    await expect(first.locator(".ac-sw")).toHaveText("✕");
    await expect(first.locator(".ac-res")).toContainText("Failure");
    await expect(first).toContainText("failed 2");
  });

  test("the pipeline and the signature of every repository come from the delivery data", async ({ page }) => {
    await open(page);
    const cells = await rows(page).evaluateAll((r) => r.map((x) => x.querySelector("td:last-child")!.textContent));
    expect(cells.every((c) => /·/.test(c || ""))).toBe(true);
    expect(cells.some((c) => /signature verified/.test(c || ""))).toBe(true);
    expect(cells.some((c) => /signature INVALID/.test(c || ""))).toBe(true);
    expect(cells.some((c) => /not verifiable here/.test(c || ""))).toBe(true);
    expect(cells.some((c) => /no signature/.test(c || ""))).toBe(true);
  });

  test("filter by ecosystem and search, with the counter", async ({ page }) => {
    await open(page);
    await page.getByTestId("ac-eco-urtc").click();
    await expect(page.getByTestId("ac-matches")).toHaveText("10 of 40 repositories");
    await expect(rows(page)).toHaveCount(10);
    await expect(page.getByTestId("ac-eco-urtc")).toHaveAttribute("aria-pressed", "true");
    await page.getByTestId("ac-eco-all").click();
    await page.getByTestId("ac-search").fill("armor-fixture-0");
    await expect(rows(page)).toHaveCount(10);
    await page.getByTestId("ac-search").fill("zzz");
    await expect(rows(page)).toHaveCount(0);
    await expect(page.getByTestId("ac-none")).toBeVisible();
    await expect(page.getByTestId("ac-table-wrap")).toBeHidden();
  });

  test("the name of a repository opens its panel, with the mouse and with the keyboard", async ({ page }) => {
    await open(page);
    await rows(page).first().locator("button.ac-link").click();
    await expect(page.locator("#repo-panel")).toBeVisible();
    await page.keyboard.press("Escape");
    await expect(page.locator("#repo-panel")).toBeHidden();
    const bar = page.locator("#ac-rate .ac-bar").first();
    await bar.focus();
    await page.keyboard.press("Enter");
    await expect(page.locator("#repo-panel")).toBeVisible();
  });

  test("the age is counted from the moment of the reading to now", async ({ page }) => {
    await page.clock.setFixedTime(new Date("2001-12-21T12:30:00Z"));
    await open(page);
    const ago = await rows(page).evaluateAll((r) => r.map((x) => x.querySelectorAll("td")[1]?.textContent || ""));
    expect(ago.some((a) => /^\d+ min$/.test(a))).toBe(true);
    expect(ago.every((a) => a === "–" || /^\d+ (min|h|d)$/.test(a))).toBe(true);
  });
});

test.describe("builds tab: privacy, nothing invented", () => {
  test("the data embedded in the page keeps no author, branch, title, message or workflow name", async ({ page }) => {
    await open(page);
    const json = await page.evaluate(() => JSON.stringify((JSON.parse(document.getElementById("dashboard-data")!.textContent!) as any).actions));
    for (const word of ["actor", "login", "branch", "title", "message", "commit", "ci.yml", "head_"]) expect(json.toLowerCase()).not.toContain(word);
    const keys = await page.evaluate(() => Object.keys((JSON.parse(document.getElementById("dashboard-data")!.textContent!) as any).actions.repos["HYDRA-UMC-FIXTURE-01"]).sort());
    expect(keys).toEqual(["bf", "bs", "dur", "last", "lastOk", "min", "min7", "n", "n7", "running", "state", "tl", "truncated"]);
  });

  test("when GitHub could not be read the last known read is shown, dated, and never as current", async ({ page }) => {
    await open(page, "stale");
    await expect(page.getByTestId("ac-stale")).toBeVisible();
    await expect(page.getByTestId("ac-stale")).toContainText("2001-12-21");
    await expect(page.getByTestId("ac-unverified")).toBeHidden();
    await expect(kpi(page, "runs")).toHaveText("248");
  });

  test("with nothing read and no earlier read every figure says not verified, never zero", async ({ page }) => {
    await open(page, "partial");
    await expect(page.getByTestId("ac-not-read")).toBeVisible();
    for (const name of ["runs", "rate", "min", "failed", "stuck"]) await expect(kpi(page, name)).toHaveText(/not verified/i);
    await expect(page.locator("#ac-legend li b").first()).toHaveText("–");
    await expect(page.locator('#ac-table tbody tr[data-state="unread"]')).toHaveCount(await rows(page).count());
    await expect(page.getByTestId("ac-rate-none")).toBeVisible();
    await expect(page.getByTestId("ac-tl-none")).toBeVisible();
    expect(await page.locator("#panel-actions .ac-sw").evaluateAll((s) => s.filter((x) => x.closest("tr")).length)).toBe(0);
  });

  test("a healthy ecosystem shows no red tile and no failure", async ({ page }) => {
    await open(page, "healthy");
    await expect(page.getByTestId("ac-k-failed")).not.toHaveClass(/ac-bad/);
    await expect(page.getByTestId("ac-k-stuck")).not.toHaveClass(/ac-bad/);
    await expect(kpi(page, "failed")).toHaveText("0");
    await expect(page.locator('#ac-table tbody tr[data-last="f"]')).toHaveCount(0);
    await expect(kpi(page, "rate")).toHaveText("100 %");
  });

  test("the compute minutes are labelled as approximate", async ({ page }) => {
    await open(page);
    await expect(page.getByTestId("ac-k-min")).toContainText("(approx.)");
    await expect(page.getByTestId("ac-note")).toContainText("approximate");
    await expect(page.locator("#ac-table thead th").nth(5)).toContainText("approx.");
  });
});

test.describe("builds tab: languages, themes, keyboard, motion", () => {
  test("no untranslated key in any of the eight languages and the texts follow the language", async ({ page }) => {
    await open(page);
    const titles = new Set<string>();
    for (const lang of LANGS) {
      await page.locator("#lang-select").selectOption(lang);
      expect(await visibleText(page), lang).not.toMatch(LEFTOVER);
      titles.add((await page.getByTestId("tab-actions").textContent()) || "");
      await expect(page.getByTestId("ac-matches")).toHaveAttribute("data-total", "40");
      await expect(page.locator("#ac-ring svg")).toHaveAttribute("aria-label", /.+/);
      await expect(page.locator("#ac-table caption")).not.toHaveText("");
      await page.getByTestId("ac-help").locator("summary").click();
      await expect(page.getByTestId("ac-help-body")).not.toContainText("{");
      await page.getByTestId("ac-help").locator("summary").click();
    }
    expect(titles.size).toBe(6);                      // the tab label is the same in English, German and French ("Builds")
    await page.locator("#lang-select").selectOption("pt");
    await expect(page.getByTestId("tab-actions")).toHaveText("Compilações");
    await expect(page.locator("#ac-title")).toHaveText("Actions / Compilações");
    await expect(page.getByTestId("ac-badge")).toHaveText("Quase em direto");
    await expect(page.locator("#ac-legend li").first()).toContainText("Sucesso");
    await page.locator("#lang-select").selectOption("es");
    await expect(page.getByTestId("tab-actions")).toHaveText("Compilaciones");
    await expect(page.getByTestId("ac-k-failed")).toContainText("build-failed abiertas");
    await page.locator("#lang-select").selectOption("ja");
    await expect(page.getByTestId("ac-badge")).toHaveText("ほぼリアルタイム");
  });

  for (const theme of ["dark", "light"]) {
    test(`axe finds no serious violation (${theme}), also filtered and with nothing read`, async ({ page }) => {
      test.setTimeout(90_000);
      await open(page);
      if (theme === "light") await page.locator("#theme-toggle").click();
      const found = [...(await serious(page)).map((x) => `all: ${x}`)];
      await page.getByTestId("ac-eco-armor").click();
      found.push(...(await serious(page)).map((x) => `armor: ${x}`));
      await page.getByTestId("ac-help").locator("summary").click();
      found.push(...(await serious(page)).map((x) => `help: ${x}`));
      await openDashboard(page, "partial");
      await gotoTab(page, "actions");
      if (theme === "light") await page.locator("#theme-toggle").click();
      found.push(...(await serious(page)).map((x) => `poor data: ${x}`));
      expect(found).toEqual([]);
    });
  }

  test("every control can be reached with the keyboard and shows its focus", async ({ page }) => {
    await open(page);
    const reached = new Set<string>();
    await page.locator("#panel-actions").focus();
    for (let i = 0; i < 40; i += 1) {
      await page.keyboard.press("Tab");
      const info = await page.evaluate(() => {
        const e = document.activeElement as HTMLElement;
        const style = getComputedStyle(e);
        return { id: e.id || e.getAttribute("class") || e.tagName, inside: !!e.closest("#panel-actions"), outline: style.outlineStyle !== "none" && parseFloat(style.outlineWidth) >= 2 };
      });
      if (info.inside) { reached.add(String(info.id).split(" ")[0]); expect(info.outline, String(info.id)).toBe(true); }
    }
    for (const needed of ["ac-bar", "ac-col", "chip", "ac-search", "ac-table-wrap", "ac-link"]) expect([...reached].some((r) => r.includes(needed)), needed).toBe(true);
  });

  test("with motion allowed the bars are drawn with an entrance, and with reduced motion they are not", async ({ page }) => {
    await page.emulateMedia({ reducedMotion: "no-preference" });
    await open(page);
    expect(await page.locator("#ac-rate .ac-fill").first().evaluate((e) => getComputedStyle(e).animationName)).toBe("t25-grow-x");
    await page.emulateMedia({ reducedMotion: "reduce" });
    expect(await page.locator("#ac-rate .ac-fill").first().evaluate((e) => getComputedStyle(e).animationName)).toBe("none");
    expect(await page.locator("#ac-ring .ac-ring-seg").first().evaluate((e) => getComputedStyle(e).animationName)).toBe("none");
    expect(await page.locator("#ac-trend .ac-col rect").first().evaluate((e) => getComputedStyle(e).animationName)).toBe("none");
  });

  test("print: the whole table is on paper and the controls are not", async ({ page }) => {
    await open(page);
    await page.emulateMedia({ media: "print" });
    await expect(page.locator("#panel-actions")).toBeVisible();
    await expect(page.locator("#ac-eco-chips")).toBeHidden();
    expect(await page.locator("#ac-table-wrap").evaluate((e) => getComputedStyle(e).maxHeight)).toBe("none");
    expect(await page.locator("#ac-table-wrap").evaluate((e) => getComputedStyle(e).overflowY)).toBe("visible");
  });

  test("the page makes no request of its own for this tab", async ({ page }) => {
    const requests: string[] = [];
    page.on("request", (r) => { if (/^https?:/.test(r.url()) && !r.url().startsWith("https://api.github.com/") && !/fonts\.(googleapis|gstatic)|\.svg/.test(r.url())) requests.push(r.url()); });
    await open(page);
    await page.getByTestId("ac-eco-armor").click();
    await page.getByTestId("ac-search").fill("a");
    await page.locator("#lang-select").selectOption("fr");
    await page.locator("#ac-rate .ac-bar").first().click();
    expect(requests.filter((u) => !u.startsWith("file:"))).toEqual([]);
  });
});

test.describe("builds tab: sizes", () => {
  test("1920x1080: everything is seen at a glance, the table scrolls inside itself and the page does not", async ({ page }) => {
    await page.setViewportSize({ width: 1920, height: 1080 });
    await open(page);
    const m = await page.evaluate(() => {
      const panel = document.getElementById("panel-actions")!;
      const wrap = document.getElementById("ac-table-wrap")!;
      return { panel: panel.scrollHeight - panel.clientHeight, page: document.documentElement.scrollHeight - document.documentElement.clientHeight, wrapH: wrap.clientHeight };
    });
    expect(m.panel).toBeLessThanOrEqual(1);
    expect(m.page).toBeLessThanOrEqual(0);
    expect(m.wrapH).toBeGreaterThan(150);
    for (const id of ["#ac-kpis", "#ac-ring", "#ac-rate", "#ac-dur", "#ac-tl", "#ac-trend", "#ac-table-wrap"]) {
      const box = await page.locator(id).boundingBox();
      expect(box, id).not.toBeNull();
      expect(box!.y + Math.min(box!.height, 60), id).toBeLessThan(1080);
    }
  });

  test("1366x768 and the tab bar still reach every tab", async ({ page }) => {
    await page.setViewportSize({ width: 1366, height: 768 });
    await open(page);
    const m = await page.evaluate(() => ({ x: document.documentElement.scrollWidth - document.documentElement.clientWidth, y: document.documentElement.scrollHeight - document.documentElement.clientHeight }));
    expect(m.x).toBeLessThanOrEqual(0);
    expect(m.y).toBeLessThanOrEqual(0);
    await expect(page.getByTestId("tab-actions")).toBeVisible();
    await expect(page.getByTestId("tab-errors")).toBeVisible();
  });

  test("390x844: no sideways scroll and the table scrolls inside its own region", async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await open(page);
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    expect(overflow).toBeLessThanOrEqual(1);
    await expect(page.getByTestId("ac-table-wrap")).toHaveAttribute("tabindex", "0");
    await expect(page.locator("#ac-kpis li")).toHaveCount(6);
  });
});
