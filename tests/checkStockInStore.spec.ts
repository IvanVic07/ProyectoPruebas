import { test, expect } from '@playwright/test';

test('Navigate to CABLES, CABLES PARA CELULAR Y TABLET, specific product, and check availability', async ({ page }) => {
  // Step 1: Go to the main page
  await page.goto('https://www.steren.com.mx');

  // Step 2: Locate the "CABLES" link
  const cablesLink = page.locator('a.ms-label.anchor_text', { hasText: 'CABLES' });
  await expect(cablesLink).toBeVisible();
  await cablesLink.click();

  // Step 3: Wait for the CABLES section to load
  await page.waitForSelector('body.category-cables');

  // Step 4: Click on "CABLES PARA CELULAR Y TABLET"
  const cablesParaCelularLink = page.locator('a.grid-cat-name[href="cables/cables-para-celular-y-tablet"]');
  await cablesParaCelularLink.scrollIntoViewIfNeeded();
  await expect(cablesParaCelularLink).toBeVisible();
  await cablesParaCelularLink.click();

  // Step 5: Wait for the "CABLES PARA CELULAR Y TABLET" page to load
  await page.waitForSelector('body.category-cables-para-celular-y-tablet');

  // Step 6: Click on a specific product
  const productLink = page.locator('a.product-item-link[href*="cable-usb-c-a-jack-usb-3-0-de-20-cm.html"]');
  await productLink.scrollIntoViewIfNeeded();
  await expect(productLink).toBeVisible();
  await productLink.click();

  // Step 7: Wait for the product page to load
  await page.waitForSelector('body.catalog-product-view');

  // Step 8: Click the "Consulta existencia en tiendas" button
  const checkAvailabilityButton = page.locator('a#disponibilidad-tienda');
  await checkAvailabilityButton.scrollIntoViewIfNeeded();
  await expect(checkAvailabilityButton).toBeVisible();
  await checkAvailabilityButton.click();

  // Step 9: Wait for the modal to appear
  const modalContent = page.locator('div.modal-content:has-text("DISPONIBILIDAD EN TIENDA")');
  await expect(modalContent).toBeVisible({ timeout: 10000 });

  // Step 10: Fill in "Código postal" and "Cantidad" fields
  const postalCodeInput = modalContent.locator('input#buscar_codigo_postal_value');
  const quantityInput = modalContent.locator('input#cantidad_producto_existencia');
  await postalCodeInput.fill('20000');
  await quantityInput.fill('2');

  // Step 11: Click the "Consultar" button
  const consultButton = modalContent.locator('button', { hasText: 'CONSULTAR' });
  await expect(consultButton).toBeVisible();
  await consultButton.click();

  // Pause for inspection
  await page.pause();
});