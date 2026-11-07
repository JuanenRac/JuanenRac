import { test, expect, openDashboard, gotoTab, LANGS, LEFTOVER, visibleText, Variant } from "./helpers";
import type { Page } from "@playwright/test";

// The tab "Scripts": the GitHub workflows of every repository (triggers, jobs, the actions they use and how the version of each one is fixed) and the scripts of
// tools/ and scripts/ by language, read once a day (data/scripts-stats.json) and embedded in the page.
// Fixture (full): 40 repositories in 4 ecosystems and 5 types, 39 read (three of them last known figures) and 1 not read; 4 of the read ones have no workflow.

async function open(page: Page, variant: Variant = "full") {
  await openDashboard(page, variant);
  await gotoTab(page, "scripts");
}

const number = (text: string | null) => Number((text || "").replace(/[^\d]/g, ""));

test.describe("scripts tab: figures", () => {
  test("the tab sits after Changelog and shows the title, the badge and seven figures", async ({ page }) => {
    await open(page);
    const ids = await page.locator("[role=tab]").evaluateAll((tabs) => tabs.map((t) => t.getAttribute("data-testid")));
    expect(ids.indexOf("tab-scripts")).toBe(ids.indexOf("tab-changelog") + 1);
    await expect(page.getByTestId("tab-scripts")).toHaveText("Scripts");
    await expect(page.locator("#sc-title")).toHaveText("Workflows and scripts");
    await expect(page.getByTestId("sc-badge")).toHaveText("Read from the repositories");
    await expect(page.getByTestId("sc-kpis").locator("li")).toHaveCount(7);
    await expect(page.getByTestId("sc-k-repos").locator("b")).toHaveText("35 / 40");
    await expect(page.getByTestId("sc-stale")).toBeHidden();
  });

  test("the figures add up with the table", async ({ page }) => {
    await open(page);
    const k = (name: string) => page.getByTestId(`sc-k-${name}`).locator("b");
    const foot = page.getByTestId("sc-total").locator("td");
    // columns of the table by repository: repository (th), ecosystem, type, workflows, jobs, uses, not pinned, scheduled, by hand, files, lines, languages
    expect(number(await foot.nth(2).textContent())).toBe(number(await k("workflows").textContent()));
    expect(number(await foot.nth(3).textContent())).toBe(number(await k("jobs").textContent()));
    expect(number(await foot.nth(4).textContent())).toBe(number(await k("uses").textContent()));
    expect(number(await foot.nth(9).textContent())).toBe(number(await k("lines").textContent()));
    const unpinned = number((await k("unpinned").textContent())!.split("(")[0]);
    expect(unpinned).toBeGreaterThan(0);
    expect(unpinned).toBeLessThanOrEqual(number(await k("uses").textContent()));
  });
});

test.describe("scripts tab: charts", () => {
  test("the triggers, the pins and the languages have one bar for the whole, each ecosystem and each type", async ({ page }) => {
    await open(page);
    for (const [id, legend] of [["sc-trig-chart", 8], ["sc-pin-chart", 5], ["sc-lang-chart", 5]] as const) {
      await expect(page.getByTestId(`${id}-svg`).locator("g[data-row]")).toHaveCount(10);
      await expect(page.getByTestId(`${id}-legend`).locator("li")).toHaveCount(legend);
      await expect(page.getByTestId(`${id}-table`).locator("tbody tr")).toHaveCount(10);
    }
  });

  test("the bars have the relief of the other tabs: shadow, dark lower half, light edge", async ({ page }) => {
    await open(page);
    const svg = page.getByTestId("sc-trig-chart-svg");
    expect(await svg.locator(".bar-depth").count()).toBeGreaterThan(5);
    expect(await svg.locator(".seg-bevel").count()).toBeGreaterThan(5);
    expect(await svg.locator(".seg-edge").count()).toBeGreaterThan(5);
  });

  test("a segment shows its value on hover and on keyboard focus", async ({ page }) => {
    await open(page);
    const seg = page.getByTestId("sc-pin-chart-svg").locator(".cd-seg").first();
    const label = (await seg.getAttribute("aria-label")) || "";
    expect(label).toMatch(/uses \(.*%\)/);
    await seg.hover();
    await expect(page.getByTestId("cd-tip")).toHaveText(label);
    await page.mouse.move(2, 2);
    await seg.focus();
    await expect(page.getByTestId("cd-tip")).toHaveText(label);
    await page.keyboard.press("Escape");
    await expect(page.getByTestId("cd-tip")).toBeHidden();
  });

  test("the most used actions can be shown 10, 15 or 30 at a time", async ({ page }) => {
    await open(page);
    const rows = page.getByTestId("sc-top-chart-svg").locator("g[data-row]");
    expect(await rows.count()).toBeLessThanOrEqual(15);
    await page.getByTestId("sc-top-n").selectOption("10");
    expect(await rows.count()).toBeLessThanOrEqual(10);
  });

  test("the actions that are not pinned to a commit are listed, never the ones of the owner", async ({ page }) => {
    await open(page);
    const items = page.getByTestId("sc-unp-list").locator("li");
    expect(await items.count()).toBeGreaterThan(0);
    const names = await items.evaluateAll((els) => els.map((e) => e.getAttribute("data-action") || ""));
    expect(names.every((n) => !n.startsWith("JuanenRac/") && !n.includes("d23441a48e51"))).toBe(true);
    expect(names).toContain("actions/setup-python@v5");
  });
});

test.describe("scripts tab: the table", () => {
  test("sorting, filtering, searching and grouping", async ({ page }) => {
    await open(page);
    const rows = page.getByTestId("sc-table").locator("tbody tr");
    await expect(page.getByTestId("sc-matches")).toHaveAttribute("data-total", "40");
    await page.getByTestId("sc-sort-wf").click();
    const first = number(await rows.first().locator("td").nth(3).textContent());
    await page.getByTestId("sc-sort-wf").click();
    expect(number(await rows.first().locator("td").nth(3).textContent())).not.toBe(first);
    await page.getByTestId("sc-eco-armor").click();
    expect(await rows.count()).toBeLessThan(40);
    await page.getByTestId("sc-search").fill("fixture-03");
    await expect(page.getByTestId("sc-matches")).toHaveAttribute("data-shown", /^\d+$/);
    await page.getByTestId("sc-search").fill("");
    await page.getByTestId("sc-eco-all").click();
    await page.getByTestId("sc-group").selectOption("eco");
    await expect(page.getByTestId("sc-table").locator("tbody tr")).toHaveCount(4);
    await page.getByTestId("sc-group").selectOption("type");
    await expect(page.getByTestId("sc-table").locator("tbody tr")).toHaveCount(5);
  });

  test("a repository that could not be read is said, not counted as zero", async ({ page }) => {
    await open(page);
    await expect(page.getByTestId("sc-table").locator("tr[data-state=unread]")).toHaveCount(1);
  });
});

test.describe("scripts tab: states and languages", () => {
  test("a stale document says how old it is", async ({ page }) => {
    await open(page, "stale");
    await expect(page.getByTestId("sc-stale")).toBeVisible();
    await expect(page.getByTestId("sc-stale")).toHaveText("The figures are 4 days old (read on 2001-12-17).");
  });

  for (const variant of ["partial", "empty"] as const) {
    test(`${variant}: nothing read says so instead of drawing zeros`, async ({ page }) => {
      await open(page, variant);
      await expect(page.getByTestId("sc-not-read")).toBeVisible();
      await expect(page.getByTestId("sc-body")).toBeHidden();
    });
  }

  for (const lang of LANGS) {
    test(`${lang}: the tab is translated`, async ({ page }) => {
      await open(page);
      await page.locator("#lang-select").selectOption(lang);
      const title = await page.locator("#sc-title").innerText();
      if (lang !== "en") expect(title).not.toBe("Workflows and scripts");
      if (lang === "es") expect(title).toBe("Workflows y scripts");
      const text = await visibleText(page);
      expect(text).not.toMatch(LEFTOVER);
      for (const id of ["sc-trig-chart-svg", "sc-pin-chart-svg", "sc-lang-chart-svg", "sc-top-chart-svg", "sc-rank-chart-svg"]) {
        const label = (await page.getByTestId(id).getAttribute("aria-label")) || "";
        expect(label, `${lang} ${id}`).not.toMatch(/\{|\}|undefined/);
      }
    });
  }
});
