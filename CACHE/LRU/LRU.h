#pragma once

#include <iostream>
#include <unordered_map>
#include "ListaDobleEnlazada.h"

template <typename K>
class LRU{
private:

    int maxSize;
    std::unordered_map<K, Nodo<K>*> cache;

    ListaDobleEnlazada<K> lista;

public:

    LRU(int maxSize) : maxSize(maxSize) {}

    void insertar(K clave){

        if(cache.find(clave) != cache.end()){
            lista.eliminarNodoDirecto(cache[clave]);
            cache.erase(clave);     
        }        

        if(lista.getSize() == maxSize){
            K clave_a_eliminar = lista.getHead()->clave; 
            lista.eliminarNodoDirecto(cache[clave_a_eliminar]);
            cache.erase(clave_a_eliminar);
        }


        Nodo<K>* nodo = lista.insertarNodo(clave);
        cache[clave] = nodo;
    }

    void mostrarCache(){
        lista.mostrarLista();
    }



};