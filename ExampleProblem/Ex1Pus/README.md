# Ex1Plus
This is the simplest of all problem type

# Problem
In this problem user must write a program that get `A` and `B` and display the sum of `A` and `B`

```
#input
    The first line contain integer number A (1 ≤ A ≤ 1000)
    The second line contain integer number B (1 ≤ A ≤ 1000)
#output
    print the result of A+B
```


# What to do
Just create file `1.in` `1.sol` , `2.in` `2.sol`...(depend on how many testcase that you want)

example `1.in` is
```
823
78

```
`1.sol` is
```
901
```

In this problem type, Grader will judge by using `?.in` as input and compare between `user program's output` and `?.sol`

TIP : when it compare it will ignore `white spaces` and `new lines`

# Example

## Here are code examples that will pass this problem

```c
#include<stdio.h>

int main(){
    int a;scanf("%d",&a);

    int b;scanf("%d",&b);
    int c=a+b;
    printf("%d",c);
}
```

```py
a = int(input())
b = int(input())
c = a+b
print(c)
```

```java
import java.util.Scanner;
public class AplusB {
    public static void main(String[] args) {
    Scanner kb = new Scanner(System.in);
        int a = kb.nextInt();
        int b = kb.nextInt();
        int c = a+b;
        System.out.println(c);
    }
}
```

## Here is the code that not pass

```c
#include<stdio.h>
int main(){
    int a;
    printf("a:");
    scanf("%d",&a);

    int b;
    printf("b:");
    scanf("%d",&b);

    int c=a+b;
    printf("%d",c);
}
```