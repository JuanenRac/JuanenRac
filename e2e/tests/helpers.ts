import { test as base, expect, Page } from "@playwright/test";

export const TABS = ["summary", "hydra-umc", "urtc", "armor", "eh3d", "projects", "evidence", "tests", "actions", "insight", "inventory", "rack", "architecture", "errors"] as const;
export const LANGS = ["en", "es", "de", "fr", "it", "ja", "zh", "pt"] as const;
export const ECOSYSTEMS = ["hydra-umc", "urtc", "armor", "eh3d"] as const;
export type Variant = "full" | "stale" | "healthy" | "minimal" | "partial" | "empty";

const SVG = '<svg xmlns="http://www.w3.org/2000/svg" width="1" height="1"/>';

/** No test ever reaches the network: the few external resources of the page are answered here. */
export async function stubNetwork(page: Page, options: { freshnessFails?: boolean } = {}) {
  await page.route(/^https?:\/\//, async (route) => {
    const url = route.request().url();
    if (url.startsWith("https://api.github.com/")) {
      if (options.freshnessFails) return route.fulfill({ status: 200, contentType: "application/json", headers: { "access-control-allow-origin": "*" }, body: "{}" });
      return route.fulfill({
        status: 200,
        contentType: "application/json",
        headers: { "access-control-allow-origin": "*" },
        body: JSON.stringify({ workflow_runs: [{ conclusion: "success", updated_at: new Date().toISOString() }] }),
      });
    }
    if (url.includes("fonts.googleapis.com")) return route.fulfill({ status: 200, contentType: "text/css", body: "" });
    if (url.includes("fonts.gstatic.com")) return route.fulfill({ status: 200, contentType: "font/woff2", body: "" });
    if (/\.svg(\?|$)/.test(url)) return route.fulfill({ status: 200, contentType: "image/svg+xml", body: SVG });
    return route.fulfill({ status: 200, contentType: "text/html", body: "<!doctype html><title>stub</title>" });
  });
}

type Fixtures = { problems: string[] };

/** Every test collects console errors and uncaught page errors and fails when there is one. */
export const test = base.extend<Fixtures>({
  locale: "en-US",
  colorScheme: "dark",
  problems: [async ({ page }, use) => {
    const problems: string[] = [];
    page.on("console", (message) => {
      if (message.type() === "error") problems.push("console: " + message.text());
    });
    page.on("pageerror", (error) => problems.push("page: " + error.message));
    await stubNetwork(page);
    await use(problems);
    expect(problems, "console and page errors").toEqual([]);
  }, { auto: true }],
});
export { expect };

export async function openDashboard(page: Page, variant: Variant = "full", hash = "") {
  await page.goto(`${variant}/index.html${hash}`);
  await page.waitForSelector("[role=tab][aria-selected=true]");
}

export async function gotoTab(page: Page, id: string) {
  await page.getByTestId(`tab-${id}`).click();
  await expect(page.locator(`#panel-${id}`)).toBeVisible();
}

export const panel = (page: Page, id: string) => page.locator(`#panel-${id}`);

export async function shown(page: Page): Promise<{ shown: number; total: number }> {
  const el = page.locator("#filters-count");
  return { shown: Number(await el.getAttribute("data-shown")), total: Number(await el.getAttribute("data-total")) };
}

export async function visibleRows(page: Page): Promise<number> {
  return page.locator("tr.project-row[data-match=\"1\"]").count();
}

/** Texts that must never be on screen: an untranslated key, a JavaScript leftover or a template placeholder. */
export const LEFTOVER = /\b[a-z][a-z0-9]*(?:_[a-z0-9]+)+\b|\b[a-z]+\.[a-z]+_[a-z_0-9]+\b|\bundefined\b|\bNaN\b|\[object Object\]|\{[a-z_]+\}/;

/** File names and manifest or protocol field names the page prints on purpose; they look like keys but are not. */
const ALLOWED_TOKENS = /depends_on|generate_dashboard|ecosystem_progress|ecosystem_status|deployment_target|authorizes_action/g;

export async function visibleText(page: Page): Promise<string> {
  return (await page.evaluate(() => document.body.innerText)).replace(ALLOWED_TOKENS, "");
}

/** Rows that are painted (the page of the list being looked at), as opposed to visibleRows, which counts every project that matches. */
export async function paintedRows(page: Page): Promise<number> {
  return page.locator("tr.project-row:not(.hidden)").count();
}
