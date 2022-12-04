# Debian-Package-Stats

## Project Description

This is a command line tool that takes the architecture of a contents index file as an argument and downloads the 
compressed contents file associated with it from a Debian mirror.

The program parses the file and outputs the statistics of the top 10 packages with the number of files. Example output:

*package name 1*.............*number of files*  
*package name 2*.............*number of files*

For the purpose of testing the program, the following link has been provided: http://ftp.uk.debian.org/debian/dists/stable/main/.

## How to use project

1. Clone the project to the local directory of choice and open it with IDE of choice.


2. Clone the project to the local directory of choice and open it with IDE of choice.


3. Open terminal and change directory to where project is kept.


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

[example image](./example.png)

## Specifications of project

1. For testing purposes a link was provided, that link is saved as an env variable and retrieved through the program 
to follow best practices of software development, but in the absence of the environment variable, the program will 
resort to using the same test link that has been hardcoded into the code. If you want to use a different link, 
you would either have to create an env file and save the new link with the expected env variable name 
or replace the hardcoded link in the program's code


2. The program expects arguments passed through the command line, this argument is the architecture variable we want to 
work with, the available architectures for the test link are ('all', 'amd64', 'arm64', 'armel', 'armhf', 'i386', 
'mips64el', 'mipsel', 'ppc64el', 's390x', 'source') should a new link be inserted, conditions have been put in place to 
still run the program but it does not validate if the required architecture exists in the new link 
i.e the program could fail if the input architecture does not exist in the new link

## Approach to solving problem

### Time spent
An estimated total of **20 hours in a span of 3 days** starting on 2/12/2022 was spent working on this project, a 
breakdown of the time spent developing this is below

1. **6 hours** - This time was used to understand the project and what needed to be done from beginning to end
2. **11 hours** - This time was used to develope the code that solves the problem
3. **3 hours** - This time was spent to refactor the code, add inline comments to the solutions, and update the readme file
for the project.


### Understanding the problem

Going through the link in the email, I had a hard time understanding the exact problem I needed to solve. My major 
issue was knowing what file I needed to download as the repository structure confused me, I decided the best way to 
understand what I needed to do was read the whole page explaining the repository structure and check things out rather 
than just reading the block about the contents indices file. After reading it whole, I could breakdown the problem 
into different actions I needed to take, the actions are below.


1. **Get link to contents index architecture file to download** - I knew I needed to download a file but how would I 
get the exact download link. My first thought was web scraping to get the exact link to the compressed indices file but 
realized all the compressed package indices file had a very uniform URL that would only change when the mirror link and 
architecture name changes. I decided requesting the exact download URL for the input architecture file was better 
as it would need less code and maintaining it would be easier as we only need to capture URL changes 
as compared to having to maintain a web scraper


2. **Download compressed index file for architecture** - Once the link was available downloading the file was fairly 
easy, I decided the best way to do this was first check if the file existed in a directory so we don't need to download 
files we already have, if it existed there was no need to request to download it. At the same time, I thought about 
what happens to the file after we calculate our statistics and don't need it again so I decided to make a method 
that deletes the file once we are done with it because if not, each time we run this program the files would pile up on 
the system


3. **Read compressed index file** - The downloaded file would be compressed so I needed a way to unzip it and read the 
contents, at first I decided to use pandas because I thought it would be relatively easy to use pandas to read the 
contents, clean it and eventually find the statistics but this was a bit difficult because of the file structure, 
so I opted to use a module that would unzip and read the contents line by line for me to clean and do whatever I wanted 
to do with the data. the data came in the format of bytes, and not strings I initially left it as that but when 
printing the statistics of the package it would print "b'package name'" and I figured having the 'b' denoting it was a 
byte spoilt the beauty so I decoded the file contents using the utf-8.  


5. **Extract and validate packagename** - At the same time, I figured having the filename column was not exactly 
necessary to solve the problem since the problem was to know the number of files a package had and sorting in 
descending order. Every filename appeared with a respective package name beside it, so every file was represented by 
a package. this led me to the conclusion that I only needed to count the number of times each unique package name
appeared. although I followed this approach, I still wrote code to handle the filename, especially those that had 
spaces in its name. I just commented it out, if you want to see the cleaned filename, follow the comments in the code. 
After doing this I would also split the lines which had more than one package name on them because they shared the same 
file. in doing this I was able to give each package name entry its individual appearance


6. **Get statistics of package name with most files** - At first, I figured I could use pandas and pass the cleaned 
package name list into a dataframe so I could do a simple groupby and get the statistics and order it but I figured 
since I did not use pandas previously, doing it at this point to extract only the statistics when there are other ways 
of doing it (which isn't complex) was just being lazy plus having to install pandas for this feature alone felt 
unnecessary so I did some googling and found a way of calculating the unique appearance of individual values in a list 
and eventually order them.

   
7. **Display top 10 statistics of package names with the most files** -  i simply displayed the package name and 
number of files

   
This was my whole process towards solving the problem, I initially followed certain approaches but changed direction 
as work went on, I also initially used certain modules and libraries but would drop them as I felt they were not needed 
to get the work done. I decided to follow an approach where maintaining the code would be easy to do and would not need 
too much third-party modules.



## Improvement to program

1. Test cases can be written for the program to ensure that it is always working as expected if the test case pass 
and if it doesn't somthing needs to be fixed or new maintainance needs to be rolled back
2. Code to handle situations where a new mirror link is inserted, the situation should handle if the input 
architecture for the new insert link doesn't exist so the program doesn't break





Last updated: 04/12/2022
Author: Adeoye Abiola Solomon
email: slmadeoye@gmail.com