#include <iostream>
#include <random>
#include <ctime>
#include <chrono>
#include "RB-TREE.h"

using namespace std;
using namespace std::chrono;

int main() {
    
    int DATOS = 0;
    int BUSQUEDA = 100000;
    int MAX = 10000;
    cout << "CANT" << " TIEMPO" << endl;

    for (int i = 100; i <= MAX; i += 100) {
        DATOS = i;
        RBTree arbolRB;

        srand(time(0));

        for (int j = 1; j <= DATOS; ++j) {
            arbolRB.insertarValor(j);
        }

        float total_comparaciones = 0;

        for (int j = 0; j < BUSQUEDA; ++j) {
            int randomValue = rand() % DATOS + 1;
            
            total_comparaciones += arbolRB.buscarValor(randomValue);

        }

        float avg_total_comparaciones = total_comparaciones / BUSQUEDA;

        cout << i << " " << avg_total_comparaciones << endl;
    }

    return 0;
}
