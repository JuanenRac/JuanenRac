import { test, expect, openDashboard, gotoTab, panel, stubNetwork, TABS, ECOSYSTEMS, LANGS, visibleText, LEFTOVER } from "./helpers";

// The page is generated from a deliberately poor dataset: it has to say "no data" or "not verified" and must never
// invent a healthy state.

test.describe("every lookup failed (partial)", () => {
  test.beforeEach(async ({ page }) => {
    await openDashboard(page, "partial");
  });

  test("no project is shown as OK", async ({ page }) => {
    await gotoTab(page, "projects");
    const rows = await page.locator("tr.project-row").count();
    expect(rows).toBe(16);
    await expect(page.locator("tr.project-row.status-ok")).toHaveCount(0);
    await expect(page.locator("tr.project-row.status-error")).toHaveCount(rows);
    await expect(page.locator("#health-resolved")).toHaveText("0");
    await expect(page.locator("#health-percent")).not.toHaveText(/^(100|[1-9]\d?(\.\d+)?)%$/);
  });

  test("the error indicator is red and counts the failures, never green", async ({ page }) => {
    const card = page.getByTestId("kpi-errors");
    await expect(card).toHaveClass(/kpi-bad/);
    await expect(card).not.toHaveClass(/kpi-ok/);
    await expect(page.getByTestId("kpi-resolved")).toHaveClass(/kpi-bad/);
    const errors = Number(await page.locator("#health-errors").innerText());
    expect(errors).toBeGreaterThanOrEqual(16);
  });

  test("the area meters and the charts say there is no data instead of drawing a state", async ({ page }) => {
    await expect(page.locator(".no-data").first()).toBeVisible();
    for (const eco of ECOSYSTEMS) {
      const progress = panel(page, "summary").getByTestId(`progress-${eco}`);
      await expect(progress).toBeVisible();
      await expect(progress.locator(".area.good, .area.fair, .area.poor")).toHaveCount(0);
      await expect(progress.locator(".ring-value[stroke-dasharray]")).toHaveCount(0);
    }
    await expect(page.getByTestId("chart-months")).toHaveCount(0);
    await expect(page.getByTestId("latest-releases")).toHaveCount(0);
  });

  test("the CI chart does not paint any repository green", async ({ page }) => {
    await expect(page.locator(".seg-ci-success")).toHaveCount(0);
    await expect(page.locator(".chart-figure .seg-ci-success, .sw-ci-success").first()).toHaveCount(0);
  });

  test("the errors tab reports the API failure", async ({ page }) => {
    await gotoTab(page, "errors");
    await expect(panel(page, "errors")).toContainText("repository listing");
  });

  test("the per-ecosystem tabs show no data, not an empty success", async ({ page }) => {
    for (const eco of ECOSYSTEMS) {
      await gotoTab(page, eco);
      await expect(panel(page, eco).locator(".no-data").first()).toBeVisible();
      await expect(panel(page, eco).locator(".area.good")).toHaveCount(0);
    }
  });

  test("no leftover keys or undefined in any tab", async ({ page }) => {
    for (const id of TABS) {
      await gotoTab(page, id);
      expect((await visibleText(page)).match(LEFTOVER), id).toBeNull();
    }
  });
});

test.describe("one project and no activity (minimal)", () => {
  test.beforeEach(async ({ page }) => {
    await openDashboard(page, "minimal");
  });

  test("one row, the KPI says one, no activity chart is invented", async ({ page }) => {
    await gotoTab(page, "projects");
    await expect(page.locator("tr.project-row")).toHaveCount(1);
    await expect(page.locator("#health-total")).toHaveText("1");
    await expect(page.getByTestId("chart-months")).toHaveCount(0);
    await expect(page.locator("[data-i18n=no_activity]").first()).toBeAttached();
  });

  test("the other ecosystems show zero projects and no data", async ({ page }) => {
    for (const eco of ["urtc", "armor", "eh3d"]) {
      await page.getByTestId(`filter-eco-${eco}`).click();
      await expect(page.locator("tr.project-row[data-match=\"1\"]")).toHaveCount(0);
      await expect(page.locator("#empty-results")).toBeVisible();
      await page.getByTestId("reset-filters").click();
    }
  });

  test("every tab and language renders without leftovers", async ({ page }) => {
    for (const lang of ["en", "ja"]) {
      await page.locator("#lang-select").selectOption(lang);
      for (const id of TABS) {
        await gotoTab(page, id);
        expect((await visibleText(page)).match(LEFTOVER), `${lang}/${id}`).toBeNull();
      }
    }
  });
});

test.describe("nothing at all (empty)", () => {
  test("renders, shows zero, and has no row, no chart and no healthy claim", async ({ page, problems }) => {
    await openDashboard(page, "empty");
    await expect(page.locator("#health-total")).toHaveText("0");
    await expect(page.locator("#health-resolved")).toHaveText("0");
    await gotoTab(page, "projects");
    await expect(page.locator("tr.project-row")).toHaveCount(0);
    await expect(page.locator(".area.good, .seg-ci-success")).toHaveCount(0);
    await expect(page.getByTestId("kpi-errors")).not.toHaveClass(/kpi-ok/);
    await expect(page.getByTestId("kpi-resolved")).not.toHaveClass(/kpi-ok/);
    for (const id of TABS) {
      await gotoTab(page, id);
      expect((await visibleText(page)).match(LEFTOVER), id).toBeNull();
    }
    expect(problems).toEqual([]);
  });

  test("the empty page works in the eight languages", async ({ page }) => {
    await openDashboard(page, "empty");
    for (const lang of LANGS) {
      await page.locator("#lang-select").selectOption(lang);
      await expect(page.locator("html")).toHaveAttribute("lang", lang);
    }
  });
});

test.describe("build freshness", () => {
  test("a reachable API shows the age of the last build", async ({ page }) => {
    await openDashboard(page);
    const badge = page.locator("#dashboard-freshness");
    await expect(badge).toHaveClass(/freshness-fresh/);
  });

  test("an unreachable API says unknown instead of fresh", async ({ page }) => {
    await page.unroute(/^https?:\/\//);
    await stubNetwork(page, { freshnessFails: true });
    await openDashboard(page);
    await expect(page.locator("#dashboard-freshness")).toHaveClass(/freshness-unknown/);
    await expect(page.locator("#dashboard-freshness")).not.toHaveClass(/freshness-fresh/);
  });
});
