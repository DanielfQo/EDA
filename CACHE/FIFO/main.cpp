#include<iostream>
#include"FIFO.h"

int main(){
    FIFO<int> cache(3);

    cache.push(1);
    cache.push(2);
    cache.push(3);

    cache.imprimir();

    cache.push(4);
    cache.push(5);
    cache.push(6);

    cache.imprimir();
}