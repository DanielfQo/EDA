#pragma once
#include <iostream>
#include "ListaEnlazada.h"

template <typename T>
class FIFO {
private:
    ListaEnlazada<T> lista;
    int maxSize;
public:
    FIFO(int maxSize) : maxSize(maxSize) {}

    void push(T value) {
        if (lista.getSize() == maxSize) {
            lista.pop();
        }
        lista.push(value);
    }

    void imprimir() {
        lista.imprimir();
    }
};
