from user_authentication.parent_login_window import ParentLoginWindow


def handle_login():
    parent_login_window = ParentLoginWindow()
    parent_login_window.mainloop()
    return parent_login_window.user_id
