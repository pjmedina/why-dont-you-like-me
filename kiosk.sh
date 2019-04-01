#!/bin/bash

launchChrome () {
xset s noblank
xset s off
xset -dpms

sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' /home/pi/.config/chromium/Default/Preferences
sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' /home/pi/.config/chromium/Default/Preferences

/usr/bin/chromium-browser --noerrdialogs --disable-infobars --incognito  --kiosk http://127.0.0.1:5000 &
}

runFlaskStuff () {
cd ~/Documents/why-dont-you-like-me/
pwd
export "FLASK_APP=app-button.py"
flask run
}

updateCode () {
cd ~/Documents/why-dont-you-like-me/
git pull
}

#updateCode

runFlaskStuff &
launchChrome
