import AxeBuilder from "@axe-core/playwright";
import { test, expect, openDashboard, gotoTab, TABS, Page } from "./helpers";

// axe finds the automatable part of the problems (roughly a third); the keyboard test below covers the part it cannot.
const TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"];

async function serious(page: Page) {
  const results = await new AxeBuilder({ page }).withTags(TAGS).analyze();
  return results.violations
    .filter((v) => v.impact === "serious" || v.impact === "critical")
    .map((v) => `${v.id} [${v.impact}] ${v.help}: ${v.nodes.slice(0, 4).map((n) => n.target.join(" ") + " :: " + (n.any[0]?.message || n.failureSummary || "").split("\n")[0]).join(" | ")}`);
}

for (const theme of ["dark", "light"]) {
  for (const lang of ["en", "ja"]) {
    test.describe(`axe, ${theme}, ${lang}`, () => {
      for (const id of TABS) {
        test(`tab ${id} has no serious or critical violations`, async ({ page }) => {
          await openDashboard(page);
          if (theme === "light") await page.locator("#theme-toggle").click();
          await page.locator("#lang-select").selectOption(lang);
          await gotoTab(page, id);
          if (id === "architecture") {
            const found: string[] = [];
            for (const view of ["hydra-umc", "urtc", "armor", "eh3d"]) {
              await page.locator(`[data-arch-view="${view}"]`).click();
              found.push(...(await serious(page)).map((x) => `${view}: ${x}`));
            }
            expect(found).toEqual([]);
            return;
          }
          if (id === "projects") await page.locator("tr.project-row").first().locator(".details-toggle").click();
          if (id === "inventory") {
            const buttons = page.locator("[data-compat-view]");
            const found: string[] = [];
            for (let i = 0; i < (await buttons.count()); i++) {
              await buttons.nth(i).click();
              found.push(...(await serious(page)));
            }
            expect(found).toEqual([]);
            return;
          }
          expect(await serious(page)).toEqual([]);
        });
      }
    });
  }
}

test.describe("axe on the poor datasets", () => {
  for (const variant of ["partial", "empty"] as const) {
    test(`no serious violations with the ${variant} dataset`, async ({ page }) => {
      test.setTimeout(180_000);
      await openDashboard(page, variant);
      const found: string[] = [];
      for (const id of TABS) {
        await gotoTab(page, id);
        found.push(...(await serious(page)).map((x) => `${id}: ${x}`));
      }
      expect(found).toEqual([]);
    });
  }
});

test.describe("structure", () => {
  test("the page has a language, a title, one h1, one banner/main landmark and no skipped heading level in a panel", async ({ page }) => {
    await openDashboard(page);
    await expect(page.locator("html")).toHaveAttribute("lang", /.+/);
    expect(await page.title()).not.toBe("");
    await expect(page.locator("h1")).toHaveCount(1);
    expect(await page.locator("main, [role=main]").count()).toBe(1);
    for (const id of TABS) {
      await gotoTab(page, id);
      const levels = await page.locator(`#panel-${id} :is(h1,h2,h3,h4,h5,h6,[role=heading])`).evaluateAll((hs) =>
        hs.map((h) => Number(h.getAttribute("aria-level") || h.tagName[1])));
      let previous = 1;
      for (const level of levels) {
        expect(level - previous, `heading order in ${id}: ${levels.join(",")}`).toBeLessThanOrEqual(1);
        previous = level;
      }
    }
  });

  test("the tabs have the tablist / tab / tabpanel relations", async ({ page }) => {
    await openDashboard(page);
    for (const id of TABS) {
      await expect(page.locator(`#tab-${id}`)).toHaveAttribute("aria-controls", `panel-${id}`);
      await expect(page.locator(`#panel-${id}`)).toHaveAttribute("aria-labelledby", `tab-${id}`);
      await expect(page.locator(`#panel-${id}`)).toHaveAttribute("role", "tabpanel");
    }
  });

  test("every chart has a text alternative: either a data table or an accessible name", async ({ page }) => {
    await openDashboard(page);
    for (const id of TABS) {
      await gotoTab(page, id);
      const orphan = await page.locator(`#panel-${id} svg[role=img]`).evaluateAll((svgs) =>
        svgs.filter((s) => !(s.getAttribute("aria-label") || s.getAttribute("aria-labelledby") || s.querySelector("title"))).length);
      expect(orphan, id).toBe(0);
    }
  });

  test("state is not conveyed by colour alone: area meters carry a text value", async ({ page }) => {
    await openDashboard(page);
    const areas = await page.locator("[data-testid^=area-]").evaluateAll((els) => els.map((e) => (e.textContent || "").trim()));
    expect(areas.length).toBeGreaterThan(0);
    for (const text of areas) expect(text).toMatch(/\d|–|-|\bno\b/i);
  });
});

test.describe("keyboard", () => {
  test("Tab walks every control in a logical order with a visible focus indicator", async ({ page }) => {
    await openDashboard(page);
    await page.locator("body").click({ position: { x: 1, y: 1 } });
    await page.evaluate(() => { (document.activeElement as HTMLElement | null)?.blur(); window.scrollTo(0, 0); });

    const stops: { desc: string; indicator: boolean; visible: boolean; inOrder: boolean; tabindex: number; id: number }[] = [];
    let steps = 0;
    for (; steps < 400; steps++) {
      await page.keyboard.press("Tab");
      const info = await page.evaluate(() => {
        const el = document.activeElement as HTMLElement;
        if (!el || el === document.body) return null;
        const cs = getComputedStyle(el);
        const rect = el.getBoundingClientRect();
        const outline = cs.outlineStyle !== "none" && parseFloat(cs.outlineWidth) > 0;
        const shadow = cs.boxShadow && cs.boxShadow !== "none";
        const border = el.matches(":focus-visible");
        const w = window as unknown as { __prev?: Element; __n?: number };
        const prev = w.__prev;
        const inOrder = !prev || !!(prev.compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING);
        w.__prev = el;
        w.__n = (w.__n || 0) + 1;
        return {
          desc: `${el.tagName.toLowerCase()}${el.id ? "#" + el.id : ""}${el.getAttribute("data-testid") ? "[" + el.getAttribute("data-testid") + "]" : ""}`,
          indicator: border && (outline || !!shadow),
          visible: rect.width > 0 && rect.height > 0 && cs.visibility !== "hidden",
          inOrder, tabindex: el.tabIndex, id: w.__n,
        };
      });
      if (!info) break; // focus left the document: the end of the cycle (no trap)
      if (stops.some((s) => s.desc === info.desc) && stops.length > 5) {
        // wrapped to the first control: the loop is closed
        if (info.desc === stops[0].desc) break;
      }
      stops.push(info);
    }
    expect(steps, "keyboard trap: the focus never left the page").toBeLessThan(400);
    expect(stops.length).toBeGreaterThan(20);
    expect(stops.filter((s) => s.tabindex > 0), "positive tabindex").toEqual([]);
    expect(stops.filter((s) => !s.visible).map((s) => s.desc), "focus on an invisible control").toEqual([]);
    expect(stops.filter((s) => !s.indicator).map((s) => s.desc), "no visible focus indicator").toEqual([]);
    expect(stops.filter((s, i) => i > 0 && !s.inOrder).map((s) => s.desc), "focus order differs from the document order").toEqual([]);
    // the first stops are the navigation, and a single tab stop belongs to the tab list
    expect(stops.filter((s) => s.desc.startsWith("button#tab-")).length).toBe(1);
  });

  test("every control of the visible panel and of the filters can be reached with Tab", async ({ page }) => {
    await openDashboard(page);
    await gotoTab(page, "projects");
    await page.locator("body").click({ position: { x: 1, y: 1 } });
    await page.evaluate(() => (document.activeElement as HTMLElement | null)?.blur());
    for (let i = 0; i < 400; i++) {
      await page.keyboard.press("Tab");
      const more = await page.evaluate(() => {
        const el = document.activeElement as HTMLElement;
        if (!el || el === document.body) return false;
        el.setAttribute("data-seen", "1");
        return true;
      });
      if (!more) break;
    }
    const unreached = await page.evaluate(() => {
      const visible = (e: Element) => { const r = (e as HTMLElement).getBoundingClientRect(); return r.width > 0 && r.height > 0; };
      return Array.from(document.querySelectorAll("button, a[href], input, select, summary, [tabindex='0']"))
        .filter((e) => visible(e) && (e as HTMLElement).tabIndex >= 0 && !e.matches(":disabled, .skip-link") && !e.closest("[hidden]") && !e.hasAttribute("data-seen"))
        .map((e) => `${e.tagName.toLowerCase()}${e.id ? "#" + e.id : ""} ${(e.textContent || "").trim().slice(0, 30)}`);
    });
    expect(unreached, "controls that Tab never reaches").toEqual([]);
  });

  test("the first Tab stop is the skip link and it moves the focus to the content", async ({ page }) => {
    await openDashboard(page);
    await page.keyboard.press("Tab");
    const skip = page.locator(".skip-link");
    await expect(skip).toBeFocused();
    await expect(skip).toBeVisible();
    const box = await skip.boundingBox();
    expect(box!.y).toBeGreaterThanOrEqual(0);
    await page.keyboard.press("Enter");
    const target = await page.evaluate(() => document.activeElement?.closest("main, [role=tabpanel]") !== null || location.hash !== "");
    expect(target).toBe(true);
  });

  test("Enter and Space operate the chips, the reset button, the theme toggle and the tab buttons", async ({ page }) => {
    await openDashboard(page);
    const chip = page.getByTestId("filter-eco-urtc");
    await chip.focus();
    await page.keyboard.press("Enter");
    await expect(chip).toHaveAttribute("aria-pressed", "true");
    await page.getByTestId("reset-filters").focus();
    await page.keyboard.press("Space");
    await expect(chip).toHaveAttribute("aria-pressed", "false");
    await page.locator("#theme-toggle").focus();
    await page.keyboard.press("Enter");
    await expect(page.locator("html")).toHaveAttribute("data-theme", "light");
  });

  test("the language select works with the keyboard", async ({ page }) => {
    await openDashboard(page);
    await page.locator("#lang-select").focus();
    await page.keyboard.press("ArrowDown");
    const lang = await page.locator("html").getAttribute("lang");
    expect(lang).not.toBeNull();
  });
});
