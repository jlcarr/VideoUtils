import moviepy.editor
#import moviepy.fx.all

from PIL import Image, ImageFont, ImageDraw
import numpy as np

import textwrap


# Global setup
search_template = Image.open('search_template.png')


def create_search_img(text):
	# Params
	font_path = 'Arial.ttf'
	font_size = 28 # in pts (3pt->4px) 24px
	text_anchor = (280, 387)
	font = ImageFont.truetype(font_path, font_size)

	# Setup
	img = search_template.copy()
	write_obj = ImageDraw.Draw(img)
	
	write_obj.text(text_anchor, text, font=font, fill=(0,0,0))
	
	return img



if __name__ == "__main__":
	create_search_img("How to make videos?").save('test.png')
