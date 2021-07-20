# Multifunge
Multifunge is an esoteric programming language based on Asciidots. 
You can find a description of how the language works [here](https://owenbechtel.com/multifunge). 
Once you download the interpreter, there are two ways to run a multifunge program.
* Pass the name of the multifunge file as an argument in the command line.
```
./multifunge.py your-program.mfg
```
* Import the interpreter into a python program, and use the `run` function.
```python
import multifunge
code = """
@ ? *   v
@?v
  *[+]!.
  >    [*]!
"""
multifunge.run(code)
```
## Input files
If you want your multifunge program to read from a file, you can add the path of the input file as an argument.
For example, `./multifunge.py examples/calculator.mfg examples/multiplication.txt` should output "51324."
You can also use `<`, but this doesn't always work for some reason.

The `run` function can take an additional string parameter. 
In this case, the program will use the string as input instead of getting input from the user.
For example, `run("@c?+!.", "a")` will run the program `@c?+!.` with the input `"a"`.
