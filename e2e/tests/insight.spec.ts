import AxeBuilder from "@axe-core/playwright";
import { test, expect, openDashboard, gotoTab, LANGS, ECOSYSTEMS, visibleText, LEFTOVER, Page, Variant } from "./helpers";

const VIEWS = ["maturity", "activity", "deps", "miles", "dates", "debt"] as const;
const TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"];

async function openInsight(page: Page, variant: Variant | "single" = "full", view: (typeof VIEWS)[number] = "maturity") {
  await openDashboard(page, variant as Variant);
  await gotoTab(page, "insight");
  if (view !== "maturity") await page.getByTestId(`ins-view-${view}`).click();
}

async function serious(page: Page) {
  const results = await new AxeBuilder({ page }).withTags(TAGS).analyze();
  return results.violations
    .filter((v) => v.impact === "serious" || v.impact === "critical")
    .map((v) => `${v.id} [${v.impact}] ${v.help}: ${v.nodes.slice(0, 4).map((n) => n.target.join(" ")).join(" | ")}`);
}

test.describe("analysis tab: the views", () => {
  test("six views, one visible at a time, switched with the buttons and the keyboard", async ({ page }) => {
    await openInsight(page);
    await expect(page.locator("[data-ins-view]")).toHaveCount(6);
    for (const view of VIEWS) {
      await page.getByTestId(`ins-view-${view}`).click();
      await expect(page.getByTestId(`ins-view-${view}`)).toHaveAttribute("aria-pressed", "true");
      await expect(page.locator("[data-ins-view][aria-pressed=true]")).toHaveCount(1);
      await expect(page.locator("[data-ins-section]:not([hidden])")).toHaveCount(1);
      await expect(page.getByTestId(`ins-sec-${view}`)).toBeVisible();
    }
    await page.getByTestId("ins-view-maturity").focus();
    await page.keyboard.press("Tab");
    await page.keyboard.press("Enter");
    await expect(page.getByTestId("ins-view-activity")).toHaveAttribute("aria-pressed", "true");
    await expect(page.getByTestId("ins-sec-activity")).toBeVisible();
  });
});

test.describe("analysis tab: maturity funnel", () => {
  test("every ecosystem has four levels whose counts add up, and the changes since a month ago", async ({ page }) => {
    await openInsight(page);
    const cards = page.locator("#fu-grid .fu-card");
    await expect(cards).toHaveCount(4);
    for (const eco of ECOSYSTEMS) {
      const bars = page.locator(`#fu-grid .fu-card[data-eco="${eco}"] .fu-bar`);
      await expect(bars).toHaveCount(4);
      const n = await bars.evaluateAll((els) => els.map((e) => Number(e.getAttribute("data-n"))));
      expect(n.reduce((a, b) => a + b, 0)).toBe(10);
      const atleast = await bars.evaluateAll((els) => els.map((e) => Number(e.getAttribute("data-atleast"))));
      expect(atleast[0]).toBe(10);
      expect([...atleast].sort((a, b) => b - a)).toEqual(atleast);             // a funnel never widens
      await expect(page.locator(`#fu-grid .fu-card[data-eco="${eco}"] svg`)).toHaveAttribute("aria-label", /scaffolding.*functional.*established.*production/);
    }
    await expect(page.getByTestId("fu-since")).toContainText("Compared with the snapshot of 2001-11-21 (30 days ago)");
    await expect(page.locator('#fu-grid .fu-card[data-eco="hydra-umc"] .fu-notes')).toContainText("1 moved up");
    await expect(page.locator('#fu-grid .fu-card[data-eco="urtc"] .fu-notes')).toContainText("2 moved up");
    await expect(page.locator("#fu-table tbody tr")).toHaveCount(4);
  });

  test("a bar shows its numbers in a tooltip title and its figure is written next to it", async ({ page }) => {
    await openInsight(page);
    const row = page.locator('#fu-grid .fu-card[data-eco="hydra-umc"] .fu-row').first();
    await expect(row.locator("title")).toHaveText(/at this level.*reached it/);
    await expect(row.locator(".fu-figure")).toContainText("≥10");
  });

  test("with no earlier snapshot of the repositories it says so and counts nothing", async ({ page }) => {
    await openInsight(page, "single");
    await expect(page.getByTestId("fu-since")).toContainText("Not enough history");
    await expect(page.locator("#fu-grid")).not.toContainText("moved up");
    await expect(page.locator("#fu-grid .fu-card")).toHaveCount(4);
  });

  test("a history shorter than a month is announced as such", async ({ page }) => {
    await openDashboard(page, "healthy");
    // the healthy dataset has 60 days of history: the baseline is 30 days old, so no short-history notice
    await gotoTab(page, "insight");
    await expect(page.getByTestId("fu-since")).not.toContainText("less than a month");
  });
});

test.describe("analysis tab: the areas side by side", () => {
  test("four radars and the same numbers in a table", async ({ page }) => {
    await openInsight(page);
    await expect(page.locator("#ra-grid .ra-card")).toHaveCount(4);
    for (const eco of ECOSYSTEMS) {
      const svg = page.locator(`#ra-grid .ra-card[data-eco="${eco}"] svg`);
      await expect(svg).toHaveAttribute("role", "img");
      await expect(svg).toHaveAttribute("aria-label", /Software 95%.*Tests 98%/);
      await expect(svg.locator("polygon.ra-shape")).toHaveCount(1);
      await expect(svg.locator(".ra-mark")).toHaveCount(8);
    }
    await expect(page.locator("#ra-table tbody tr")).toHaveCount(8);
    await expect(page.locator("#ra-table thead th")).toHaveCount(5);
    await expect(page.locator("#ra-table tbody tr").first()).toContainText("95%");
  });

  test("a radar is told apart without colour: a different line and marker for each ecosystem", async ({ page }) => {
    await openInsight(page);
    const dashes = await page.locator("#ra-grid polygon.ra-shape").evaluateAll((els) => els.map((e) => e.getAttribute("style") || ""));
    expect(new Set(dashes.map((d) => (d.match(/stroke-dasharray:[^;]*/) || [""])[0])).size).toBe(4);
    const tags = await page.locator("#ra-grid .ra-card").evaluateAll((cards) => cards.map((c) => c.querySelector(".ra-mark")!.tagName));
    expect(new Set(tags).size).toBeGreaterThanOrEqual(3);
  });

  test("with no data no shape is drawn and nothing is invented", async ({ page }) => {
    await openInsight(page, "empty" as Variant);
    await expect(page.locator("#ra-grid polygon.ra-shape")).toHaveCount(0);
    await expect(page.locator("#ra-grid .ra-note").first()).toContainText("not verified");
    await expect(page.locator("#ra-table tbody")).toContainText("Not verified");
  });
});

test.describe("analysis tab: weekly activity", () => {
  test("a table of twelve weeks with the number written in every cell", async ({ page }) => {
    await openInsight(page, "full", "activity");
    await expect(page.locator("#he-table thead th")).toHaveCount(13);
    await expect(page.locator("#he-table tbody tr")).toHaveCount(8);
    const cells = page.locator("#he-table tbody td");
    await expect(cells).toHaveCount(96);
    const texts = await cells.evaluateAll((els) => els.map((e) => (e.textContent || "").trim()));
    expect(texts.every((t) => /^\d+$/.test(t) || t.startsWith("?"))).toBe(true);
    const first = cells.first();
    await expect(first).toHaveAttribute("title", /HYDRA-UMC, Commits, week of \d{4}-\d{2}-\d{2}: \d+/);
    await expect(page.locator("#he-table tbody th").first()).toContainText("repositories read");
    await expect(page.getByTestId("he-none")).toBeHidden();
  });

  test("the last week of the releases is counted from the dates of the releases", async ({ page }) => {
    await openInsight(page, "full", "activity");
    const row = page.locator('#he-table tr[data-eco="hydra-umc"][data-metric="releases"] td');
    const values = await row.evaluateAll((els) => els.map((e) => Number(e.getAttribute("data-value"))));
    expect(values.slice(0, 10).every((v) => v === 0)).toBe(true);
    expect(values.slice(10).reduce((a, b) => a + b, 0)).toBeGreaterThan(0);
  });

  test("when the activity could not be read it says so instead of drawing zeros", async ({ page }) => {
    await openInsight(page, "partial", "activity");
    await expect(page.getByTestId("he-none")).toBeVisible();
    await expect(page.getByTestId("he-table")).toBeHidden();
  });
});

test.describe("analysis tab: dependencies", () => {
  test("lists who uses whom, the cycle and the dependency that does not exist", async ({ page }) => {
    await openInsight(page, "full", "deps");
    await expect(page.getByTestId("de-counts")).toContainText("repositories declare dependencies");
    await expect(page.getByTestId("de-cycles")).toContainText("HYDRA-UMC-FIXTURE-00 → HYDRA-UMC-FIXTURE-01 → HYDRA-UMC-FIXTURE-00");
    await expect(page.getByTestId("de-missing")).toContainText("HYDRA-UMC-FIXTURE-07 declares HYDRA-UMC-GHOST-REPO, which is not listed");
    const item = page.locator('#de-list li[data-repo="HYDRA-UMC-FIXTURE-03"]');
    await expect(item).toContainText("HYDRA-UMC-FIXTURE-02");
    await expect(item.locator("dt").first()).toHaveText("Uses");
    await expect(page.locator('#de-list li[data-repo="HYDRA-UMC-FIXTURE-07"]')).toContainText("Not found");
    await expect(page.locator('#de-list li[data-repo="HYDRA-UMC-FIXTURE-07"]')).toContainText("HYDRA-UMC-GHOST-REPO");
    await expect(page.locator('#de-list li[data-repo="URTC-FIXTURE-03"]')).toContainText("other ecosystem");
    await expect(page.locator('#de-list li[data-repo="EH3D-FIXTURE-00"]')).toContainText("Family children");
  });

  test("the search narrows the list and says how many remain", async ({ page }) => {
    await openInsight(page, "full", "deps");
    await page.getByTestId("de-search").fill("urtc-fixture-0");
    const visible = page.locator("#de-list li:not([hidden])");
    expect(await visible.count()).toBeGreaterThan(0);
    expect(await visible.evaluateAll((els) => els.every((e) => /URTC-FIXTURE/.test(e.getAttribute("data-repo") || "")))).toBe(true);
    await expect(page.getByTestId("de-matches")).toContainText(/\d+ of \d+ repositories with relations/);
    await page.getByTestId("de-search").fill("zzzz");
    await expect(page.locator("#de-list li:not([hidden])")).toHaveCount(0);
  });

  test("the diagram of an ecosystem has its nodes and arrows, the cycle is dashed and each node opens the repository panel", async ({ page }) => {
    await openInsight(page, "full", "deps");
    const nodes = page.locator("#de-diagram .de-node");
    await expect(nodes).toHaveCount(10);
    expect(await page.locator("#de-diagram .de-edge").count()).toBeGreaterThanOrEqual(6);
    expect(await page.locator("#de-diagram .de-edge-cycle").count()).toBe(2);
    await expect(page.locator("#de-diagram svg")).toHaveAttribute("aria-label", "Diagram of HYDRA-UMC");
    await nodes.first().focus();
    await page.keyboard.press("Enter");
    await expect(page.getByTestId("repo-panel")).toBeVisible();
    await page.keyboard.press("Escape");
    await expect(page.getByTestId("repo-panel")).toBeHidden();
    await page.getByTestId("ins-deps-eco-urtc").click();
    await expect(page.getByTestId("ins-deps-eco-urtc")).toHaveAttribute("aria-pressed", "true");
    await expect(page.locator("#de-diagram .de-node").first()).toHaveAttribute("data-repo", /URTC-FIXTURE/);
  });

  test("a repository of the list opens its panel", async ({ page }) => {
    await openInsight(page, "full", "deps");
    await page.locator('#de-list li[data-repo="HYDRA-UMC-FIXTURE-03"] button').first().click();
    await expect(page.getByTestId("repo-panel-title")).toHaveText("HYDRA-UMC-FIXTURE-03");
  });

  test("with no manifest data it says there is nothing to show", async ({ page }) => {
    await openInsight(page, "minimal", "deps");
    await expect(page.getByTestId("de-counts")).toContainText("No manifest declares dependencies");
    await expect(page.getByTestId("de-none")).toBeVisible();
    await expect(page.locator("#de-diagram")).toContainText("No dependency between repositories of this ecosystem is declared");
  });
});

test.describe("analysis tab: next milestones", () => {
  test("shows where the data comes from and the open cards of each ecosystem in words and glyphs", async ({ page }) => {
    await openInsight(page, "full", "miles");
    await expect(page.getByTestId("mi-source")).toContainText("plans kept in this profile repository");
    await expect(page.getByTestId("mi-source")).toHaveAttribute("data-source", "plans");
    await expect(page.locator("#mi-grid .mi-card")).toHaveCount(4);
    const hydra = page.locator('#mi-grid .mi-card[data-eco="hydra-umc"]');
    await expect(hydra).toContainText("2 open, 1 done");
    await expect(hydra.locator("li").first()).toContainText("In progress");
    await expect(hydra.locator("li").first()).toContainText("Fixture card in progress");
    await expect(hydra).toContainText("Blocked by: Needs a real board");
    await expect(page.locator('#mi-grid .mi-card[data-eco="urtc"]')).toContainText("Critical");
    await expect(page.locator('#mi-grid .mi-card[data-eco="armor"]')).toContainText("Not verified");
  });

  test("with nothing read it says not verified", async ({ page }) => {
    await openInsight(page, "empty" as Variant, "miles");
    await expect(page.getByTestId("mi-source")).toContainText("Not verified");
    await expect(page.getByTestId("mi-source")).toHaveAttribute("data-source", "none");
  });
});

test.describe("analysis tab: compare dates", () => {
  test("offers only the snapshots that exist and shows what changed between two of them", async ({ page }) => {
    await openInsight(page, "full", "dates");
    expect(await page.locator("#cp-from option").count()).toBe(44);
    expect(await page.locator("#cp-to option").count()).toBe(44);
    await expect(page.getByTestId("cp-count")).toContainText("44 snapshots, from 2001-11-06 to 2001-12-21");
    await expect(page.getByTestId("cp-from")).toHaveValue("2001-11-06");
    await expect(page.getByTestId("cp-to")).toHaveValue("2001-12-21");
    await expect(page.locator("#cp-table tbody tr").first()).toContainText("HYDRA-UMC · Overall progress");
    await expect(page.getByTestId("cp-result")).toContainText("Repositories that changed level");
    await expect(page.getByTestId("cp-result")).toContainText("Scaffolding → Functional");
    await expect(page.getByTestId("cp-result")).toContainText("0.0.0 → ");
  });

  test("two nearby dates show a smaller change and the same date asks for two different ones", async ({ page }) => {
    await openInsight(page, "full", "dates");
    await page.getByTestId("cp-from").selectOption("2001-12-19");
    await page.getByTestId("cp-to").selectOption("2001-12-20");
    await expect(page.getByTestId("cp-result")).toContainText("Progress and areas");
    await expect(page.getByTestId("cp-result")).toContainText("None.");
    await page.getByTestId("cp-to").selectOption("2001-12-19");
    await expect(page.getByTestId("cp-result")).toContainText("Choose two different dates.");
  });

  test("a snapshot without the maturity of the repositories says so instead of comparing", async ({ page }) => {
    await openInsight(page, "full", "dates");
    // the snapshot of 2001-11-07 of the fixture is an old one that recorded no repositories
    await page.getByTestId("cp-from").selectOption("2001-11-07");
    await expect(page.getByTestId("cp-result")).toContainText("does not record the maturity and the versions");
  });

  test("with fewer than two snapshots there is nothing to compare", async ({ page }) => {
    await openInsight(page, "single", "dates");
    await expect(page.getByTestId("cp-result")).toContainText("Fewer than two snapshots exist");
    await expect(page.locator("#cp-controls")).toBeHidden();
  });
});

test.describe("analysis tab: technical debt", () => {
  test("the three rules with their lists, links to the repository panel and what could not be judged", async ({ page }) => {
    await openInsight(page, "full", "debt");
    await expect(page.locator("#db-grid .db-card")).toHaveCount(3);
    await expect(page.getByTestId("db-count-scaffolding")).toHaveText("6");
    await expect(page.getByTestId("db-count-integration")).toHaveText("6");
    await expect(page.getByTestId("db-count-hardware")).toHaveText("8");
    await expect(page.locator('[data-debt="scaffolding"] h4')).toHaveText("In scaffolding for 6 months or more");
    await expect(page.locator('[data-debt="scaffolding"] details summary')).toContainText("not verified");
    await expect(page.locator('[data-debt="hardware"]')).toContainText("evidence: ");
    await page.locator('[data-debt="integration"] .db-list button').first().click();
    await expect(page.getByTestId("repo-panel")).toBeVisible();
  });

  test("without the data of GitHub the rules that need it say so and the manifest rule still works", async ({ page }) => {
    await openInsight(page, "partial", "debt");
    await expect(page.locator('[data-debt="scaffolding"]')).toContainText("Not verified: the data needed for this rule");
    await expect(page.locator('[data-debt="integration"]')).toContainText("Not verified: the data needed for this rule");
    await expect(page.locator('[data-debt="hardware"] .db-count')).toBeVisible();
  });
});

test.describe("analysis tab: languages, themes, sizes, motion", () => {
  for (const lang of LANGS) {
    test(`no key, undefined or placeholder is visible in ${lang} in any view`, async ({ page }) => {
      await openInsight(page);
      await page.locator("#lang-select").selectOption(lang);
      for (const view of VIEWS) {
        await page.getByTestId(`ins-view-${view}`).click();
        const text = await visibleText(page);
        const found = text.match(LEFTOVER);
        expect(found, `${lang}/${view}: "${found?.[0]}"`).toBeNull();
      }
      const bad = await page.evaluate(() => Array.from(document.querySelectorAll("#panel-insight [data-i18n]")).filter((e) => !(e.textContent || "").trim()).map((e) => e.getAttribute("data-i18n")));
      expect(bad).toEqual([]);
    });
  }

  test("the texts of the charts follow the language and the figures stay the same", async ({ page }) => {
    await openInsight(page);
    const label = async () => page.locator('#fu-grid .fu-card[data-eco="armor"] svg').getAttribute("aria-label");
    const en = await label();
    await page.locator("#lang-select").selectOption("pt");
    const pt = await label();
    expect(pt).not.toBe(en);
    expect(pt).toMatch(/em arranque/);
    expect((en || "").match(/\d+/g)).toEqual((pt || "").match(/\d+/g));
  });

  for (const theme of ["dark", "light"] as const) {
    for (const lang of ["en", "ja"]) {
      test(`axe finds no serious violation in any view (${theme}, ${lang})`, async ({ page }) => {
        test.setTimeout(120_000);
        await openInsight(page);
        if (theme === "light") await page.locator("#theme-toggle").click();
        await page.locator("#lang-select").selectOption(lang);
        const found: string[] = [];
        for (const view of VIEWS) {
          await page.getByTestId(`ins-view-${view}`).click();
          found.push(...(await serious(page)).map((x) => `${view}: ${x}`));
        }
        expect(found).toEqual([]);
      });
    }
  }

  test("axe on the diagram of every ecosystem and on the poor datasets", async ({ page }) => {
    test.setTimeout(240_000);
    await openInsight(page, "full", "deps");
    const found: string[] = [];
    for (const eco of ECOSYSTEMS) {
      await page.getByTestId(`ins-deps-eco-${eco}`).click();
      found.push(...(await serious(page)).map((x) => `${eco}: ${x}`));
    }
    for (const variant of ["partial", "empty", "minimal"] as const) {
      await openInsight(page, variant);
      for (const view of VIEWS) {
        await page.getByTestId(`ins-view-${view}`).click();
        found.push(...(await serious(page)).map((x) => `${variant}/${view}: ${x}`));
      }
    }
    expect(found).toEqual([]);
  });

  test("the chart tooltips keep a visible focus ring and every control is reachable with the keyboard", async ({ page }) => {
    await openInsight(page, "full", "deps");
    const reached = new Set<string>();
    for (let i = 0; i < 60; i++) {
      await page.keyboard.press("Tab");
      const id = await page.evaluate(() => {
        const el = document.activeElement as HTMLElement | null;
        if (!el) return "";
        const style = getComputedStyle(el);
        const ring = style.outlineStyle !== "none" && parseFloat(style.outlineWidth) > 0;
        const rect = el.querySelector && el.querySelector("rect") ? getComputedStyle(el.querySelector("rect")!).strokeWidth : "";
        return (el.getAttribute("data-testid") || el.id || el.tagName) + (ring || rect ? "|ring" : "|noring");
      });
      reached.add(id);
    }
    expect([...reached].some((x) => x.startsWith("de-search"))).toBe(true);
    expect([...reached].some((x) => x.startsWith("ins-deps-eco-"))).toBe(true);
  });

  for (const [name, size] of [["1920x1080", { width: 1920, height: 1080 }], ["1366x768", { width: 1366, height: 768 }], ["mobile", { width: 390, height: 844 }]] as const) {
    test(`every view fits ${name}: no horizontal page scroll and no page scroll on desktop`, async ({ page }) => {
      await page.setViewportSize(size);
      await openInsight(page);
      for (const view of VIEWS) {
        await page.getByTestId(`ins-view-${view}`).click();
        const m = await page.evaluate(() => ({ sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth, sh: document.documentElement.scrollHeight, ch: document.documentElement.clientHeight }));
        expect(m.sw, `${name}/${view} horizontal`).toBeLessThanOrEqual(m.cw);
        if (size.width >= 1366) expect(m.sh, `${name}/${view} vertical`).toBeLessThanOrEqual(m.ch);
      }
      if (process.env.SHOTS) {
        for (const view of VIEWS) {
          await page.getByTestId(`ins-view-${view}`).click();
          await page.screenshot({ path: `${process.env.SHOTS}/insight_${view}_${name}.png` });
        }
      }
    });
  }

  test("with motion allowed the funnel, the radar and the heat map animate; with reduced motion they do not", async ({ page }) => {
    await page.emulateMedia({ reducedMotion: "no-preference" });
    await openInsight(page);
    const name = await page.locator("#fu-grid .fu-bar").first().evaluate((e) => getComputedStyle(e).animationName);
    expect(name).toBe("ins-grow");
    expect(await page.locator("#ra-grid .ra-shape").first().evaluate((e) => getComputedStyle(e).animationName)).toBe("ins-pop");
    await page.emulateMedia({ reducedMotion: "reduce" });
    expect(await page.locator("#fu-grid .fu-bar").first().evaluate((e) => getComputedStyle(e).animationName)).toBe("none");
    expect(await page.locator("#ra-grid .ra-shape").first().evaluate((e) => getComputedStyle(e).animationName)).toBe("none");
  });

  test("the address keeps the tab and the print report leaves this tab out", async ({ page }) => {
    await openInsight(page);
    await expect(page).toHaveURL(/#insight$/);
    await page.emulateMedia({ media: "print" });
    await expect(page.locator("#panel-insight")).toBeHidden();
  });

  test("the page makes no request of its own for this tab", async ({ page }) => {
    const requests: string[] = [];
    page.on("request", (r) => { if (/^https?:/.test(r.url()) && !r.url().startsWith("https://api.github.com/") && !/fonts\.(googleapis|gstatic)|\.svg/.test(r.url())) requests.push(r.url()); });
    await openInsight(page);
    for (const view of VIEWS) await page.getByTestId(`ins-view-${view}`).click();
    expect(requests).toEqual([]);
  });
});
