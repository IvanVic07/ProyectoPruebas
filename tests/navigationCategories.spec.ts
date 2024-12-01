import { test, expect } from '@playwright/test';

test('navigate to the "Bafles" subcategory on Steren', async ({ page }) => {

  // Navigate to the Steren homepage
  await page.goto('https://www.steren.com.mx/');

  // Select the Audio category from the menu
  const audioCategory = page.locator('a#ui-id-3'); 
  await expect(audioCategory).toBeVisible(); 
  await audioCategory.click(); 

  // Select the "Bafles" subcategory
  const speakersCategory = page.locator('a.grid-cat-name[href="audio/bafles"]'); 
  await expect(speakersCategory).toBeVisible(); 
  await speakersCategory.click();

  // Verify that the Speakers subcategory page has loaded using the breadcrumb
  const subcategoryBreadcrumb = page.locator('li.item.category11 strong'); 
  await expect(subcategoryBreadcrumb).toBeVisible(); 
  await expect(subcategoryBreadcrumb).toContainText('Bafles'); 

  // Verify that products in the subcategory are visible
  const products = page.locator('.product-item-info'); 
  await expect(products.first()).toBeVisible(); 

  // Pause to observe the results
  await page.pause();
});