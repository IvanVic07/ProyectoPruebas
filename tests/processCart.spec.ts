import { test, expect } from '@playwright/test';

test('search and add product to cart on Steren', async ({ page }) => {
    
    // Navigate to the Steren homepage
    await page.goto('https://www.steren.com.mx/');
  
    // Verify that the page title is as expected
    await expect(page).toHaveTitle(/Cyber Days 2024 en Steren/);
  
    // Find the search field and type the desired term
    const searchInput = page.locator('input[placeholder="Buscar en toda la tienda..."]');
    await expect(searchInput).toBeVisible();
    await searchInput.fill('audífonos ultraconfort');
  
    // Click on the search button
    await page.keyboard.press('Enter');
  
    // Verify that the search results are visible
    const searchResultsTitle = page.locator("li.item.search strong");
    await expect(searchResultsTitle).toBeVisible();
    await expect(searchResultsTitle).toContainText("audífonos ultraconfort");
  
    // Select the first product from the results
    const firstProduct = page.locator('ol.products.list.items.product-items > li.item.product.product-item').first();
    await expect(firstProduct).toBeVisible(); 
    await firstProduct.click(); 
  
    // Select the blue color
    const colorBlueOption = page.locator('#option-label-color-93-item-783'); 
    await expect(colorBlueOption).toBeVisible();
    await colorBlueOption.click();
  
    // Wait for the "Add to cart" button to be visible and click it
    const addToCartButton = page.locator('button#product-addtocart-button');
    await expect(addToCartButton).toBeVisible();
    await addToCartButton.click();
  
    // Verify that the product has been successfully added to the cart
    const successMessage = page.locator('.message-success'); 
    await expect(successMessage).toBeVisible();
  
    // Pause to observe the results
    await page.pause();
});