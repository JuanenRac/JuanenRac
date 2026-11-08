import { defineConfig } from "@playwright/test";
import * as path from "path";
import { pathToFileURL } from "url";

// FIXTURE_DIR holds full/, minimal/, partial/ and empty/ (see fixture/build_fixture.py).
const fixtureDir = process.env.FIXTURE_DIR || path.join(__dirname, "fixture", "out");
const baseURL = pathToFileURL(fixtureDir).href.replace(/\/?$/, "/");

export default defineConfig({
  testDir: "./tests",
  timeout: 60_000,
  expect: { timeout: 7_000 },
  fullyParallel: true,
  workers: 2,
  // a runner that stalls for a minute (a page that does not finish loading) is not a defect of the page: one retry in CI, none on a developer machine
  retries: process.env.CI ? 1 : 0,
  reporter: process.env.CI ? [["list"], ["html", { open: "never" }]] : [["list"]],
  outputDir: "test-results",
  use: {
    baseURL,
    screenshot: "only-on-failure",
    trace: "off",
    contextOptions: { reducedMotion: "reduce" },
    actionTimeout: 15_000,
  },
  projects: [{ name: "chromium", use: { browserName: "chromium" } }],
});
