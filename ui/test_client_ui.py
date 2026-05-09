from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.checkout_page import CheckoutPage
from utils.conftest import load_config, page, config


def test_login(page, config):
    login_page = LoginPage(page)

    login_page.goto()
    login_page.login(config["credentials"]["username"], config["credentials"]["password"])

    # Verify login success by checking URL
    page.wait_for_url("**/inventory.html", timeout=config["timeouts"]["page_load"])


def test_invalid_credentials_login(page, config):
    login_page = LoginPage(page)

    login_page.goto()
    login_page.login("invalid_user", "invalid_password")

    # Wait for error message to appear
    page.wait_for_selector(LoginPage.ERROR_MESSAGE, timeout=config["timeouts"]["action"])
    
    # Get error message and assert it contains expected text
    error_message = login_page.get_error_message()
    expected_error_text = "Epic sadface: Username and password do not match any user in this service"
    
    assert expected_error_text in error_message, f"Expected '{expected_error_text}' in error message, but got: '{error_message}'"

    # Keep browser open for 3 seconds to see the error
    page.wait_for_timeout(3000)


def test_add_item_to_cart(page, config):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    login_page.goto()
    login_page.login(config["credentials"]["username"], config["credentials"]["password"])

    inventory_page.wait_for_loaded(timeout=config["timeouts"]["page_load"])
    assert page.locator(InventoryPage.INVENTORY_ITEM).count() > 0

    # Add first item to cart
    inventory_page.add_item_by_index(0)
    assert inventory_page.cart_badge_count() == "1"

    # Add second item to cart
    inventory_page.add_item_by_index(1)
    assert inventory_page.cart_badge_count() == "2"

    # Open cart and verify both items
    inventory_page.open_cart()
    assert inventory_page.cart_item_count() == 2

    # Verify first item details
    first_item = inventory_page.get_cart_item_by_index(0)
    assert "Sauce Cabs" in first_item["name"]
    assert "$" in first_item["price"]
    assert float(first_item["price"].replace("$", "")) > 0

    # Verify second item details
    second_item = inventory_page.get_cart_item_by_index(1)
    assert "Sauce Labs" in second_item["name"]
    assert "$" in second_item["price"]
    assert float(second_item["price"].replace("$", "")) > 0

    # Ensure items are different
    assert first_item["name"] != second_item["name"], "Added items should be different products"

    # Keep browser open for 5 seconds to see the result
    page.wait_for_timeout(5000)


def test_add_random_item_and_complete_checkout(page, config):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    checkout_page = CheckoutPage(page)

    # Login
    login_page.goto()
    login_page.login(config["credentials"]["username"], config["credentials"]["password"])

    # Load inventory and add random item
    inventory_page.wait_for_loaded(timeout=config["timeouts"]["page_load"])
    assert page.locator(InventoryPage.INVENTORY_ITEM).count() > 0

    added_item = inventory_page.add_random_item_to_cart()
    assert inventory_page.cart_badge_count() == "1"

    # Open cart
    inventory_page.open_cart()
    assert inventory_page.cart_item_count() == 1

    # Verify added item is in cart
    cart_item = inventory_page.get_cart_item_by_index(0)
    assert cart_item["name"] == added_item["name"]
    assert cart_item["price"] == added_item["price"]

    # Proceed to checkout
    checkout_page.checkout()

    # Fill user information
    checkout_page.fill_user_info(
        first_name="John",
        last_name="Doe",
        postal_code="12345"
    )
    checkout_page.continue_to_overview()

    # Verify cart item on overview page
    assert inventory_page.cart_item_count() == 1
    assert added_item["name"] in inventory_page.get_cart_item_by_index(0)["name"]

    # Complete order
    checkout_page.finish_order()

    # Verify order completion
    assert checkout_page.is_order_complete()
    confirmation_message = checkout_page.get_order_confirmation_message()
    assert "Thank you for your order" in confirmation_message

    # Keep browser open for 3 seconds to see confirmation
    page.wait_for_timeout(3000)
