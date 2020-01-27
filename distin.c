#include<stdlib.h>
#include<unistd.h>
#include<string.h>
#include<stdio.h>
#include"types.h"


int GetOnlineJudgeTypes(){
				char buf[MAXBUFSIZE];
				getcwd(buf,MAXBUFSIZE);
				char *p;
				p=strstr(buf,"codeforces");
				if(p!=NULL){
								return CODEFORCES;
				}
				p=strstr(buf,"nowcoder");
				if(p!=NULL){
								return NOWCODER;
				}
				return -1;
}
				
