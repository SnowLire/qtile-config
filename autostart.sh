#!/usr/bin/env bash

killall -9 xfsettingsd xfce-polkit picom polybar xfce4-power-manager mpd flameshot

~/.fehbg &
xfsettingsd &
/usr/lib/xfce-polkit/xfce-polkit &
xfce4-power-manager &
exec thunar --daemon &
exec mpd &
exec otd &
exec flameshot &
exec /usr/bin/openrgb --startminimized --profile 'Main' &
exec qbittorrent &

sleep 3s
pkill openrgb
