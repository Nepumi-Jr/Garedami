# Garedami(ガレダミ)

Garademi is auto grading system that use for judging user's source code.

Garedami are from 2 words.

- Gareda(ガレダ) is Grader
- mi(ミ) is stand for ***Miracle***

## Ability
- Compile and run in any programming language.
- Flexible Configurable Problem

## Requirement
- python 3.8
  - yaml
  - json

To use it you have to call function Judge in [judge.py](https://github.com/Nepumi-Jr/Garademi/blob/main/Src/Judge.py) and require 4 arguments.
- idTask (as str)
    ... self-explanatory but we don't use them much.
- proLang (as str)
    is programming language that user what to compile
- problemDir (as str)
    is Directory of that problem.
- src (asstr)
    is source code that user want to judge

## how it's working
After call by [judge.py](https://github.com/Nepumi-Jr/Garademi/blob/main/Src/Judge.py), it will do 4 main Process

1. Gathering problem info
2. Checking src lang with Problem
3. Compile src
4. Run and Judge src

## Configulation
You can config anything you want in Config Folder

If it not found, it will create by itself for first time

Config folder will look like this

```
Config/
├── Langs/
|   ├── C.yaml
|   └── Cpp.yaml
|   ...
├── Grader.yaml
├── ProblemDefault.yaml
└── Verdict.yaml
```
### Langs
in each lang you can config 3 things
- `BIN_FILE`: Path for Binary file
- `BIN_PATH`: Path for Binary Folder
- `TIME_FACTOR`: Time factor for each language (eg. C = 1, Python = 5,Java = 1.5) Because each language have different performance

### Grader
- `COMPILE_TIME`: Compiler time (in ms)
- `JUDGE_TIME`: Judge time (in ms)
- `MAX_DISPLAY`: Max verdict to display. If it over, we will use short form.
- `MAX_TEST_CASE`: self explain

### Default_Problem()
is config for each problem
- `timeLimit`: is Time limit in each testcase (in ms)
- `memLimit`: is Memory limit in each testcase (in md)
- `judging`: is **cmd** for judging in each testcase
- `compiling`: is **cmd** for compile in each *language* 
- `running`: is **cmd** for run in each *language* 

### Verdict
use to convert verdict symbol to Full form.For example
- `P`: Pass
- `-`: Wrong answer
- `T`: Time Limit Exceed

...

- `?`: use for unknown verdict symbol

## Problem or Task
In this Garademi you can make a lot of thing in one problem.
So I will show example *Basic problem* to ***FULL** custom problem*

### Basic Problem (No Custom Judge)
It just use for compare between src output and solution in each test-case. Here is stucture for Basic Problem.
```
SomeProblem/
├── CompileSpace
|   |-- Custom_Header...
|   └── Src_Program
|   
├── 1.in
├── 1.sol
├── 2.in
├── 2.sol
├── ...
├── 10.sol
└── Config.yaml (Not require but better than noting)
```
Every time when you use grader.User's src will go in `CompileSpace\Src_Program` and run it.

It will use input from `?.in` and check output with `?.sol`.In each `?.in` and `?.sol` we call it `Testcase`.You can have any `Testcase` Number that you want.(But not over than `MAX_TEST_CASE` in `Config\Grader`)

### Fully Customed Problem.
In Basic Problem you must output **exactly** as `?.sol`.But some problem you there are **more than one** answer.You can use Custom Judge by config them in `Config.yaml`.You can look example from `StandardJudge\StdJudge` which just use in Basic Problem.
```
SomeProblem/
├── Shadow
|   └── Original Header
├── CompileSpace (will copy from Shadow)
|   |-- Custom_Header...
|   └── Src_Program
|   
├── 1.in
├── 1.sol
├── 2.in
├── 2.sol
├── ...
├── 10.sol
├── Custom_Judge
└── Config.yaml 
```
>It's not different from Basic Problem

But you can custom in `Config.yaml` and `Custom_Judge`

## TODO
- Test in Linux os
- Supporting a custom compare in Otog.org
- Error Handling
- more Path access

- or maybe more.
