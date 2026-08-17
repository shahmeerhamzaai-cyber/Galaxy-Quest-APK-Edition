[app]
title = Galaxy Quest
package.name = galaxyquest
package.domain = org.galaxyquest
version = 1.8

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,wav,mp3

requirements = python3,kivy,charset-normalizer==2.1.1

android.api = 35
android.minapi = 24
android.ndk = 28c
android.ndk_api = 24

orientation = landscape
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[python-for-android]
p4a.branch = master
