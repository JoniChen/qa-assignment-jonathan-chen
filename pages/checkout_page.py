class CheckoutPage:
    CHECKOUT_BUTTON = "[data-test=checkout]"
    FIRST_NAME_FIELD = "[data-test=firstName]"
    LAST_NAME_FIELD = "[data-test=lastName]"
    POSTAL_CODE_FIELD = "[data-test=postalCode]"
    CONTINUE_BUTTON = "[data-test=continue]"
    FINISH_BUTTON = "[data-test=finish]"
    ORDER_CONFIRMATION = "[data-test=complete-header]"
    ORDER_CONFIRMATION_TEXT = ".complete-header"

    def __init__(self, page):
        self.page = page

    def checkout(self):
        self.page.click(self.CHECKOUT_BUTTON)

    def fill_user_info(self, first_name: str, last_name: str, postal_code: str):
        self.page.fill(self.FIRST_NAME_FIELD, first_name)
        self.page.fill(self.LAST_NAME_FIELD, last_name)
        self.page.fill(self.POSTAL_CODE_FIELD, postal_code)

    def continue_to_overview(self):
        self.page.click(self.CONTINUE_BUTTON)

    def finish_order(self):
        self.page.click(self.FINISH_BUTTON)

    def get_order_confirmation_message(self) -> str:
        return self.page.locator(self.ORDER_CONFIRMATION_TEXT).inner_text()

    def is_order_complete(self) -> bool:
        return self.page.locator(self.ORDER_CONFIRMATION).count() > 0
