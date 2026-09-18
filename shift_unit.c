#include <stdio.h>
#include <string.h>
#include <assert.h>
#include <stdlib.h>
#define WORDS 96
static unsigned long long src[WORDS], dst[WORDS], chk[WORDS];
static void shift_into(unsigned long long *dst, const unsigned long long *src, int sh) {
    int w = sh >> 6, b = sh & 63;
    memset(dst, 0, sizeof(unsigned long long)*WORDS);
    for (int i = w; i < WORDS; i++) {
        unsigned long long v = src[i - w] << b;
        if (b && i - w - 1 >= 0) v |= src[i - w - 1] >> (64 - b);
        dst[i] = v;
    }
}
static int get(unsigned long long*A,int i){return (A[i>>6]>>(i&63))&1ULL;}
static void set(unsigned long long*A,int i){A[i>>6]|=1ULL<<(i&63);}
int main(){
    int bad=0;
    for (int trial=0; trial<200; trial++){
        memset(src,0,sizeof src); memset(chk,0,sizeof chk);
        for(int k=0;k<40;k++){ int p=rand()%3000; set(src,p); set(chk,p); }
        for (int sh=1; sh<=600; sh++){
            shift_into(dst,src,sh);
            /* reference: for each set bit p, expect bit p+sh */
            for (int p=0;p<6000-sh;p++) if (get(src,p)) set(chk,p); /* rebuild */
        }
        /* do it properly: reference for one sh */
        for (int sh=1; sh<=600; sh++){
            memset(chk,0,sizeof chk);
            for (int p=0;p<6000;p++) if (get(src,p)) { int q=p+sh; if(q<6144) set(chk,q); }
            shift_into(dst,src,sh);
            for (int i=0;i<WORDS;i++) if (dst[i]!=chk[i]) { printf("MISMATCH sh=%d word=%d\n",sh,i); bad++; if(bad>3) return 1; break; }
        }
    }
    printf(bad? "FAILURES: %d\n":"shift_into verified on random sets, shifts 1..600\n", bad);
    return 0;
}
