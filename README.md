# Debian-Package-Stats

## Project Description

This is a command line tool that takes the architecture of a contents index file as an argument and downloads the 
compressed contents file associated with it from a debian mirror.

The program parses the file and output the statistics of the top 10 packages that have the most files associated with them.  
Example output:

*package name 1*.............*number of files*  
*package name 2*.............*number of files*

For the purpose of testing the program, the following link has been provided: http://ftp.uk.debian.org/debian/dists/stable/main/.

## How to use project

1. Clone project to local directory of choice and open with IDE of choice


2. Create virtual environment using a python 3 interpreter (Interpreter used is python3.9)


3. Open terminal and change directory to where project is kept


4. Install dependencies and program requirements by running the command below in the terminal box
```bash
pip install -r requirements.txt
```

5. Once requirements are installed, run program by calling any of the two lines below where
**'$architecture-argument' is the name of the architecture you want to find out the statistics for**
```bash
runner.py $architecture-argument
```
or
```bash
python runner.py $architecture-argument
```
![sample program run](https://photos.app.goo.gl/6YeKfAyECGnJ6G5QA)