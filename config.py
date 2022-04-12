# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os, re, shutil, subprocess
from libqtile import bar, hook, layout, widget, qtile
from libqtile.config import EzClick as Click, EzDrag as Drag, Group, EzKey as Key, Match, Rule, Screen
from libqtile.lazy import lazy

home = os.path.expanduser('~')
terminal = 'kitty'

keys = [
    # Switch between windows
    Key('M-h', lazy.layout.left(),
        desc='Move focus to left'),
    Key('M-l', lazy.layout.right(),
        desc='Move focus to right'),
    Key('M-j', lazy.layout.down(),
        desc='Move focus down'),
    Key('M-k', lazy.layout.up(),
        desc='Move focus up'),
    Key('M-<space>', lazy.layout.next(),
        desc='Move window focus to other window'),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key('M-S-h', lazy.layout.shuffle_left(),
        desc='Move window to the left'),
    Key('M-S-l', lazy.layout.shuffle_right(),
        desc='Move window to the right'),
    Key('M-S-j', lazy.layout.shuffle_down(),
        desc='Move window down'),
    Key('M-S-k', lazy.layout.shuffle_up(),
        desc='Move window up'),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key('M-C-h', lazy.layout.grow_left(),
        desc='Grow window to the left'),
    Key('M-C-l', lazy.layout.grow_right(),
        desc='Grow window to the right'),
    Key('M-C-j', lazy.layout.grow_down(),
        desc='Grow window down'),
    Key('M-C-k', lazy.layout.grow_up(),
        desc='Grow window up'),
    Key('M-n', lazy.layout.normalize(),
        desc='Reset all window sizes'),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        'M-S-<Return>',lazy.layout.toggle_split(),
        desc='Toggle between split and unsplit sides of stack',
    ),
    # Applicaion binds
    Key('M-f', lazy.spawn('thunar'),
        desc='Launch Thunar'),
    Key('M-<Return>', lazy.spawn(terminal),
        desc='Launch terminal'),
    Key('M-w', lazy.spawn('firefox'),
        desc='Launch Firefox'),
    Key('M-e', lazy.spawn('geany'),
        desc='Lauch Geany'),
    Key('<Print>', lazy.spawn('flameshot gui'),
        desc='Take screenshot'),

    # Audio binds
    Key('<XF86AudioRaiseVolume>', lazy.spawn('volume --inc'),
        desc='Increase Volume'),
    Key('<XF86AudioLowerVolume>', lazy.spawn('volume --dec'),
        desc='Decrease Volume'),
    Key('<XF86AudioMute>', lazy.spawn('volume --toggle'),
        desc='Mute/Unmute'),

    # MPD binds
    Key('<XF86AudioStop>', lazy.spawn('mpc stop')),
    Key('<XF86AudioPlay>', lazy.spawn('mpc toggle')),
    Key('<XF86AudioPrev>', lazy.spawn('mpc prev')),
    Key('<XF86AudioNext>', lazy.spawn('mpc next')),

    # Toggle between different layouts as defined below
    Key('M-<Tab>', lazy.next_layout(),
        desc='Toggle between layouts'),
    Key('M-c', lazy.window.kill(),
        desc='Kill focused window'),
    Key('M-C-r', lazy.reload_config(),
        desc='Reload the config'),
    Key('M-C-q', lazy.shutdown(),
        desc='Shutdown Qtile'),
    Key('M-r', lazy.spawncmd(),
        desc='Spawn a command using a prompt widget'),
]

groups = [Group(i) for i in '12345']

for i in groups:
    keys.extend(
        [
            # Mod1 + letter of group = switch to group
            Key(
                f'M-{i.name}',
                lazy.group[i.name].toscreen(),
                desc=f'Switch to group {i.name}',
            ),
            # Mod1 + Shift + letter of group = switch to & move focused window to group
            Key(
                f'M-S-{i.name}',
                lazy.window.togroup(i.name, switch_group=True),
                desc=f'Switch to & move focused window to group {i.name}',
            ),
        ]
    )

layouts = [
    layout.Columns(border_focus_stack=['#d75f5f', '#8f3d3d'], border_width=2),
    # layout.Max(),
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font     = 'Inter',
    fontsize = 12,
    padding  = 3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.Mpd2(),
                widget.Systray(),
                widget.Clock(format='%Y-%m-%d %a %H:%M'),
                widget.KeyboardLayout(),
            ],
            24,
            background = '#333333',
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=['ff00ff', '000000', 'ff00ff', '000000']  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag('M-1', lazy.window.set_position_floating(),
        start=lazy.window.get_position()),
    Drag('M-3', lazy.window.set_size_floating(),
        start=lazy.window.get_size()),
    Click('M-2', lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class='confirmreset'),  # gitk
        Match(wm_class='makebranch'),  # gitk
        Match(wm_class='maketag'),  # gitk
        Match(wm_class='ssh-askpass'),  # ssh-askpass
        Match(title='branchdialog'),  # gitk
        Match(title='pinentry'),  # GPG key password entry
        Match(title=r'osu\!.*'), # osu!
    ]
)
auto_fullscreen = True
focus_on_window_activation = 'smart'
reconfigure_screens = True

@hook.subscribe.restart
def cleanup():
    shutil.rmtree(os.path.expanduser('~/.config/qtile/__pycache__'))

@hook.subscribe.shutdown
def killall():
    shutil.rmtree(os.path.expanduser('~/.config/qtile/__pycache__'))
    subprocess.Popen(['killall', 'xfce-polkit', 'picom', 'thunar'])

@hook.subscribe.startup
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.run([home])

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = 'qtile'
