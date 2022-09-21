# Logical function minimization

## Project description

Project is dedicated to minimizing logical function rapidly. 
Application can handle obligatory implicant, that must be covered
and supplementary implicants, that do not have to be covered, but
can be used to improve minimization.

## Installation guidelines

Application is developed on programming language Python. In order to
install project download source code. For running application required
Python 3.X version.

## Running guidelines

In order to run project pass file `view.py` to Python interpreter.

## Use cases

```
Enter obligatory implicants:
   0000 0001 0010 1101 1110
Enter supplementary implicants:
   0110 0111 1100
+-----+-----+
|  0  | ___*|
|-0000| 000*|
|  1  | 011*|
|-0001| 110*|
|-0010| __*_|
|  3  | 00*0|
|-1101| 11*0|
|-1110| _*__|
|-0111| 0*10|
|  2  | *___|
|-1100| *110|
|-0110|
+-----+-----+

Core imps
   Imp(110*) Imp(000*)
Reduced imps
   Imp(011*) Imp(00*0) Imp(11*0) Imp(*110) Imp(0*10)
Imps to cover
   Imp(0010) Imp(1110)
Best coverage
   Imp(00*0) Imp(11*0)

```

### Input

Application first will ask for obligatory implicants and then
supplementary implicant. In order to invoke minimization sets,
which function equal one on, should be entered in following format.
Zero stands low level signal as argument and One stands for
high level signal as argument. All implicants should have same length
and be separated by space as shown in example.

> Please do not enter implicants with symbol '*' denoting already
> reduced arguments. This feature is in development and not
> implemented yet.

### Output table

Output table consist of columns. Each column contains implicants,
that have same number of reduced arguments. Columns sorted from left
to right in order of increasing number of reduced arguments. Preceding
minus ‘-’ symbol denotes consumed implicant. Preceding space ‘ ’
denotes prime implicant, that was not consumed by other implicants.
- *Core imps* make up core of function. Core is set of implicant, that
covers original implicants uncoverable by other implicants.
- *Reduced imps* are prime implicants. Implicants listed in *core imps* are
not presents in this list.
- Imps to cover are obligatory implicants not covered by core of function.
- Best coverage is subsequence of *reduced imps*, that provides best coverage
of *imps to cover*.

