stylus:
	stylus -u nib -w ./src/static/assets/stylus/main.styl -o ./src/static/assets/css/
web:
	stylus -u nib -w ./src/static/stylus/styl.styl -o ./src/static/css/
style:
	sass --watch src/static/styles/main.scss:src/static/css/main.css
