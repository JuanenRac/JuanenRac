import AxeBuilder from "@axe-core/playwright";
import { test, expect, openDashboard, gotoTab, LANGS, LEFTOVER, visibleText, Page, Variant } from "./helpers";

// "Declared against verified": the manifest declares an evidence level, the CI of the repository publishes records, the page compares them.
// Fixture (full): of 40 repositories 7 verified, 3 declare more than they prove, 5 failing, 5 expired, 10 publish nothing, 5 with invalid records, 5 not readable.

const STATES = ["verified", "below", "failing", "expired", "nodata", "invalid", "unread"] as const;
const FULL: Record<string, number> = { verified: 7, below: 3, failing: 5, expired: 5, nodata: 10, invalid: 5, unread: 5 };

async function serious(page: Page) {
  const results = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"]).analyze();
  return results.violations.filter((v) => v.impact === "serious" || v.impact === "critical").map((v) => `${v.id}: ${v.nodes.slice(0, 3).map((n) => n.target.join(" ")).join(" | ")}`);
}

async function open(page: Page, variant: Variant = "full") {
  await openDashboard(page, variant);
  await gotoTab(page, "evidence");
}

test.describe("declared against verified", () => {
  test("a row per repository with the declared and the verified level, the state in glyph and text, and a counter per state", async ({ page }) => {
    await open(page);
    const rows = page.locator("#cie-table tbody tr");
    await expect(rows).toHaveCount(40);
    await expect(page.locator("#cie-matches")).toHaveAttribute("data-shown", "40");
    for (const state of STATES) {
      await expect(page.locator(`[data-cie-count="${state}"]`)).toHaveText(String(FULL[state]));
      await expect(rows.locator(`td[data-cie="${state}"]`)).toHaveCount(FULL[state]);
    }
    await expect(page.locator('[data-cie-count="all"]')).toHaveText("40");
    for (const cell of await page.locator("#cie-table td[data-cie]").all()) {
      expect((await cell.locator(".cie-glyph").textContent())?.trim()).toMatch(/^[✓▼✕◷?!]$/);
      await expect(cell.locator(".cie-glyph")).toHaveAttribute("aria-hidden", "true");
      expect(((await cell.textContent()) || "").length).toBeGreaterThan(3);
    }
    await expect(rows.first().locator("th button")).toBeVisible();
  });

  test("the table has its columns and a caption", async ({ page }) => {
    await open(page);
    await expect(page.locator("#cie-table thead th")).toHaveCount(7);
    expect(await page.locator("#cie-table caption").textContent()).toContain("declared");
    await expect(page.locator("#cie-source")).toContainText("ci-evidence:ci-evidence.json");
    await expect(page.locator("#cie-source")).toContainText("14");
  });

  test("nothing published, unreadable or invalid is never shown as verified and has no link", async ({ page }) => {
    await open(page);
    for (const state of ["nodata", "unread", "invalid"]) {
      const rows = page.locator(`#cie-table tbody tr[data-state="${state}"]`);
      expect(await rows.count()).toBe(FULL[state]);
      for (const row of await rows.all()) {
        const cells = row.locator("td");
        await expect(cells.nth(3)).toHaveText("Not verified");           // the verified level
        await expect(row.locator("a")).toHaveCount(0);
      }
    }
    await expect(page.locator('#cie-table tbody tr[data-state="verified"] td').nth(3)).not.toHaveText("Not verified");
  });

  test("the date of a run links to the run inside the repository, and nothing else does", async ({ page }) => {
    await open(page);
    const links = await page.locator("#cie-table a").evaluateAll((as) => as.map((a) => [a.getAttribute("href"), a.getAttribute("rel"), a.getAttribute("target"), a.closest("tr")!.getAttribute("data-repo")]));
    expect(links.length).toBeGreaterThan(10);
    for (const [href, rel, target, repo] of links) {
      expect(href).toMatch(new RegExp(`^https://github\\.com/JuanenRac/${repo}/actions/runs/\\d+$`));
      expect(rel).toContain("noopener");
      expect(target).toBe("_blank");
    }
  });

  test("the declared level is the one of the manifest, the verified one never exceeds what passed", async ({ page }) => {
    await open(page);
    const below = page.locator('#cie-table tbody tr[data-state="below"]');
    await expect(below).toHaveCount(3);
    for (const row of await below.all()) {
      const cells = row.locator("td");
      const declared = (await cells.nth(2).textContent()) || "";
      const verified = (await cells.nth(3).textContent()) || "";
      expect(declared).not.toBe(verified);
      expect(["Bench", "Field", "Simulator"]).toContain(declared);
      expect(["Host test", "Simulator", "Bench"]).toContain(verified);
    }
  });

  test("each state filters the table, keeps the counter and resets with All", async ({ page }) => {
    await open(page);
    for (const state of STATES) {
      await page.getByTestId(`cie-state-${state}`).click();
      await expect(page.getByTestId(`cie-state-${state}`)).toHaveAttribute("aria-pressed", "true");
      await expect(page.getByTestId("cie-state-all")).toHaveAttribute("aria-pressed", "false");
      await expect(page.locator("#cie-table tbody tr")).toHaveCount(FULL[state]);
      await expect(page.locator("#cie-matches")).toHaveText(`${FULL[state]} of 40 repositories`);
    }
    await page.getByTestId("cie-state-all").click();
    await expect(page.locator("#cie-table tbody tr")).toHaveCount(40);
  });

  test("the repositories that need attention come first", async ({ page }) => {
    await open(page);
    const order = await page.locator("#cie-table tbody tr").evaluateAll((rows) => rows.map((r) => r.getAttribute("data-state")));
    const rank = ["failing", "below", "expired", "invalid", "unread", "nodata", "verified"];
    const ranks = order.map((s) => rank.indexOf(s!));
    expect(ranks).toEqual([...ranks].sort((a, b) => a - b));
  });

  test("works from the keyboard and opens the panel of a repository", async ({ page }) => {
    await open(page);
    await page.getByTestId("cie-state-failing").focus();
    await page.keyboard.press("Enter");
    await expect(page.locator("#cie-table tbody tr")).toHaveCount(5);
    const first = page.locator("#cie-table tbody tr th button").first();
    const name = (await first.textContent()) || "";
    await first.click();
    await expect(page.locator("#repo-panel")).toBeVisible();
    await expect(page.locator("#repo-panel-title")).toHaveText(name);
  });

  test("without any evidence read, the page says so and verifies nothing", async ({ page }) => {
    for (const variant of ["minimal", "partial"] as Variant[]) {
      await open(page, variant);
      await expect(page.getByTestId("cie-not-read")).toBeVisible();
      await expect(page.locator('[data-cie-count="verified"]')).toHaveText("0");
      await expect(page.locator('#cie-table td[data-cie="verified"]')).toHaveCount(0);
      const total = Number(await page.locator('[data-cie-count="all"]').textContent());
      await expect(page.locator('[data-cie-count="unread"]')).toHaveText(String(total));
    }
  });

  test("with no repository at all nothing is drawn and nothing is verified", async ({ page }) => {
    await open(page, "empty");
    await expect(page.locator('[data-cie-count="all"]')).toHaveText("0");
    await expect(page.locator("#cie-table")).toBeHidden();
    await expect(page.locator("#cie-matches")).toHaveText("0 of 0 repositories");
  });

  test("the last known data page keeps the view", async ({ page }) => {
    await open(page, "stale");
    await expect(page.locator("#cie-table tbody tr")).toHaveCount(40);
  });

  test("the view is not on any other tab", async ({ page }) => {
    await openDashboard(page);
    await expect(page.locator("#panel-summary #cie-view")).toHaveCount(0);
    await expect(page.locator("#panel-evidence #cie-view")).toHaveCount(1);
  });
});

test.describe("declared against verified, languages and themes", () => {
  test("no untranslated key in any of the eight languages and the table follows the language", async ({ page }) => {
    await open(page);
    const titles = new Set<string>();
    for (const lang of LANGS) {
      await page.locator("#lang-select").selectOption(lang);
      expect(await visibleText(page), lang).not.toMatch(LEFTOVER);
      titles.add((await page.locator("#cie-title").textContent()) || "");
      await expect(page.locator("#cie-table thead th").first()).not.toHaveText("");
      await expect(page.locator("#cie-matches")).toHaveAttribute("data-total", "40");
      await expect(page.locator("#cie-source")).not.toContainText("{");
    }
    expect(titles.size).toBe(8);
    await page.locator("#lang-select").selectOption("pt");
    await expect(page.locator("#cie-title")).toHaveText("Declarado face a verificado");
    await page.locator("#lang-select").selectOption("ja");
    await expect(page.locator("#cie-title")).toHaveText("宣言と検証の比較");
  });

  test("the states of the table are translated, not left in English", async ({ page }) => {
    await open(page);
    await page.locator("#lang-select").selectOption("de");
    await expect(page.getByTestId("cie-state-verified")).toContainText("Geprüft");
    await expect(page.locator('#cie-table td[data-cie="verified"]').first()).toContainText("Geprüft");
    await page.locator("#lang-select").selectOption("pt");
    await expect(page.locator('#cie-table td[data-cie="nodata"]').first()).toContainText("Não verificado");
  });

  for (const theme of ["dark", "light"]) {
    test(`axe finds no serious violation (${theme})`, async ({ page }) => {
      test.setTimeout(90_000);
      await open(page);
      if (theme === "light") await page.locator("#theme-toggle").click();
      const found = [...(await serious(page)).map((x) => `all: ${x}`)];
      await page.getByTestId("cie-state-failing").click();
      found.push(...(await serious(page)).map((x) => `failing: ${x}`));
      await page.getByTestId("cie-state-verified").click();
      found.push(...(await serious(page)).map((x) => `verified: ${x}`));
      expect(found).toEqual([]);
    });
  }
});

test.describe("declared against verified, sizes", () => {
  for (const [name, width, height] of [["1920x1080", 1920, 1080], ["1366x768", 1366, 768], ["390x844", 390, 844]] as const) {
    test(`fits ${name} without scrolling the page sideways`, async ({ page }) => {
      await page.setViewportSize({ width, height });
      await open(page);
      await page.locator("#cie-view").scrollIntoViewIfNeeded();
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      expect(overflow).toBeLessThanOrEqual(1);
      const box = await page.locator("#cie-view").boundingBox();
      expect(box!.width).toBeLessThanOrEqual(width);
      for (const state of STATES) await expect(page.getByTestId(`cie-state-${state}`)).toBeVisible();
    });
  }

  test("no request of its own: the view draws from the data embedded in the page", async ({ page }) => {
    await open(page);
    const requests: string[] = [];
    page.on("request", (r) => { if (r.url().startsWith("http")) requests.push(r.url()); });
    await page.getByTestId("cie-state-below").click();
    await page.getByTestId("cie-state-all").click();
    expect(requests).toEqual([]);
  });
});
