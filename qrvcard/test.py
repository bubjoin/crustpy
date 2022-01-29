# pip install qrcode[pil]

import qrcode

img = qrcode.make('Hello, World!')
img.save("qrcode.png")