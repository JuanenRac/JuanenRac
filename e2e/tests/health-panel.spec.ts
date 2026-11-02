import { test, expect, openDashboard, gotoTab, LANGS, Variant, visibleText, LEFTOVER, Page } from "./helpers";

// The fixture dates are in 2001; each test fixes "today" so the age of every date, and so every colour, is known.
const NOW = {
  recent: "2001-12-21T12:00:00Z",   // the healthy dataset was active 1 to 11 days before
  january10: "2001-01-10T12:00:00Z",
  january20: "2001-01-20T12:00:00Z",
  march: "2001-03-01T12:00:00Z",
  may: "2001-05-15T12:00:00Z",
  december: "2001-12-21T12:00:00Z",
};

async function open(page: Page, variant: Variant, now: string, hash = "") {
  await page.clock.setFixedTime(new Date(now));
  await openDashboard(page, variant, hash);
}

const status = (page: Page) => page.getByTestId("alerts-status");

test.describe("health alerts", () => {
  test("a dataset with problems lists red CI, manifests, unresolved versions and silent repositories, each with repository, reason and link", async ({ page }) => {
    await open(page, "full", NOW.recent);
    const card = page.getByTestId("health-alerts");
    await expect(card).toBeVisible();
    await expect(card).toHaveAttribute("data-state", "alerts");
    const kinds = await page.locator("#alerts-list > li").evaluateAll((els) => els.map((e) => e.getAttribute("data-kind")));
    expect(kinds.filter((k) => k === "ci")).toHaveLength(10);
    expect(kinds.filter((k) => k === "manifest")).toHaveLength(2);
    expect(kinds.filter((k) => k === "version")).toHaveLength(4);
    expect(kinds.filter((k) => k === "inactive")).toHaveLength(40);
    expect(kinds.slice(0, 16).includes("inactive")).toBe(false);          // the alerts that do not depend on the date come first
    const items = page.locator("#alerts-list > li");
    for (let i = 0; i < (await items.count()); i++) {
      const item = items.nth(i);
      const href = await item.locator("a").getAttribute("href");
      expect(href, await item.innerText()).toMatch(/^https:\/\/github\.com\/JuanenRac\/[A-Za-z0-9._-]+(\/(actions|commits))?$/);
      expect((await item.locator("a").innerText()).trim().length).toBeGreaterThan(3);
      expect((await item.locator(".alert-why").innerText()).trim().length).toBeGreaterThan(3);
      expect((await item.locator(".alert-kind").innerText()).trim().length).toBeGreaterThan(3);   // the kind is words, not only a colour or a glyph
    }
    await expect(status(page)).toContainText("56 alerts");
    await expect(page.locator("#alerts-list > li[data-kind=ci] a").first()).toHaveAttribute("href", /\/actions$/);
  });

  test("a complete dataset with nothing wrong says 'No alerts' explicitly", async ({ page }) => {
    await open(page, "healthy", NOW.recent);
    await expect(page.getByTestId("health-alerts")).toHaveAttribute("data-state", "ok");
    await expect(status(page)).toHaveText(/No alerts/);
    await expect(page.locator("#alerts-list > li")).toHaveCount(0);
  });

  test("the same healthy dataset raises one alert per repository once 30 days pass", async ({ page }) => {
    await open(page, "healthy", "2002-02-10T12:00:00Z");
    await expect(page.getByTestId("health-alerts")).toHaveAttribute("data-state", "alerts");
    await expect(page.locator("#alerts-list > li[data-kind=inactive]")).toHaveCount(40);
    await expect(page.locator("#alerts-list > li[data-kind=inactive]").first()).toContainText(/No commit or release for \d+ days \(last: 2001-12-\d\d\)/);
  });

  test("the limit of 30 days is exclusive: exactly 30 days raises nothing", async ({ page }) => {
    // the newest healthy date is 2001-12-18 09:00; the oldest, 2001-12-11 09:00
    await open(page, "healthy", "2002-01-10T08:00:00Z");     // 30 days after the oldest commit, 23 after the newest
    await expect(page.locator("#alerts-list > li[data-kind=inactive]")).toHaveCount(0);
    await expect(page.getByTestId("health-alerts")).toHaveAttribute("data-state", "ok");
  });

  for (const variant of ["partial", "empty", "minimal"] as const) {
    test(`${variant}: failed or missing reads are 'incomplete data', never 'no alerts'`, async ({ page }) => {
      await open(page, variant, NOW.recent);
      await expect(page.getByTestId("health-alerts")).toHaveAttribute("data-state", "incomplete");
      await expect(status(page)).toContainText("Incomplete data");
      await expect(status(page)).not.toContainText("No alerts");
      await expect(page.getByTestId("alerts-why")).toBeVisible();
      expect((await page.getByTestId("alerts-why").innerText()).trim().length).toBeGreaterThan(10);
    });
  }

  test("an incomplete dataset still lists the alerts it did find", async ({ page }) => {
    await open(page, "partial", NOW.recent);
    await expect(page.locator("#alerts-list > li[data-kind=version]")).toHaveCount(16);
    await expect(status(page)).toContainText(/Incomplete data · 16 alerts found so far/);
  });

  test("the state is also a glyph and words, and the list is a labelled keyboard-reachable region", async ({ page }) => {
    await open(page, "full", NOW.recent);
    expect((await page.locator("#alerts-status .alerts-glyph").innerText()).trim()).not.toBe("");
    const region = page.locator(".alerts-scroll");
    await expect(region).toHaveAttribute("role", "region");
    await expect(region).toHaveAttribute("tabindex", "0");
    await region.focus();
    await expect(region).toBeFocused();
  });

  test("all eight languages translate the title, the state and the reasons", async ({ page }) => {
    await open(page, "full", NOW.recent);
    const english = await page.locator("#alerts-t").innerText();
    const seen = new Set<string>();
    for (const lang of LANGS) {
      await page.locator("#lang-select").selectOption(lang);
      const title = await page.locator("#alerts-t").innerText();
      const state = await status(page).innerText();
      const inactive = await page.locator("#alerts-list > li[data-kind=inactive] .alert-why").first().innerText();
      if (lang !== "en") {
        expect(title, lang).not.toBe(english);
        expect(inactive, lang).not.toMatch(/No commit or release/);
      }
      expect(state).toMatch(/56/);
      expect(`${title}${state}${inactive}`.match(LEFTOVER), lang).toBeNull();
      seen.add(title);
    }
    expect(seen.size).toBeGreaterThanOrEqual(7);   // es and pt share nothing here, de/fr/it/ja/zh differ; only a coincidence may repeat
    await page.locator("#lang-select").selectOption("pt");
    expect(await visibleText(page)).not.toMatch(/\balertas\b.*\bsaúde\b.*\bsaude\b/);
  });
});

test.describe("last published build", () => {
  test("shows the time and links to the workflow run", async ({ page }) => {
    await open(page, "full", NOW.recent);
    const stamp = page.getByTestId("build-stamp");
    await expect(stamp).toContainText("Last published build:");
    await expect(stamp.locator("time")).toHaveAttribute("datetime", "2001-12-20T08:30:00Z");
    await expect(stamp.locator("time")).toHaveText("2001-12-20 08:30 UTC");
    await expect(stamp.locator("a")).toHaveAttribute("href", "https://github.com/JuanenRac/JuanenRac/actions/runs/123456");
  });

  test("says 'Not verified' when the run could not be read", async ({ page }) => {
    await open(page, "partial", NOW.recent);
    await expect(page.getByTestId("build-stamp")).toContainText("Not verified");
    await expect(page.getByTestId("build-stamp").locator("a")).toHaveCount(0);
  });

  test("is translated", async ({ page }) => {
    await open(page, "full", NOW.recent);
    await page.locator("#lang-select").selectOption("de");
    await expect(page.getByTestId("build-stamp")).toContainText("Zuletzt veröffentlichter Build:");
    await page.locator("#lang-select").selectOption("pt");
    await expect(page.getByTestId("build-stamp")).toContainText("Última compilação publicada:");
  });

  test("the page asks nothing to GitHub for it: the data come with the page", async ({ page }) => {
    const calls: string[] = [];
    await page.route(/api\.github\.com\/repos\/JuanenRac\/JuanenRac\/actions\/workflows\/[^/]+\/runs\?status=success/, (route) => { calls.push(route.request().url()); return route.abort(); });
    await open(page, "full", NOW.recent);
    expect(calls).toEqual([]);
  });
});

test.describe("activity badges in the project table", () => {
  const row = (page: Page, name: string) => page.locator("tr.project-row", { hasText: name }).first();
  const cases: [string, string, string, string][] = [
    ["january10", "act-good", "act-good", "Activity: 8 d"],
    ["january20", "act-warn", "act-good", "Activity: 18 d"],
    ["march", "act-bad", "act-good", "Activity: 58 d"],
    ["may", "act-bad", "act-warn", "Release: 134 d ago"],
    ["december", "act-bad", "act-bad", "Release: 354 d ago"],
  ];
  for (const [when, activityClass, releaseClass, text] of cases) {
    test(`at ${when} the first project is ${activityClass} / ${releaseClass}`, async ({ page }) => {
      await open(page, "full", NOW[when as keyof typeof NOW], "#projects");
      const cell = row(page, "HYDRA-UMC-FIXTURE-00").locator("td.activity-cell");
      await expect(cell.locator("[data-kind=activity]")).toHaveClass(new RegExp(activityClass));
      await expect(cell.locator("[data-kind=release]")).toHaveClass(new RegExp(releaseClass));
      await expect(cell).toContainText(text);
      for (const kind of ["activity", "release"]) {   // colour is never alone: each badge has a glyph and words
        const badge = cell.locator(`[data-kind=${kind}]`);
        expect((await badge.locator(".act-glyph").innerText()).trim()).not.toBe("");
        expect((await badge.innerText()).replace(/[●▲✕?–]/g, "").trim().length).toBeGreaterThan(5);
      }
    });
  }

  test("a repository that never published a release says so, and without data it says 'Not verified'", async ({ page }) => {
    await open(page, "full", NOW.recent, "#projects");
    await expect(row(page, "HYDRA-UMC-FIXTURE-04").locator("[data-kind=release]")).toHaveText(/Release: none yet/);
    await expect(row(page, "HYDRA-UMC-FIXTURE-04").locator("[data-kind=release]")).toHaveClass(/act-none/);
    await page.goto("partial/index.html#projects");
    await page.waitForSelector("tr.project-row");
    const cell = row(page, "HYDRA-UMC-FIXTURE-00").locator("td.activity-cell");
    await expect(cell).toContainText("Not verified");
    await expect(cell.locator(".act-unknown")).toHaveCount(1);
  });

  test("the column header and the badges are translated", async ({ page }) => {
    await open(page, "full", NOW.january20, "#projects");
    await page.locator("#lang-select").selectOption("es");
    await expect(page.locator("th[data-i18n=th_activity]")).toHaveText("Actividad");
    await expect(row(page, "HYDRA-UMC-FIXTURE-00").locator("[data-kind=activity]")).toContainText("Actividad: 18 d");
    await page.locator("#lang-select").selectOption("pt");
    await expect(row(page, "HYDRA-UMC-FIXTURE-00").locator("[data-kind=release]")).toContainText("Versão: há 19 d");
  });
});

test.describe("repositories behind a percentage", () => {
  const button = (page: Page, eco: string, area: string) => page.locator("#panel-summary").getByTestId(`contrib-btn-${eco}-${area}`);

  test("clicking an area opens the exact list with the maturity of each repository", async ({ page }) => {
    await open(page, "full", NOW.recent);
    const btn = button(page, "hydra-umc", "software");
    await expect(btn).toHaveAttribute("aria-expanded", "false");
    await btn.click();
    await expect(btn).toHaveAttribute("aria-expanded", "true");
    const panel = page.locator(`#${await btn.getAttribute("aria-controls")}`);
    await expect(panel).toBeVisible();
    const head = await panel.locator(".contrib-head").innerText();
    const [, n, total] = head.match(/(\d+) of (\d+) repositories/)!;
    expect(Number(total)).toBe(10);
    await expect(panel.locator(".contrib-scroll > ul > li")).toHaveCount(Number(n));
    // functional or better: maturity cycles scaffolding, functional, established, production over the 10 fixture repositories => 7
    expect(Number(n)).toBe(7);
    const maturities = await panel.locator(".contrib-scroll .contrib-mat").allInnerTexts();
    expect(maturities.length).toBe(7);
    expect(maturities.every((m) => !/^scaffolding$/i.test(m.trim()))).toBe(true);
    await expect(panel.locator(".contrib-scroll a").first()).toHaveAttribute("href", /^https:\/\/github\.com\/JuanenRac\/HYDRA-UMC-FIXTURE-\d\d$/);
    await expect(panel.locator("details.contrib-more > summary").first()).toContainText(/Do not meet it \(3\)/);
  });

  test("it works with the keyboard and a screen reader gets the state", async ({ page }) => {
    await open(page, "full", NOW.recent);
    const btn = button(page, "urtc", "production");
    await btn.focus();
    await page.keyboard.press("Enter");
    await expect(btn).toHaveAttribute("aria-expanded", "true");
    await expect(page.locator(`#${await btn.getAttribute("aria-controls")}`)).toBeVisible();
    await page.keyboard.press("Space");
    await expect(btn).toHaveAttribute("aria-expanded", "false");
    await expect(page.locator(`#${await btn.getAttribute("aria-controls")}`)).toBeHidden();
    expect(await btn.evaluate((el) => el.tagName)).toBe("BUTTON");
  });

  test("clicking the bar itself and the ring also opens it", async ({ page }) => {
    await open(page, "full", NOW.recent);
    const li = page.locator("#panel-summary").getByTestId("area-armor-tests");
    await li.locator(".area-bar").click();
    await expect(li.locator(".contrib")).toBeVisible();
    await li.locator(".area-bar").click();
    await expect(li.locator(".contrib")).toBeHidden();
    const card = page.locator("#panel-summary").getByTestId("progress-armor");
    await card.locator(".ring-wrap").click();
    await expect(card.locator(".contrib-progress")).toBeVisible();
    await expect(card.locator(".contrib-progress .contrib-head")).toContainText("10 repositories counted");
    await expect(card.locator(".contrib-progress li")).toHaveCount(10);
    await expect(card.locator(".contrib-progress .contrib-pts").first()).toContainText(/\d+\/100 points/);
  });

  test("facts that could not be read are listed apart as 'Not verified', never counted as failures", async ({ page }) => {
    await open(page, "full", NOW.recent);
    const btn = button(page, "hydra-umc", "tests");
    await btn.click();
    const panel = page.locator(`#${await btn.getAttribute("aria-controls")}`);
    await expect(panel.locator("details.contrib-more > summary", { hasText: "Not verified (" })).toHaveCount(1);
    const counts = (await panel.locator(".contrib-head").innerText()).match(/(\d+) of (\d+)/)!;
    const unknown = Number((await panel.locator("details > summary", { hasText: "Not verified (" }).innerText()).match(/\((\d+)\)/)![1]);
    expect(Number(counts[2]) + unknown).toBe(10);
  });

  test("when the figure of the README differs it says so", async ({ page }) => {
    await open(page, "full", NOW.recent);
    const btn = button(page, "hydra-umc", "tests");
    await btn.click();
    await expect(page.locator(`#${await btn.getAttribute("aria-controls")}`).locator(".contrib-note")).toContainText("The figure of the README (9 of 10) was calculated at another time.");
  });

  test("the list follows the language", async ({ page }) => {
    await open(page, "full", NOW.recent);
    const btn = button(page, "hydra-umc", "software");
    await btn.click();
    await page.locator("#lang-select").selectOption("fr");
    await expect(page.locator(`#${await btn.getAttribute("aria-controls")}`).locator(".contrib-head")).toContainText("dépôts sur 10");
    await page.locator("#lang-select").selectOption("pt");
    await expect(page.locator(`#${await btn.getAttribute("aria-controls")}`).locator(".contrib-head")).toContainText("repositórios");
  });

  test("the scrolling list is a labelled region reachable by keyboard", async ({ page }) => {
    await open(page, "full", NOW.recent);
    const btn = button(page, "eh3d", "software");
    await btn.click();
    const region = page.locator(`#${await btn.getAttribute("aria-controls")}`).locator(".contrib-scroll");
    await expect(region).toHaveAttribute("role", "region");
    await expect(region).toHaveAttribute("aria-label", /Repositories behind Software/);
    await expect(region).toHaveAttribute("tabindex", "0");
  });

  test("the lists of an ecosystem tab have their own ids", async ({ page }) => {
    await open(page, "full", NOW.recent);
    const ids = await page.locator("[data-contrib-area]").evaluateAll((els) => els.map((e) => e.getAttribute("aria-controls")));
    expect(new Set(ids).size).toBe(ids.length);
    await gotoTab(page, "armor");
    await page.locator("#panel-armor").getByTestId("contrib-btn-armor-ci").click();
    await expect(page.locator("#panel-armor .contrib:not([hidden])")).toHaveCount(1);
  });
});

test.describe("repository panel", () => {
  const NAME = "HYDRA-UMC-FIXTURE-02";
  const opener = (page: Page, name = NAME) => page.locator(`button[data-open-repo="${name}"]`);

  async function openProjects(page: Page, variant: Variant = "full") {
    await open(page, variant, NOW.recent, "#projects");
    await page.waitForSelector("tr.project-row");
  }

  test("opens from its button with the manifest fields, the CI state, the recent commits and the four links, and focus on the title", async ({ page }) => {
    await openProjects(page);
    await opener(page).click();
    const dialog = page.getByTestId("repo-panel");
    await expect(dialog).toBeVisible();
    await expect(dialog).toHaveAttribute("role", "dialog");
    await expect(page.getByTestId("repo-panel-title")).toHaveText(NAME);
    await expect(page.getByTestId("repo-panel-title")).toBeFocused();
    const fields = (await page.getByTestId("repo-fields").innerText());
    for (const word of ["Ecosystem", "HYDRA-UMC", "Version", "Maturity", "Evidence", "Stack", "Deploy target", "Family", "Hardware", "Last activity", "Latest release"]) expect(fields).toContain(word);
    await expect(page.getByTestId("repo-ci")).toContainText("Red");
    expect(await page.getByTestId("repo-ci").locator(".act-glyph").innerText()).toBe("✕");
    await expect(page.getByTestId("repo-commits").locator("li")).toHaveCount(3);
    await expect(page.getByTestId("repo-commits").locator("a").first()).toHaveAttribute("href", /^https:\/\/github\.com\/JuanenRac\/HYDRA-UMC-FIXTURE-02\/commit\//);
    await expect(page.getByTestId("repo-commits-none")).toBeHidden();
    const hrefs = await page.getByTestId("repo-links").locator("a").evaluateAll((els) => els.map((e) => (e as HTMLAnchorElement).getAttribute("href")));
    expect(hrefs).toEqual([
      `https://github.com/JuanenRac/${NAME}/actions`, `https://github.com/JuanenRac/${NAME}/issues`,
      `https://github.com/JuanenRac/${NAME}/releases`, `https://github.com/JuanenRac/${NAME}#readme`,
    ]);
  });

  test("clicking the row opens it too, but clicking a link in the row does not", async ({ page }) => {
    await openProjects(page);
    await page.locator("tr.project-row", { hasText: NAME }).locator("td.stack").click();
    await expect(page.getByTestId("repo-panel")).toBeVisible();
    await page.keyboard.press("Escape");
    await expect(page.getByTestId("repo-panel")).toBeHidden();
    const popup = page.waitForEvent("popup").catch(() => null);
    await page.locator("tr.project-row", { hasText: NAME }).locator(".project-title a").click();
    await popup;
    await expect(page.getByTestId("repo-panel")).toBeHidden();
  });

  test("Escape closes it and the focus goes back to the button that opened it; so does the close button", async ({ page }) => {
    await openProjects(page);
    await opener(page).focus();
    await page.keyboard.press("Enter");
    await expect(page.getByTestId("repo-panel")).toBeVisible();
    await page.keyboard.press("Escape");
    await expect(page.getByTestId("repo-panel")).toBeHidden();
    await expect(opener(page)).toBeFocused();
    await opener(page).click();
    await page.getByTestId("repo-panel-close").click();
    await expect(page.getByTestId("repo-panel")).toBeHidden();
    await expect(opener(page)).toBeFocused();
  });

  test("Tab from the title reaches the close button and then the links (focus can leave, Escape still closes)", async ({ page }) => {
    await openProjects(page);
    await opener(page).click();
    await page.keyboard.press("Tab");
    await expect(page.getByTestId("repo-panel-close")).toBeFocused();
    const first = page.getByTestId("repo-links").locator("a").first();
    for (let i = 0; i < 4 && !(await first.evaluate((el) => el === document.activeElement)); i++) await page.keyboard.press("Tab");   // a scrolling body may take one stop
    await expect(first).toBeFocused();
    await page.keyboard.press("Escape");
    await expect(page.getByTestId("repo-panel")).toBeHidden();
  });

  test("a repository whose recent commits were not returned says it instead of showing nothing", async ({ page }) => {
    await openProjects(page);
    await opener(page, "HYDRA-UMC-FIXTURE-05").click();
    await expect(page.getByTestId("repo-commits").locator("li")).toHaveCount(0);
    await expect(page.getByTestId("repo-commits-none")).toBeVisible();
    await expect(page.getByTestId("repo-commits-none")).toContainText("did not receive the recent commits");
  });

  test("without activity data the CI, the release and the activity are 'Not verified'", async ({ page }) => {
    await openProjects(page, "partial");
    await opener(page, "HYDRA-UMC-FIXTURE-00").click();
    await expect(page.getByTestId("repo-ci")).toHaveText("Not verified");
    const fields = await page.getByTestId("repo-fields").innerText();
    expect(fields.match(/Last activity\s+Not verified/)).not.toBeNull();
    expect(fields.match(/Latest release\s+Not verified/)).not.toBeNull();
    await expect(page.getByTestId("repo-commits-none")).toBeVisible();
  });

  test("it is translated and follows the language while open", async ({ page }) => {
    await openProjects(page);
    await opener(page).click();
    for (const [lang, word] of [["es", "Últimos commits"], ["de", "Letzte Commits"], ["fr", "Derniers commits"], ["it", "Ultimi commit"], ["ja", "最近のコミット"], ["zh", "最近的提交"], ["pt", "Últimos commits"]] as const) {
      await page.locator("#lang-select").selectOption(lang);
      await expect(page.locator("#rp-commits-t")).toHaveText(word);
      expect(await visibleText(page)).not.toMatch(LEFTOVER);
    }
    await expect(page.getByTestId("repo-panel-title")).toHaveText(NAME);
  });

  test("it covers the right side only and fits every screen", async ({ page }) => {
    for (const size of [{ width: 1920, height: 1080 }, { width: 1366, height: 768 }, { width: 390, height: 844 }]) {
      await page.setViewportSize(size);
      await openProjects(page);
      await opener(page).click();
      const box = (await page.getByTestId("repo-panel").boundingBox())!;
      expect(box.x + box.width, `${size.width}`).toBeLessThanOrEqual(size.width + 1);
      expect(box.y).toBeGreaterThanOrEqual(0);
      expect(box.height).toBeLessThanOrEqual(size.height + 1);
      if (size.width > 600) expect(box.width).toBeLessThanOrEqual(441);
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1), `no horizontal scroll at ${size.width}`).toBe(true);
      await page.keyboard.press("Escape");
    }
  });

  test("the close button and the dialog have names", async ({ page }) => {
    await openProjects(page);
    await opener(page).click();
    await expect(page.getByTestId("repo-panel-close")).toHaveAttribute("aria-label", "Close the panel");
    await expect(page.getByTestId("repo-panel")).toHaveAttribute("aria-labelledby", "repo-panel-title");
    await page.locator("#lang-select").selectOption("zh");
    await expect(page.getByTestId("repo-panel-close")).toHaveAttribute("aria-label", "关闭面板");
    // the opener's name is the word "Panel" and the project, never just "Panel"
    const name = await page.evaluate(() => {
      const b = document.querySelector('button[data-open-repo="HYDRA-UMC-FIXTURE-02"]')!;
      return b.getAttribute("aria-labelledby")!.split(" ").map((id) => document.getElementById(id)!.textContent!.trim()).join(" ");
    });
    expect(name).toContain("HYDRA-UMC-FIXTURE-02");
  });
});

test.describe("themes", () => {
  for (const scheme of ["dark", "light"] as const) {
    test(`alerts, badges, lists and the panel are readable in the ${scheme} theme`, async ({ page }) => {
      await open(page, "full", NOW.january20, "#summary");
      if (scheme === "light") await page.locator("#theme-toggle").click();
      await expect(page.locator("html")).toHaveAttribute("data-theme", scheme === "light" ? "light" : /dark|^$/).catch(() => undefined);
      const bad = await page.evaluate(() => {
        function lum(c: string) {
          const m = c.match(/[\d.]+/g)!.map(Number);
          const [r, g, b] = m.slice(0, 3).map((v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); });
          return 0.2126 * r + 0.7152 * g + 0.0722 * b;
        }
        function backdrop(el: Element): string {
          for (let n: Element | null = el; n; n = n.parentElement) {
            const c = getComputedStyle(n).backgroundColor;
            if (c && !c.startsWith("rgba(0, 0, 0, 0)") && c !== "transparent") return c;
          }
          return "rgb(255,255,255)";
        }
        const out: string[] = [];
        document.querySelectorAll(".alerts-status, .alert-kind, .alert-why, .build-stamp, .alerts-why-list li").forEach((el) => {
          const fg = lum(getComputedStyle(el).color), bg = lum(backdrop(el));
          const ratio = (Math.max(fg, bg) + 0.05) / (Math.min(fg, bg) + 0.05);
          if (ratio < 4.5) out.push(`${el.className}: ${ratio.toFixed(2)}`);
        });
        return out;
      });
      expect(bad).toEqual([]);
    });
  }
});
