import AxeBuilder from "@axe-core/playwright";
import { test, expect, openDashboard, gotoTab, LANGS, LEFTOVER, visibleText, Page, Variant } from "./helpers";

// The delivery pipeline and the signatures, the legends, the complete address, the side bar that can be hidden, the scroll arrows of the tab bar and the links of
// the architecture. Fixture (full): of the 40 repositories one in five publishes a .sig (index % 5 = 0), one in five a .minisig (3), one in five publishes no
// signature file (1), one in five has no release (4) and one in five gives no assets at all (2); one in four declares the whole pipeline (index % 4 = 0).

async function serious(page: Page) {
  const results = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"]).analyze();
  return results.violations.filter((v) => v.impact === "serious" || v.impact === "critical").map((v) => `${v.id}: ${v.nodes.slice(0, 3).map((n) => n.target.join(" ")).join(" | ")}`);
}

const hash = (page: Page) => page.evaluate(() => location.hash);

test.describe("tab bar", () => {
  test("arrows appear only when tabs do not fit and bring the hidden ones into view", async ({ page }) => {
    await page.setViewportSize({ width: 1100, height: 800 });
    await openDashboard(page);
    const next = page.getByTestId("tabs-scroll-next");
    await expect(next).toBeVisible();
    await expect(page.getByTestId("tabs-scroll-prev")).toBeHidden();
    await next.click();
    await expect(page.getByTestId("tabs-scroll-prev")).toBeVisible();
    const scrolled = await page.locator("nav.tabs").evaluate((el) => el.scrollLeft);
    expect(scrolled).toBeGreaterThan(0);
  });

  for (const [w, h] of [[1920, 1080], [1366, 768], [768, 1024], [390, 844]] as const) {
    test(`${w}x${h}: every tab can be reached and none is cut without a way to scroll`, async ({ page }) => {
      await page.setViewportSize({ width: w, height: h });
      await openDashboard(page);
      const info = await page.locator("nav.tabs").evaluate((el) => ({ over: el.scrollWidth - el.clientWidth > 2 }));
      const next = page.getByTestId("tabs-scroll-next");
      if (info.over) await expect(next).toBeVisible();
      else await expect(next).toBeHidden();
      await page.getByTestId("tab-errors").focus();
      await page.keyboard.press("Enter");
      await expect(page.locator("#panel-errors")).toBeVisible();
      const box = await page.getByTestId("tab-errors").boundingBox();
      const bar = await page.locator("nav.tabs").boundingBox();
      expect(box && bar && box.x >= bar.x - 1 && box.x + box.width <= bar.x + bar.width + 1).toBeTruthy();
    });
  }
});

test.describe("signatures in the evidence tab", () => {
  test("a signature file is present but not verified, no file is no signature, unreadable assets are not verified", async ({ page }) => {
    await openDashboard(page, "full", "#evidence");
    const cell = (name: string) => page.locator(`#ev-table tr[data-repo="${name}"] td[data-item="signed"]`);
    await expect(cell("ARMOR-FIXTURE-00")).toHaveAttribute("data-status", "present");   // index 10: .sig
    await expect(cell("ARMOR-FIXTURE-03")).toHaveAttribute("data-status", "present");   // .minisig
    await expect(cell("ARMOR-FIXTURE-01")).toHaveAttribute("data-status", "no");        // a release without a signature file
    await expect(cell("ARMOR-FIXTURE-02")).toHaveAttribute("data-status", "unverified"); // the assets were not returned
    await expect(cell("ARMOR-FIXTURE-04")).toHaveAttribute("data-status", "no");        // no release at all
    await expect(cell("ARMOR-FIXTURE-00")).toContainText("Signature present, not verified here");
  });

  test("the summary on top counts what is missing and links to nothing it cannot prove", async ({ page }) => {
    await openDashboard(page, "full", "#evidence");
    const sum = page.getByTestId("ev-summary");
    await expect(sum).toBeVisible();
    for (const key of ["unsigned", "present", "sigunk", "nohw"]) await expect(sum.locator(`li[data-sum="${key}"]`)).toHaveCount(1);
    const n = async (key: string) => Number(await sum.locator(`li[data-sum="${key}"]`).getAttribute("data-n"));
    // 8 .sig + 8 .minisig = 16 with a signature file
    expect(await n("present")).toBe(16);
    expect(await n("sigunk")).toBeGreaterThan(0);
    expect(await n("unsigned")).toBeGreaterThan(0);
    expect(await n("nohw")).toBeGreaterThan(0);
    await expect(sum).not.toContainText("{");
  });

  test("a cell that is not verified or missing explains why and links to the repository", async ({ page }) => {
    await openDashboard(page, "full", "#evidence");
    const button = page.locator('#ev-table tr[data-repo="ARMOR-FIXTURE-01"] td[data-item="signed"] button.ev-why-btn');
    await expect(button).toHaveAttribute("aria-expanded", "false");
    await button.click();
    await expect(button).toHaveAttribute("aria-expanded", "true");
    const box = page.getByTestId("ev-why");
    await expect(box).toBeVisible();
    await expect(box).toContainText("no signature file");
    const link = box.getByRole("link", { name: "Open the repository" });
    await expect(link).toHaveAttribute("href", "https://github.com/JuanenRac/ARMOR-FIXTURE-01");
    await expect(box.getByRole("link", { name: "Open its releases" })).toHaveAttribute("href", "https://github.com/JuanenRac/ARMOR-FIXTURE-01/releases");
    await box.getByRole("button", { name: "Open its panel" }).click();
    await expect(page.getByTestId("repo-panel")).toBeVisible();
    await page.keyboard.press("Escape");
    // the same button closes the explanation, and opens it again
    await button.click();
    await expect(box).toBeHidden();
    await button.click();
    await expect(box).toBeVisible();
  });

  test("the explanation of an unverified cell works with the keyboard", async ({ page }) => {
    await openDashboard(page, "full", "#evidence");
    const button = page.locator('#ev-table tr[data-repo="ARMOR-FIXTURE-02"] td[data-item="signed"] button.ev-why-btn');
    await button.focus();
    await page.keyboard.press("Enter");
    await expect(page.getByTestId("ev-why")).toContainText("could not be read");
    await page.getByTestId("ev-why").getByRole("button", { name: "Close" }).click();
    await expect(page.getByTestId("ev-why")).toBeHidden();
  });

  test("the signature appears in the panel of the repository with the declared pipeline", async ({ page }) => {
    await openDashboard(page, "full", "#projects?repo=ARMOR-FIXTURE-00");
    const fields = page.getByTestId("repo-fields");
    await expect(fields).toContainText("Delivery pipeline");
    await expect(fields).toContainText("Published");
    await expect(fields).toContainText("GitHub Actions");
    await expect(fields).toContainText("signed with the release key");
    await expect(fields).toContainText("signed on this computer");
    await expect(fields).toContainText("signature file present (not verified here)");
    await expect(fields.getByRole("link", { name: /actions\/runs\// })).toHaveAttribute("href", /^https:\/\/github\.com\/JuanenRac\/ARMOR-FIXTURE-00\/actions\/runs\//);
  });

  test("a repository that declares nothing says not declared", async ({ page }) => {
    await openDashboard(page, "full", "#projects?repo=ARMOR-FIXTURE-02");
    const fields = page.getByTestId("repo-fields");
    await expect(fields).toContainText("Delivery pipeline");
    await expect(fields).toContainText("not declared");
    await expect(fields).toContainText("not verified");
  });
});

test.describe("delivery pipeline in the projects", () => {
  test("every row has a pipeline state and the filter counts add up", async ({ page }) => {
    await openDashboard(page, "full", "#projects");
    const cells = page.locator("td.pipe-cell");
    expect(await cells.count()).toBe(40);
    for (const text of await cells.allTextContents()) expect(text).not.toBe("");
    let total = 0;
    for (const state of ["published", "signed", "built", "release_only", "undeclared"]) {
      total += Number(await page.getByTestId(`filter-pipeline-${state}`).locator("b").textContent());
    }
    expect(total).toBe(40);
  });

  test("the filter keeps only the repositories of that state and the address says so", async ({ page }) => {
    await openDashboard(page, "full", "#projects");
    await page.getByTestId("filter-pipeline-published").click();
    const count = Number(await page.getByTestId("filter-pipeline-published").locator("b").textContent());
    const state = await page.locator("#filters-count").getAttribute("data-shown");
    expect(Number(state)).toBe(count);
    await expect.poll(() => hash(page)).toContain("pipe=published");
    for (const t of await page.locator("tr.project-row[data-match='1'] td.pipe-cell").allTextContents()) expect(t).toContain("Published");
    await page.getByTestId("reset-filters").click();
    await expect.poll(() => hash(page)).not.toContain("pipe=");
  });

  test("an unknown value in the address is ignored", async ({ page }) => {
    await openDashboard(page, "full", "#projects?pipe=bogus&st=evil&mat=%3Cscript%3E&fam=nope&days=7&evc=x&evm=nonsense,tests");
    await expect(page.locator("#filters-count")).toHaveAttribute("data-shown", "40");
    expect(await page.locator("#project-search").inputValue()).toBe("");
  });
});

test.describe("complete state in the address", () => {
  test("filters, search and period are written and read back", async ({ page }) => {
    await openDashboard(page, "full", "#projects");
    await page.getByTestId("filter-maturity-production").click();
    await page.getByTestId("project-search").fill("fixture");
    await expect.poll(() => hash(page)).toContain("mat=production");
    await expect.poll(() => hash(page)).toContain("q=fixture");
    const url = await page.evaluate(() => location.href);
    const shownBefore = await page.locator("#filters-count").getAttribute("data-shown");
    await page.goto("about:blank");
    await page.goto(url);
    await page.waitForSelector("[role=tab][aria-selected=true]");
    await expect(page.getByTestId("project-search")).toHaveValue("fixture");
    await expect(page.getByTestId("filter-maturity-production")).toHaveAttribute("aria-pressed", "true");
    await expect(page.locator("#filters-count")).toHaveAttribute("data-shown", shownBefore || "");
  });

  test("evidence filters and the period of the history travel in the address", async ({ page }) => {
    await openDashboard(page, "full", "#evidence?evc=urtc&evm=signed,hw&evu=1");
    await expect(page.getByTestId("ev-eco-urtc")).toHaveAttribute("aria-pressed", "true");
    await expect(page.getByTestId("ev-missing-signed")).toHaveAttribute("aria-pressed", "true");
    await expect(page.getByTestId("ev-missing-hw")).toHaveAttribute("aria-pressed", "true");
    await expect(page.getByTestId("ev-unverified")).toHaveAttribute("aria-pressed", "true");
    await page.getByTestId("ev-reset").click();
    await expect.poll(() => hash(page)).toBe("#evidence");
    await page.getByTestId("ev-eco-eh3d").click();
    await expect.poll(() => hash(page)).toContain("evc=eh3d");
    await openDashboard(page, "full", "#summary?days=30");
    await expect(page.getByTestId("evo-30")).toHaveAttribute("aria-pressed", "true");
  });

  test("the compact mode and the repository keep working with the rest", async ({ page }) => {
    await openDashboard(page, "full", "#projects?view=compact&mat=production&repo=ARMOR-FIXTURE-00");
    await expect(page.locator(".app, :root").first()).toBeVisible();
    await expect(page.getByTestId("repo-panel")).toBeVisible();
    await expect(page.getByTestId("mode-compact")).toHaveAttribute("aria-pressed", "true");
    expect(await hash(page)).toContain("view=compact");
    expect(await hash(page)).toContain("mat=production");
  });

  test("the search text is cleaned: markup and control characters never reach the box", async ({ page }) => {
    await openDashboard(page, "full", "#projects?q=%3Cimg%20src%3Dx%20onerror%3Dalert(1)%3E%0Aabc");
    const value = await page.getByTestId("project-search").inputValue();
    expect(value).not.toMatch(/[<>"'`&\\\n]/);
    expect(value.length).toBeLessThanOrEqual(80);
  });
});

test.describe("side bar", () => {
  test("it can be hidden and shown, the state is remembered and the button is accessible", async ({ page }) => {
    await page.setViewportSize({ width: 1366, height: 768 });
    await openDashboard(page);
    const button = page.getByTestId("side-toggle");
    await expect(button).toBeVisible();
    await expect(button).toHaveAttribute("aria-expanded", "true");
    await expect(page.locator("#sidebar")).toBeVisible();
    await button.click();
    await expect(button).toHaveAttribute("aria-expanded", "false");
    await expect(page.locator("#sidebar")).toBeHidden();
    await expect(button).toHaveAttribute("aria-label", "Show the filters panel");
    await page.reload();
    await page.waitForSelector("[role=tab][aria-selected=true]");
    await expect(page.locator("#sidebar")).toBeHidden();
    await page.getByTestId("side-toggle").focus();
    await page.keyboard.press("Enter");
    await expect(page.locator("#sidebar")).toBeVisible();
  });

  test("with the storage blocked it still works", async ({ page }) => {
    await page.addInitScript(() => {
      Object.defineProperty(window, "localStorage", { get() { throw new Error("blocked"); } });
    });
    await page.setViewportSize({ width: 1366, height: 768 });
    await openDashboard(page);
    await page.getByTestId("side-toggle").click();
    await expect(page.locator("#sidebar")).toBeHidden();
  });

  test("it is not offered on a phone, where the filters have their own button", async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await openDashboard(page);
    await expect(page.getByTestId("side-toggle")).toBeHidden();
  });
});

test.describe("legends and notes", () => {
  test("the axes of the radars are named, in the legend and in the table", async ({ page }) => {
    await openDashboard(page, "full", "#insight");
    const legend = page.getByTestId("ra-legend");
    await expect(legend).toBeVisible();
    await expect(legend).toContainText("1 Software");
    await expect(legend).toContainText("8 Production");
    await expect(page.getByTestId("ra-table")).toContainText("Software");
  });

  test("the checks of the host programs are labelled as such and never as unit tests", async ({ page }) => {
    await openDashboard(page, "full", "#tests");
    await expect(page.getByTestId("ts-checks-note")).toContainText("host programs");
    await expect(page.getByTestId("ts-checks-note")).toContainText("not unit tests");
    await expect(page.locator("#ts-eco-table")).toContainText("Host-program checks (apart)");
    await expect(page.locator("#panel-tests")).not.toContainText("Checks (apart)");
  });

  test("the bar of the CI is followed by what this page read of the latest run on main", async ({ page }) => {
    await openDashboard(page, "full", "#summary");
    const note = page.getByTestId("ci-live-hydra-umc").first();
    await expect(note).toContainText("Live:");
    await expect(note).toContainText("latest run on main green");
    const [g, n, r] = [Number(await note.getAttribute("data-g")), Number(await note.getAttribute("data-n")), Number(await note.getAttribute("data-r"))];
    expect(g + r).toBeLessThanOrEqual(n);
    expect(n).toBe(10);
    await expect(note).toHaveAttribute("title", /README status/);
  });

  test("the activity badges give the exact UTC moment", async ({ page }) => {
    await openDashboard(page, "full", "#projects");
    const title = await page.locator("td.activity-cell [data-kind='activity']").first().getAttribute("title");
    expect(title).toMatch(/\d{4}-\d{2}-\d{2} \d{2}:\d{2} UTC/);
    expect(title).toContain("whole days elapsed");
  });

  test("a history shorter than the minimum says how many days are missing and when", async ({ page }) => {
    await openDashboard(page, "single", "#insight");
    await page.getByTestId("ins-view-dates").click();
    const note = page.getByTestId("hist-gap-dates");
    await expect(note).toBeVisible();
    await expect(note).toContainText("Insufficient history");
    await expect(note).toContainText("estimated date");
    expect(Number(await note.getAttribute("data-missing"))).toBeGreaterThan(0);
    for (const view of ["deps", "miles", "debt"]) {
      await page.getByTestId(`ins-view-${view}`).click();
      await expect(page.getByTestId(`hist-gap-${view}`)).toBeVisible();
    }
  });

  test("with enough history the note is not shown", async ({ page }) => {
    await openDashboard(page, "full", "#insight");
    await page.getByTestId("ins-view-dates").click();
    await expect(page.getByTestId("hist-gap-dates")).toHaveCount(0);
  });
});

test.describe("architecture", () => {
  test("a repository named in a block opens its panel, with the keyboard too; names that are not repositories stay text", async ({ page }) => {
    // The fixture has no repository with the names of the architecture, so one is added to the data the page reads.
    await page.addInitScript(() => {
      const parse = JSON.parse;
      JSON.parse = function (text: string, reviver?: any) {
        const value = parse(text, reviver);
        if (value && value.config && value.repos && !value.repos["HYDRA-UMC-OS"]) {
          value.repos["HYDRA-UMC-OS"] = { eco: "hydra-umc", ecoLabel: "HYDRA-UMC", maturity: "functional", evidence: "", role: "", roleKey: "", stack: "c", deploy: "", deployKey: "", family: "", parent: "", hardware: null, version: "0.1.0", known: false, ci: null, release: null, commitDate: null, commits: null, sig: null, builtOn: "", sigKind: "", signedOn: "", artifact: "", pipeline: "undeclared" };
        }
        return value;
      } as typeof JSON.parse;
    });
    await openDashboard(page, "full", "#architecture");
    const buttons = page.locator("#panel-architecture button.arch-repo");
    expect(await buttons.count()).toBeGreaterThan(0);
    await expect(buttons.first()).toHaveAccessibleName("Open the panel of HYDRA-UMC-OS");
    await expect(page.locator("#panel-architecture li", { hasText: "CM5 / Linux" }).locator("button")).toHaveCount(0);
    await buttons.first().focus();
    await page.keyboard.press("Enter");
    await expect(page.getByTestId("repo-panel")).toBeVisible();
    await expect(page.getByTestId("repo-panel-title")).toHaveText("HYDRA-UMC-OS");
    await page.keyboard.press("Escape");
    await expect(buttons.first()).toBeFocused();
  });
});

test.describe("optional alert about green builds without a signed release", () => {
  test("it is off in the published configuration", async ({ page }) => {
    await openDashboard(page, "full", "#summary");
    await expect(page.locator("li[data-kind='unsigned']")).toHaveCount(0);
  });

  test("when the configuration turns it on it names the repositories that built on GitHub Actions and have no signature", async ({ page }) => {
    await page.addInitScript(() => {
      const parse = JSON.parse;
      JSON.parse = function (text: string, reviver?: any) {
        const value = parse(text, reviver);
        if (value && value.config && value.repos) value.config.signature_alert = { enabled: true, after_days: 14 };
        return value;
      } as typeof JSON.parse;
    });
    await openDashboard(page, "full", "#summary");
    const items = page.locator("li[data-kind='unsigned']");
    expect(await items.count()).toBeGreaterThan(0);
    const first = items.first();
    await expect(first).toContainText("Green build without signed release");
    await expect(first.locator("a")).toHaveAttribute("href", /^https:\/\/github\.com\/JuanenRac\/[A-Za-z0-9._-]+\/releases$/);
    // a repository with the signature file present is never named
    const names = await items.locator("a").allTextContents();
    expect(names).not.toContain("ARMOR-FIXTURE-00");
  });
});

test.describe("quality", () => {
  for (const lang of LANGS) {
    test(`${lang}: no key or placeholder shows in the evidence, the projects and the analysis`, async ({ page }) => {
      await openDashboard(page, "full");
      await page.selectOption("#lang-select", lang);
      for (const tab of ["evidence", "projects", "insight", "tests"]) {
        await gotoTab(page, tab);
        const text = await visibleText(page);
        expect(text, tab).not.toMatch(LEFTOVER);
      }
      await gotoTab(page, "evidence");
      await page.locator('#ev-table td[data-item="signed"] button.ev-why-btn').first().click();
      expect(await visibleText(page)).not.toMatch(LEFTOVER);
    });
  }

  for (const scheme of ["light", "dark"] as const) {
    test(`${scheme}: no serious accessibility problem in the new parts`, async ({ page }) => {
      test.setTimeout(240_000);
      await page.emulateMedia({ colorScheme: scheme });
      await openDashboard(page, "full", "#evidence");
      await page.locator('#ev-table td[data-item="signed"] button.ev-why-btn').first().click();
      expect(await serious(page), "evidence").toEqual([]);
      await gotoTab(page, "projects");
      expect(await serious(page), "projects").toEqual([]);
      await openDashboard(page, "full", "#projects?repo=ARMOR-FIXTURE-00");
      expect(await serious(page), "panel").toEqual([]);
      await gotoTab(page, "insight");
      expect(await serious(page), "insight").toEqual([]);
      await openDashboard(page, "single", "#insight");
      await page.getByTestId("ins-view-dates").click();
      expect(await serious(page), "history gap").toEqual([]);
    });
  }

  for (const [w, h] of [[1920, 1080], [1366, 768], [390, 844]] as const) {
    test(`${w}x${h}: the evidence tab does not scroll sideways`, async ({ page }) => {
      await page.setViewportSize({ width: w, height: h });
      await openDashboard(page, "full", "#evidence");
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      expect(overflow).toBeLessThanOrEqual(1);
    });
  }

  test("print: the buttons that only work on screen are not printed", async ({ page }) => {
    await openDashboard(page, "full", "#evidence");
    await page.locator('#ev-table td[data-item="signed"] button.ev-why-btn').first().click();
    await page.emulateMedia({ media: "print" });
    await expect(page.getByTestId("side-toggle")).toBeHidden();
    await expect(page.getByTestId("tabs-scroll-next")).toBeHidden();
  });

  test("no request of its own leaves the page", async ({ page }) => {
    const requests: string[] = [];
    page.on("request", (r) => { if (/^https?:/.test(r.url()) && !r.url().startsWith("https://api.github.com/") && !/fonts|\.svg/.test(r.url())) requests.push(r.url()); });
    await openDashboard(page, "full", "#evidence");
    await page.locator('#ev-table td[data-item="signed"] button.ev-why-btn').first().click();
    expect(requests).toEqual([]);
  });
});
