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
	sender = [text[1] for text in texts]
	texts = [text[0
	] for text in texts]
	
	bubble_width = bubble_ratio * image_width
	text_width = bubble_width - text_margin_l - text_margin_r

	font = ImageFont.truetype(font_path, font_size)
	total_texts = ' '.join(texts)
	total_texts_width = font.getlength(total_texts)
	char_width = len(total_texts) / total_texts_width
	line_len = int(char_width * text_width)

	texts = ['\n'.join(textwrap.wrap(text, line_len)) for text in texts]

	bubble_heights = [
		text_margin_t + font.getsize_multiline(text)[1] + text_margin_d + bubble_margin
		for text in texts
	]
	bubble_heights = [image_margin] + bubble_heights
	total_text_height = sum(bubble_heights)
	bubble_heights = list(np.cumsum(bubble_heights))


	img = Image.new('RGB', (image_width, total_text_height), color=back_color)
	write_obj = ImageDraw.Draw(img)
	
	for i, (s, text) in enumerate(zip(sender, texts)):
		text_size = font.getsize_multiline(text)
	
		if s % 2 == 0:
			bubble_color = self_bubble_color
			
			right_edge = image_width - image_margin
			rect_upper = (
				right_edge - text_margin_l - text_size[0] - text_margin_r,
				bubble_heights[i]
			)
			rect_lower = (
				right_edge,
				bubble_heights[i+1] - bubble_margin
			)
		else:
			bubble_color = other_bubble_color
			
			rect_upper = (image_margin, bubble_heights[i])
			rect_lower = (
				rect_upper[0] + text_margin_l + text_size[0] + text_margin_r,
				bubble_heights[i+1] - bubble_margin
			)

		text_anchor = (
			rect_upper[0] + text_margin_l,
			bubble_heights[i] + text_margin_t
		)
		
		write_obj.rounded_rectangle([rect_upper, rect_lower], radius=bubble_corner_radius, fill=bubble_color)
		write_obj.text(text_anchor, text, font=font, color=text_color)
		
	return img, bubble_heights


if __name__ == "__main__":
	texts = [
		("This is the first text", 0),
		("This is the reply", 1),
		("This is a very long text that runs on and on and on without step, it's very annoying but I gotta hit the quota somehow", 0)
	]

	create_text_convo_img(texts)[0].save('test.png')
