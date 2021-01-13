"""
    Example when try to use
"""

import Judge

if __name__ == "__main__":
    print(Judge.judge(
        "696969","C","D:\\TheCodeOfIsla\\A lot Programing After Isla\\Garademi\\TestProblems\\Pattern1" , 
        """
        #include<stdio.h>
        int main(){
            int n;scanf("%d",&n);
            for(int i=0;i<n;i++){
                for(int j=0;j<n;j++)printf("*")
                printf("\n")
            }
            return 0;
        }
        """
    ))
