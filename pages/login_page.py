class LoginPage:
    URL = "/"
    USERNAME_FIELD = "[data-test=username]"
    PASSWORD_FIELD = "[data-test=password]"
    LOGIN_BUTTON = "[data-test=login-button]"
    ERROR_MESSAGE = "[data-test=error]"

    def __init__(self, page):
        self.page = page

    def goto(self):
        self.page.goto(self.URL)

    def login(self, username: str, password: str):
        self.page.fill(self.USERNAME_FIELD, username)
        self.page.fill(self.PASSWORD_FIELD, password)
        self.page.click(self.LOGIN_BUTTON)

    def get_error_message(self) -> str:
        error_element = self.page.locator(self.ERROR_MESSAGE)
        if error_element.count() > 0:
            return error_element.inner_text()
        return ""
