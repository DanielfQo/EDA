# Nombre del compilador
CXX = g++

# Flags del compilador
CXXFLAGS = -Wall -g

# Archivos fuente
SRCS = main.cpp RB-TREE.cpp

# Archivos objeto
OBJS = $(SRCS:.cpp=.o)

# Nombre del ejecutable
TARGET = programa

# Regla por defecto
all: $(TARGET)

# Regla para compilar el ejecutable
$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJS)

# Regla para compilar archivos .cpp a .o
%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Regla para limpiar archivos compilados
clean:
	rm -f $(OBJS) $(TARGET)

# Regla para ejecutar el programa
run: $(TARGET)
	./$(TARGET)