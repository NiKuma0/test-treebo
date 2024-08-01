build:
	-mkdir dist/
	git archive -o dist/todolist.sourcecode.zip HEAD

build-image:
	-mkdir dist/
	docker buildx build . -t todolist
	docker save -o dist/todolist.image.tar todolist