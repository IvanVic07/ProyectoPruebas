import { test, expect } from '@playwright/test';

test('buscar y agregar producto al carrito en Steren', async ({ page }) => {
    
    // Navigate to the Steren homepage
    await page.goto('https://www.steren.com.mx/');
  
    // Verificar que el título de la página sea el esperado.
    await expect(page).toHaveTitle(/Cyber Days 2024 en Steren/);
  
    // Encontrar el campo de búsqueda y escribir el término deseado.
    const searchInput = page.locator('input[placeholder="Buscar en toda la tienda..."]');
    await expect(searchInput).toBeVisible();
    await searchInput.fill('audífonos ultraconfort');
  
    // Clic en el botón de búsqueda.
    await page.keyboard.press('Enter');
  
    // Verificar que los resultados de la búsqueda sean visibles.
    const searchResultsTitle = page.locator("li.item.search strong");
    await expect(searchResultsTitle).toBeVisible();
    await expect(searchResultsTitle).toContainText("audífonos ultraconfort");
  
    // Seleccionar el tercer producto de los resultados.
  const thirdProduct = page.locator('ol.products.list.items.product-items > li.item.product.product-item').nth(2); // Índice 2 para el tercer elemento.
  await expect(thirdProduct).toBeVisible(); // Verificar que el tercer producto es visible.
  await thirdProduct.click(); // Hacer clic en el tercer producto.
  
    // Seleccionar el color azul.
    const colorBlueOption = page.locator('#option-label-color-93-item-783'); // Selector del color azul.
    await expect(colorBlueOption).toBeVisible();
    await colorBlueOption.click();
  
    // Esperar a que el botón "Añadir al carrito" sea visible y hacer clic.
    const addToCartButton = page.locator('button#product-addtocart-button');
    await expect(addToCartButton).toBeVisible();
    await addToCartButton.click();
  
    // Verificar que el producto haya sido agregado correctamente al carrito.
    const successMessage = page.locator('.message-success'); // Cambiar al selector que aparezca en la página.
    await expect(successMessage).toBeVisible();
  
    // Pausar para observar los resultados.
    await page.pause();
  });