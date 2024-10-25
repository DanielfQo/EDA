#pragma once
#include <iostream>

template <typename T>
class Node {
public:
    T dato;
    Node* next;

    Node(T dato) : dato(dato), next(nullptr) {}
};

template <typename T>
class ListaEnlazada {
private:
    Node<T>* head;
    Node<T>* tail;
    int size;

public:
    ListaEnlazada() : head(nullptr), tail(nullptr), size(0) {}

    ~ListaEnlazada() {
        while (head != nullptr) {
            Node<T>* temp = head;
            head = head->next;
            delete temp;
        }
    }

    int getSize() const {
        return size;
    }

    Node<T>* push(T value) {
        Node<T>* newNode = new Node<T>(value);
        if (tail != nullptr) {
            tail->next = newNode;
        }
        tail = newNode;
        if (head == nullptr) {
            head = newNode;
        }
        size++;
        return newNode;
    }

    void pop() {
        if (head != nullptr) {
            Node<T>* temp = head;
            head = head->next;
            delete temp;
            if (head == nullptr) {
                tail = nullptr;
            }
        }
        size--;
    }

    void imprimir() {
        Node<T>* temp = head;
        while (temp != nullptr) {
            std::cout << temp->dato << " ";
            temp = temp->next;
        }
        std::cout << std::endl;
    }

    Node<T>* getHead() const {
        return head;
    }

    Node<T>* getTail() const {
        return tail;
    }
};