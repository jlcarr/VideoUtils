import moviepy.editor

from PIL import Image, ImageDraw
import numpy as np
import io
import pygments

# class override for video formatting
class VideoFormatter(pygments.formatters.ImageFormatter):
	def __init__(self, resolution=(720, 1280), **options):
		super().__init__(**options)
		self.resolution = resolution
		
		def format(self, tokensource, outfile):
			self._create_drawables(tokensource)
			self._draw_line_numbers()
			im = Image.new('RGBA', self.resolution, self.background_color)
			#self._paint_line_number_bg(im)
			draw = ImageDraw.Draw(im)
			# Highlight
			if self.hl_lines:
				x = self.image_pad + self.line_number_width - self.line_number_pad + 1
				recth = self._get_line_height()
				rectw = im.size[0] - x
				for linenumber in self.hl_lines:
					y = self._get_line_y(linenumber - 1)
					draw.rectangle([(x, y), (x + rectw, y + recth)], fill=self.hl_color)
			for pos, value, font, text_fg, text_bg in self.drawables:
				if text_bg:
					text_size = draw.textsize(text=value, font=font)
					draw.rectangle([pos[0], pos[1], pos[0] + text_size[0], pos[1] + text_size[1]], fill=text_bg)
				draw.text(pos, value, font=font, fill=text_fg)
			print(im.size)
			im.save(outfile, self.image_format.upper())
		

def create_coding_scene(code, name="", timing=0.1, resolution=(1280, 720)):
	lexer = pygments.lexers.PythonLexer()
	tokens = list(pygments.lex(code, lexer))
	fin = [tokens[-1]]
	print(f"{len(tokens)} tokens to process")
	
	formatter = pygments.formatters.ImageFormatter(style="dracula")
	img = Image.new('RGB', resolution, color=formatter.background_color)
	formatter._paint_line_number_bg(img)
	
	clip_list = []
	used_tokens = []
	for i,token in enumerate(tokens):
		print(f"Processing up to token {i}")
		formatter = pygments.formatters.ImageFormatter(style="dracula")
		new_img = pygments.format(used_tokens + fin, formatter)
		new_img = Image.open(io.BytesIO(new_img))
		img.paste(new_img)
		clip_list.append(moviepy.editor.ImageClip(np.array(img), duration=timing))
		
		if formatter._get_image_size(formatter.maxlinelength, formatter.maxlineno-2)[-1] > img.size[-1]:
			break
			
		used_tokens.append(token)

	video = moviepy.editor.concatenate_videoclips(clip_list, method='compose')
	
	return video
	
if __name__ == "__main__":
	with open(__file__, 'r') as f:
		code = f.read()
	video = create_coding_scene(code)
	#video.write_videofile('test.mp4', fps=60, threads=0, preset='slow')
	video.write_videofile('test.mp4', fps=24, audio_codec='aac', threads=0, preset='ultrafast', ffmpeg_params=['-crf', '32'])
