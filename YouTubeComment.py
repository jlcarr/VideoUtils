import moviepy.editor
#import moviepy.fx.all

from PIL import Image, ImageFont, ImageDraw
import numpy as np

import textwrap


# Global setup

def create_comment_img(username, date, likes, text, pfp="./AssetDev/pfp-A.jpg", readmore=False):
	# Setup
	pfp = Image.open(pfp)
	pfp = pfp.resize((80,80))
	mask = Image.new('L', pfp.size, 0)
	write_obj = ImageDraw.Draw(mask) 
	write_obj.ellipse((0, 0) + mask.size, fill=255)
	pfp.putalpha(mask)

	lines = text.count('\n')

	img = Image.new(mode='RGBA', size=(1280, 172 + 40 * lines + 48 * int(readmore)), color=(255,255,255))
	write_obj = ImageDraw.Draw(img)
	
	# Profile Picture
	img.paste(pfp, (0,2), pfp)

	# Username
	font_path = 'Roboto-Bold.ttf'
	font = ImageFont.truetype(font_path, 26)
	write_obj.text((112, 28), '@'+username, anchor='ls', font=font, fill=(15,15,15))
	offset = font.getlength('@'+username+' ' )

	# Date
	font_path = 'Roboto-Regular.ttf'
	font = ImageFont.truetype(font_path, 24)
	write_obj.text((112 + offset, 28), date, anchor='ls', font=font, fill=(96,96,96))
	
	# Comment
	font_path = 'Roboto-Regular.ttf'
	font = ImageFont.truetype(font_path, 28)
	write_obj.text((112, 74), text, anchor='ls', spacing=14, font=font, fill=(15,15,15))
	offset = 74 + 40 * lines

	if readmore:
		offset += 48
		font_path = 'Roboto-Medium.ttf'
		font = ImageFont.truetype(font_path, 28)
		write_obj.text((112, offset), "Read more", anchor='ls', font=font, fill=(96,96,96))
		
	# Likes
	thumbsup = Image.open('thumbs-up.png')
	thumbsdown = Image.open('thumbs-down.png')
	img.paste(thumbsup, (110, offset + 35))
	font_path = 'Roboto-Regular.ttf'
	font = ImageFont.truetype(font_path, 24)
	write_obj.text((160, offset + 59), likes, anchor='ls', spacing=14, font=font, fill=(96,96,96))
	lroffset = font.getlength(likes)
	img.paste(thumbsdown, (190 + int(lroffset), offset + 35))
	font_path = 'Roboto-Medium.ttf'
	font = ImageFont.truetype(font_path, 24)
	write_obj.text((280 + lroffset, offset + 59), "Reply", anchor='ls', spacing=14, font=font, fill=(15,15,15))

	return img


if __name__ == "__main__":
	create_comment_img("username", "2 days ago", "1K", "Comment text.\nMulti-lined.").save('test.png')

