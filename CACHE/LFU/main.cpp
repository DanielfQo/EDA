#include<iostream>
#include"LFU.h"

using namespace std;

int main() {

    LFU<int> cache(3);

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

    return 0;
}