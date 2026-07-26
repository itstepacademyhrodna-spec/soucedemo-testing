from playwright.sync_api import sync_playwright
import time
import pytest

@pytest.fixture()
def page():
   with sync_playwright() as driver:
        browser = driver.chromium.launch(headless=False)
        page = browser.new_page()

        yield page  
        browser.close()
        

        
def test_login_success(page):

    page.goto("https://saucedemo.com")

    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    assert "inventory.html" in page.url

    time.sleep(1)
    product_items = page.locator(".inventory_item")
    assert product_items.count() > 0

def test_login_invalid_password(page):

    page.goto("https://saucedemo.com")

    page.fill("#user-name", "standard_user")
    page.fill("#password", "12345678")
    page.click("#login-button")
    
    time.sleep(1)

    url = page.url
    assert "inventory.html" not in url
    error_box = page.locator("[data-test='error']")
    assert error_box.is_visible() == True
    assert "Username and password do not match" in error_box.inner_text()

def test_login_by_enter(page):

    page.goto ("https://saucedemo.com")

    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.locator("#password").press("Enter")

    time.sleep(1)
    assert "inventory.html" in page.url
    product_items = page.locator(".inventory_item")
    assert product_items.count() > 0

def test_add_all_products_to_cart(page):

    page.goto("https://www.saucedemo.com")

    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")

    buttons = page.locator("button.btn_inventory")
    total_products = buttons.count()

    for i in range(total_products):
        buttons.nth(i).click()
        time.sleep(1)

    cart_badge = page.locator(".shopping_cart_badge")

    assert cart_badge.inner_text() == str(total_products)


def test_open_all_products(page):

    page.goto("https://saucedemo.com")
    
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    time.sleep(1)

    for i in range(6):
        catalog_item = page.locator(".inventory_item").nth(i)

        catalog_name = catalog_item.locator(".inventory_item_name").inner_text()
        catalog_price = catalog_item.locator(".inventory_item_price").inner_text()

        catalog_item.locator(".inventory_item_name").click()
        time.sleep(1)

        page_name = page.locator(".inventory_details_name").inner_text()
        page_price = page.locator(".inventory_details_price").inner_text()

        assert catalog_name == page_name
        assert catalog_price == page_price
        assert "inventory-item.html" in page.url

        page.click("#back-to-products")
        time.sleep(1)

