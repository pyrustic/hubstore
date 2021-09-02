from cyberpunk_theme import Cyberpunk
from cyberpunk_theme import constant
from cyberpunk_theme.widget import button, entry, listbox, label, frame
import tkstyle


def get_theme():
    theme = Cyberpunk()
    theme.add(get_button_style(), pattern="*Button")
    theme.add(get_entry_style(), pattern="*Entry")
    theme.add(get_listbox_style(), pattern="*Listbox")
    theme.add(get_frame_line_style(), pattern="*frame_line")
    theme.add(get_label_title_style(), pattern="*label_title")
    theme.add(get_label_notification_style(), pattern="*label_notification")
    theme.add(get_entry_owner_name_style(), pattern="*entry_owner_name")
    theme.add(get_entry_repo_name_style(), pattern="*entry_repo_name")
    theme.add(get_readonly_entry_style(), pattern="*info_toplevel*Entry")
    theme.add(get_readonly_entry_style(), pattern="*openlist_toplevel*Entry")
    theme.add(get_readonly_entry_style(), pattern="*error_toplevel*Entry")
    theme.add(get_readonly_entry_style(), pattern="*installer_toplevel*Entry")
    theme.add(get_readonly_entry_style(), pattern="*promoted_toplevel*Entry")
    return theme


def get_button_style():
    style = button.get_button_style_2()
    style.foreground = "gray"
    style.padX = 5
    style.padY = 0
    style.highlightThickness = 1
    style.highlightBackground = "#292D31"
    style.font = "Liberation Mono", 11, "normal"
    return style


def get_entry_style():
    style = entry.get_style()
    style.font = "Liberation Mono", 11, "normal"
    return style


def get_listbox_style():
    style = listbox.get_style()
    style.font = "Liberation Mono", 11, "normal"
    return style


def get_frame_line_style():
    style = frame.get_style()
    style.background = "#009191"
    style.background = "#4E7F7A"
    return style


def get_label_title_style():
    style = label.get_style()
    style.foreground = "#009191"
    style.foreground = "#4E7F7A"
    style.font = ("Liberation Mono", 12, "bold")
    return style


def get_label_notification_style():
    style = label.get_style()
    style.foreground = "#606060"
    style.font = ("Liberation Mono", 9, "italic")
    return style


def get_entry_owner_name_style():
    style = entry.get_style()
    style.font = "Liberation Mono", 9, "normal"
    style.readonlyBackground = "#121519"
    return style


def get_entry_repo_name_style():
    style = entry.get_style()
    style.readonlyBackground = "#00312C"
    style.readonlyBackground = "#0B0E12"
    style.foreground = "#3CA46F"
    style.foreground = "#ABAEB2"
    style.font = "Liberation Mono", 11, "bold"
    return style


def get_highlight_style():
    style = tkstyle.Frame()
    style.highlightBackground = "#101010"
    #style.highlightColor = "#384848"
    style.highlightColor = "#384848"
    style.highlightBackground = "#384848"
    return style


def get_unhighlight_style():
    style = tkstyle.Frame()
    style.highlightThickness = 2
    style.highlightColor = "#121519"
    style.highlightBackground = "#121519"
    return style


def get_readonly_entry_style():
    style = tkstyle.Entry()
    style.readonlyBackground = "#121519"
    return style


def get_entry_description_style():
    style = tkstyle.Entry()
    style.font = "Liberation Mono", 11, "normal"
    return style


def get_info_entry_owner_repo_style():
    style = tkstyle.Entry()
    style.font = "Liberation Mono", 12, "bold"
    return style


def get_package_size_style():
    style = tkstyle.Entry()
    style.foreground = "#26718A"
    return style


def get_text_search_style():
    style = tkstyle.Entry()
    style.highlightThickness = 0
    style.foreground = "#009191"
    style.foreground = "gray"
    style.padX = 1
    style.padY = 0
    return style
