#include <iostream>
#include <random>
#include <ctime>
#include <chrono>
#include "RB-TREE.h"

using namespace std;
using namespace std::chrono;

int main() {
    
    int DATOS = 0;
    int BUSQUEDA = 10000;
    int MAX = 10000;
    cout << "CANT" << " TIEMPO" << endl;

    for (int i = 100; i <= MAX; i += 100) {
        DATOS = i;
        RBTree arbolRB;

        srand(time(0));

        for (int j = 1; j <= DATOS; ++j) {
            arbolRB.insertarValor(j);
        }

        double total_time_used = 0;

        for (int j = 0; j < BUSQUEDA; ++j) {
            int randomValue = rand() % DATOS + 1;

            auto start = high_resolution_clock::now();
            bool found = arbolRB.buscarValor(randomValue);
            auto end = high_resolution_clock::now();

            auto duration = duration_cast<nanoseconds>(end - start).count();
            
            total_time_used += duration;
        }

        // Calculamos el tiempo promedio por búsqueda
        double avg_time_used = total_time_used / BUSQUEDA;

        // Mostramos el tiempo promedio
        cout << i << " " << avg_time_used << endl;
    }

    return 0;
}
