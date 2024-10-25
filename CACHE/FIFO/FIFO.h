#pragma once
#include <iostream>
#include <unordered_map>
#include "ListaEnlazada.h"

template <typename T>
class FIFO {
private:
    ListaEnlazada<T> lista;
    std::unordered_map<T, Node<T>*> cache;

    int maxSize;
public:
    FIFO(int maxSize) : maxSize(maxSize) {}

    void push(T value) {
        if (lista.getSize() == maxSize) {
            cache.erase(lista->getHead()->dato);
            lista.pop();
        }
        cache[value] = lista.push(value);
    }

    void imprimir() {
        lista.imprimir();
    }
};
