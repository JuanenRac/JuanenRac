import { test, expect, openDashboard, gotoTab, LANGS, LEFTOVER, visibleText, Page } from "./helpers";

// The card "Shared contract pins" of the Sentinel tab. Fixture (full): A.R.M.O.R. with one pin behind and one current, URTC with one pin behind and a note
// that some repositories could not be read, HYDRA-UMC with no machine readable pins.

async function open(page: Page) {
  await page.clock.setFixedTime(new Date("2001-12-21T12:30:00Z"));
  await openDashboard(page, "full");
  await gotoTab(page, "sentinel");
}

test.describe("shared contract pins", () => {
  test("each ecosystem shows its current version and its pins, the behind ones first", async ({ page }) => {
    await open(page);
    await expect(page.locator("#pn-title")).toHaveText("Shared contract pins");
    const armor = page.getByTestId("pn-table-armor").locator("tbody tr");
    await expect(armor).toHaveCount(2);
    await expect(armor.first()).toHaveAttribute("data-state", "behind");
    await expect(armor.first().locator(".sn-gl")).toHaveText("▲");
    await expect(armor.first()).toContainText("Behind");
    await expect(armor.last()).toContainText("Current");
    await expect(page.locator("#pn-body .pn-block[data-eco=armor]")).toContainText("0.8.1.1");
  });

  test("a source that is not published is said, and unread repositories are not counted as current", async ({ page }) => {
    await open(page);
    await expect(page.locator("#pn-body .pn-block[data-eco=hydra-umc]")).toContainText("No pins published");
    await expect(page.locator("#pn-body .pn-block[data-eco=urtc]")).toContainText("could not be read");
  });

  test("the card is translated in the 8 languages with no leftover key", async ({ page }) => {
    await open(page);
    const titles = new Set<string>();
    for (const lang of LANGS) {
      await page.locator("#lang-select").selectOption(lang);
      expect(await visibleText(page), lang).not.toMatch(LEFTOVER);
      titles.add((await page.locator("#pn-title").textContent()) || "");
    }
    expect(titles.size).toBe(8);
    await page.locator("#lang-select").selectOption("pt");
    await expect(page.locator("#pn-title")).toHaveText("Versões fixadas dos contratos partilhados");
  });
});
