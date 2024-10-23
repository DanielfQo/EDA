#include <iostream>

template <typename K, typename V>
class Nodo {
public:
    K clave;
    V valor;
    Nodo* siguiente;
    Nodo* anterior;

    Nodo(K c, V v) : clave(c), valor(v), siguiente(nullptr), anterior(nullptr) {}
};

template <typename K, typename V>
class ListaDobleEnlazada {
private:
    Nodo<K, V>* head;
    Nodo<K, V>* tail;
    int size;

public:
    ListaDobleEnlazada() : head(nullptr), tail(nullptr), size(0) {}

    Nodo<K, V>* insertarNodo(K clave, V valor);
    V* buscarValor(K clave);
    void eliminarNodo(K clave);
    void eliminarNodoDirecto(Nodo<K, V>* nodo);
    void mostrarLista();
    Nodo<K, V>* getHead() { return head; }
    int getSize() { return size; }
};

template <typename K, typename V>
Nodo<K, V>* ListaDobleEnlazada<K, V>::insertarNodo(K clave, V valor) {
    Nodo<K, V>* nuevoNodo = new Nodo<K, V>(clave, valor);
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

template <typename K, typename V>
V* ListaDobleEnlazada<K, V>::buscarValor(K clave) {
    Nodo<K, V>* temp = head;
    while (temp != nullptr) {
        if (temp->clave == clave) {
            return &(temp->valor); 
        }
        temp = temp->siguiente;
    }
    return nullptr;
}

template <typename K, typename V>
void ListaDobleEnlazada<K, V>::eliminarNodo(K clave) {
    Nodo<K, V>* temp = head;
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

template <typename K, typename V>
void ListaDobleEnlazada<K, V>::eliminarNodoDirecto(Nodo<K, V>* nodo) {
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

template <typename K, typename V>
void ListaDobleEnlazada<K, V>::mostrarLista() {
    Nodo<K, V>* temp = head;
    while (temp != nullptr) {
        std::cout << "[" << temp->clave << ": " << temp->valor << "] ";
        temp = temp->siguiente;
    }
    std::cout << std::endl;
}
