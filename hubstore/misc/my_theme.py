import tkstyle
from cyberpunk_theme import Cyberpunk
from cyberpunk_theme.widget import button
from cyberpunk_theme.widget import entry
from cyberpunk_theme.widget import label
from cyberpunk_theme.widget import text
from cyberpunk_theme.widget import radiobutton
from cyberpunk_theme import constant


# ========================================
# HUBSTORE THEME BASED ON CYBERPUNK THEME
# ========================================
def get_theme():
    theme = Cyberpunk()
    theme.add(get_button_style(), pattern="*Button")
    theme.add(_get_header_buttons_style(), pattern="*button_go")
    theme.add(_get_header_buttons_style(), pattern="*menu_frame*Button")
    theme.add(_get_entry_owner_name_style(), pattern="*entry_owner_name")
    theme.add(get_entry_repo_name_default_style(), pattern="*entry_repo_name")
    theme.add(_get_entry_running_app_name_style(), pattern="*entry_running_app_name")
    theme.add(_get_button_close_style(), pattern="*button_close")
    theme.add(_get_label_path_app_info_style(),
                    pattern="*toplevel_app_info*label_path")
    theme.add(_get_entry_path_app_info_style(),
                    pattern="*toplevel_app_info*entry_path")
    theme.add(_get_entry_form_app_info_style(),
                    pattern="*toplevel_app_info*central_frame*Entry")
    theme.add(_get_text_description_app_info_style(),
                    pattern="*toplevel_app_info*central_frame*Text")
    theme.add(_get_text_description_app_info_style(),
                    pattern="*about_view*Text")
    theme.add(_get_radiobbuton_style(), pattern="*Radiobutton")
    theme.add(_get_entry_form_app_info_style(),
                    pattern="*downloader_information_frame*Entry")
    theme.add(_get_title_latest_release_style(),
                    pattern="*title_latest_release")
    theme.add(_get_title_latest_release_style(),
                    pattern="*init_geet_label")
    theme.add(_get_text_description_app_info_style(),
                    pattern="*init_geet_view*Text")
    theme.add(_get_text_description_app_info_style(),
                    pattern="*exception_view*Text")
    return theme

# ===================================
#              GENERAL
# ===================================


# button style
def get_button_style():
    style = button.get_style()
    style.cursor = "hand1"
    style.background = "#181818"
    style.foreground = "#A098A0"
    style.highlightBackground = "#484048"
    style.highlightColor = "white"
    style.highlightThickness = 1
    style.relief = "flat"
    style.padY = 0
    style.activeBackground = "#202020"
    style.activeForeground = "#D0C8D0"
    return style

# button go (search)
def _get_button_go_style():
    style = button.get_style()
    style.highlightBackground = "#000000"
    style.highlightColor = "#000000"
    style.background = "#005954"
    style.foreground = "#ffffff"
    style.activeBackground = "#408984"
    style.activeForeground = "#ECFFFF"
    style.highlightThickness = 0
    style.relief = "flat"
    style.padY = 0
    return style

# header button style
def _get_header_buttons_style():
    style = button.get_style()
    style.cursor = "hand1"
    style.highlightBackground = "#204343"
    style.highlightColor = "white"
    style.highlightThickness = 1
    style.padY = 0
    style.background = "#002323"
    style.foreground = "#C0DBDB"
    style.activeBackground = "#003333"
    style.activeForeground = "#C8FBFB"
    style.borderWidth = 0
    style.activeBorderWidth = 0
    style.relief = "flat"
    style.font = constant.FONT_FAV_NORMAL
    return style


# entry owner name
def _get_entry_owner_name_style():
    style = entry.get_style()
    style.readonlyBackground = constant.COLOR_BLACK
    style.foreground = "#989098"
    style.font = constant.FONT_DEFAULT_FAMILY, 11, "bold"
    return style

# entry repo name
def get_entry_repo_name_default_style():
    style = entry.get_style()
    style.readonlyBackground = "#00312C"
    style.foreground = constant.COLOR_ALMOST_WHITE
    style.font = constant.FONT_DEFAULT_FAMILY, 12, "bold"
    #style.highlightThickness = 1
    return style

# entry repo name (bis)
def get_entry_repo_name_hovered_style():
    style = entry.get_style()
    style.readonlyBackground = "#00413C"
    style.foreground = "#E0E8EF"
    #style.highlightThickness = 1
    style.font = constant.FONT_DEFAULT_FAMILY, 12, "bold"
    return style

# entry running app name
def _get_entry_running_app_name_style():
    style = entry.get_style()
    style.readonlyBackground = "#181818"
    style.foreground = "#A098A0"
    style.highlightBackground = "#484048"
    style.highlightThickness = 1
    style.font = constant.FONT_DEFAULT_FAMILY, 12, "bold"
    return style

def _get_button_close_style():
    style = tkstyle.Button()
    style.background = constant.COLOR_BLACK
    style.activeBackground = constant.COLOR_BLACK
    style.activeForeground = "#FF0023"
    style.foreground = "#606060"
    style.borderWidth = 0
    style.highlightThickness = 0
    style.highlightBackground = "#606060"
    style.padX = 0
    style.padY = 0
    return style


def _get_label_path_app_info_style():
    style = label.get_style()
    style.background = "#005954"
    style.foreground = "#ECFFFF"
    style.font = constant.FONT_FAV_BOLD
    return style

def _get_entry_path_app_info_style():
    style = entry.get_style()
    style.background = "white"
    style.readonlyBackground = "#18817C"
    style.foreground = "#ECFFFF"
    return style

def _get_entry_form_app_info_style():
    style = entry.get_style()
    style.font = constant.FONT_FAV_NORMAL
    style.readonlyBackground = "#101818"
    style.highlightThickness = 0
    style.foreground = "#B4C7EF"
    style.relief = "flat"
    style.selectBackground = "#B4C7EF"
    return style

def _get_text_description_app_info_style():
    style = text.get_style()
    style.font = constant.FONT_FAV_NORMAL
    style.readonlyBackground = "#B4C7EF"  # TODO: remove this nan ?
    style.background = "#101818"
    style.highlightThickness = 0
    style.foreground = "#B4C7EF"
    style.relief = "flat"
    #style.inactiveSelectBackground = "#B4C7EF"
    return style


def _get_radiobbuton_style():
    style = radiobutton.get_style()
    style.background = constant.COLOR_BLACK
    style.foreground = "#8C9FB7"
    style.font = constant.FONT_FAV_NORMAL
    style.highlightThickness = 0
    style.activeBackground = "black"
    style.activeForeground = "#B4C7EF"
    style.selectColor = constant.COLOR_BLACK
    return style


def _get_title_latest_release_style():
    style = label.get_style()
    style.background = "#005954"
    style.foreground = "#ECFFFF"
    style.font = constant.FONT_FAV_BOLD
    return style


# button auth style
def get_button_auth_style():
    style = button.get_style()
    style.cursor = "hand1"
    style.background = "#183018"
    style.foreground = "#A0C0A0"
    style.highlightBackground = "#484048"
    style.highlightColor = "white"
    style.highlightThickness = 1
    style.relief = "flat"
    style.padY = 0
    style.activeBackground = "#202020"
    style.activeForeground = "#D0C8D0"
    return style
