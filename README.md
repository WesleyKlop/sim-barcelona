# Barcelona Trash Art

For the 2022 edition of the SIM study trip to Barcelona we created a MVP
for a trash can that motivates people to throw away their trash by turning it into art!

## Hardware ingredients

- Raspberry Pi 4b
- A webcam
- A big, red, button
- A screen
- A trashcan to mount it on

## Software

It's built utilizing the Magenta fast arbitrary style transfer model found here: https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2  
When the button is pressed we take a picture using the webcam, load a random style, and transfer it onto the webcam image.

We use Flask as a web server to serve our dumb ui. This ui listens to server-sent events to update the state of the page. The Pi is automatically
booted to this page using a systemd service and simple shell script to start chromium in kiosk mode.
