# 1ari-mp - *"Jefferson Disk"*

## Synopsis

This repository contains the work done for a SUPINFO school project where
students were asked to code a cipher system, the [Jefferson Disk], in Python
and Pygame for the graphical user interface.  
Being a group project, it involved two persons:
 * DOURNEAU Pierre-Louis ([@pldiiw])
 * Clément GRIMAUD ([@ehrakis])

## Installation

Requires Python 3.5+ and Pygame.

Clone the repository:

    git clone https://github.com/pldiiw/1ari-mp.git

Then run the GUI:

    python3 src/JeffersonGUI.py

## Tests

There's a test suite inside the `test/` directory.

To run it, just execute the test script:

    ./run_tests.sh

It requires mypy. If don't have it, just run:

    pip3 install mypy-lang

## Project Hierarchy

All source files can be found in the `src/` directory.  
Tests are under the `test/` directory.

## Code guidelines

### PEP-8

Coding conventions are important to keep the code base clean. We followed the
guidelines defined in the [PEP-8]. [YAPF] helped us reach this goal without
headaches, and by saving a lot of time.

### Function annotations

[Function annotations] is a new language feature introduced in Python 3.5. It
can be used to explicitly type function parameters and variables. Along with
[Mypy], it helped us avoid bugs ahead of runtime, sketch the _flow_ of the code
and easily understand and share function type signatures.

## Tools used

### Git

Sharing code and combining with the work of others can be an intricate process.
Git hugely facilitates this by providing the appropriate tools to get a more
organized workflow and keep track of our advancement.

### YAPF

[YAPF] is a code formatter for Python that goes further than others linting
tools. It totally rearrange the code to get a consistent code style, following
a given style guide, like the PEP-8.

### Isort

[Isort] is a little utility that alphabetically sort imports and seperate them
into sections, making imports more readable and pleasent. Alongside YAPF, it
pushes even further the concept of a consistent code style.

## Notes on function naming

The functions and procedures names asked in the subject differ a bit from the
ones we wrote. We chose to slightly modify the naming to have a codebase
matching the PEP-8 closer and having more expressive names, resulting in more
readable code.

Here's a corresponding table with on the left the subroutine
name in the subject and on the right the matching name inside our code:

| Name in the subject | In the actual code                 |
|--------------------:|:-----------------------------------|
| convertLetters      | sanitize_message                   |
| mix                 | generate_disk                      |
| createCylinder      | write_cylinder_to_file             |
| loadCylinder        | load_cylinder_from_file            |
| KeyOK               | is_key_valid                       |
| createKey           | generate_key                       |
| find                | find                               |
| shift               | jefferson_shift                    |
| cipherLetter        | cipher_letter                      |
| cipherText          | cipher_message                     |
| displayCylinder     | draw_disk                          |
| displayCylinders    | draw_cylinder                      |
| enterKey            |                                    |
| rotateCylinder      | rotate_disk_from_cylinder_in_place |
| rotateCylinders     | draw_rotation_buttons              |

## Questions

The following sections contains the answers to the questions which are in the
[subject](subject.pdf).

### _Decipher the text_ `GRMYSGBOAAMQGDPEYVWLDFDQQQZXXVMSZFS` _with the cylinder inside the_ [`cylinder-example.txt`](cylinder-example.txt) _file and the key_ `[12, 16, 29, 6, 33, 9, 22, 15, 20, 3, 1, 30, 32, 36, 19, 10, 35, 27, 25, 26, 2, 18, 31, 14, 34, 17, 23, 7, 8, 21, 4, 13, 11, 24, 28, 5]`.
The message is : "The quick brown fox jump over the lazy dog"

### _Encrypt a text of your choice with a cylinder and a key of your choice. Attach them to your project._
If we encrypt the message "Hello world" with the cylinder in the file "cylinder-question.txt" and the key [8, 4, 6, 7, 2, 1, 10, 5, 3, 9]
we got : 'XNUEDNRCHN'

### _What do you think of the security of this algorithm?_
This algorithm is not really secure for short message but the longer your message the more secure it is.
This algorithm was quite secure before computer comming but now it is no more secure enought.

### _What are the main qualities and downsides of this algorithm?_
The qualities are that if you have a message long enought it will be harder de decrypt and this algorithm is quite easy to set up.
The mains downsides are that with a computer it is we can easily devrypt the message without knowing the key, and it is a system with a unique key so someone could intercept it.

### _How many keys there is in a cylinder of_ `n` _disks?_
There is n! key possible because it is a permutation without repetition of n disk.

## LICENSE

This repository is under the Unlicense. See LICENSE file for more
information.  
EXCEPTING the file [`subject.pdf`](subject.pdf) which is licensed to SUPINFO
International University under the terms of the [FreeBSD License].

[FreeBSD License]: https://en.wikipedia.org/wiki/BSD_licenses#2-clause
[Jefferson Disk]: https://en.wikipedia.org/wiki/Jefferson_disk
[@pldiiw]: https://github.com/pldiiw
[@ehrakis]: https://github.com/ehrakis
[PEP-8]: https://www.python.org/dev/peps/pep-0008/
[YAPF]: https://github.com/google/yapf
[Function annotations]: https://www.python.org/dev/peps/pep-3107/
[Mypy]: http://www.mypy-lang.org/
[Isort]: https://github.com/timothycrosley/isort
