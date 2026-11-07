import { test, expect, openDashboard, gotoTab } from "./helpers";

// The life of the charts: key figures count up to their value, what is red pulses a little, hovering a segment dims the others. With less motion asked for, none of it moves.

test.describe("charts with life", () => {
  test("a key figure ends with its exact text when motion is allowed", async ({ page }) => {
    await page.emulateMedia({ reducedMotion: "no-preference" });
    await openDashboard(page);
    await gotoTab(page, "code");
    await expect(page.getByTestId("cd-k-repos").locator("b")).toHaveText("39 / 40", { timeout: 4000 });
    await expect(page.getByTestId("cd-k-code").locator("b")).toHaveText(/^[\d.,\s  ]+$/, { timeout: 4000 });
    await gotoTab(page, "scripts");
    await expect(page.getByTestId("sc-k-repos").locator("b")).toHaveText("35 / 40", { timeout: 4000 });
  });

  test("with reduced motion the figure is the text from the first frame and nothing pulses", async ({ page }) => {
    await page.emulateMedia({ reducedMotion: "reduce" });
    await openDashboard(page);
    await gotoTab(page, "scripts");
    await expect(page.getByTestId("sc-k-repos").locator("b")).toHaveText("35 / 40");
    const names = await page.locator(".ac-kpi, .ac-sw").evaluateAll((els) => els.map((e) => getComputedStyle(e).animationName));
    expect(names.every((n) => n === "none")).toBe(true);
  });

  test("hovering a segment of a chart dims the others", async ({ page }) => {
    await page.emulateMedia({ reducedMotion: "no-preference" });
    await openDashboard(page);
    await gotoTab(page, "code");
    const segs = page.getByTestId("cd-prop-svg").locator(".cd-seg");
    await segs.first().hover();
    const dimmed = await segs.nth(1).evaluate((e) => Number(getComputedStyle(e).opacity));
    expect(dimmed).toBeLessThan(1);
  });
});
