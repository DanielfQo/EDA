#include "RB-TREE.h"
#include<iostream>
#include <iomanip>

Nodo::Nodo(int dato){
    this->dato = dato;
    this->padre = nullptr;
    this->izq = nullptr;
    this->der = nullptr;
    this->color = 1;
}

RBTree::RBTree(){
    this->root = nullptr;
}

Nodo* RBTree::getRoot(){
    return this->root;
}

void RBTree::rotarDerecha(Nodo* x) {
    Nodo* y = x->izq;
    x->izq = y->der; 
    if (y->der != nullptr)
        y->der->padre = x;  
    y->padre = x->padre;   
    if (x->padre == nullptr)
        this->root = y;    
    else if (x == x->padre->der)
        x->padre->der = y;  
    else x->padre->izq = y;  
    y->der = x;             
    x->padre = y;           
}


void RBTree::rotarIzquierda(Nodo* x){
    Nodo* y = x->der;
    x->der = y->izq;
    if(y->izq != nullptr)
        y->izq->padre = x;
    y->padre = x->padre;
    if(x->padre == nullptr)
        this->root = y;
    else if(x == x->padre->izq)
        x->padre->izq = y;
    else x->padre->der = y;
    y->izq = x;
    x->padre = y;

}

void RBTree::insertarFixup(Nodo* z) {
    while (z->padre != nullptr && z->padre->color == 1) {
        if (z->padre == z->padre->padre->izq) {
            Nodo* y = z->padre->padre->der; 

            
            if (y != nullptr && y->color == 1) {
                z->padre->color = 0;          
                y->color = 0;                 
                z->padre->padre->color = 1;   
                z = z->padre->padre;          
            } else {
                
                if (z == z->padre->der) {
                    z = z->padre;
                    rotarIzquierda(z);
                }

                z->padre->color = 0;       
                z->padre->padre->color = 1; 
                rotarDerecha(z->padre->padre); 
            }
        } else {
            Nodo* y = z->padre->padre->izq; 

            if (y != nullptr && y->color == 1) {
                z->padre->color = 0;
                y->color = 0;
                z->padre->padre->color = 1;
                z = z->padre->padre;
            } else {
                if (z == z->padre->izq) {
                    z = z->padre;
                    rotarDerecha(z);
                }
                z->padre->color = 0;
                z->padre->padre->color = 1;
                rotarIzquierda(z->padre->padre);
            }
        }
    }

    this->root->color = 0;
}

void RBTree::insertarValor(int dato){
    Nodo* z = new Nodo(dato);

    Nodo* x = this->root;
    Nodo* y = nullptr;

    while(x != nullptr){
        y = x;
        if(dato < x->dato)
            x = x->izq;
        else
            x = x->der;
    }

    z->padre = y;

    if(y == nullptr)
        this->root = z;
    else if(dato < y->dato)
        y->izq = z;
    else
        y->der = z;
    
    z->izq = nullptr;
    z->der = nullptr;
    z->color = 1;

    this->insertarFixup(z);
}

int RBTree::buscarValor(int dato){
    Nodo* x = this->root;
    int comparaciones = 0;
    while(x != nullptr && x->dato != dato){
        if(dato < x->dato)
            x = x->izq;
        else
            x = x->der;
        comparaciones++;
    }

    return comparaciones;
}

void RBTree::imprimirArbol(Nodo* nodo, int nivel) {
    if (nodo != nullptr) {
        imprimirArbol(nodo->der, nivel + 1);

        cout << setw(4 * nivel) << "";
        cout << nodo->dato << (nodo->color == 1 ? " [R]" : " [N]") << endl;
        imprimirArbol(nodo->izq, nivel + 1);
    }
}