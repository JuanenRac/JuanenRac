import AxeBuilder from "@axe-core/playwright";
import { test, expect, openDashboard, gotoTab, LANGS, LEFTOVER, visibleText, Page, Variant } from "./helpers";

// The tab "Tests": the automated tests each repository DECLARES (its README or its glance file), per ecosystem and per project.
// Fixture (full): HYDRA-UMC 1551 tests (9 repositories; one counts checks), URTC 1410, A.R.M.O.R. 1032, EH3D 1617; 34 declared, 3 declare nothing, 3 could not
// be read today and show their last known count; the history has 29 days with counts (two missing days break the lines).

const TOTALS: Record<string, number> = { "hydra-umc": 1551, urtc: 1410, armor: 1032, eh3d: 1617 };
const ECOS = ["hydra-umc", "urtc", "armor", "eh3d"] as const;

async function serious(page: Page) {
  const results = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"]).analyze();
  return results.violations.filter((v) => v.impact === "serious" || v.impact === "critical").map((v) => `${v.id}: ${v.nodes.slice(0, 3).map((n) => n.target.join(" ")).join(" | ")}`);
}

async function open(page: Page, variant: Variant | "single" = "full") {
  await openDashboard(page, variant as Variant);
  await gotoTab(page, "tests");
}

const rows = (page: Page) => page.locator("#ts-list .ts-row");

test.describe("tests tab: total per ecosystem", () => {
  test("the tab is there, says the figures are declared and explains how they are calculated", async ({ page }) => {
    await open(page);
    await expect(page.locator("[role=tab]")).toHaveCount(16);
    await expect(page.getByTestId("tab-tests")).toHaveText("Tests");
    await expect(page.getByTestId("ts-badge")).toHaveText("Declared, not run here");
    const help = page.getByTestId("ts-help");
    await expect(page.getByTestId("ts-help-body")).toBeHidden();
    await help.locator("summary").click();
    await expect(page.getByTestId("ts-help-body")).toBeVisible();
    const text = (await page.getByTestId("ts-help-body").textContent()) || "";
    expect(text).toContain("dashboard-config.json");
    expect(text).toContain("HYDRA-UMC-DOCS/data/glance.json");
    expect(text).toContain("README");
    expect(text).toContain("not run by the dashboard");
    expect(text).not.toContain("{");
    await help.locator("summary").click();
    await expect(page.getByTestId("ts-help-body")).toBeHidden();
  });

  test("a bar per ecosystem with the total, and a table with the same figures", async ({ page }) => {
    await open(page);
    const bars = page.locator("#ts-eco-chart .ts-bar-g");
    await expect(bars).toHaveCount(4);
    for (const eco of ECOS) {
      const bar = page.locator(`#ts-eco-chart .ts-bar-g[data-eco="${eco}"]`);
      await expect(bar).toHaveAttribute("data-n", String(TOTALS[eco]));
      await expect(bar.locator("text.ts-value")).toHaveText(new RegExp("^" + String(TOTALS[eco]).replace(/(\d)(?=(\d{3})$)/, "$1[\\s\\u202f]?") + "$"));
      expect(await bar.getAttribute("aria-label")).toMatch(new RegExp(`${TOTALS[eco]} tests declared by \\d+ of 10 repositories`));
    }
    const table = page.locator("#ts-eco-table");
    await expect(table.locator("caption")).toHaveText("Tests declared per ecosystem");
    await expect(table.locator("thead th")).toHaveCount(6);
    await expect(table.locator("tbody tr")).toHaveCount(4);
    const first = (await table.locator("tbody tr").first().locator("td").allTextContents()).map((t) => t.replace(/[\s ]/g, ""));
    expect(first[0]).toBe(String(TOTALS["hydra-umc"]));
    expect(first[2]).toBe("9/10");
    // the checks of the host programs are listed apart and never added to the tests
    expect(Number(first[1])).toBeGreaterThan(10000);
    expect(Number(first[1])).not.toBe(TOTALS["hydra-umc"]);
  });

  test("the last known counts are marked with a banner and a date", async ({ page }) => {
    await open(page);
    await expect(page.getByTestId("ts-stale")).toContainText("the last known count is shown (the newest is from 2001-12-20). Repositories affected: 3.");
    const row = page.locator('#ts-list .ts-row[data-state="lastknown"]').first();
    await expect(row).toContainText("Last known (2001-12-20)");
    await expect(page.locator('#ts-list .ts-row[data-state="lastknown"]')).toHaveCount(3);
  });

  test("when GitHub could not be read the last known figures stay, with the banner, and what was never known is not verified", async ({ page }) => {
    await open(page, "stale");
    await expect(page.getByTestId("ts-stale")).toBeVisible();
    await expect(page.locator('#ts-list .ts-row[data-state="lastknown"]')).toHaveCount(32);
    await expect(page.locator('#ts-list .ts-row[data-state="unread"]')).toHaveCount(8);
    await expect(page.getByTestId("ts-stale")).toContainText("Repositories affected: 32.");
    await expect(page.locator('#ts-list .ts-row[data-state="declared"]')).toHaveCount(0);
    await expect(page.getByTestId("ts-unverified")).toBeVisible();
    await expect(page.locator('#ts-list .ts-row[data-state="unread"]').first()).toContainText("Not verified");
    await expect(page.getByTestId("ts-not-read")).toBeHidden();
  });

  test("nothing read and no history: not verified everywhere, no bar, no zero", async ({ page }) => {
    for (const variant of ["partial", "minimal"] as Variant[]) {
      await open(page, variant);
      await expect(page.getByTestId("ts-not-read")).toBeVisible();
      await expect(page.locator("#ts-eco-chart .ts-bar")).toHaveCount(0);
      await expect(page.locator("#ts-eco-chart .ts-bar-g").first()).toHaveAttribute("aria-label", /Not verified$/);
      await expect(page.locator('#ts-list .ts-row[data-state="unread"]')).toHaveCount(await page.locator("#ts-list .ts-row").count());
      await expect(page.getByTestId("ts-evo-msg")).toContainText("Missing data");
      for (const t of await page.locator("td.tests-cell").allTextContents()) expect(t).toBe("Not verified");
    }
  });

  test("with no repository at all nothing is drawn", async ({ page }) => {
    await open(page, "empty");
    await expect(page.getByTestId("ts-matches")).toHaveText("0 of 0 projects");
    await expect(page.getByTestId("ts-none")).toBeHidden();
    await expect(page.locator("#ts-list .ts-row")).toHaveCount(0);
    await expect(page.locator("#ts-eco-chart .ts-bar")).toHaveCount(0);
  });
});

test.describe("tests tab: evolution", () => {
  test("a line per ecosystem, broken at the days without a snapshot, with a table of the same figures", async ({ page }) => {
    await open(page);
    await expect(page.getByTestId("ts-evo-wrap")).toBeVisible();
    await expect(page.locator("#ts-evo-svg path.evo-line")).toHaveCount(8);          // 4 ecosystems x 2 stretches (two days are missing)
    await expect(page.locator("#ts-evo-legend li")).toHaveCount(4);
    const table = page.locator("#ts-evo-table");
    await expect(table.locator("tbody tr")).toHaveCount(29);
    await expect(table.locator("thead th")).toHaveCount(5);
    await expect(table.locator("tbody tr").last().locator("th")).toHaveText("2001-12-21");
    const label = await page.locator("#ts-evo-svg").getAttribute("aria-label");
    expect(label).toContain("2001-11-21");
    expect(label).toContain("2001-12-21");
    await expect(page.locator("#ts-evo-svg .evo-end-label").first()).toContainText(/\d/);
    // no snapshot is interpolated: the two missing days are not in the table
    const dates = await table.locator("tbody th").allTextContents();
    expect(dates).not.toContain("2001-11-30");
    expect(dates).not.toContain("2001-12-01");
  });

  test("the end of each line says the same as its bar", async ({ page }) => {
    await open(page);
    const ends = await page.locator("#ts-evo-svg .evo-end-label").allTextContents();
    for (const eco of ECOS) {
      const label = { "hydra-umc": "HYDRA-UMC", urtc: "URTC", armor: "A.R.M.O.R.", eh3d: "EH3D" }[eco];
      const end = ends.find((t) => t.startsWith(label + " "))!;
      expect(end.replace(/[\s ]/g, "").replace(label.replace(/\s/g, ""), "")).toMatch(/^\d+$/);
    }
  });

  test("a single snapshot gives a message, not a line", async ({ page }) => {
    await open(page, "single");
    await expect(page.getByTestId("ts-evo-msg")).toContainText("Only one snapshot has the counts (2001-12-21)");
    await expect(page.getByTestId("ts-evo-wrap")).toBeHidden();
    await expect(page.locator("#ts-evo-table tbody tr")).toHaveCount(1);
  });

  test("no history with counts says that data are missing", async ({ page }) => {
    await open(page, "minimal");
    await expect(page.getByTestId("ts-evo-msg")).toHaveText("Missing data: no daily snapshot has the test counts yet.");
    await expect(page.getByTestId("ts-evo-wrap")).toBeHidden();
  });
});

test.describe("tests tab: per project", () => {
  test("a row per project ordered by the declared count, the ones with no number at the end", async ({ page }) => {
    await open(page);
    await expect(rows(page)).toHaveCount(40);
    await expect(page.getByTestId("ts-matches")).toHaveText("40 of 40 projects");
    const counts = await rows(page).evaluateAll((els) => els.map((e) => [e.getAttribute("data-state"), e.getAttribute("data-n")]));
    const numeric = counts.filter((c) => c[1] !== null).map((c) => Number(c[1]));
    expect(numeric.length).toBe(32);   // 40 minus 5 that count checks and 3 that declare nothing (29 declared + 3 last known)
    for (let i = 1; i < numeric.length; i++) expect(numeric[i - 1]).toBeGreaterThanOrEqual(numeric[i]);
    expect(counts.slice(0, numeric.length).every((c) => c[1] !== null)).toBe(true);
    expect(counts.slice(-3).map((c) => c[0])).toEqual(["undeclared", "undeclared", "undeclared"]);
    await expect(rows(page).first()).toContainText("EH3D-FIXTURE-01");
    await expect(rows(page).first()).toContainText("359 tests");
  });

  test("every bar is as long as its count and checks have no bar", async ({ page }) => {
    await open(page);
    const widths = await rows(page).evaluateAll((els) => els.map((e) => [e.getAttribute("data-n"), (e.querySelector(".ts-fill") as HTMLElement | null)?.style.getPropertyValue("--w") ?? null]));
    for (const [n, w] of widths) {
      if (n === null) expect(w).toBeNull();
      else expect(parseFloat(w as string)).toBeCloseTo(Math.max(1.5, (Number(n) / 359) * 100), 0);
    }
    const checks = page.locator('#ts-list .ts-row[data-state="declared"]:not([data-n])').first();
    await expect(checks).toContainText("host-program checks (not unit tests)");
    await expect(checks.locator(".ts-fill")).toHaveCount(0);
  });

  test("the source is stated: README or glance.json", async ({ page }) => {
    await open(page);
    await expect(rows(page).first()).toHaveAttribute("title", "Declared in the README of the repository");
    await page.locator('#ts-list .ts-row[data-repo="HYDRA-UMC-FIXTURE-09"]').scrollIntoViewIfNeeded();
    await expect(page.locator('#ts-list .ts-row[data-repo="HYDRA-UMC-FIXTURE-09"]')).toHaveAttribute("title", "Declared in the glance.json of the repository");
    await expect(page.locator('#ts-proj-table tbody tr').first().locator("td").last()).toHaveText("README");
  });

  test("filter by ecosystem", async ({ page }) => {
    await open(page);
    for (const eco of ECOS) {
      await page.getByTestId(`ts-eco-${eco}`).click();
      await expect(page.getByTestId(`ts-eco-${eco}`)).toHaveAttribute("aria-pressed", "true");
      await expect(rows(page)).toHaveCount(10);
      const names = await rows(page).evaluateAll((els) => els.map((e) => e.getAttribute("data-repo")));
      const prefix = { "hydra-umc": "HYDRA-UMC-", urtc: "URTC-", armor: "ARMOR-", eh3d: "EH3D-" }[eco];
      expect(names.every((n) => n!.startsWith(prefix))).toBe(true);
      await expect(page.getByTestId("ts-matches")).toHaveText("10 of 40 projects");
    }
    await page.getByTestId("ts-eco-all").click();
    await expect(rows(page)).toHaveCount(40);
  });

  test("filter by family, search and both together; no match says so", async ({ page }) => {
    await open(page);
    const families = await page.locator("#ts-family option").allTextContents();
    expect(families.length).toBeGreaterThan(2);
    await page.locator("#ts-family").selectOption({ index: 1 });
    const shown = await rows(page).count();
    expect(shown).toBeGreaterThan(0);
    expect(shown).toBeLessThan(40);
    await page.locator("#ts-family").selectOption("all");
    await page.getByTestId("ts-search").fill("urtc-fixture-0");
    await expect(rows(page)).toHaveCount(10);
    await page.getByTestId("ts-search").fill("urtc-fixture-03");
    await expect(rows(page)).toHaveCount(1);
    await page.getByTestId("ts-eco-armor").click();
    await expect(rows(page)).toHaveCount(0);
    await expect(page.getByTestId("ts-none")).toBeVisible();
    await expect(page.getByTestId("ts-matches")).toHaveText("0 of 40 projects");
    await page.getByTestId("ts-search").fill("");
    await page.getByTestId("ts-eco-all").click();
    await expect(page.getByTestId("ts-none")).toBeHidden();
    await expect(rows(page)).toHaveCount(40);
  });

  test("a click opens the panel of the repository with its declared tests, Escape closes it", async ({ page }) => {
    await open(page);
    await rows(page).first().click();
    const panel = page.locator("#repo-panel");
    await expect(panel).toBeVisible();
    await expect(panel.locator("dt", { hasText: "Tests (declared)" })).toBeVisible();
    await expect(panel.locator("dt", { hasText: "Tests (declared)" }).locator("xpath=following-sibling::dd[1]")).toHaveText("359 tests · README");
    await page.keyboard.press("Escape");
    await expect(panel).toBeHidden();
  });

  test("the panel of a repository that declares nothing, counts checks or shows a last known value says so", async ({ page }) => {
    await open(page);
    const value = async (name: string) => {
      await page.locator(`#ts-list .ts-row[data-repo="${name}"]`).click();
      const text = await page.locator("#repo-panel dt", { hasText: "Tests (declared)" }).locator("xpath=following-sibling::dd[1]").textContent();
      await page.keyboard.press("Escape");
      return text;
    };
    expect(await value("URTC-FIXTURE-02")).toBe("56 tests · Last known (2001-12-20)");
    const undeclared = await page.locator('#ts-list .ts-row[data-state="undeclared"]').first().getAttribute("data-repo");
    expect(await value(undeclared!)).toBe("Not declared");
    const checks = await page.locator('#ts-list .ts-row[data-state="declared"]:not([data-n])').first().getAttribute("data-repo");
    expect(await value(checks!)).toMatch(/^\d+ host-program checks \(not unit tests\) · /);
  });

  test("the projects table has a Tests column", async ({ page }) => {
    await openDashboard(page);
    await gotoTab(page, "projects");
    await expect(page.locator("#panel-projects thead th", { hasText: "Tests" })).toHaveCount(1);
    const cell = page.locator('tr.project-row td.tests-cell[data-tests-for="EH3D-FIXTURE-01"]');
    await expect(cell).toHaveText("359");
    await expect(cell).toHaveAttribute("title", "Declared in the README of the repository");
    await expect(page.locator('td.tests-cell[data-tests-for="URTC-FIXTURE-02"]')).toHaveText("56 (2001-12-20)");
    await expect(page.locator("tr.project-row td.tests-cell.ts-muted").first()).not.toHaveText("");
    expect(await page.locator("tr.project-row td.tests-cell").count()).toBe(40);
  });
});

test.describe("tests tab: languages, themes, keyboard, motion", () => {
  test("no untranslated key in any of the eight languages and everything follows the language", async ({ page }) => {
    await open(page);
    const titles = new Set<string>();
    for (const lang of LANGS) {
      await page.locator("#lang-select").selectOption(lang);
      expect(await visibleText(page), lang).not.toMatch(LEFTOVER);
      titles.add((await page.locator("#ts-title").textContent()) || "");
      await expect(page.getByTestId("ts-matches")).toHaveAttribute("data-total", "40");
      await expect(page.getByTestId("ts-eco-svg")).toHaveAttribute("aria-label", /.+/);
      await expect(page.locator("#ts-eco-table caption")).not.toHaveText("");
      await page.getByTestId("ts-help").locator("summary").click();
      await expect(page.getByTestId("ts-help-body")).not.toContainText("{");
      await page.getByTestId("ts-help").locator("summary").click();
    }
    expect(titles.size).toBe(8);
    await page.locator("#lang-select").selectOption("pt");
    await expect(page.locator("#ts-title")).toHaveText("Testes automáticos por ecossistema");
    await expect(page.getByTestId("tab-tests")).toHaveText("Testes");
    await expect(page.getByTestId("ts-badge")).toHaveText("Declarado, não executado aqui");
    await page.locator("#lang-select").selectOption("es");
    await expect(page.getByTestId("tab-tests")).toHaveText("Pruebas");
    await expect(rows(page).first()).toContainText("359 pruebas");
    await page.locator("#lang-select").selectOption("ja");
    await expect(page.locator("#ts-title")).toHaveText("エコシステム別の自動テスト");
    await page.locator("#lang-select").selectOption("de");
    await expect(page.locator('#ts-list .ts-row[data-state="undeclared"]').first()).toContainText("Nicht erklärt");
    await expect(page.locator("#panel-projects thead th").nth(6)).toHaveText("Tests");
  });

  for (const theme of ["dark", "light"]) {
    test(`axe finds no serious violation (${theme}), also with a filter and with poor data`, async ({ page }) => {
      test.setTimeout(90_000);
      await open(page);
      if (theme === "light") await page.locator("#theme-toggle").click();
      const found = [...(await serious(page)).map((x) => `all: ${x}`)];
      await page.getByTestId("ts-eco-urtc").click();
      found.push(...(await serious(page)).map((x) => `urtc: ${x}`));
      await page.getByTestId("ts-help").locator("summary").click();
      found.push(...(await serious(page)).map((x) => `help: ${x}`));
      await open(page, "partial");
      if (theme === "light" && (await page.locator("html").getAttribute("data-theme")) !== "light") await page.locator("#theme-toggle").click();
      found.push(...(await serious(page)).map((x) => `partial: ${x}`));
      expect(found).toEqual([]);
    });
  }

  test("the keyboard reaches the chips, the filters, the rows and the bars", async ({ page }) => {
    await open(page);
    await page.getByTestId("ts-eco-chips").locator("button").first().focus();
    await page.keyboard.press("Tab");
    await page.keyboard.press("Enter");
    await expect(page.getByTestId("ts-eco-hydra-umc")).toHaveAttribute("aria-pressed", "true");
    await expect(rows(page)).toHaveCount(10);
    const bar = page.locator("#ts-eco-chart .ts-bar-g").first();
    await bar.focus();
    await expect(bar).toBeFocused();
    const outline = await bar.evaluate((e) => getComputedStyle(e).outlineStyle);
    expect(outline).not.toBe("none");
    await rows(page).first().focus();
    await page.keyboard.press("Enter");
    await expect(page.locator("#repo-panel")).toBeVisible();
    await page.keyboard.press("Escape");
    await expect(page.locator("#repo-panel")).toBeHidden();
    await expect(rows(page).first()).toBeFocused();
  });

  test("the address keeps the tab", async ({ page }) => {
    await open(page);
    await expect(page).toHaveURL(/#tests$/);
    await page.reload();
    await expect(page.locator("#panel-tests")).toBeVisible();
  });

  test("with motion allowed the bars and the lines are drawn with an entrance, and with reduced motion they are not", async ({ page }) => {
    await page.emulateMedia({ reducedMotion: "no-preference" });
    await open(page);
    expect(await page.locator("#ts-eco-chart .ts-bar").first().evaluate((e) => getComputedStyle(e).animationName)).toBe("t25-grow-y");
    expect(await page.locator("#ts-list .ts-fill").first().evaluate((e) => getComputedStyle(e).animationName)).toBe("t25-grow-x");
    await page.emulateMedia({ reducedMotion: "reduce" });
    expect(await page.locator("#ts-eco-chart .ts-bar").first().evaluate((e) => getComputedStyle(e).animationName)).toBe("none");
    expect(await page.locator("#ts-list .ts-fill").first().evaluate((e) => getComputedStyle(e).animationName)).toBe("none");
    await expect(page.locator("#ts-eco-chart .ts-bar-g").first()).toHaveAttribute("data-n", /\d+/);
  });

  test("print: the report includes the totals and the lists, without the controls", async ({ page }) => {
    await open(page);
    await page.emulateMedia({ media: "print" });
    await expect(page.locator("#panel-tests")).toBeVisible();
    await expect(page.locator("#ts-eco-chart")).toBeVisible();
    await expect(page.locator("#ts-eco-chips")).toBeHidden();
    const max = await page.locator("#ts-list-wrap").evaluate((e) => getComputedStyle(e).maxHeight);
    expect(max).toBe("none");
  });

  test("the page makes no request of its own for this tab", async ({ page }) => {
    const requests: string[] = [];
    page.on("request", (r) => { if (/^https?:/.test(r.url()) && !r.url().startsWith("https://api.github.com/") && !/fonts\.(googleapis|gstatic)|\.svg/.test(r.url())) requests.push(r.url()); });
    await open(page);
    await page.getByTestId("ts-eco-armor").click();
    await page.getByTestId("ts-search").fill("a");
    await page.locator("#lang-select").selectOption("fr");
    expect(requests).toEqual([]);
  });
});

test.describe("tests tab: sizes", () => {
  for (const [name, width, height] of [["1920x1080", 1920, 1080], ["1366x768", 1366, 768], ["390x844", 390, 844]] as const) {
    test(`fits ${name} without scrolling the page sideways`, async ({ page }) => {
      await page.setViewportSize({ width, height });
      await open(page);
      for (const id of ["#ts-eco-chart", "#ts-evo-wrap", "#ts-list-wrap"]) {
        await page.locator(id).scrollIntoViewIfNeeded();
        const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
        expect(overflow, id).toBeLessThanOrEqual(1);
        const box = await page.locator(id).boundingBox();
        expect(box!.width).toBeLessThanOrEqual(width);
      }
      await expect(page.locator("#ts-eco-chart .ts-bar-g")).toHaveCount(4);
      await expect(page.getByTestId("ts-eco-all")).toBeVisible();
      if (width >= 1366) {
        const chart = await page.locator("#ts-eco-chart").boundingBox();
        expect(chart!.width).toBeGreaterThan(400);
      }
    });
  }
});
