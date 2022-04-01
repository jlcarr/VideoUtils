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


def create_search_scene(text, timing=0.05, resolution=(720, 1280)):
	# Main loop
	clip_list = []
	for i in range(len(text)+1):
		img = create_search_img(text[:i])
		clip_list.append(moviepy.editor.ImageClip(np.array(img)[:,:,:-1], duration=timing))
		
	video = moviepy.editor.concatenate_videoclips(clip_list, method='compose')

	return video


if __name__ == "__main__":
	#create_search_img("How to make videos?").save('test.png')

	video = create_search_scene("How to make videos?")
	video.write_videofile('test.mp4', fps=60, threads=0, preset='slow')
