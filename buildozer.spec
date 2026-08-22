[app]

title = Galaxy Quest
package.name = galaxyquest
package.domain = org.galaxyquest
version = 1.8

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,wav,mp3

requirements = python3,kivy

orientation = landscape
fullscreen = 0

# Android
android.api = 35
android.minapi = 24
android.ndk = 27.2.12479018
android.ndk_api = 24
android.archs = armeabi-v7a
android.accept_sdk_license = True

# Python-for-Android
p4a.fork = kivy
p4a.branch = master


[buildozer]

log_level = 2
warn_on_root = 1
