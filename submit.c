#include<stdio.h>
#include<unistd.h>
#include<stdlib.h>
#include<string.h>
#include"types.h"
#include"distin.c"

int main(){
				int type=GetOnlineJudgeTypes();
				switch(type){
					case CODEFORCES:
						execl("/home/mysakure/.local/bin/cf","cf","submit",NULL);
						break;
			    case NOWCODER:
				  	execl("/home/mysakure/.local/bin/now","now","submit",NULL);
						break;
					default:
						printf("error\n");
				}
				return 0;
}
