#include<iostream>
#include<random>
#include<ctime>
#include"RB-TREE.h"

using namespace std;

int main(){
    RBTree arbolRB;

    srand(time(0));

    for (int i = 1; i <= 100000; ++i) {
        arbolRB.insertarValor(i);
    }

    clock_t start, end;
    double total_time_used = 0;

    // Realizamos 10000 búsquedas
    for (int i = 0; i < 10000; ++i) {
        int randomValue = rand() % 10000 + 1;

        start = clock();
        bool found = arbolRB.buscarValor(randomValue);
        end = clock();

        total_time_used += ((double) (end - start)) / CLOCKS_PER_SEC;
    }

    // Calculamos el tiempo promedio por búsqueda
    double avg_time_used = total_time_used / 10000;

    // Mostramos el tiempo promedio
    cout << "Tiempo promedio de búsqueda: " << avg_time_used << " segundos" << endl;

    return 0;
}
