import { test, expect } from '@playwright/test';

test('search store with city and keyword filters', async ({ page }) => {

    // Navigate to Steren's homepage
    await page.goto('https://www.steren.com.mx/');
  
    // Click on the "Tiendas" link in the main menu
    const storesLink = page.locator('a#ui-id-8');
    await expect(storesLink).toBeVisible(); 
    await storesLink.click(); 
  
    // Wait for the store locator page to load
    await page.waitForLoadState('networkidle');
  
    // Verify that location permission was blocked
    const locationPrompt = page.locator('text=Block'); 
    if (await locationPrompt.isVisible()) {
      await locationPrompt.click(); 
    }
  
    // Select the city "Aguascalientes"
    const cityDropdown = page.locator('select.select-steren'); 
    await expect(cityDropdown).toBeVisible(); 
    await cityDropdown.selectOption({ label: 'Aguascalientes' }); 
  
    // Perform the search with the keyword "Espacio"
    const searchInput = page.locator('input#searchteam'); 
    await expect(searchInput).toBeVisible(); 
    await searchInput.fill('Espacio');
  
    const searchButton = page.locator('button:has-text("Buscar tienda")');
    await expect(searchButton).toBeVisible();
    await searchButton.click();
  
    // Verify the search results are updated
    const resultsForKeyword = page.locator('ul#listStores h3'); 
    await expect(resultsForKeyword).toContainText('Espacio'); 
  
    // Pause to observe the results
    await page.pause();
  });