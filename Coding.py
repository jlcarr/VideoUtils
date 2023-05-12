import moviepy.editor

from PIL import Image, ImageDraw
import numpy as np
import io
import pygments
from pygments.token import Token


paren_map = {
	(Token.Punctuation, '['): (Token.Punctuation, ']'),
	(Token.Punctuation, '('): (Token.Punctuation, ')'),
	(Token.Punctuation, '{'): (Token.Punctuation, '}'),
	(Token.Literal.String.Double, '"'): (Token.Literal.String.Double, '"'),
	(Token.Literal.String.Single, "'"): (Token.Literal.String.Single, "'"),
}

def create_coding_scene(code, style="dracula", animate_cursor=True, animate_parens=True, fps=20, duration=None, resolution=(1280, 720), verbose=False):
	lexer = pygments.lexers.PythonLexer()
	tokens = list(pygments.lex(code, lexer))
	fin = [tokens[-1]]
	if verbose:
		print(f"{len(tokens)} tokens to process")
	
	formatter = pygments.formatters.ImageFormatter(style=style)
	background = Image.new('RGB', resolution, color=formatter.background_color)
	
	img_list = []
	paren_stack = []
	prev_tokens = []
	cursor = [(Token.Text, '|')] if animate_cursor else []
	for i,(ttype, token) in enumerate(tokens):
		if verbose:
			print(f"Processing up to token {i}: {(ttype, token)}")
		if (ttype, token) == (Token.Text.Whitespace, '\n') \
			and i < len(tokens) \
			and tokens[i+1][1].startswith('\t'):
			prev_tokens.append((ttype, token))
			continue
		if animate_parens:
			if paren_stack and (ttype, token) == paren_stack[-1]:
				paren_stack.pop()
			elif (ttype, token) in paren_map:
				paren_stack.append(paren_map[(ttype, token)])
		is_tab = ttype == Token.Text and token.startswith('\t')
		for j in range(len(token)):
			if is_tab:
				j = len(token)-1
			used_tokens = prev_tokens + [(ttype, token[:j+1])] + cursor + paren_stack[::-1] + fin
			formatter = pygments.formatters.ImageFormatter(style=style)
			new_img = pygments.format(used_tokens, formatter)
			new_img = Image.open(io.BytesIO(new_img))
			img = background.copy()
			formatter._paint_line_number_bg(img)
			img.paste(new_img)
			img_list.append(np.array(img))
			if is_tab:
				break
			
		prev_tokens.append((ttype, token))
		
		if formatter._get_image_size(formatter.maxlinelength, formatter.maxlineno-2)[-1] > img.size[-1]:
			break

	if duration is not None:
		fps = len(img_list)/duration
	video = moviepy.editor.ImageSequenceClip(img_list, fps=fps)
	
	#typing_audio = moviepy.editor.AudioFileClip('typing.mp3')
	#typing_audio = moviepy.editor.afx.audio_loop(typing_audio, duration=video.duration)
	#video.audio = typing_audio
	
	return video


if __name__ == "__main__":
	with open(__file__, 'r') as f:
		code = f.read()
	#code = "	[({\"\", ''},)]"
	video = create_coding_scene(code, verbose=True)
	#video.write_videofile('test.mp4', fps=60, threads=0, preset='slow')
	video.write_videofile('test.mp4', fps=24, audio_codec='aac', threads=0, preset='ultrafast', ffmpeg_params=['-crf', '32'])
