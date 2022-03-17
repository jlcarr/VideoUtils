import moviepy.editor
#import moviepy.fx.all

from PIL import Image, ImageFont, ImageDraw
import numpy as np

import textwrap

def create_text_convo_img(texts):
	# Params
	back_color = (0,0,0)
	self_bubble_color = (25,140,255)
	other_bubble_color = (38,38,38)
	text_color = (255,255,255)
	font_path = 'SF-Pro.ttf'
	font_size = 36 # in pts (3pt->4px) 24px
	image_width = 750
	image_height = 1334
	image_margin = 32
	bubble_ratio = 0.70
	bubble_corner_radius = 34
	bubble_margin = 18
	text_margin_l = 25
	text_margin_r = 26
	text_margin_t = 14
	text_margin_d = 22


	# Setup
	bubble_width = bubble_ratio * image_width
	text_width = bubble_width - text_margin_l - text_margin_r

	font = ImageFont.truetype(font_path, font_size)
	total_texts = ' '.join(texts)
	total_texts_width = font.getlength(total_texts)
	char_width = len(total_texts) / total_texts_width
	line_len = int(char_width * text_width)

	texts = ['\n'.join(textwrap.wrap(text, line_len)) for text in texts]


	img = Image.new('RGB', (image_width, image_height), color=back_color)
	write_obj = ImageDraw.Draw(img)
	
	height_cursor = image_margin
	for text in texts:
		text_size = font.getsize_multiline(text)
	
		rect_tl = (image_margin, height_cursor)
		rect_dr = (
			rect_tl[0] + text_margin_l + text_size[0] + text_margin_r,
			rect_tl[1] + text_margin_t + text_size[1] + text_margin_d
		)
		write_obj.rounded_rectangle([rect_tl, rect_dr], radius=bubble_corner_radius, fill=other_bubble_color)
	
		text_anchor = (
			rect_tl[0] + text_margin_l,
			height_cursor + text_margin_t
		)
		write_obj.text(text_anchor, text, font=font, color=text_color)
		
		height_cursor = rect_dr[1] + bubble_margin
		
	img.save('test.png')


if __name__ == "__main__":
	texts = [
		"This is the first text",
		"This is the reply",
		"This is a very long text that runs on and on and on without step, it's very annoying but I gotta hit the quota somehow"
	]
	create_text_convo_img(texts)
