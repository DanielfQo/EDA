#include <iostream>
#include <unordered_map>
#include "ListaDobleEnlazada.h"

template <typename K, typename V>
class LRU{
private:

    int maxSize;
    std::unordered_map<K, Nodo<K,V>*> cache;

    ListaDobleEnlazada<K,V> lista;

public:

    LRU(int maxSize) : maxSize(maxSize) {}

    void insertar(K clave, V valor){

        if(cache.find(clave) != cache.end()){
            lista.eliminarNodoDirecto(cache[clave]);
            cache.erase(clave);     
        }        

        if(lista.getSize() == maxSize){
            K clave_a_eliminar = lista.getHead()->clave; 
            lista.eliminarNodoDirecto(cache[clave_a_eliminar]);
            cache.erase(clave_a_eliminar);
        }


        Nodo<K,V>* nodo = lista.insertarNodo(clave, valor);
        cache[clave] = nodo;
    }

    void mostrarCache(){
        lista.mostrarLista();
    }



};