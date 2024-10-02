#include<iostream>
#include "RB-TREE.h"

using namespace std;

int main(){
    RBTree arbol;

    arbol.insertarValor(10);
    arbol.insertarValor(20);
    arbol.insertarValor(30);
    arbol.insertarValor(15);
    arbol.insertarValor(25);
    arbol.insertarValor(35);
    arbol.insertarValor(40);
    arbol.insertarValor(50);
    arbol.insertarValor(60);
    arbol.insertarValor(70);

    arbol.imprimirArbol(arbol.getRoot());
}