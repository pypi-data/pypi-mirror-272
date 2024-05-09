# BrainTest

This project makes it possible to write brainf\*ck programs by running python unit tests.

Who knows what exciting programs you could be unwittingly writing while running your unit tests?!

Well wonder no longer!

Braintest is designed to be a drop in replacement for python's `unittest` module. It will run your tests (mostly) as normal, while also outputing a brainf\*ck program. Exceptions being: `unittest`'s verbosity option is overwritten, so you can't alter the verbosity of tests while running this.

## Demo

![demo gif of hello world](demo.gif)

## Usage

First install braintest:

```
python -m pip install braintest
```

Write your tests as you usually would with when using python's `unittest` and then replace `unittest` with `braintest` in your test command e.g.:

```
python -m braintest | tee my_program.bf
```

This will print out the results of the unit test, as well as write a brainf\*ck program to `my_program.bf`.

Then you can use a locally installed brainf\*ck interpreter to run your newly created program!

## Running a program

A simple brainf\*ck interpreter can be found in this repo. To run a program, pipe the program into the interpreter:

```
cat my_program.bf | python brainfuck-simple.py
```

Note: credit to Pablo Jorge where this brainf\*ck interpreter is [from](https://github.com/pablojorge/brainfuck/blob/master/python/brainfuck-simple.py) (with a slight modification to make it work with newer python versions)

## Writing programs

To write a `.` - write a successful unit test

To write a `+` - write a test that throws an exception

To write a `-` - write a test that throws a KeyError (admittedly this is a bit hacky)

To write a `>` - write a test that fails

To write a `[` - skip a test

To write a `]` - write a test that fails that you expect to fail

To write a `<` - write a test that succeeds when it shouldn't

To write a `,` - write a test that throws an IOError

You can see examples of all of these in action in the sample `program.py` provided in this repo.
Be careful though! Tests are ran in order based on their alphabetical sorting of their function names.

## Why?

For fun.

## But seriously, why?

While I was waiting for my tests to complete I was staring at the python unittest output and thought it looked kind of like brainf\*ck. So I thought it would be fun to override the default test runner to output valid brainf\*ck characters.
