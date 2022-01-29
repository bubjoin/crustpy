# pip install qrcode[pil]

import qrcode

data = """
BEGIN:VCARD
VERSION:3.0
N:산책;김;;;
FN:김산책
TITLE:산책왕
ORG:동네마실팀
URL:https://동네마실팀홈페이지
TEL:010-0000-0000
EMAIL:산책왕@동네마실팀이메일
ADR:대한민국
END:VCARD
"""

qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_M,
    box_size=10, 
    border=4,
)
qr.add_data(data)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save('qrvcard.png')

from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import CircleModuleDrawer
from qrcode.image.styles.moduledrawers import GappedSquareModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask

img_1 = qr.make_image(image_factory=StyledPilImage, \
    module_drawer=CircleModuleDrawer())
img_1.save('qrvcard_style1.png')

img_2 = qr.make_image(image_factory=StyledPilImage, \
    color_mask=RadialGradiantColorMask(), \
    module_drawer=GappedSquareModuleDrawer())
img_2.save('qrvcard_style2.png')

img_3 = qr.make_image(image_factory=StyledPilImage, \
    embeded_image_path="embed.png", \
    module_drawer=GappedSquareModuleDrawer())
img_3.save('qrvcard_style3.png')