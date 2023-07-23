import moviepy.editor
#import moviepy.fx.all

from PIL import Image, ImageFont, ImageDraw
import numpy as np

import textwrap


# Global setup

def create_comment_img(username, date, text, pfp="./AssetDev/pfp-A.jpg"):
	# Setup
	pfp = Image.open(pfp)
	pfp = pfp.resize((80,80))
	mask = Image.new('L', pfp.size, 0)
	write_obj = ImageDraw.Draw(mask) 
	write_obj.ellipse((0, 0) + mask.size, fill=255)
	pfp.putalpha(mask)

	img = Image.new(mode='RGBA', size=(1280, 95), color=(255,255,255))
	write_obj = ImageDraw.Draw(img)
	
	# Profile Picture
	img.paste(pfp, (0,3), pfp)

	# Username
	font_path = 'Roboto-Medium.ttf'
	font_size = 26 # in pts (3pt->4px) 24px
	font = ImageFont.truetype(font_path, font_size)
	write_obj.text((112, 30), '@'+username, anchor='ls', font=font, fill=(15,15,15))
	offset = font.getlength('@'+username+' ' )

	# Date
	font_path = 'Roboto-Regular.ttf'
	font_size = 24 # in pts (3pt->4px) 24px
	font = ImageFont.truetype(font_path, font_size)
	write_obj.text((112 + offset, 30), date, anchor='ls', font=font, fill=(96,96,96))
	

	# Comment
	font_path = 'Roboto-Regular.ttf'
	font_size = 28 # in pts (3pt->4px) 24px
	font = ImageFont.truetype(font_path, font_size)
	write_obj.text((112, 76), text, anchor='ls', font=font, fill=(15,15,15))

	return img


if __name__ == "__main__":
	create_comment_img("username", "1 day ago", "This is my comment text.").save('test.png')

