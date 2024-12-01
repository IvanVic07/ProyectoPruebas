import { test, expect } from '@playwright/test';

test('Subscribe to newsletter on Steren website', async ({ page }) => {
  // Step 1: Go to the Steren website
  await page.goto('https://www.steren.com.mx');

  // Step 2: Scroll to the footer section
  await page.locator('footer.page-footer').scrollIntoViewIfNeeded();
  await expect(page.locator('footer.page-footer')).toBeVisible();

  // Step 3: Locate the email input field
  const emailInput = page.locator('input#newsletter');

  // Step 4: Fill in the email input field with the email
  await emailInput.fill('losjackys@hotmail.com');

  // Step 5: Locate the "Enviar" button
  const enviarButton = page.locator('button#newsletterbutton');

  // Step 6: Click on the "Enviar" button
  await enviarButton.click();

  // Step 7: Pause for manual inspection
  await page.pause(); // This will keep the browser open and allow you to inspect
});