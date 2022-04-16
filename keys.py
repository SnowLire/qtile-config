import os

from libqtile.config import EzKey as Key
from libqtile.lazy import lazy

from config import groups

browser = 'firefox'
editor = 'geany'
filemanager = 'thunar'
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
    Key('M-f', lazy.spawn(filemanager),
        desc='Launch file manager'),
    Key('M-<Return>', lazy.spawn(terminal),
        desc='Launch terminal'),
    Key('M-w', lazy.spawn(browser),
        desc='Launch browser'),
    Key('M-e', lazy.spawn(editor),
        desc='Launch editor'),
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
    Key('A-r', lazy.spawn(os.path.expanduser('~/.config/openbox/rofi/bin/launcher')),
        desc='Open rofi'),
]

for i in groups:
    keys.extend(
        [
            Key(f'M-{i.name}', lazy.group[i.name].toscreen(),
                desc=f'Switch to group {i.name}'),
            Key(f'M-S-{i.name}', lazy.window.togroup(i.name, switch_group=True),
                desc=f'Switch to & move focused window to group {i.name}'),
        ]
    )
