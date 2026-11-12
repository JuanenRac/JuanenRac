import { test, expect, openDashboard, gotoTab, TABS, panel, Variant } from "./helpers";

test.describe("initial load", () => {
  for (const variant of ["full", "minimal", "partial", "empty"] as Variant[]) {
    test(`loads without console or page errors (${variant})`, async ({ page, problems }) => {
      await openDashboard(page, variant);
      await expect(page.locator("h1").first()).toBeVisible();
      await expect(page).toHaveTitle(/Ecosystem Status/);
      await expect(page.locator("html")).toHaveAttribute("lang", "en");
      expect(problems).toEqual([]);
    });
  }

  test("starts on the summary tab with only one panel visible", async ({ page }) => {
    await openDashboard(page);
    await expect(page.getByTestId("tab-summary")).toHaveAttribute("aria-selected", "true");
    for (const id of TABS) {
      if (id === "summary") await expect(panel(page, id)).toBeVisible();
      else await expect(panel(page, id)).toBeHidden();
    }
  });

  test("has exactly 19 tabs, each with its own panel", async ({ page }) => {
    await openDashboard(page);
    await expect(page.locator("[role=tab]")).toHaveCount(19);
    await expect(page.locator("[role=tabpanel]")).toHaveCount(19);
  });
});

test.describe("tabs", () => {
  test("a click opens each tab and shows only its panel", async ({ page }) => {
    await openDashboard(page);
    for (const id of TABS) {
      await gotoTab(page, id);
      await expect(page.getByTestId(`tab-${id}`)).toHaveAttribute("aria-selected", "true");
      await expect(page.locator("[role=tab][aria-selected=true]")).toHaveCount(1);
      await expect(page.locator("[role=tabpanel]:not([hidden])")).toHaveCount(1);
      await expect(page).toHaveURL(new RegExp(`#${id}$`));
    }
  });

  test("the arrow keys, Home and End move between the tabs (roving tabindex)", async ({ page }) => {
    await openDashboard(page);
    await page.getByTestId("tab-summary").focus();
    await page.keyboard.press("ArrowRight");
    await expect(page.getByTestId("tab-hydra-umc")).toBeFocused();
    await expect(page.getByTestId("tab-hydra-umc")).toHaveAttribute("aria-selected", "true");
    await expect(page.getByTestId("tab-hydra-umc")).toHaveAttribute("tabindex", "0");
    await expect(page.getByTestId("tab-summary")).toHaveAttribute("tabindex", "-1");
    await page.keyboard.press("End");
    await expect(page.getByTestId("tab-errors")).toBeFocused();
    await expect(panel(page, "errors")).toBeVisible();
    await page.keyboard.press("ArrowRight"); // wraps around
    await expect(page.getByTestId("tab-summary")).toBeFocused();
    await page.keyboard.press("ArrowLeft"); // wraps back
    await expect(page.getByTestId("tab-errors")).toBeFocused();
    await page.keyboard.press("Home");
    await expect(page.getByTestId("tab-summary")).toBeFocused();
    await expect(panel(page, "summary")).toBeVisible();
  });

  test("only the selected tab is in the Tab order", async ({ page }) => {
    await openDashboard(page);
    const stops = await page.locator("[role=tab]").evaluateAll((tabs) => tabs.filter((t) => (t as HTMLElement).tabIndex >= 0).length);
    expect(stops).toBe(1);
  });

  for (const id of TABS) {
    test(`the hash #${id} opens that tab`, async ({ page }) => {
      await openDashboard(page, "full", `#${id}`);
      await expect(page.getByTestId(`tab-${id}`)).toHaveAttribute("aria-selected", "true");
      await expect(panel(page, id)).toBeVisible();
    });
  }

  test("an unknown hash falls back to the summary", async ({ page }) => {
    await openDashboard(page, "full", "#nonsense");
    await expect(page.getByTestId("tab-summary")).toHaveAttribute("aria-selected", "true");
  });

  test("changing the hash while the page is open changes the tab", async ({ page }) => {
    await openDashboard(page);
    await page.evaluate(() => { location.hash = "inventory"; });
    await expect(panel(page, "inventory")).toBeVisible();
  });

  test("the chosen tab is remembered in localStorage and restored on reload", async ({ page }) => {
    await openDashboard(page);
    await gotoTab(page, "evidence");
    expect(await page.evaluate(() => localStorage.getItem("hydra-dashboard-tab"))).toBe("evidence");
    await page.goto("full/index.html"); // no hash
    await expect(page.getByTestId("tab-evidence")).toHaveAttribute("aria-selected", "true");
  });

  test("the hash wins over the remembered tab", async ({ page }) => {
    await openDashboard(page);
    await gotoTab(page, "evidence");
    await page.goto("full/index.html#urtc");
    await page.reload();
    await expect(page.getByTestId("tab-urtc")).toHaveAttribute("aria-selected", "true");
  });

  test("works when localStorage is not available", async ({ page, problems }) => {
    await page.addInitScript(() => {
      const fail = () => { throw new DOMException("blocked", "SecurityError"); };
      Object.defineProperty(window, "localStorage", { get: fail });
    });
    await openDashboard(page);
    await gotoTab(page, "projects");
    await gotoTab(page, "armor");
    await page.keyboard.press("ArrowRight");
    await expect(page.getByTestId("tab-eh3d")).toHaveAttribute("aria-selected", "true");
    await page.locator("#theme-toggle").click();
    await page.locator("#lang-select").selectOption("de");
    await expect(page.locator("html")).toHaveAttribute("lang", "de");
    expect(problems).toEqual([]);
  });

  test("the per-ecosystem and summary buttons lead to the projects tab filtered", async ({ page }) => {
    await openDashboard(page);
    await gotoTab(page, "urtc");
    await page.getByTestId("show-projects-urtc").click();
    await expect(panel(page, "projects")).toBeVisible();
    await expect(page.getByTestId("filter-eco-urtc")).toHaveAttribute("aria-pressed", "true");
    await expect(page.locator("tr.project-row[data-match=\"1\"]")).toHaveCount(10);
  });
});
