import { test, expect } from '@playwright/test';

test('Navigate to Smart Switches in the Smart Home category and apply filter', async ({ page }) => {

  // Navigate to the Steren homepage
  await page.goto('https://www.steren.com.mx/');

  // Click on the "Smart Home" category
  const smartHomeCategory = page.locator('a#ui-id-1');
  await expect(smartHomeCategory).toBeVisible();
  await smartHomeCategory.click(); 

  // Wait for the Smart Home page to load
  await page.waitForLoadState('networkidle');

  // Verify that we are on the "Smart Home" page
  const smartHomeTitle = page.locator('li.item.category214 strong'); 
  await expect(smartHomeTitle).toBeVisible(); 
  await expect(smartHomeTitle).toContainText('SMART HOME'); 

  // Select the "Smart Switches" subcategory
  const smartSwitchesCategory = page.locator('a.grid-cat-name[href="smart-home/apagadores-inteligentes"]'); 
  await expect(smartSwitchesCategory).toBeVisible();
  await smartSwitchesCategory.click(); 

  // Verify that the subcategory page loaded using the breadcrumb
  const switchesTitle = page.locator('li.item.category488 strong'); 
  await expect(switchesTitle).toBeVisible();
  await expect(switchesTitle).toContainText('Apagadores Inteligentes'); 

  // Apply the color filter (white)
  const colorFilter = page.locator('#layered-filter-block div[data-role="title"]:has-text("Color")'); 
  await expect(colorFilter).toBeVisible(); 

  // Check if the filter is already expanded
  const isExpanded = await colorFilter.getAttribute('aria-expanded');
  if (isExpanded !== 'true') {
    await colorFilter.click(); 
  }

  // Select the "White" color within the expanded color filter
  const whiteColorOption = page.locator(
    'div.filter-options-content[aria-hidden="false"] div[data-option-id="777"]'
  ); 
  await expect(whiteColorOption).toBeVisible(); 
  await whiteColorOption.click(); 

  // Pause to observe the result
  await page.pause();
});