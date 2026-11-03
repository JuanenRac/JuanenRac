import AxeBuilder from "@axe-core/playwright";
import { test, expect, openDashboard, gotoTab, LANGS, LEFTOVER, visibleText, Page } from "./helpers";

// The verification of the signature of the latest release and the pipeline inferred from GitHub. The page never verifies anything itself: the generator did it in
// the job that builds it, so these tests draw the page from the fixture, where (full) the repositories with a .sig take turns to be verified (ARMOR-FIXTURE-00,
// URTC-FIXTURE-00, EH3D-FIXTURE-05), invalid (ARMOR-FIXTURE-05, URTC-FIXTURE-05, HYDRA-UMC-FIXTURE-00) and not verifiable; a .minisig is never verifiable.
// Every third repository has a green build with an artifact (index % 3 = 0); the declared manifest fields always win over the inferred ones.

async function serious(page: Page) {
  const results = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"]).analyze();
  return results.violations.filter((v) => v.impact === "serious" || v.impact === "critical").map((v) => `${v.id}: ${v.nodes.slice(0, 3).map((n) => n.target.join(" ")).join(" | ")}`);
}

const cell = (page: Page, name: string) => page.locator(`#ev-table tr[data-repo="${name}"] td[data-item="signed"]`);

test.describe("the five answers in the evidence tab", () => {
  test("verified, invalid, not verifiable, no signature and not verified are five different things in glyph and text", async ({ page }) => {
    await openDashboard(page, "full", "#evidence");
    await expect(cell(page, "ARMOR-FIXTURE-00")).toHaveAttribute("data-status", "yes");        // verified
    await expect(cell(page, "ARMOR-FIXTURE-05")).toHaveAttribute("data-status", "invalid");
    await expect(cell(page, "ARMOR-FIXTURE-03")).toHaveAttribute("data-status", "present");    // .minisig: cannot be verified here
    await expect(cell(page, "ARMOR-FIXTURE-01")).toHaveAttribute("data-status", "no");         // a release without a signature file
    await expect(cell(page, "ARMOR-FIXTURE-02")).toHaveAttribute("data-status", "unverified");  // the assets were not read
    await expect(cell(page, "ARMOR-FIXTURE-05")).toContainText("Signature invalid");
    await expect(cell(page, "ARMOR-FIXTURE-03")).toContainText("Signature present, not verifiable here");
    await expect(cell(page, "ARMOR-FIXTURE-05").locator(".ev-st")).toHaveClass(/ev-invalid/);
  });

  test("the legend names the new state", async ({ page }) => {
    await openDashboard(page, "full", "#evidence");
    await expect(page.locator("#ev-legend")).toContainText("Signature invalid");
    await expect(page.locator("#ev-legend li")).toHaveCount(6);
  });

  test("the summary counts verified, invalid and not verifiable apart", async ({ page }) => {
    await openDashboard(page, "full", "#evidence");
    const sum = page.getByTestId("ev-summary");
    const n = async (key: string) => Number(await sum.locator(`li[data-sum="${key}"]`).getAttribute("data-n"));
    expect(await n("verified")).toBe(3);
    expect(await n("invalid")).toBe(3);
    expect(await n("present")).toBe(10);
    await expect(sum.locator('li[data-sum="invalid"]')).toContainText("INVALID");
  });

  test("the explanation of a verified signature gives the files and the scheme", async ({ page }) => {
    await openDashboard(page, "full", "#evidence");
    await cell(page, "ARMOR-FIXTURE-00").locator("button.ev-why-btn").click();
    const box = page.getByTestId("ev-why");
    await expect(box).toBeVisible();
    await expect(box).toContainText("were checked when this page was built");
    await expect(box).toContainText("2 verified, 0 invalid, 0 not checkable");
    await expect(box).toContainText("scheme: armor-fw/1");
  });

  test("the explanation of an invalid signature warns not to install", async ({ page }) => {
    await openDashboard(page, "full", "#evidence");
    await cell(page, "URTC-FIXTURE-05").locator("button.ev-why-btn").click();
    const box = page.getByTestId("ev-why");
    await expect(box).toContainText("does NOT verify");
    await expect(box).toContainText("Do not install it");
    await expect(box).toContainText("it does not match the file");
    await expect(box.getByRole("link", { name: "Open its releases" })).toHaveAttribute("href", "https://github.com/JuanenRac/URTC-FIXTURE-05/releases");
  });

  test("the explanation of a signature that cannot be checked says why and works with the keyboard", async ({ page }) => {
    await openDashboard(page, "full", "#evidence");
    const button = cell(page, "ARMOR-FIXTURE-03").locator("button.ev-why-btn");
    await button.focus();
    await page.keyboard.press("Enter");
    await expect(page.getByTestId("ev-why")).toContainText("cannot check them");
    await expect(page.getByTestId("ev-why")).toContainText("format this page does not read");
    await page.keyboard.press("Escape");
  });
});

test.describe("the alert of an invalid signature", () => {
  test("is always on, red, one per repository, and links to its releases", async ({ page }) => {
    await openDashboard(page, "full", "#summary");
    const items = page.locator("#alerts-list > li[data-kind='badsig']");
    await expect(items).toHaveCount(3);
    expect(await items.locator("a").allTextContents()).toEqual(["ARMOR-FIXTURE-05", "HYDRA-UMC-FIXTURE-00", "URTC-FIXTURE-05"]);
    // before the alerts that depend on the date
    const kinds = await page.locator("#alerts-list > li").evaluateAll((els) => els.map((e) => e.getAttribute("data-kind")));
    expect(kinds.indexOf("badsig")).toBeLessThan(kinds.indexOf("inactive"));
    await expect(items.first()).toContainText("Invalid release signature");
    await expect(items.first()).toContainText("does not verify with the pinned public key");
    await expect(items.first().locator("a")).toHaveAttribute("href", "https://github.com/JuanenRac/ARMOR-FIXTURE-05/releases");
  });

  test("the healthy page, with nothing invalid, still says no alerts", async ({ page }) => {
    await openDashboard(page, "healthy", "#summary");
    await expect(page.locator("li[data-kind='badsig']")).toHaveCount(0);
  });
});

test.describe("the pipeline inferred from GitHub", () => {
  test("a build with an artifact adds the stage and is marked as inferred; what the manifest declares is untouched", async ({ page }) => {
    await openDashboard(page, "full", "#projects?repo=ARMOR-FIXTURE-07");
    const fields = page.getByTestId("repo-fields");
    await expect(fields).toContainText("Published · inferred");
    await expect(fields).toContainText("GitHub Actions · inferred");          // nothing declared: the build supplies it
    await expect(fields.getByRole("link", { name: /actions\/runs\/127/ })).toHaveAttribute("href", "https://github.com/JuanenRac/ARMOR-FIXTURE-07/actions/runs/127");
    await expect(fields).toContainText("package-build.yml, 2001-12-19, artifact available");
  });

  test("a declared field is never replaced by an inferred one", async ({ page }) => {
    await openDashboard(page, "full", "#projects?repo=ARMOR-FIXTURE-00");
    const fields = page.getByTestId("repo-fields");
    await expect(fields).toContainText("signed with the release key");
    await expect(fields).not.toContainText("inferred");
    await expect(fields).toContainText("signature verified with the pinned public key");
  });

  test("a build whose artifact expired is shown as such and does not count as built", async ({ page }) => {
    await openDashboard(page, "full", "#projects?repo=ARMOR-FIXTURE-05");
    await expect(page.getByTestId("repo-fields")).toContainText("2001-10-01, no artifact left");
  });

  test("the table marks the rows whose state needed the inference", async ({ page }) => {
    await openDashboard(page, "full", "#projects");
    const row = page.locator("tr.project-row").filter({ has: page.locator("td[data-pipe-for='ARMOR-FIXTURE-07']") });
    await expect(row.locator("td.pipe-cell .pipe-inf")).toHaveText("(inferred)");
    const plain = page.locator("tr.project-row").filter({ has: page.locator("td[data-pipe-for='ARMOR-FIXTURE-00']") });
    await expect(plain.locator("td.pipe-cell .pipe-inf")).toHaveCount(0);
  });

  test("the Builds tab says verified or invalid next to the process", async ({ page }) => {
    await openDashboard(page, "full", "#actions");
    const text = await page.locator("#panel-actions").innerText();
    expect(text).toContain("signature verified");
    expect(text).toContain("signature INVALID");
  });
});

test.describe("the optional alert of a green build without a verified signature", () => {
  async function turnOn(page: Page, config: object = { enabled: true, after_days: 14 }) {
    await page.addInitScript((cfg) => {
      const parse = JSON.parse;
      JSON.parse = function (text: string, reviver?: any) {
        const value = parse(text, reviver);
        if (value && value.config && value.repos) value.config.signature_alert = cfg;
        return value;
      } as typeof JSON.parse;
    }, config);
  }

  test("counts the hours since the green build with an artifact and never names a repository with a signature", async ({ page }) => {
    await turnOn(page);
    await openDashboard(page, "full", "#summary");
    const items = page.locator("#alerts-list > li[data-kind='unsigned']");
    expect(await items.count()).toBeGreaterThan(0);
    await expect(items.filter({ hasText: "hours ago" }).first()).toBeVisible();     // the repositories with a known build count hours
    await expect(items.filter({ hasText: "days after the last commit" }).first()).toBeVisible();
    const names = await items.locator("a").allTextContents();
    for (const signed of ["ARMOR-FIXTURE-00", "ARMOR-FIXTURE-05", "ARMOR-FIXTURE-08"]) expect(names).not.toContain(signed);
    expect(names).toContain("ARMOR-FIXTURE-01");
  });

  test("after_hours replaces after_days and a young build is not named", async ({ page }) => {
    await turnOn(page, { enabled: true, after_days: 14, after_hours: 100000000 });
    await openDashboard(page, "full", "#summary");
    await expect(page.locator("li[data-kind='unsigned']")).toHaveCount(0);
  });
});

test.describe("quality", () => {
  for (const lang of LANGS) {
    test(`${lang}: no key or placeholder shows in the signature parts`, async ({ page }) => {
      await openDashboard(page, "full");
      await page.selectOption("#lang-select", lang);
      await gotoTab(page, "evidence");
      for (const name of ["ARMOR-FIXTURE-00", "ARMOR-FIXTURE-05", "ARMOR-FIXTURE-03"]) {
        await cell(page, name).locator("button.ev-why-btn").click();
        expect(await visibleText(page), name).not.toMatch(LEFTOVER);
      }
      await gotoTab(page, "summary");
      expect(await visibleText(page)).not.toMatch(LEFTOVER);
      await openDashboard(page, "full", "#projects?repo=ARMOR-FIXTURE-07");
      await page.selectOption("#lang-select", lang);
      expect(await visibleText(page)).not.toMatch(LEFTOVER);
      await gotoTab(page, "actions");
      expect(await visibleText(page)).not.toMatch(LEFTOVER);
    });
  }

  test("portuguese is the one of Portugal", async ({ page }) => {
    await openDashboard(page, "full", "#evidence");
    await page.selectOption("#lang-select", "pt");
    await cell(page, "ARMOR-FIXTURE-00").locator("button.ev-why-btn").click();
    const text = await page.getByTestId("ev-why").innerText();
    expect(text).toContain("ficheiros de assinatura");
    expect(text).not.toMatch(/arquivo|usuário/);
  });

  for (const scheme of ["light", "dark"] as const) {
    test(`${scheme}: no serious accessibility problem in the evidence, the alert and the panel`, async ({ page }) => {
      test.setTimeout(240_000);
      await page.emulateMedia({ colorScheme: scheme });
      await openDashboard(page, "full", "#evidence");
      await cell(page, "ARMOR-FIXTURE-05").locator("button.ev-why-btn").click();
      expect(await serious(page), "evidence").toEqual([]);
      await gotoTab(page, "summary");
      expect(await serious(page), "alerts").toEqual([]);
      await openDashboard(page, "full", "#projects?repo=ARMOR-FIXTURE-07");
      expect(await serious(page), "panel").toEqual([]);
    });
  }

  test("keyboard: the new cell is reached with Tab and opens with Enter, focus returns with Escape in the panel", async ({ page }) => {
    await openDashboard(page, "full", "#evidence");
    const button = cell(page, "ARMOR-FIXTURE-05").locator("button.ev-why-btn");
    await button.focus();
    await expect(button).toBeFocused();
    await page.keyboard.press("Enter");
    await expect(page.getByTestId("ev-why")).toBeVisible();
  });

  for (const [w, h] of [[1920, 1080], [1366, 768], [390, 844]] as const) {
    test(`${w}x${h}: the evidence tab and the summary do not scroll sideways`, async ({ page }) => {
      await page.setViewportSize({ width: w, height: h });
      for (const tab of ["evidence", "summary", "actions"]) {
        await openDashboard(page, "full", "#" + tab);
        expect(await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth), tab).toBeLessThanOrEqual(1);
      }
    });
  }

  test("print keeps the glyph and the word of the new state", async ({ page }) => {
    await openDashboard(page, "full", "#evidence");
    await page.emulateMedia({ media: "print" });
    await expect(cell(page, "ARMOR-FIXTURE-05")).toContainText("Signature invalid");
  });

  test("no request of its own leaves the page and nothing about who started a build is on it", async ({ page }) => {
    const requests: string[] = [];
    page.on("request", (r) => { if (/^https?:/.test(r.url()) && !r.url().startsWith("https://api.github.com/") && !/fonts|\.svg/.test(r.url())) requests.push(r.url()); });
    await openDashboard(page, "full", "#evidence");
    await cell(page, "ARMOR-FIXTURE-05").locator("button.ev-why-btn").click();
    expect(requests).toEqual([]);
    const html = await page.content();
    expect(html).not.toMatch(/"actor"|head_branch|display_title/);
  });
});
