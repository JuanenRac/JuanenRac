import { test, expect, openDashboard, gotoTab, LANGS } from "./helpers";

// The coverage card of the summary, and the honest "not measured / not verified" state of the new cards of the Builds and Scripts tabs while a reading does not carry
// their figures. Fixture (full): the dashboard lists every repository with a manifest and three public ones have none; (partial): the list of repositories was not read.

test.describe("coverage card", () => {
  test("it gives the three figures and names the repositories without a manifest", async ({ page }) => {
    await openDashboard(page, "full");
    const card = page.getByTestId("eco-unclassified");
    await expect(card).toBeVisible();
    await expect(card).toHaveAttribute("data-state", "gap");
    await expect(card.locator(".sub")).toHaveAttribute("data-without", "3");
    await expect(card.locator(".number")).toHaveText("3");
    await expect(card).toHaveAttribute("title", /fixture-plain-a/);
    const owner = Number(await card.locator(".sub").getAttribute("data-owner"));
    const shown = Number(await card.locator(".sub").getAttribute("data-shown"));
    expect(owner - shown).toBe(3);
    await expect(card.locator(".sub")).toHaveText(`owner ${owner} · shown ${shown} · no manifest 3`);
  });

  test("with nothing unclassified it is a zero and not a gap", async ({ page }) => {
    await openDashboard(page, "healthy");
    const card = page.getByTestId("eco-unclassified");
    await expect(card).toHaveAttribute("data-state", "ok");
    await expect(card.locator(".number")).toHaveText("0");
  });

  test("a list of repositories that could not be read says not verified, never zero", async ({ page }) => {
    await openDashboard(page, "partial");
    const card = page.getByTestId("eco-unclassified");
    await expect(card).toHaveAttribute("data-state", "unknown");
    await expect(card.locator(".number")).toHaveText("–");
    await expect(card.locator(".sub")).toHaveText("not verified");
  });

  test("the label and the figures follow the language", async ({ page }) => {
    await openDashboard(page, "full");
    await page.locator("#lang-select").selectOption("de");
    await expect(page.getByTestId("eco-unclassified").locator(".label")).toHaveText("Nicht zugeordnet");
    await expect(page.getByTestId("eco-unclassified").locator(".sub")).toContainText("Inhaber");
    await page.locator("#lang-select").selectOption("pt");
    await expect(page.getByTestId("eco-unclassified").locator(".label")).toHaveText("Sem classificação");
  });
});

test.describe("new cards without figures", () => {
  test("the speed figures of the Builds tab are in a closed section that opens on a click", async ({ page }) => {
    await openDashboard(page, "full");
    await gotoTab(page, "actions");
    const section = page.getByTestId("ac-perf");
    await expect(section).toBeVisible();
    await expect(section).not.toHaveAttribute("open", "");
    await expect(page.locator("#ac-perf-title")).toHaveText("Speed, queue and flaky runs");
    await page.locator("#ac-perf-title").click();
    await expect(section).toHaveAttribute("open", "");
    await expect(page.getByTestId("ac-perf-body")).toBeVisible();
    await expect(page.getByTestId("ac-perf-none")).toBeHidden();
    await expect(page.getByTestId("ac-perf-kpis").locator("li")).toHaveCount(4);
    await expect(page.getByTestId("ac-perf-k-dur").locator("b")).toHaveText(/\S+ · \S+/);
  });

  test("when no reading carries the speed figures the section says not measured, never zero", async ({ page }) => {
    await openDashboard(page, "partial");
    await gotoTab(page, "actions");
    await page.locator("#ac-perf-title").click();
    await expect(page.getByTestId("ac-perf-none")).toBeVisible();
    await expect(page.getByTestId("ac-perf-body")).toBeHidden();
  });

  test("the lint card of the Scripts tab says it is not verified when the count does not carry the findings", async ({ page }) => {
    await openDashboard(page, "full");
    await gotoTab(page, "scripts");
    await expect(page.getByTestId("sc-lint-none")).toBeVisible();
    await expect(page.getByTestId("sc-lint-body")).toBeHidden();
    await expect(page.getByTestId("sc-kpis").locator("li")).toHaveCount(7);
  });

  for (const lang of LANGS) {
    test(`the titles of both cards are translated in ${lang}`, async ({ page }) => {
      await openDashboard(page, "full");
      await page.locator("#lang-select").selectOption(lang);
      await gotoTab(page, "actions");
      const perf = await page.locator("#ac-perf-title").innerText();
      await gotoTab(page, "scripts");
      const lint = await page.locator("#sc-lint-title").innerText();
      for (const text of [perf, lint]) {
        expect(text.length).toBeGreaterThan(3);
        expect(text).not.toMatch(/ac_perf|sc_lint|undefined|\{\w+\}/);
      }
      if (lang !== "en") {
        expect(perf).not.toBe("Speed, queue and flaky runs");
        expect(lint).not.toBe("Workflow lint: three levels");
      }
    });
  }
});
