import { test, expect, openDashboard, gotoTab, panel, shown, visibleRows, LANGS } from "./helpers";

const TOTAL = 40;

test.describe("search and filters", () => {
  test.beforeEach(async ({ page }) => {
    await openDashboard(page);
  });

  test("the counter starts at N of M with every project", async ({ page }) => {
    expect(await shown(page)).toEqual({ shown: TOTAL, total: TOTAL });
    expect(await visibleRows(page)).toBe(TOTAL);
    await expect(page.locator("#filters-count")).toContainText(String(TOTAL));
    await expect(page.getByTestId("reset-filters")).toBeDisabled();
  });

  test("searching by name opens the projects tab and narrows the rows", async ({ page }) => {
    await page.getByTestId("project-search").fill("urtc-fixture-03");
    await expect(panel(page, "projects")).toBeVisible();
    expect(await visibleRows(page)).toBe(1);
    expect(await shown(page)).toEqual({ shown: 1, total: TOTAL });
    await expect(page.locator("tr.project-row:not(.hidden)")).toContainText("URTC-FIXTURE-03");
  });

  test("the search is case-insensitive and ignores surrounding spaces", async ({ page }) => {
    await page.getByTestId("project-search").fill("  ARMOR-Fixture-07 ");
    expect(await visibleRows(page)).toBe(1);
  });

  test("searching by description finds the project that carries the text", async ({ page }) => {
    await page.getByTestId("project-search").fill("zzdesc17");
    expect(await visibleRows(page)).toBe(1);
    await page.getByTestId("project-search").fill("searchable text");
    expect(await visibleRows(page)).toBe(TOTAL);
  });

  test("searching by stack and by deployment target", async ({ page }) => {
    await page.getByTestId("project-search").fill("rust");
    expect(await visibleRows(page)).toBe(10);
    await page.getByTestId("project-search").fill("mobile");
    expect(await visibleRows(page)).toBe(10);
  });

  test("a search without matches shows the empty message and a zero counter", async ({ page }) => {
    await page.getByTestId("project-search").fill("no-such-project-xyz");
    expect(await visibleRows(page)).toBe(0);
    await expect(page.locator("#empty-results")).toBeVisible();
    expect(await shown(page)).toEqual({ shown: 0, total: TOTAL });
    await expect(page.locator("#health-total")).toHaveText("0");
    await page.getByTestId("reset-filters").click();
    await expect(page.locator("#empty-results")).toBeHidden();
    expect(await visibleRows(page)).toBe(TOTAL);
  });

  for (const [testid, expected] of [
    ["filter-eco-hydra-umc", 10], ["filter-eco-urtc", 10], ["filter-eco-armor", 10], ["filter-eco-eh3d", 10],
    ["filter-maturity-production", 10], ["filter-maturity-scaffolding", 10],
    ["filter-deploy-cm5", 10], ["filter-deploy-mobile", 10],
    ["filter-role-api", 8], ["filter-role-service", 8], ["filter-role-firmware", 8],
    ["filter-status-error", 4], ["filter-status-ok", 36],
  ] as [string, number][]) {
    test(`the filter ${testid} leaves ${expected} projects and a second click clears it`, async ({ page }) => {
      const chip = page.getByTestId(testid);
      await chip.click();
      await expect(chip).toHaveAttribute("aria-pressed", "true");
      await expect(panel(page, "projects")).toBeVisible();
      expect(await visibleRows(page)).toBe(expected);
      expect(await shown(page)).toEqual({ shown: expected, total: TOTAL });
      await chip.click();
      await expect(chip).toHaveAttribute("aria-pressed", "false");
      expect(await visibleRows(page)).toBe(TOTAL);
    });
  }

  test("the family select filters by family", async ({ page }) => {
    const options = await page.getByTestId("filter-family").locator("option").evaluateAll((o) => o.map((x) => (x as HTMLOptionElement).value));
    expect(options.length).toBeGreaterThan(2);
    await page.getByTestId("filter-family").selectOption(options[1]);
    const n = await visibleRows(page);
    expect(n).toBeGreaterThan(0);
    expect(n).toBeLessThan(TOTAL);
    const families = await page.locator("tr.project-row:not(.hidden)").evaluateAll((r) => [...new Set(r.map((x) => (x as HTMLElement).dataset.family))]);
    expect(families).toHaveLength(1);
  });

  test("combined filters intersect: ecosystem + maturity + deployment", async ({ page }) => {
    await page.getByTestId("filter-eco-hydra-umc").click();
    await page.getByTestId("filter-maturity-production").click();
    const afterTwo = await visibleRows(page);
    expect(afterTwo).toBe(2);
    await page.getByTestId("filter-deploy-mobile").click();
    const afterThree = await visibleRows(page);
    expect(afterThree).toBeLessThanOrEqual(afterTwo);
    const rows = await page.locator("tr.project-row:not(.hidden)").evaluateAll((r) =>
      r.map((x) => { const d = (x as HTMLElement).dataset; return [d.ecosystem, d.maturity, d.deploy]; }));
    for (const row of rows) expect(row).toEqual(["hydra-umc", "production", "mobile"]);
  });

  test("filters and search combine; an impossible combination is empty", async ({ page }) => {
    await page.getByTestId("filter-eco-urtc").click();
    await page.getByTestId("project-search").fill("armor-fixture");
    expect(await visibleRows(page)).toBe(0);
    await expect(page.locator("#empty-results")).toBeVisible();
    await page.getByTestId("project-search").fill("urtc-fixture-0");
    expect(await visibleRows(page)).toBe(10);
  });

  test("the ecosystem banners and family headers follow the filters", async ({ page }) => {
    await page.getByTestId("filter-eco-armor").click();
    const banners = page.locator(".ecosystem-banner-row:not(.hidden)");
    await expect(banners).toHaveCount(1);
    await expect(banners).toHaveAttribute("data-ecosystem-banner", "armor");
    expect(await page.locator(".family-header-row:not(.hidden)").count()).toBeGreaterThan(0);
    await expect(page.locator(".family-header-row:not(.hidden):not([data-ecosystem=armor])")).toHaveCount(0);
  });

  test("reset clears the search, every chip and the family", async ({ page }) => {
    await page.getByTestId("project-search").fill("fixture-01");
    await page.getByTestId("filter-maturity-functional").click();
    await page.getByTestId("filter-family").selectOption({ index: 1 });
    await expect(page.getByTestId("reset-filters")).toBeEnabled();
    await page.getByTestId("reset-filters").click();
    await expect(page.getByTestId("project-search")).toHaveValue("");
    await expect(page.locator(".sidebar .chip[aria-pressed=true]")).toHaveCount(0);
    await expect(page.getByTestId("filter-family")).toHaveValue("all");
    expect(await visibleRows(page)).toBe(TOTAL);
    await expect(page.getByTestId("reset-filters")).toBeDisabled();
  });

  test("the filters are available from every tab and lead to the projects", async ({ page }) => {
    for (const tab of ["summary", "evidence", "architecture", "errors"]) {
      await gotoTab(page, tab);
      await page.getByTestId("filter-eco-eh3d").click();
      await expect(panel(page, "projects")).toBeVisible();
      await page.getByTestId("reset-filters").click();
    }
  });

  test("the 'show the projects' button goes to the projects tab", async ({ page }) => {
    await page.getByTestId("show-projects").click();
    await expect(panel(page, "projects")).toBeVisible();
  });

  test("the counter is right in every language after filtering", async ({ page }) => {
    await page.getByTestId("filter-eco-urtc").click();
    for (const lang of LANGS) {
      await page.locator("#lang-select").selectOption(lang);
      const text = await page.locator("#filters-count").innerText();
      expect(text, lang).toMatch(/10/);
      expect(text, lang).toMatch(/40/);
    }
  });

  test("a filtered row that gets hidden closes its detail row", async ({ page }) => {
    await gotoTab(page, "projects");
    const toggle = page.locator("tr.project-row").first().locator(".details-toggle");
    await toggle.click();
    await expect(toggle).toHaveAttribute("aria-expanded", "true");
    await page.getByTestId("project-search").fill("no-such-project-xyz");
    await expect(toggle).toHaveAttribute("aria-expanded", "false");
  });
});
