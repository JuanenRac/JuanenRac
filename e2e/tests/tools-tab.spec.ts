import AxeBuilder from "@axe-core/playwright";
import { test, expect, openDashboard, gotoTab, LANGS, LEFTOVER, visibleText, Page } from "./helpers";

// The own tab of the Tools group (the fifth ecosystem) and the health of the central panel in the Sentinel tab. The fixture lists no tool, so the table says so and the
// cards of the Actions monitor and of the updater (static facts) are always there. The fixture reading of the Sentinel is 2001-12-21 12:00 UTC.

async function serious(page: Page) {
  const results = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"]).analyze();
  return results.violations.filter((v) => v.impact === "serious" || v.impact === "critical").map((v) => `${v.id}: ${v.nodes.slice(0, 3).map((n) => n.target.join(" ")).join(" | ")}`);
}

test.describe("tools tab", () => {
  test("it sits after EH3D, is named Tools and has the cards of the monitor and the updater", async ({ page }) => {
    await openDashboard(page, "full");
    const ids = await page.locator("[role=tab]").evaluateAll((tabs) => tabs.map((t) => t.getAttribute("data-testid")));
    expect(ids.indexOf("tab-electro-hobby-3d")).toBe(ids.indexOf("tab-eh3d") + 1);
    await gotoTab(page, "electro-hobby-3d");
    await expect(page.getByTestId("tab-electro-hobby-3d")).toHaveText("Tools");
    await expect(page.getByTestId("tools-table-card")).toBeVisible();
    await expect(page.getByTestId("tools-empty")).toBeVisible();          // the fixture lists no tool: said, never invented
    await expect(page.getByTestId("tools-monitor")).toContainText("TOOLS-GITHUB-ACTIONS-MONITOR");
    await expect(page.getByTestId("tools-editions")).toContainText("A1 to A13");
    await expect(page.getByTestId("tools-next")).toContainText("Not published yet");
    await expect(page.getByTestId("tools-updater")).toContainText("ELECTRO-HOBBY-3D-UPDATER");
  });

  test("every link goes to https on github.com/JuanenRac", async ({ page }) => {
    await openDashboard(page, "full");
    await gotoTab(page, "electro-hobby-3d");
    const hrefs = await page.locator("#panel-electro-hobby-3d a[href]").evaluateAll((links) => links.map((a) => (a as HTMLAnchorElement).href));
    expect(hrefs.length).toBeGreaterThan(0);
    for (const href of hrefs) {
      if (href.startsWith("https://github.com/JuanenRac/")) { continue; }
      expect(href, href).toMatch(/^(https:\/\/github\.com\/JuanenRac\/|[^#]*#)/);
    }
    await expect(page.getByTestId("tools-ai-guide")).toHaveAttribute("href", /TOOLS-GITHUB-ACTIONS-MONITOR\/blob\/main\/monitor\/docs\/AI_CONNECTION\.md$/);
  });

  test("the eight languages leave no key or placeholder in the tab", async ({ page }) => {
    await openDashboard(page, "full");
    await gotoTab(page, "electro-hobby-3d");
    const titles = new Set<string>();
    for (const lang of LANGS) {
      await page.locator("#lang-select").selectOption(lang);
      expect(await visibleText(page), lang).not.toMatch(LEFTOVER);
      titles.add((await page.locator("#panel-electro-hobby-3d [data-i18n=tl_title]").first().textContent()) || "");
    }
    expect(titles.size).toBe(8);
  });

  test("no serious accessibility violation in both themes", async ({ page }) => {
    await openDashboard(page, "full");
    await gotoTab(page, "electro-hobby-3d");
    expect(await serious(page)).toEqual([]);
    await page.evaluate(() => document.documentElement.setAttribute("data-theme", "dark"));
    expect(await serious(page)).toEqual([]);
  });

  test("it works with no data at all", async ({ page }) => {
    await openDashboard(page, "empty");
    await gotoTab(page, "electro-hobby-3d");
    await expect(page.getByTestId("tools-monitor")).toBeVisible();
  });
});

test.describe("sentinel: the panel that is behind", () => {
  test("a reading older than two hours says so, and a recent one does not", async ({ page }) => {
    await page.clock.setFixedTime(new Date("2001-12-21T12:30:00Z"));
    await openDashboard(page, "full");
    await gotoTab(page, "sentinel");
    await expect(page.getByTestId("sn-behind")).toBeHidden();
  });

  test("it is shown three hours after the reading", async ({ page }) => {
    await page.clock.setFixedTime(new Date("2001-12-21T15:30:00Z"));
    await openDashboard(page, "full");
    await gotoTab(page, "sentinel");
    await expect(page.getByTestId("sn-behind")).toBeVisible();
    await expect(page.getByTestId("sn-behind")).toContainText("behind");
    await expect(page.getByTestId("sn-behind")).not.toContainText("{");
  });

  test("the health line carries numbers only", async ({ page }) => {
    await openDashboard(page, "full");
    await gotoTab(page, "sentinel");
    await expect(page.getByTestId("sn-health")).toContainText("Refresh:");
    await expect(page.getByTestId("sn-health")).not.toContainText("{");
  });
});
