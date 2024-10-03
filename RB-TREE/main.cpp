#include<iostream>
#include<random>
#include<ctime>
#include"RB-TREE.h"

using namespace std;

int main(){
    RBTree arbolRB;

    srand(time(0));

    for (int n = 10; n <= 10000; n += 10) {
        double total_time = 0.0;

        for (int j = 0; j < 100; ++j) {
            // Clear the tree for each iteration
            arbolRB = RBTree();

            // Insert n random values
            for (int i = 0; i < n; ++i) {
                int valor = rand() % 100 + 1; 
                arbolRB.insertarValor(valor);
            }

            // Measure the time taken to search for the value 50
            clock_t start = clock();
            arbolRB.buscarValor(50);
            clock_t end = clock();

            total_time += double(end - start) / CLOCKS_PER_SEC * 1000;
        }

        double average_time = total_time / 100;
        cout << "Average time taken to search in tree with " << n << " elements: " << average_time << " milliseconds" << endl;
    }

    cout << arbolRB.buscarValor(50) << endl;
}