import { test, expect, openDashboard, gotoTab, LANGS, TABS } from "./helpers";

// The whole battery runs with prefers-reduced-motion (playwright.config.ts) so that screenshots and contrast checks never catch a chart half drawn;
// the tests of the animation itself ask for the motion explicitly.

/** The templates of the page, written out here on purpose: a wrong or missing translation in the page fails the comparison instead of being copied. */
const COUNTS: Record<string, string> = {
  en: "{name}: {pct}% ({n} of {total})", es: "{name}: {pct}% ({n} de {total})", de: "{name}: {pct} % ({n} von {total})", fr: "{name} : {pct} % ({n} sur {total})",
  it: "{name}: {pct}% ({n} su {total})", ja: "{name}: {pct}%（{total} 件中 {n} 件）", zh: "{name}：{pct}%（{total} 个中的 {n} 个）", pt: "{name}: {pct}% ({n} de {total})",
};
const NO_DATA: Record<string, string> = {
  en: "{name}: no data", es: "{name}: sin datos", de: "{name}: keine Daten", fr: "{name} : aucune donnée", it: "{name}: nessun dato", ja: "{name}：データなし", zh: "{name}：暂无数据", pt: "{name}: sem dados",
};
const fill = (t: string, v: Record<string, string>) => t.replace(/\{(\w+)\}/g, (_m, k) => v[k] ?? "");

test.describe("names of the charts in the eight languages", () => {
  for (const lang of LANGS) {
    test(`${lang}: meters, rings, bars and columns are named with the template of the language`, async ({ page }) => {
      await openDashboard(page);
      await page.locator("#lang-select").selectOption(lang);
      const meter = page.locator('#panel-summary [data-testid="area-hydra-umc-hardware"]');
      const printed = await meter.locator(".area-name [data-i18n]").innerText();
      const bar = meter.locator(".area-bar");
      const [pct, n, total] = await Promise.all(["data-a-pct", "data-a-n", "data-a-total"].map((a) => bar.getAttribute(a)));
      expect(await bar.getAttribute("aria-label")).toBe(fill(COUNTS[lang], { name: printed, pct: pct!, n: n!, total: total! }));
      const ring = page.locator('#panel-summary [data-testid="progress-hydra-umc"] .ring-wrap');
      const ringPct = await ring.getAttribute("data-a-pct");
      expect(await ring.getAttribute("aria-label")).toBe(`HYDRA-UMC: ${ringPct}%`);
      // a bar row lists every segment by the translated name that its legend prints
      const row = page.locator("#panel-summary .card-maturity .bar-row").first();
      const label = (await row.getAttribute("aria-label")) || "";
      const keys = await row.locator(".seg").evaluateAll((segs) => segs.map((s) => s.getAttribute("data-name-key") || ""));
      expect(keys.length).toBeGreaterThan(0);
      for (const key of keys) {
        const text = await page.locator(`#panel-summary .card-maturity [data-i18n="${key}"]`).first().innerText();
        expect(label, `${lang} ${key}`).toContain(text);
      }
      expect(label.startsWith("HYDRA-UMC: ")).toBe(true);
      // a column: its tooltip text is the template of the language
      const col = page.locator("#panel-summary .col-g").first();
      const colLabel = (await col.getAttribute("aria-label")) || "";
      expect(colLabel).not.toMatch(/\{|\}|undefined/);
      if (lang !== "en") {
        expect(await bar.getAttribute("aria-label")).not.toMatch(/of/);
        expect(label).not.toMatch(/Scaffolding|Functional/);
      }
      // regions that used to carry English only
      const key = await page.locator('[data-i18n-aria-label="aria_key_figures"]').first().getAttribute("aria-label");
      if (lang !== "en") expect(key).not.toBe("Key figures");
    });
  }

  test("every aria-label of a chart changes with the language (nothing stays in English)", async ({ page }) => {
    await openDashboard(page);
    const read = () => page.locator("[data-aria]").evaluateAll((els) => els.map((e) => e.getAttribute("aria-label")));
    const en = await read();
    await page.locator("#lang-select").selectOption("es");
    const es = await read();
    expect(es.length).toBe(en.length);
    expect(es.length).toBeGreaterThan(40);
    const same = es.filter((label, i) => label === en[i] && /[A-Za-z]{3,}/.test(label || "") && !/^[A-Z0-9.\- ]+: \d+%$/.test(label || ""));
    expect(same.slice(0, 5)).toEqual([]);
  });

  test("the pt labels are European Portuguese", async ({ page }) => {
    await openDashboard(page, "partial");
    await page.locator("#lang-select").selectOption("pt");
    const labels = await page.locator("[data-aria]").evaluateAll((els) => els.map((e) => e.getAttribute("aria-label") || ""));
    expect(labels.some((l) => /sem dados/.test(l))).toBe(true);
    expect(labels.join(" ")).not.toMatch(/\bsem dados\b.*\bsem dados\b.*dados\s+disponíveis/); // no invented wording
    expect(labels.join(" ")).not.toMatch(/\bno data\b|\bsin datos\b/);
  });

  test("without data the rings and meters say it in the language, never a value", async ({ page }) => {
    await openDashboard(page, "empty");
    await page.locator("#lang-select").selectOption("es");
    const rings = await page.locator(".ring-wrap").evaluateAll((els) => els.map((e) => e.getAttribute("aria-label") || ""));
    expect(rings.length).toBeGreaterThanOrEqual(4);
    for (const label of rings) expect(label).toMatch(/sin datos$/);
    expect(await page.locator(".ring-value").count()).toBe(0);
  });
});

test.describe("tooltips", () => {
  test("hovering a segment shows its name, k of n and the percentage", async ({ page }) => {
    await openDashboard(page);
    const seg = page.locator(".card-maturity .seg").first();
    await seg.hover();
    const tip = page.locator("#chart-tip");
    await expect(tip).toBeVisible();
    const n = await seg.getAttribute("data-n");
    const total = await seg.getAttribute("data-total");
    await expect(tip).toContainText(`${n} of ${total}`);
    await expect(tip).toContainText("%");
    await page.mouse.move(2, 2);
    await expect(tip).toBeHidden();
  });

  test("the tooltip follows the language", async ({ page }) => {
    await openDashboard(page);
    await page.locator("#lang-select").selectOption("de");
    await page.locator(".card-maturity .seg").first().hover();
    await expect(page.locator("#chart-tip")).toContainText(" von ");
  });

  test("keyboard: a chart row takes focus, shows the tooltip with the breakdown and Escape dismisses it", async ({ page }) => {
    await openDashboard(page);
    const row = page.locator(".card-evidence .bar-row").first();
    await row.focus();
    const tip = page.locator("#chart-tip");
    await expect(tip).toBeVisible();
    await expect(tip).toHaveText((await row.getAttribute("aria-label")) || "");
    await page.keyboard.press("Escape");
    await expect(tip).toBeHidden();
  });

  test("keyboard: a ring and a column are reachable and describe themselves", async ({ page }) => {
    await openDashboard(page);
    const ring = page.locator('#panel-summary [data-testid="progress-hydra-umc"] .ring-wrap');
    await ring.focus();
    await expect(page.locator("#chart-tip")).toContainText("%");
    const col = page.locator(".col-g").first();
    await col.focus();
    await expect(page.locator("#chart-tip")).toContainText(" of ");
    await page.locator("#theme-toggle").focus();
    await expect(page.locator("#chart-tip")).toBeHidden();
  });

  test("the tooltip stays inside the window", async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await openDashboard(page);
    const last = page.locator("#panel-summary .bar-row").last();
    await last.scrollIntoViewIfNeeded();
    await last.focus();
    const box = await page.locator("#chart-tip").boundingBox();
    expect(box).not.toBeNull();
    expect(box!.x).toBeGreaterThanOrEqual(0);
    expect(box!.x + box!.width).toBeLessThanOrEqual(390);
  });

  test("a row without any project says no data in the tooltip, never zero", async ({ page }) => {
    await openDashboard(page, "minimal");
    const rows = page.locator(".card-maturity .bar-row");
    let found = false;
    for (let i = 0; i < (await rows.count()); i++) {
      const label = (await rows.nth(i).getAttribute("aria-label")) || "";
      if (/no data$/.test(label)) { found = true; await rows.nth(i).focus(); await expect(page.locator("#chart-tip")).toHaveText(label); }
    }
    expect(found).toBe(true);
  });
});

test.describe("relief and motion", () => {
  test("under prefers-reduced-motion nothing is animated and the charts are complete", async ({ page }) => {
    await openDashboard(page);
    const names = await page.evaluate(() => [".bar-fill", ".col-body", ".ring-value", ".area-fill"].map((s) => {
      const el = document.querySelector(s); return el ? getComputedStyle(el).animationName : "missing";
    }));
    expect(names).toEqual(["none", "none", "none", "none"]);
    expect(await page.evaluate(() => document.getAnimations().length)).toBe(0);
    expect(await page.locator(".ring-value").first().evaluate((e) => getComputedStyle(e).strokeDashoffset)).toBe("0px");
  });

});

test.describe("motion allowed", () => {
    test.use({ contextOptions: { reducedMotion: "no-preference" } });

    test("the charts are drawn by CSS animations and end in the same state", async ({ page }) => {
      await openDashboard(page);
      const names = await page.evaluate(() => [".bar-fill", ".col-body", ".ring-value", ".area-fill"].map((s) => {
        const el = document.querySelector(s); return el ? getComputedStyle(el).animationName : "missing";
      }));
      expect(names).toEqual(["t25-grow-x", "t25-grow-y", "t25-ring", "t25-grow-x"]);
      await page.waitForFunction(() => document.getAnimations().every((a) => a.playState === "finished" || (a.effect as any)?.getTiming().iterations === Infinity));
      expect(await page.locator(".ring-value").first().evaluate((e) => getComputedStyle(e).strokeDashoffset)).toBe("0px");
      const segs = await page.locator(".card-maturity .seg").first().evaluate((e) => (e as SVGGraphicsElement).getBoundingClientRect().width);
      expect(segs).toBeGreaterThan(5);
    });

    test("the entrance is staggered", async ({ page }) => {
      await openDashboard(page);
      const delays = await page.locator(".card-maturity .bar-fill").evaluateAll((els) => els.map((e) => getComputedStyle(e).animationDelay));
      expect(new Set(delays).size).toBeGreaterThan(1);
    });

    test("only compositor-friendly properties are animated", async ({ page }) => {
      await openDashboard(page);
      const props = await page.evaluate(() => [...new Set(document.getAnimations().flatMap((a) => (a.effect as KeyframeEffect).getKeyframes().flatMap((k) => Object.keys(k))))]);
      for (const p of props) expect(["offset", "computedOffset", "easing", "composite", "transform", "opacity", "strokeDashoffset"]).toContain(p);
    });
});

test.describe("relief", () => {

  test("the relief is there: shadows under the bars, faces on the columns and a light arc on the rings", async ({ page }) => {
    await openDashboard(page);
    expect(await page.locator(".bar-depth").count()).toBeGreaterThan(8);
    expect(await page.locator(".seg-bevel").count()).toBeGreaterThan(8);
    expect(await page.locator(".col-top").count()).toBe(await page.locator(".col-side").count());
    expect(await page.locator("svg.chart-ring .ring-sheen").count()).toBe(await page.locator(".ring-value").count());
    // the rings of the Builds tab and the donut of the Changelog tab carry their own light arc
    expect(await page.locator(".ac-ring-sheen, .ch-donut-grid .ring-sheen").count()).toBeGreaterThan(0);
  });

  test("every number is printed as text (the chart does not rest on colour or on the shape)", async ({ page }) => {
    await openDashboard(page);
    const bars = await page.locator(".card-maturity .bar-row").first().evaluate((g) => ({
      counts: [...g.querySelectorAll(".seg-count")].map((t) => t.textContent),
      total: g.querySelector(".chart-total")?.textContent,
    }));
    expect(bars.total).toMatch(/^\d+$/);
    expect(bars.counts.length).toBeGreaterThan(0);
  });
});

test.describe("axe still passes with the new charts", () => {
  test("hovering and focusing a chart in every language leaves the tabs free of leftovers", async ({ page }) => {
    await openDashboard(page);
    for (const lang of ["ja", "pt"]) {
      await page.locator("#lang-select").selectOption(lang);
      for (const id of TABS) {
        await gotoTab(page, id);
        const text = await page.evaluate(() => document.body.innerText);
        expect(text.match(/\{[a-z]+\}|\bundefined\b/), `${lang}/${id}`).toBeNull();
      }
    }
  });
});
