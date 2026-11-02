import { test, expect, openDashboard, gotoTab, panel, shown, visibleRows, paintedRows, LANGS } from "./helpers";

const TOTAL = 40;
const PAGE = 25;
const SCOPES = ["all", "hydra-umc", "urtc", "armor", "eh3d", "electro-hobby-3d"] as const;

const scope = (page: any, id: string) => page.getByTestId(`scope-${id}`);

test.describe("scope bar of the projects tab", () => {
  test.beforeEach(async ({ page }) => {
    await openDashboard(page);
    await gotoTab(page, "projects");
  });

  test("the bar has All, the four ecosystems and the cross-cutting scope, and starts on All", async ({ page }) => {
    for (const id of SCOPES) await expect(scope(page, id)).toBeVisible();
    await expect(scope(page, "all")).toHaveAttribute("aria-pressed", "true");
    await expect(scope(page, "urtc")).toHaveAttribute("aria-pressed", "false");
    await expect(scope(page, "all").locator("b")).toHaveText(String(TOTAL));
    await expect(scope(page, "urtc").locator("b")).toHaveText("10");
  });

  test("there are no comparison boxes and no table or cards switch", async ({ page }) => {
    await expect(page.locator("#panel-projects input[type=checkbox]")).toHaveCount(0);
    await expect(page.locator("[data-view-toggle], [data-testid*=compare], [data-testid*=cards]")).toHaveCount(0);
  });

  test("All is paginated: not every project is painted at once", async ({ page }) => {
    expect(await paintedRows(page)).toBe(PAGE);
    expect(await visibleRows(page)).toBe(TOTAL); // the counter counts the matches, not the page
    expect(await shown(page)).toEqual({ shown: TOTAL, total: TOTAL });
    await expect(page.getByTestId("pager")).toBeVisible();
    await expect(page.locator("#pager-info")).toContainText("1");
    await expect(page.getByTestId("pager-prev")).toBeDisabled();
  });

  test("next and previous move through the pages and the last page has the rest", async ({ page }) => {
    await page.getByTestId("pager-next").click();
    expect(await paintedRows(page)).toBe(TOTAL - PAGE);
    await expect(page.getByTestId("pager-next")).toBeDisabled();
    await expect(page.getByTestId("pager-prev")).toBeEnabled();
    expect(await page.evaluate(() => location.hash)).toBe("#projects?page=2");
    await page.getByTestId("pager-prev").click();
    expect(await paintedRows(page)).toBe(PAGE);
    expect(await page.evaluate(() => location.hash)).toBe("#projects");
  });

  test("the pages never repeat or lose a project", async ({ page }) => {
    const names = async () => page.locator("tr.project-row:not(.hidden)").evaluateAll((r) => r.map((x) => (x as HTMLElement).dataset.name));
    const first = await names();
    await page.getByTestId("pager-next").click();
    const second = await names();
    expect(new Set([...first, ...second]).size).toBe(TOTAL);
  });

  for (const id of ["hydra-umc", "urtc", "armor", "eh3d"]) {
    test(`choosing ${id} paints only its 10 projects, no pager, N of M = 10 of ${TOTAL}`, async ({ page }) => {
      await scope(page, id).click();
      await expect(scope(page, id)).toHaveAttribute("aria-pressed", "true");
      await expect(scope(page, "all")).toHaveAttribute("aria-pressed", "false");
      expect(await paintedRows(page)).toBe(10);
      expect(await shown(page)).toEqual({ shown: 10, total: TOTAL });
      await expect(page.getByTestId("pager")).toBeHidden();
      const ecos = await page.locator("tr.project-row:not(.hidden)").evaluateAll((r) => [...new Set(r.map((x) => (x as HTMLElement).dataset.ecosystem))]);
      expect(ecos).toEqual([id]);
      await expect(page.getByTestId(`filter-eco-${id}`)).toHaveAttribute("aria-pressed", "true"); // the side panel shows the same scope
      expect(await page.evaluate(() => location.hash)).toBe(`#projects?scope=${id}`);
    });
  }

  test("the cross-cutting scope with no project says so instead of listing others", async ({ page }) => {
    await scope(page, "electro-hobby-3d").click();
    expect(await paintedRows(page)).toBe(0);
    expect(await shown(page)).toEqual({ shown: 0, total: TOTAL });
    await expect(page.locator("#empty-results")).toBeVisible();
  });

  test("the families of the chosen ecosystem are listed under the bar and narrow the list", async ({ page }) => {
    await expect(page.locator("#scope-sub-hint")).toBeVisible(); // All: pick an ecosystem first
    await scope(page, "urtc").click();
    await expect(page.locator("#scope-sub-hint")).toBeHidden();
    const chips = page.locator("#scope-sub-chips button");
    expect(await chips.count()).toBeGreaterThan(0);
    const before = await visibleRows(page);
    await chips.first().click();
    await expect(chips.first()).toHaveAttribute("aria-pressed", "true");
    const after = await visibleRows(page);
    expect(after).toBeGreaterThan(0);
    expect(after).toBeLessThanOrEqual(before);
    expect(await shown(page)).toEqual({ shown: after, total: TOTAL });
    await chips.first().click();
    expect(await visibleRows(page)).toBe(before);
  });

  test("scope and the side filters combine; the counter follows both", async ({ page }) => {
    await scope(page, "hydra-umc").click();
    await page.getByTestId("filter-maturity-production").click();
    expect(await visibleRows(page)).toBe(2);
    expect(await shown(page)).toEqual({ shown: 2, total: TOTAL });
    await page.getByTestId("project-search").fill("no-such-project-xyz");
    expect(await shown(page)).toEqual({ shown: 0, total: TOTAL });
    await page.getByTestId("reset-filters").click();
    await expect(scope(page, "all")).toHaveAttribute("aria-pressed", "true"); // reset also leaves the scope
    expect(await visibleRows(page)).toBe(TOTAL);
  });

  test("the ecosystem chip of the side panel and the scope bar are the same thing", async ({ page }) => {
    await page.getByTestId("filter-eco-armor").click();
    await expect(scope(page, "armor")).toHaveAttribute("aria-pressed", "true");
    await page.getByTestId("filter-eco-armor").click();
    await expect(scope(page, "all")).toHaveAttribute("aria-pressed", "true");
  });

  test("changing a filter goes back to the first page", async ({ page }) => {
    await page.getByTestId("pager-next").click();
    await page.getByTestId("filter-status-ok").click();
    await expect(page.locator("#pager-info")).toHaveAttribute("data-page", "1");
  });

  test("the pager and the scope bar are named in every language", async ({ page }) => {
    for (const lang of LANGS) {
      await page.locator("#lang-select").selectOption(lang);
      const nav = await page.getByTestId("pager").getAttribute("aria-label");
      expect(nav, lang).toBeTruthy();
      expect((await page.locator("#pager-info").innerText()).match(/[{}]/), lang).toBeNull();
      expect((await page.locator("#scope-t").innerText()).length, lang).toBeGreaterThan(1);
      if (lang !== "en") {
        expect(nav, lang).not.toBe("Project list pages");
        expect(await page.getByTestId("pager-next").innerText(), lang).not.toBe("Next");
      }
    }
  });
});

test.describe("scope in the address and remembered", () => {
  test("the address names the scope and the page", async ({ page }) => {
    await openDashboard(page, "full", "#projects?scope=armor");
    await expect(panel(page, "projects")).toBeVisible();
    await expect(scope(page, "armor")).toHaveAttribute("aria-pressed", "true");
    expect(await paintedRows(page)).toBe(10);
    await page.goto("full/index.html#projects?scope=all&page=2");
    expect(await paintedRows(page)).toBe(TOTAL - PAGE);   // let the change of address take effect before reloading
    await page.reload();
    expect(await paintedRows(page)).toBe(TOTAL - PAGE);
  });

  test("an unknown scope or a broken page number is ignored", async ({ page }) => {
    await openDashboard(page, "full", "#projects?scope=nonsense&page=zzz");
    await expect(panel(page, "projects")).toBeVisible();
    await expect(scope(page, "all")).toHaveAttribute("aria-pressed", "true");
    expect(await paintedRows(page)).toBe(PAGE);
    await page.goto("full/index.html#projects?scope=%E0%A4%A");
    await page.reload();
    await expect(panel(page, "projects")).toBeVisible();
  });

  test("changing the hash while open changes the scope", async ({ page }) => {
    await openDashboard(page, "full", "#projects");
    await page.evaluate(() => { location.hash = "projects?scope=eh3d"; });
    await expect(scope(page, "eh3d")).toHaveAttribute("aria-pressed", "true");
    expect(await paintedRows(page)).toBe(10);
  });

  test("the scope is remembered and comes back the next time the projects are opened", async ({ page }) => {
    await openDashboard(page);
    await gotoTab(page, "projects");
    await scope(page, "urtc").click();
    expect(await page.evaluate(() => localStorage.getItem("hydra-dashboard-scope"))).toBe("urtc");
    await page.goto("full/index.html");
    await expect(page.getByTestId("tab-projects")).toHaveAttribute("aria-selected", "true"); // the tab is remembered too
    await expect(scope(page, "urtc")).toHaveAttribute("aria-pressed", "true");
    expect(await paintedRows(page)).toBe(10);
  });

  test("the remembered scope does not change the summary figures until the projects are opened", async ({ page }) => {
    await openDashboard(page);
    await gotoTab(page, "projects");
    await scope(page, "urtc").click();
    await page.goto("full/index.html#summary");
    await page.reload();
    await expect(page.locator("#health-total")).toHaveText(String(TOTAL));
  });

  test("the address wins over the remembered scope", async ({ page }) => {
    await openDashboard(page);
    await gotoTab(page, "projects");
    await scope(page, "urtc").click();
    await page.goto("full/index.html#projects?scope=armor");
    await page.reload();
    await expect(scope(page, "armor")).toHaveAttribute("aria-pressed", "true");
  });

  test("works when localStorage is blocked", async ({ page, problems }) => {
    await page.addInitScript(() => {
      Object.defineProperty(window, "localStorage", { get: () => { throw new DOMException("blocked", "SecurityError"); } });
    });
    await openDashboard(page, "full", "#projects");
    await scope(page, "armor").click();
    expect(await paintedRows(page)).toBe(10);
    await page.getByTestId("pager").isHidden();
    expect(problems).toEqual([]);
  });
});

test.describe("scope with other data", () => {
  test("with a single project the pager stays hidden and the bar still works", async ({ page }) => {
    await openDashboard(page, "minimal", "#projects");
    await expect(page.getByTestId("pager")).toBeHidden();
    expect(await paintedRows(page)).toBe(1);
    await scope(page, "urtc").click();
    expect(await paintedRows(page)).toBe(0);
    await expect(page.locator("#empty-results")).toBeVisible();
  });

  test("with no data at all the bar shows zero counts and nothing is listed", async ({ page }) => {
    await openDashboard(page, "empty", "#projects");
    expect(await paintedRows(page)).toBe(0);
    await expect(scope(page, "all").locator("b")).toHaveText("0");
  });
});
