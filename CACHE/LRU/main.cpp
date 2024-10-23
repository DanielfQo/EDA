#include "LRU.h"

using namespace std;

int main(){

    LRU<char, int> cache(4);
    cache.insertar('c', 9);
    cache.mostrarCache();
    cache.insertar('a', 8);
    cache.mostrarCache();
    cache.insertar('d', 3);
    cache.mostrarCache();
    cache.insertar('b', 2);
    cache.mostrarCache();
    cache.insertar('e', 7);
    cache.mostrarCache();
    cache.insertar('b', 10);
    cache.mostrarCache();
    cache.insertar('a', 11);
    cache.mostrarCache();
    cache.insertar('b', 12);
    cache.mostrarCache();
    cache.insertar('c', 15);
    cache.mostrarCache();
    cache.insertar('d', 1);
    cache.mostrarCache();



}