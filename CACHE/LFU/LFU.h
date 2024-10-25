#pragma once

#include <iostream>
#include <unordered_map>
#include "Heap.h"

template <typename T>
class LFU {
private:
    std::unordered_map<T, Nodo<T>*> cache;
    FibonacciHeap<T> heap;
    int maxSize;

public:
    LFU(int maxSize) : maxSize(maxSize) {} 

    void insertar(T clave) {   
        
        if (cache.find(clave) == cache.end()) {
            if(maxSize == heap.getSize()) {
                T claveEliminar = heap.extraerMin();
                cache.erase(claveEliminar);
            }
            Nodo<T>* nodo = heap.insertar(clave);
            cache[clave] = nodo;
        } else {
            Nodo<T>* nodo = cache[clave];
            int frecuencia = nodo->frecuencia + 1;
            heap.eliminarNodo(nodo);
            cache[clave] = heap.insertarConFrecuencia(clave,frecuencia);
        }
    }

    T obtenerMenosFrecuente() {
        return heap.obtenerMin();
    }

    T extraerMenosFrecuente() {
        T clave = heap.extraerMin();
        cache.erase(clave);
        return clave;
    }

    void mostrarCache() {
        for (const auto& pair : cache) {
            std::cout << "Clave: " << pair.first << ", Frecuencia: " << pair.second->frecuencia << std::endl;
        }
        std::cout << std::endl;
    }
};
