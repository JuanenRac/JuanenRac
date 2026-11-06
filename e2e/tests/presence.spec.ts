import AxeBuilder from "@axe-core/playwright";
import { test, expect, openDashboard, gotoTab, LANGS, LEFTOVER, visibleText, Page, Variant } from "./helpers";

// The card "Signature and attestation of the latest release" of the Sentinel tab and the two fields of the panel of a repository. Presence only: no key and no
// proof is verified. Fixture (full): 40 repositories, 8 without a release, 32 with release files (8 per ecosystem); signature present 16, absent 8, unknown 8;
// attestation present 6, partial 6, absent 6, unknown 14.

async function serious(page: Page) {
  const results = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"]).analyze();
  return results.violations.filter((v) => v.impact === "serious" || v.impact === "critical").map((v) => `${v.id}: ${v.nodes.slice(0, 3).map((n) => n.target.join(" ")).join(" | ")}`);
}

async function open(page: Page, variant: Variant = "full") {
  await page.clock.setFixedTime(new Date("2001-12-21T12:30:00Z"));
  await openDashboard(page, variant);
  await gotoTab(page, "sentinel");
}

test.describe("presence of signature and attestation", () => {
  test("the card counts the repositories with release files by ecosystem", async ({ page }) => {
    await open(page);
    await expect(page.locator("#pr-title")).toHaveText("Signature and attestation of the latest release");
    const rows = page.getByTestId("pr-eco-table").locator("tbody tr");
    await expect(rows).toHaveCount(4);
    const cells = await rows.evaluateAll((trs) => trs.map((tr) => Array.from(tr.querySelectorAll("td")).map((td) => Number(td.textContent))));
    for (const row of cells) expect(row[0]).toBe(8);
    const sum = (col: number) => cells.reduce((acc, row) => acc + row[col], 0);
    expect([sum(1), sum(2), sum(3), sum(4)]).toEqual([16, 0, 8, 8]);        // signature: present, partial, absent, unknown
    expect([sum(5), sum(6), sum(7), sum(8)]).toEqual([6, 6, 6, 14]);        // attestation
  });

  test("every repository with release files has a row with a glyph and a word, the worst first", async ({ page }) => {
    await open(page);
    const rows = page.getByTestId("pr-repo-table").locator("tbody tr");
    await expect(rows).toHaveCount(32);
    const first = rows.first();
    await expect(first.locator(".pr-st").first()).toHaveAttribute("data-state", "absent");
    await expect(first.locator(".pr-st .sn-gl").first()).toHaveText("✕");
    await expect(first.locator(".pr-st").first()).toContainText("Absent");
    await expect(page.getByTestId("pr-repo-table").locator("tr[data-repo=ARMOR-FIXTURE-00] .pr-st[data-state=present]")).toHaveCount(2);
    await expect(page.getByTestId("pr-repo-table").locator("tr[data-repo=ARMOR-FIXTURE-00]")).toContainText("1 of 1 files have a signature file");
    await expect(page.getByTestId("pr-repo-table").locator(".pr-st[data-state=unknown]").first()).toContainText("Unknown");
  });

  test("a repository without a release is not in the card and the panel says what it knows", async ({ page }) => {
    await open(page);
    const names = await page.getByTestId("pr-repo-table").locator("tbody tr").evaluateAll((trs) => trs.map((tr) => tr.getAttribute("data-repo")));
    expect(names.length).toBe(32);
    await page.getByTestId("pr-repo-table").locator("tr[data-repo=ARMOR-FIXTURE-00] button").click();
    const fields = page.locator("#repo-fields");
    await expect(fields).toContainText("Signature files");
    await expect(fields).toContainText("Build attestation");
    await expect(fields.locator(".pr-st[data-state=present]")).toHaveCount(2);
  });

  test("the 8 languages have no key or placeholder left", async ({ page }) => {
    await open(page);
    const titles = new Set<string>();
    for (const lang of LANGS) {
      await page.locator("#lang-select").selectOption(lang);
      expect(await visibleText(page), lang).not.toMatch(LEFTOVER);
      titles.add((await page.locator("#pr-title").textContent()) || "");
      await expect(page.getByTestId("pr-repo-table")).not.toContainText("{");
    }
    expect(titles.size).toBe(8);
    await page.locator("#lang-select").selectOption("pt");
    await expect(page.locator("#pr-title")).toHaveText("Assinatura e atestação da última versão");
  });

  test("axe finds nothing serious in either theme", async ({ page }) => {
    await open(page);
    expect(await serious(page)).toEqual([]);
    await page.emulateMedia({ colorScheme: "light" });
    expect(await serious(page)).toEqual([]);
  });

  test("with nothing read the card says not verified and never a state", async ({ page }) => {
    await open(page, "partial");
    await expect(page.getByTestId("pr-none")).toBeVisible();
    await expect(page.getByTestId("pr-none")).not.toHaveText("");
    await expect(page.locator(".pr-st[data-state=present]")).toHaveCount(0);
    await expect(page.locator(".pr-st[data-state=absent]")).toHaveCount(0);
  });
});
