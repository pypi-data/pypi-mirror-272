from psychopy.app.themes.colors.app import BaseAppColorScheme, BaseColor


class CatppuccinLatteAppColors(BaseAppColorScheme):
    name = "catppuccin_latte"
    colors = {
        "text": "#4c4f69",
        "frame_bg": "#dce0e8",
        "panel_bg": "#e6e9ef",
        "tab_bg": "#eff1f5",
        "docker_bg": "#ccd0da",
        "docker_fg": "#4c4f69",
        "bmpbutton_bg_hover": "#dc8a78",
        "bmpbutton_fg_hover": "#eff1f5",
        "txtbutton_bg_hover": "#dc8a78",
        "txtbutton_fg_hover": "#eff1f5",
        "rt_timegrid": "#8c8fa1",
        "rt_comp": "#7287fd",
        "rt_comp_force": "#df8e1d",
        "rt_comp_disabled": "#9ca0b0",
        "rt_static": BaseColor("#dc8a78") * 77,
        "rt_static_disabled": BaseColor("#9ca0b0") * 77,
        "fl_routine_fg": "#eff1f5",
        "fl_routine_bg_slip": "#7287fd",
        "fl_routine_bg_nonslip": "#179299",
        "fl_flowline_bg": "#8c8fa1",
        "fl_flowline_fg": "#eff1f5",
    }