import { test, expect, openDashboard, gotoTab, TABS, Page } from "./helpers";
import * as fs from "fs";

// SHOTS=dir keeps a screenshot of every tab and viewport for a visual review.
const SHOTS = process.env.SHOTS || "";

async function overflow(page: Page) {
  return page.evaluate(() => ({
    scrollW: document.documentElement.scrollWidth, clientW: document.documentElement.clientWidth,
    scrollH: document.documentElement.scrollHeight, clientH: document.documentElement.clientHeight,
    bodyScrollW: document.body.scrollWidth,
  }));
}

async function shoot(page: Page, name: string) {
  if (!SHOTS) return;
  fs.mkdirSync(SHOTS, { recursive: true });
  await page.screenshot({ path: `${SHOTS}/${name}.png` });
}

test.describe("1920x1080: the page is an application, it does not scroll", () => {
  test.use({ viewport: { width: 1920, height: 1080 } });
  for (const id of TABS) {
    test(`tab ${id} fits without page scroll`, async ({ page }) => {
      await openDashboard(page);
      await gotoTab(page, id);
      const o = await overflow(page);
      expect(o.scrollH, "vertical page scroll").toBeLessThanOrEqual(o.clientH);
      expect(o.scrollW, "horizontal page scroll").toBeLessThanOrEqual(o.clientW);
      await shoot(page, `1920-${id}`);
    });
  }

  test("a long panel scrolls inside itself, not the page", async ({ page }) => {
    await openDashboard(page);
    await gotoTab(page, "projects");
    const inner = await page.evaluate(() => {
      const wrap = document.querySelector("#panel-projects .table-wrapper") as HTMLElement;
      return { scrolls: wrap.scrollHeight > wrap.clientHeight, overflowY: getComputedStyle(wrap).overflowY };
    });
    expect(inner.scrolls).toBe(true);
    expect(["auto", "scroll"]).toContain(inner.overflowY);
  });
});

test.describe("1366x768: laptop", () => {
  test.use({ viewport: { width: 1366, height: 768 } });
  for (const id of TABS) {
    test(`tab ${id} has no horizontal scroll and no page scroll`, async ({ page }) => {
      await openDashboard(page);
      await gotoTab(page, id);
      const o = await overflow(page);
      expect(o.scrollW, "horizontal").toBeLessThanOrEqual(o.clientW);
      expect(o.scrollH, "vertical").toBeLessThanOrEqual(o.clientH);
      await shoot(page, `1366-${id}`);
    });
  }
});

for (const [label, width, height] of [["768x1024 tablet", 768, 1024], ["390x844 phone", 390, 844]] as [string, number, number][]) {
  test.describe(label, () => {
    test.use({ viewport: { width, height }, hasTouch: true });

    for (const id of TABS) {
      test(`tab ${id} has no horizontal page scroll`, async ({ page }) => {
        await openDashboard(page);
        await gotoTab(page, id);
        const o = await overflow(page);
        expect(o.scrollW, "horizontal").toBeLessThanOrEqual(o.clientW);
        await shoot(page, `${width}-${id}`);
      });
    }

    test("the tabs scroll sideways inside their bar", async ({ page }) => {
      await openDashboard(page);
      const bar = await page.evaluate(() => {
        const el = document.querySelector("nav.tabs") as HTMLElement;
        return { overflowX: getComputedStyle(el).overflowX, scrollW: el.scrollWidth, clientW: el.clientWidth };
      });
      expect(["auto", "scroll"]).toContain(bar.overflowX);
      if (width < 600) expect(bar.scrollW).toBeGreaterThan(bar.clientW);
    });

    test("the active tab is scrolled into view when it is selected", async ({ page }) => {
      await openDashboard(page);
      await page.getByTestId("tab-errors").scrollIntoViewIfNeeded();
      await page.getByTestId("tab-errors").click();
      const box = await page.getByTestId("tab-errors").boundingBox();
      expect(box!.x).toBeGreaterThanOrEqual(0);
      expect(box!.x + box!.width).toBeLessThanOrEqual(width + 1);
    });

    test("the filters are collapsed and the button expands and collapses them", async ({ page }) => {
      await openDashboard(page);
      const toggle = page.locator("#filters-toggle");
      await expect(toggle).toBeVisible();
      await expect(toggle).toHaveAttribute("aria-expanded", "false");
      await expect(page.getByTestId("project-search")).toBeHidden();
      await toggle.click();
      await expect(toggle).toHaveAttribute("aria-expanded", "true");
      await expect(page.getByTestId("project-search")).toBeVisible();
      await page.getByTestId("project-search").fill("urtc-fixture-01");
      await expect(page.locator("#panel-projects")).toBeVisible();
      await toggle.click();
      await expect(page.getByTestId("project-search")).toBeHidden();
    });

    test("the projects table scrolls inside its own wrapper", async ({ page }) => {
      await openDashboard(page);
      await gotoTab(page, "projects");
      const o = await overflow(page);
      expect(o.scrollW).toBeLessThanOrEqual(o.clientW);
      const wrapperOverflow = await page.evaluate(() => getComputedStyle(document.querySelector("#panel-projects .table-wrapper")!).overflowX);
      expect(["auto", "scroll"]).toContain(wrapperOverflow);
    });

    test("tap targets of the main controls are at least 24 px", async ({ page }) => {
      await openDashboard(page);
      for (const selector of ["[role=tab]", "#theme-toggle", "#lang-select", "#filters-toggle"]) {
        const boxes = await page.locator(selector).evaluateAll((els) => els.map((e) => { const r = e.getBoundingClientRect(); return [r.width, r.height]; }));
        for (const [w, h] of boxes) {
          expect(w, selector).toBeGreaterThanOrEqual(24);
          expect(h, selector).toBeGreaterThanOrEqual(24);
        }
      }
    });
  });
}

test.describe("desktop: the filters are always visible", () => {
  test.use({ viewport: { width: 1920, height: 1080 } });
  test("the filter toggle is hidden and the search is visible", async ({ page }) => {
    await openDashboard(page);
    await expect(page.locator("#filters-toggle")).toBeHidden();
    await expect(page.getByTestId("project-search")).toBeVisible();
  });
});
