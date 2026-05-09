import random


class InventoryPage:
    INVENTORY_ITEM = "[data-test='inventory-item']"
    ADD_TO_CART_BUTTON = "button[id^='add-to-cart']"
    CART_BADGE = "[data-test=shopping-cart-badge]"
    CART_LINK = "[data-test=shopping-cart-link]"
    CART_ITEM = ".cart_item"
    CART_ITEM_NAME = ".cart_item_label .inventory_item_name"
    CART_ITEM_PRICE = ".inventory_item_price"

    def __init__(self, page):
        self.page = page

    def wait_for_loaded(self, timeout: int):
        self.page.wait_for_url("**/inventory.html", timeout=timeout)

    def add_first_item_to_cart(self):
        self.page.click(self.ADD_TO_CART_BUTTON)

    def add_item_by_index(self, index: int):
        buttons = self.page.locator(self.ADD_TO_CART_BUTTON)
        buttons.nth(index).click()

    def add_random_item_to_cart(self) -> dict:
        buttons = self.page.locator(self.ADD_TO_CART_BUTTON)
        item_count = buttons.count()
        
        if item_count == 0:
            raise RuntimeError("No items available to add to cart")
        
        random_index = random.randint(0, item_count - 1)
        
        # Get item details before clicking
        inventory_items = self.page.locator(self.INVENTORY_ITEM)
        item = inventory_items.nth(random_index)
        name = item.locator(".inventory_item_name").inner_text()
        price = item.locator(".inventory_item_price").inner_text()
        
        # Add item to cart
        buttons.nth(random_index).click()
        
        return {"name": name, "price": price, "index": random_index}

    def cart_badge_count(self) -> str:
        return self.page.locator(self.CART_BADGE).inner_text()

    def open_cart(self):
        self.page.click(self.CART_LINK)

    def cart_item_count(self) -> int:
        return self.page.locator(self.CART_ITEM).count()

    def first_cart_item_name(self) -> str:
        return self.page.locator(self.CART_ITEM_NAME).inner_text()

    def get_cart_item_by_index(self, index: int) -> dict:
        cart_items = self.page.locator(self.CART_ITEM)
        if index >= cart_items.count():
            raise IndexError(f"Cart item index {index} out of range")
        
        item = cart_items.nth(index)
        name = item.locator(self.CART_ITEM_NAME).inner_text()
        price = item.locator(self.CART_ITEM_PRICE).inner_text()
        
        return {"name": name, "price": price}
