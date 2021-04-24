# Multifunge
Multifunge is an esoteric programming language based on Asciidots and Befunge. You can find a description of how the language works [here](https://owenbechtel.com/multifunge). Once you download the interpreter, there are two ways to run a multifunge program.
1. Pass the name of the multifunge file as an argument in the command line.
```
python multifunge.py your-program.mfg
```
2. Import the interpreter into a python program, and use the `run` function.
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
