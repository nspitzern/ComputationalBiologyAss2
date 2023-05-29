# ComputationalBiologyAss2

## What is this all about?
### The goal
Simulating a Genetic Algorithm to solve a problem of Mono-Alphabetic encryption on a text file.

### Types of algorithms
There are three types of algorithms:
- Regular - Runs a regular GA.
- Darwin - Runs a Darwin GA with local optimization on the solutions that are not passed on to the next generation.
- Lamarck - Runs a Lamarck GA with local optimization on the solutions that are passed on to the next generation.

### Files to provide
1. enc.txt
2. Letter_Freq.txt
3. Letter2_Freq.txt
4. dict.txt

These files should be in the executable's directory.

## Setting up the environment
Python version should be 3.6 or above.

Install all the requirements by running:
>pip install -r requirements.txt

## Running the program
To run in CLI mode run:
>python main.py [*required flags*] [*optional flags*]

The available flag are:

Optional:
> *-n*: Setting the number of max tries the algorithm will run *[default 10]*.<br>
> *-ps*: Setting the size of the population *[default 300]*.<br>
> *-acc*: Setting the fitness goal of the algorithm *[default 0.99]*.

Required flags:
> *-r*: Run a regular Genetic Algorithm.<br>
> *-d*: Run a Darwin Genetic Algorithm.<br>
> *-l*: Run a Lamarck Genetic Algorithm.

***Notice***: Only one of the required flags can be chosen.

## Create executable file
Install pyinstaller:
>pip install pyinstaller

Create executable:
>pyinstaller -wF -p src main.py

## Running the Executable
To run the executable in CLI mode run:
>main.exe [*required flags*] [*optional flags*]

***Notice***: The flags here are the same as the flags to the python file.