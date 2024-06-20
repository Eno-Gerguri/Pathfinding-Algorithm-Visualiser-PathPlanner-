from screenshot_manager.tag_manager.parent_tag_window import ParentTagWindow


def handle_select_tag(tags):
    parent_tag_window = ParentTagWindow(tags)
    parent_tag_window.mainloop()
    return parent_tag_window.selected_tag
