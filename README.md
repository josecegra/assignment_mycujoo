# assignment_mycujoo

`src`: folder where the source code is

`docker`: folder for creating a docker image (it includes the python package `assignment_mycujoo-0.0.1.tar.gz`)

For the execution of the code it is necessary to create a folder (let’s name it `executions`) with the file `oriental_picture.png` inside.


## Executing the code with python

requirements: `opencv-python==4.2.0.32`,`pytesseract==0.3.2` 

- open terminal

- change the directory to the folder `docker`

- `pip install assignment_mycujoo-0.0.1.tar.gz`

- change the directory to the folder `executions`

- `run_assignment_mycujoo`


## Executing the code with docker

### Build docker image:

- open terminal

- change the directory to the folder `docker`

- `docker build -t mycujoo_image .`

### Run docker image

- change the directory to the folder `executions`

- `docker run -it --mount src="$(pwd)",target=/work_dir,type=bind mycujoo_image`
