#ifndef RED_BLACK_TREE_RBTREE_H
#define RED_BLACK_TREE_RBTREE_H


using namespace std;

class Nodo{
    public:
        int dato;
        Nodo *padre;
        Nodo *izq;
        Nodo *der;
        bool color; // 1 = rojo , 0 = negro

        Nodo(int dato);
};

class RBTree{

    private:
    Nodo* root;
    protected:

    void insertarFixup(Nodo* z);
    void rotarIzquierda(Nodo* x);
    void rotarDerecha(Nodo* x);

    public:

    RBTree();
    Nodo* getRoot();
    void insertarValor(int dato);
    void eliminarValor(int dato);
    bool buscarValor(int dato);
    void imprimirArbol(Nodo* nodo, int nivel = 0);
};

#endif //RED_BLACK_TREE_RBTREE_H