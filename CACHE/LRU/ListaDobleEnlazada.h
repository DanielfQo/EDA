#pragma once

#include <iostream>

template <typename K>
class Nodo {
public:
    K clave;
    Nodo* siguiente;
    Nodo* anterior;

    Nodo(K c) : clave(c), siguiente(nullptr), anterior(nullptr) {}
};

template <typename K>
class ListaDobleEnlazada {
private:
    Nodo<K>* head;
    Nodo<K>* tail;
    int size;

public:
    ListaDobleEnlazada() : head(nullptr), tail(nullptr), size(0) {}

    Nodo<K>* insertarNodo(K clave);
    void eliminarNodo(K clave);
    void eliminarNodoDirecto(Nodo<K>* nodo);
    void mostrarLista();
    Nodo<K>* getHead() { return head; }
    int getSize() { return size; }
};

template <typename K>
Nodo<K>* ListaDobleEnlazada<K>::insertarNodo(K clave) {
    Nodo<K>* nuevoNodo = new Nodo<K>(clave);
    if (head == nullptr) {
        head = tail = nuevoNodo;
    } else {
        tail->siguiente = nuevoNodo;
        nuevoNodo->anterior = tail;
        tail = nuevoNodo;
    }
    size++;
    return nuevoNodo;
}


template <typename K>
void ListaDobleEnlazada<K>::eliminarNodo(K clave) {
    Nodo<K>* temp = head;
    while (temp != nullptr) {
        if (temp->clave == clave) {
            if (temp->anterior != nullptr) {
                temp->anterior->siguiente = temp->siguiente;
            } else {
                head = temp->siguiente;
            }
            if (temp->siguiente != nullptr) {
                temp->siguiente->anterior = temp->anterior;
            } else {
                tail = temp->anterior;
            }
            delete temp;
            size--;
            return;
        }
        temp = temp->siguiente;
    }
    
}

template <typename K>
void ListaDobleEnlazada<K>::eliminarNodoDirecto(Nodo<K>* nodo) {
    if (nodo->anterior != nullptr) {
        nodo->anterior->siguiente = nodo->siguiente;
    } else {
        head = nodo->siguiente;
    }
    if (nodo->siguiente != nullptr) {
        nodo->siguiente->anterior = nodo->anterior;
    } else {
        tail = nodo->anterior;
    }
    delete nodo;
    size--;
}

template <typename K>
void ListaDobleEnlazada<K>::mostrarLista() {
    Nodo<K>* temp = head;
    while (temp != nullptr) {
        std::cout << "[" << temp->clave << "] ";
        temp = temp->siguiente;
    }
    std::cout << std::endl;
}
