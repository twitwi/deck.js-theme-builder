
SASSOPTS=--scss --style expanded

all:
	make _fontbox.scss
	#make theme-variations
	make sass-generate

sass-generate:
	sass --update ${SASSOPTS} .

theme-variations: tools/generate-variations.py
	$<

_fontbox.scss: _fontbox.scss.in tools/get-and-use-local-fonts.py
	tools/get-and-use-local-fonts.py $<


.PHONY: sass-generate theme-variations
