import { test, expect, openDashboard, gotoTab, panel } from "./helpers";

test.describe("disclosures", () => {
  test("a project's notes open and close with the toggle (and the state follows aria-expanded)", async ({ page }) => {
    await openDashboard(page);
    await gotoTab(page, "projects");
    const toggle = page.locator("tr.project-row").first().locator(".details-toggle");
    const target = page.locator("#" + (await toggle.getAttribute("data-details-target")));
    await expect(target).toBeHidden();
    await toggle.click();
    await expect(toggle).toHaveAttribute("aria-expanded", "true");
    await expect(target).toBeVisible();
    await expect(target).toContainText("Fixture project number");
    await toggle.click();
    await expect(toggle).toHaveAttribute("aria-expanded", "false");
    await expect(target).toBeHidden();
  });

  test("the toggle works with the keyboard", async ({ page }) => {
    await openDashboard(page);
    await gotoTab(page, "projects");
    const toggle = page.locator("tr.project-row").first().locator(".details-toggle");
    await toggle.focus();
    await page.keyboard.press("Enter");
    await expect(toggle).toHaveAttribute("aria-expanded", "true");
    await page.keyboard.press("Space");
    await expect(toggle).toHaveAttribute("aria-expanded", "false");
  });

  test("the errors / unknown details open and close", async ({ page }) => {
    await openDashboard(page);
    await gotoTab(page, "errors");
    const details = panel(page, "errors").locator("details");
    expect(await details.count()).toBeGreaterThan(0);
    const first = details.first();
    const initial = await first.evaluate((d) => (d as HTMLDetailsElement).open);
    await first.locator("summary").click();
    expect(await first.evaluate((d) => (d as HTMLDetailsElement).open)).toBe(!initial);
    await first.locator("summary").click();
    expect(await first.evaluate((d) => (d as HTMLDetailsElement).open)).toBe(initial);
  });

  test("the errors tab names the repositories that have a problem, and the unresolved versions", async ({ page }) => {
    await openDashboard(page);
    await gotoTab(page, "errors");
    const text = await panel(page, "errors").innerText();
    expect(text).toContain("URTC-FIXTURE-GHOST");
    expect(text).toContain("ARMOR-FIXTURE-BAD");
    expect(text).toContain("FIXTURE-08");
  });

  test("the architecture switcher shows one ecosystem at a time", async ({ page }) => {
    await openDashboard(page);
    await gotoTab(page, "architecture");
    for (const view of ["hydra-umc", "urtc", "armor", "eh3d"]) {
      await page.locator(`[data-arch-view="${view}"]`).click();
      await expect(page.locator(`[data-arch-view="${view}"]`)).toHaveAttribute("aria-pressed", "true");
      await expect(page.locator(".arch-panel:not([hidden])")).toHaveCount(1);
      await expect(page.locator(`[data-arch-panel="${view}"]`)).toBeVisible();
      await expect(page.getByTestId(`arch-${view}`)).toBeVisible();
    }
  });

  test("the compatibility view buttons switch panels", async ({ page }) => {
    await openDashboard(page);
    await gotoTab(page, "inventory");
    const buttons = page.locator("[data-compat-view]");
    const n = await buttons.count();
    expect(n).toBeGreaterThan(1);
    for (let i = 0; i < n; i++) {
      await buttons.nth(i).click();
      const view = await buttons.nth(i).getAttribute("data-compat-view");
      await expect(page.locator(`[data-compat-panel="${view}"]`)).toBeVisible();
    }
  });
});

test.describe("links", () => {
  test("every project links to https://github.com/JuanenRac/<name> and the rows match the KPI", async ({ page }) => {
    await openDashboard(page);
    await gotoTab(page, "projects");
    const rows = page.locator("tr.project-row");
    const count = await rows.count();
    await expect(page.locator("#health-total")).toHaveText(String(count));
    const titles = await rows.locator(".project-title a").evaluateAll((as) => as.map((a) => [a.getAttribute("href"), a.textContent]));
    expect(titles).toHaveLength(count);
    for (const [href, name] of titles) expect(href).toBe(`https://github.com/JuanenRac/${name!.trim()}`);
    expect(new Set(titles.map((t) => t[0])).size).toBe(count);
  });

  test("every link of the page is https (or an in-page anchor) and opens safely", async ({ page }) => {
    await openDashboard(page);
    const links = await page.locator("a[href]").evaluateAll((as) => as.map((a) => ({
      href: a.getAttribute("href") || "", target: a.getAttribute("target"), rel: a.getAttribute("rel") || "", text: (a.textContent || "").trim(),
    })));
    expect(links.length).toBeGreaterThan(100);
    for (const link of links) {
      if (link.href.startsWith("#")) continue;
      expect(link.href, link.text).toMatch(/^https:\/\//);
      expect(link.href, link.text).not.toMatch(/\s|undefined|null|\{/);
      if (link.target === "_blank") expect(link.rel, link.href).toMatch(/noopener/);
      if (link.href.startsWith("https://github.com/")) expect(link.href).toMatch(/^https:\/\/github\.com\/JuanenRac(\/|$)/);
    }
  });

  test("every in-page anchor points to an element that exists", async ({ page }) => {
    await openDashboard(page);
    const missing = await page.evaluate(() => Array.from(document.querySelectorAll("a[href^='#']:not(.crumbs a)"))
      .map((a) => a.getAttribute("href")!.slice(1)).filter((id) => id && !document.getElementById(id)));
    expect(missing).toEqual([]);
  });

  test("the links of the breadcrumb are routes of the page itself", async ({ page }) => {
    await openDashboard(page, "full", "#projects?scope=urtc");
    const hrefs = await page.locator(".crumbs a").evaluateAll((as) => as.map((a) => a.getAttribute("href")));
    expect(hrefs).toEqual(["#summary", "#projects"]);
  });

  test("the release lists link to the repositories", async ({ page }) => {
    await openDashboard(page);
    const hrefs = await page.locator("[data-testid=latest-releases] a, [data-testid=oldest-releases] a").evaluateAll((as) => as.map((a) => a.getAttribute("href")));
    expect(hrefs.length).toBeGreaterThan(0);
    for (const href of hrefs) expect(href).toMatch(/^https:\/\/github\.com\/JuanenRac\/[A-Za-z0-9._-]+/);
  });

  test("the project links open in a new tab, so the app itself stays put", async ({ page }) => {
    await openDashboard(page);
    await gotoTab(page, "projects");
    expect(await page.locator("tr.project-row .project-title a").first().getAttribute("target")).toBe("_blank");
  });
});
