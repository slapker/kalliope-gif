# kalliope-gif

A neuron to make funny Gif with Kalliope


## Synopsis

Make kalliope creating a Gif with your Webcam !

## Installation

  ```
  kalliope install --git-url https://github.com/slapker/kalliope-gif.git
  ```


## Options

| parameter        | required | default   | choices | comment                                                                                    |
|------------------|----------|-----------|---------|--------------------------------------------------------------------------------------------|
| nb_photos        | yes      |           | Int     | Number of photos for making the Gif                                                        |
| duration         | yes      |           | Decimal | Time between each frame for the Gif                                                        |
| directory        | yes      |           | string  | Directory's path for the Gif                                                               |
| send-to-telegram | yes      |           | boolean | Yes if you want to send the gif to your own telegram contact/chan                          |
| timer            | no       | 1         | Int     | Times between each photo                                                                   |
| reverse          | no       | False     | boolean | If you want a "looping" gif                                                                |
| telegram-cli     | no       |           |         | Your telegram-cli path                                                                     |
| telegram-pub     | no       |           |         | Your telegram-pub path                                                                     |
| telegram-chan    | no       |           |         | Your telegram-chan name                                                                    |
| synapse          | no       |           |         | The name of the synapse launche once your Gif is sent to telegram                          |



## Synapses example

```yaml
  - name: "Make-gif"
    signals:
      - order: "Make me a gif"
    neurons:
      - kalliope_gif:
          nb_photos : 10
          directory: "/home/XXXXX/webcam_kalliope/"
          reverse : True
          timer: 1
          duration : 0.2
          synapse: "upload-over"
          send-to-telegram : True
          telegram-cli : "/home/XXXXX/tg/bin/telegram-cli"
          telegram-pub : "/home/XXXXX/tg/tg-server.pub"
          telegram-chan : "myTelegramChan"
      - say :
          message :
            - "Nice Gif dude !"


  - name: "upload-over"
    signals:
      - order: "upload-is-over"
    neurons:
      - say:
          message:
            - "The Gif has been sent to Telegram"

```
