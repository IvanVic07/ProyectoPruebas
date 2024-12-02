import { test, expect, chromium } from '@playwright/test';

test('click "Iniciar sesión" on Steren website', async () => {
  const browser = await chromium.launch({ headless: false });

  const context = await browser.newContext({
    userAgent:
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    viewport: { width: 1280, height: 720 },
    locale: 'en-US',
  });

  // Add headers to mimic a real browser
  await context.setExtraHTTPHeaders({
    'Accept-Language': 'en-US,en;q=0.9',
    'Upgrade-Insecure-Requests': '1',
  });

  // Disable WebDriver detection
  await context.addInitScript(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => false });
  });

  const page = await context.newPage();

  // Navigate to the website
  await page.goto('https://www.steren.com.mx/');

  // Wait for the verification to complete and for the "Iniciar sesión" button to appear
  await page.waitForSelector("a[href*='/customer/account/login']", { timeout: 30000 });

  // Click the "Iniciar sesión" button using refined selector
  const loginButton = page.getByRole('link', { name: 'Iniciar sesión' });
  await loginButton.click();

  // Wait for the login form to load
  await page.waitForSelector("input[name='sterencard']", { timeout: 30000 });

  // Pause to inspect the page
  await page.pause();
});