#include<iostream>
#include"LFU.h"

using namespace std;

int main() {
    LFU<int> cache(4);
    cache.insertar(1);
    cache.insertar(1);
    cache.insertar(1);
    cache.insertar(1);
    cache.insertar(1);
    cache.insertar(1);
    cache.mostrarCache();
    cache.insertar(2);
    cache.insertar(2);
    cache.insertar(2);
    cache.insertar(2);
    cache.insertar(2);
    cache.mostrarCache();
    cache.insertar(3);
    cache.insertar(3);
    cache.insertar(3);
    cache.mostrarCache();
    cache.insertar(4);
    cache.insertar(4);
    cache.insertar(4);
    cache.insertar(4);
    cache.mostrarCache();
    cache.insertar(5);
    cache.mostrarCache();
    cache.insertar(6);
    cache.mostrarCache();
    cache.insertar(7);
    cache.mostrarCache();
    cache.insertar(8);
    cache.mostrarCache();

    //1 1 1 2 3 4 5 6


    return 0;
}