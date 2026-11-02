import { test, expect, openDashboard, gotoTab, TABS, LANGS, visibleText, LEFTOVER } from "./helpers";

test.describe("languages", () => {
  test("the selector offers the eight languages", async ({ page }) => {
    await openDashboard(page);
    const values = await page.locator("#lang-select option").evaluateAll((options) => options.map((o) => (o as HTMLOptionElement).value));
    expect(values.sort()).toEqual([...LANGS].sort());
  });

  for (const lang of LANGS) {
    test(`no key, undefined or placeholder is visible in ${lang} on any tab`, async ({ page }) => {
      await openDashboard(page);
      await page.locator("#lang-select").selectOption(lang);
      await expect(page.locator("html")).toHaveAttribute("lang", lang);
      for (const id of TABS) {
        await gotoTab(page, id);
        if (id === "architecture") {
          for (const view of ["hydra-umc", "urtc", "armor", "eh3d"]) {
            await page.locator(`[data-arch-view="${view}"]`).click();
            const text = await visibleText(page);
            expect(text.match(LEFTOVER), `${lang} ${id}/${view}`).toBeNull();
          }
        }
        const text = await visibleText(page);
        const found = text.match(LEFTOVER);
        expect(found, `${lang} / ${id}: "${found?.[0]}"`).toBeNull();
      }
    });

    test(`every i18n element has a translation in ${lang} and the translated attributes are filled`, async ({ page }) => {
      await openDashboard(page);
      await page.locator("#lang-select").selectOption(lang);
      const report = await page.evaluate(() => {
        const bad: string[] = [];
        document.querySelectorAll("[data-i18n]").forEach((el) => {
          const text = (el.textContent || "").trim();
          if (!text || text === el.getAttribute("data-i18n")) bad.push(`empty/key: ${el.getAttribute("data-i18n")}`);
        });
        document.querySelectorAll("[data-i18n-aria-label]").forEach((el) => {
          if (!(el.getAttribute("aria-label") || "").trim()) bad.push(`aria-label: ${el.getAttribute("data-i18n-aria-label")}`);
        });
        document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
          if (!(el.getAttribute("placeholder") || "").trim()) bad.push(`placeholder: ${el.getAttribute("data-i18n-placeholder")}`);
        });
        return bad;
      });
      expect(report).toEqual([]);
    });
  }

  test("a translated page really changes: the tab labels differ from English in every other language", async ({ page }) => {
    await openDashboard(page);
    const english = await page.getByTestId("tab-projects").innerText();
    for (const lang of LANGS.filter((l) => l !== "en")) {
      await page.locator("#lang-select").selectOption(lang);
      expect(await page.getByTestId("tab-projects").innerText(), lang).not.toBe(english);
    }
  });

  test("Portuguese is the one of Portugal", async ({ page }) => {
    await openDashboard(page);
    await page.locator("#lang-select").selectOption("pt");
    const all = (await page.evaluate(() => document.documentElement.textContent || "")).toLowerCase();
    for (const brazilian of ["arquivo ", "tela ", "celular", "usuário "]) {
      expect(all.includes(brazilian), brazilian).toBe(false);
    }
  });

  test("the language is remembered and restored", async ({ page }) => {
    await openDashboard(page);
    await page.locator("#lang-select").selectOption("fr");
    await page.reload();
    await expect(page.locator("html")).toHaveAttribute("lang", "fr");
    await expect(page.locator("#lang-select")).toHaveValue("fr");
  });

  test("the browser language picks the first language", async ({ browser }) => {
    const context = await browser.newContext({ locale: "ja-JP" });
    const page = await context.newPage();
    await page.goto("full/index.html");
    await expect(page.locator("html")).toHaveAttribute("lang", "ja");
    await context.close();
  });

  test("an unsupported browser language falls back to English", async ({ browser }) => {
    const context = await browser.newContext({ locale: "ko-KR" });
    const page = await context.newPage();
    await page.goto("full/index.html");
    await expect(page.locator("html")).toHaveAttribute("lang", "en");
    await context.close();
  });

  test("the filter counter is translated and keeps its numbers", async ({ page }) => {
    await openDashboard(page);
    for (const lang of LANGS) {
      await page.locator("#lang-select").selectOption(lang);
      const text = await page.locator("#filters-count").innerText();
      expect(text, lang).toMatch(/40/);
      expect(text, lang).not.toMatch(/\{/);
    }
  });
});

test.describe("theme", () => {
  test("dark is the default and the toggle switches to light and back", async ({ page }) => {
    await openDashboard(page);
    await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
    await page.locator("#theme-toggle").click();
    await expect(page.locator("html")).toHaveAttribute("data-theme", "light");
    const lightBg = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
    await page.locator("#theme-toggle").click();
    await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
    const darkBg = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
    expect(lightBg).not.toBe(darkBg);
  });

  test("the theme is remembered", async ({ page }) => {
    await openDashboard(page);
    await page.locator("#theme-toggle").click();
    await page.reload();
    await expect(page.locator("html")).toHaveAttribute("data-theme", "light");
  });

  test("text stays readable in light: dark text on a light background", async ({ page }) => {
    await openDashboard(page);
    await page.locator("#theme-toggle").click();
    const [bg, fg] = await page.evaluate(() => {
      const luminance = (c: string) => {
        const [r, g, b] = (c.match(/\d+(\.\d+)?/g) || [0, 0, 0]).slice(0, 3).map(Number);
        return 0.2126 * r + 0.7152 * g + 0.0722 * b;
      };
      return [luminance(getComputedStyle(document.body).backgroundColor), luminance(getComputedStyle(document.body).color)];
    });
    expect(bg).toBeGreaterThan(fg);
  });

  test("a light system preference does not override the dark default", async ({ browser }) => {
    const context = await browser.newContext({ colorScheme: "light", locale: "en-US" });
    const page = await context.newPage();
    await page.goto("full/index.html");
    await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
    await context.close();
  });
});
