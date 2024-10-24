#pragma once

#include <iostream>
#include <cmath>
#include <vector> 
#include <stdexcept>

template <typename T>
struct Nodo {
    T clave;
    int frecuencia;
    int grado;
    Nodo* padre;
    Nodo* hijo;
    Nodo* izquierda;
    Nodo* derecha;
    bool marca;

    Nodo(T valor) : clave(valor), frecuencia(1), grado(0), padre(nullptr), hijo(nullptr), izquierda(this), derecha(this), marca(false) {}
};

template <typename T>
class FibonacciHeap {
private:
    Nodo<T>* minimo;
    int n;

    void unir(Nodo<T>* y, Nodo<T>* x) {
        y->izquierda->derecha = y->derecha;
        y->derecha->izquierda = y->izquierda;
        y->padre = x;
        if (x->hijo == nullptr) {
            x->hijo = y;
            y->derecha = y;
            y->izquierda = y;
        } else {
            y->izquierda = x->hijo;
            y->derecha = x->hijo->derecha;
            x->hijo->derecha = y;
            y->derecha->izquierda = y;
        }
        x->grado++;
        y->marca = false;
    }

    void consolidar() {
        int D = std::log2(n) + 1;
        std::vector<Nodo<T>*> A(D, nullptr);

        std::vector<Nodo<T>*> listaRaices;
        Nodo<T>* x = minimo;
        if (x != nullptr) {
            do {
                listaRaices.push_back(x);
                x = x->derecha;
            } while (x != minimo);
        }

        for (Nodo<T>* w : listaRaices) {
            x = w;
            int d = x->grado;
            while (A[d] != nullptr) {
                Nodo<T>* y = A[d];
                if (x->frecuencia > y->frecuencia) std::swap(x, y);
                unir(y, x);
                A[d] = nullptr;
                d++;
            }
            A[d] = x;
        }

        minimo = nullptr;
        for (Nodo<T>* y : A) {
            if (y != nullptr) {
                if (minimo == nullptr) {
                    minimo = y;
                    minimo->izquierda = minimo;
                    minimo->derecha = minimo;
                } else {
                    y->izquierda = minimo;
                    y->derecha = minimo->derecha;
                    minimo->derecha->izquierda = y;
                    minimo->derecha = y;
                    if (y->clave < minimo->clave) minimo = y;
                }
            }
        }
    }

public:
    FibonacciHeap() : minimo(nullptr), n(0) {}


    int getSize() {
        return n;
    }

    Nodo<T>* insertar(T clave) {
        Nodo<T>* nodo = new Nodo<T>(clave);
        if (minimo == nullptr) {
            minimo = nodo;
        } else {
            nodo->izquierda = minimo;
            nodo->derecha = minimo->derecha;
            minimo->derecha->izquierda = nodo;
            minimo->derecha = nodo;
            if (clave < minimo->frecuencia) minimo = nodo;
        }
        n++;
        return nodo;
    }

    void aumentarFrecuencia(Nodo<T>* nodo) {
        if (nodo == nullptr) throw std::runtime_error("Nodo no válido");
        
        nodo->frecuencia++;

        if (nodo->frecuencia > minimo->frecuencia) {
            if (nodo->padre != nullptr) {
                if (nodo->padre->hijo == nodo) {
                    nodo->padre->hijo = (nodo->derecha == nodo) ? nullptr : nodo->derecha; 
                }
                nodo->izquierda->derecha = nodo->derecha;
                nodo->derecha->izquierda = nodo->izquierda;
                nodo->padre = nullptr;
            }
            nodo->izquierda = minimo;
            nodo->derecha = minimo->derecha;
            minimo->derecha->izquierda = nodo;
            minimo->derecha = nodo;

            if (nodo->frecuencia > minimo->frecuencia) {
                minimo = nodo;
            }
        }
    }

    T obtenerMin() {
        if (minimo == nullptr) throw std::runtime_error("Heap vacío");
        return minimo->clave;
    }

    T extraerMin() {
        if (minimo == nullptr) throw std::runtime_error("Heap vacío");
        Nodo<T>* z = minimo;
        if (z != nullptr) {
            if (z->hijo != nullptr) {
                Nodo<T>* x = z->hijo;
                do {
                    Nodo<T>* siguiente = x->derecha;
                    x->izquierda = minimo;
                    x->derecha = minimo->derecha;
                    minimo->derecha->izquierda = x;
                    minimo->derecha = x;
                    x->padre = nullptr;
                    x = siguiente;
                } while (x != z->hijo);
            }
            z->izquierda->derecha = z->derecha;
            z->derecha->izquierda = z->izquierda;
            if (z == z->derecha) {
                minimo = nullptr;
            } else {
                minimo = z->derecha;
                consolidar();
            }
            n--;
        }
        T claveMinima = z->clave;
        delete z;
        return claveMinima;
    }

    bool estaVacio() {
        return minimo == nullptr;
    }
};


