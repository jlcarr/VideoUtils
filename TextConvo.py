import moviepy.editor
#import moviepy.fx.all

from PIL import Image, ImageFont, ImageDraw
import numpy as np

import textwrap


# Global setup
texting_template = Image.open('texting_template.png')
bbox = [(22,70), (275,337)]
texting_base = Image.new('RGBA', texting_template.size, color=(0,0,0,0))
texting_base_write = ImageDraw.Draw(texting_base)
texting_base_write.rectangle(bbox, fill='white')


def create_text_convo_img(texts):
	# Params
	back_color = (255,255,255) #(0,0,0)
	self_bubble_color = (25,140,255)
	other_bubble_color = (232, 232, 232) # (38,38,38)
	self_text_color = (255,255,255) #(255,255,255)
	other_text_color = (0,0,0) #(255,255,255)
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
	texts = [text[0] for text in texts]
	
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
	
	# Main loop
	for i, (s, text) in enumerate(zip(sender, texts)):
		text_size = font.getsize_multiline(text)
	
		# Place the bubble depending on the sender
		if s % 2 == 0:
			bubble_color = self_bubble_color
			text_color = self_text_color
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
			text_color = other_text_color
			rect_upper = (image_margin, bubble_heights[i])
			rect_lower = (
				rect_upper[0] + text_margin_l + text_size[0] + text_margin_r,
				bubble_heights[i+1] - bubble_margin
			)

		# Now draw
		text_anchor = (
			rect_upper[0] + text_margin_l,
			bubble_heights[i] + text_margin_t
		)
		write_obj.rounded_rectangle([rect_upper, rect_lower], radius=bubble_corner_radius, fill=bubble_color)
		write_obj.text(text_anchor, text, font=font, fill=text_color)
		
	return img, bubble_heights


def construct_texting_frame(template, texts_img, texts_height):
	img = texting_base.copy()
	img.paste(texts_img, (bbox[0][0], bbox[1][1]-texts_height))
	img.paste(template, (0,0), template)
	return img
	

def create_text_convo_scene(texts, name="",timing=1):
	# Setup
	if not isinstance(timing, list):
		timing = [timing] * (len(texts)+1)
	
	texts_img, bubble_heights = create_text_convo_img(texts)
	ratio = (bbox[1][0] - bbox[0][0])/texts_img.size[0]
	texts_img = texts_img.resize((int(texts_img.size[0] * ratio), int(texts_img.size[1] * ratio)))
	bubble_heights = [int(height * ratio) for height in bubble_heights]
	
	font = ImageFont.truetype('SF-Pro.ttf', 14)
	template = texting_template.copy()
	template_write = ImageDraw.Draw(template)
	template_write.text((150, 95), name, anchor="mm", font=font, fill=(0,0,0))
	
	def frame_maker(height_diff, height):
		def result(t):
			return np.array(construct_texting_frame(template, texts_img, int(height_diff * t + height)))[:,:,:-1]
		return result
		
	# Main loop
	clip_list = []
	for i, (height, t) in enumerate(zip(bubble_heights, timing)):
		img = construct_texting_frame(template, texts_img, height)
		clip_list.append(moviepy.editor.ImageClip(np.array(img), duration=t))
		if i < len(texts):
			duration = 0.125
			height_diff = (bubble_heights[i+1] - height)/duration
			clip_list.append(moviepy.editor.VideoClip(make_frame=frame_maker(height_diff,height), duration=duration))
	
	video = moviepy.editor.concatenate_videoclips(clip_list, method='compose')
	return video


if __name__ == "__main__":
	texts = [
		("This is the first text", 0),
		("This is the reply", 1),
		("This is a very long text that runs on and on and on without step, it's very annoying but I gotta hit the quota somehow", 0)
	]
	#create_text_convo_img(texts)[0].save('test.png')
	video = create_text_convo_scene(texts, name="Buddy", timing=2)
	video.write_videofile('test.mp4', fps=60, audio_codec='aac', threads=0, preset='slow')
	#video.write_videofile('test.mp4', fps=24, audio_codec='aac', threads=0, preset='ultrafast', ffmpeg_params=['-crf', '32'])
