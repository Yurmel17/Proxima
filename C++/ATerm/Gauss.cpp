#include <iostream>
#include <math.h>
#include <windows.h>
#include <iomanip>
#include <string>

using namespace std;

void mostrar(long double x[][10], int cx, int lx, string prompt = "Resultado: "){ //Esta es una funcion que muestra matrices, por ahora puede ser ignorada

    cout << endl << endl << prompt << endl;
    for (int i = 1; i <= lx; ++i) {
		for (int j = 1; j <= cx; ++j) {
			cout << right << setw(2) << "| "
				<< right << setw(9) << x[i][j] << " |";
		}

		cout <<  endl;
    }

    for (int n = 1; n <= cx; ++n) {

			cout << "---------";
		}
		cout << endl;
    
}
int main(){

    long double x[10][10], di, nm, t[10];
    int lx, cx, cc;
    bool found;

    cout << "Inserte la cantidad de filas de su matriz x: ";
	cin >> lx;
	cout << "Inserte la cantidad de columnas de su matriz x: ";
	cin >> cx;

    cx = cx + 1; // Esto añade una columna, que sera la que almacena las constantes

	for (int i = 1; i <= lx; i++) { //Pide que se inserte la matriz
        cc = 0;
		for (int j = 1; j <= cx; j++) {
            
            if(j != cx){
                cout << "Inserte la variable en [" << i << "][" << j << "] : ";
                cin >> x[i][j];
            }
            else{
                cout << "Inserte la solucion en la coordenada [" << i << "][" << j << "] : ";
                cin >> x[i][j];
            }

		}
	}

	mostrar(x, cx , lx , "Su matriz es: "); // Muestra el sistema de ecuaciones insertado

    if(lx > cx){ //Verifica si hay mas variables que constantes, si es asi, la matriz tiene infinitas soluciones
        cout << "La matriz tiene soluciones infinitas" << endl;
        system("pause");
        return 0;
    }
//WIP
    cc = 1; //Columna clave, columna en que debe aparecer un 1 en la matriz en funcion de la fila analizada

    for(int i = 1; i <= lx;++i ){
        
        if(cc == i && x[i][cc] == 0){ //Trata de arreglar las cosas si la variable que debe ser 1 es 0

            found = false;

            if(i < lx){ // Verifica si la fila con el 0 es la ultima, si no, busca filas para intercambiar
                for( int j = i + 1; j <= lx; ++j){

                    if(x[j][cc] > 0){
                        for(int k = 1; k <= cx; ++k){

                            t[k] = x[i][k];
                            x[i][k] = x[j][k];
                            x[j][k] = t[k];
                        }
                    found = true;
                    }
                }
            }

            if(found == false){  //Si no encuentra una fila sin 0 o esta en la ultima fila, o no hay soluciones o hay infinitas
                cout << "Problema encontrado en la fila " << i << endl;
                cout << "La matriz o tiene soluciones infinitas, o no tiene, verificando . . ." << endl;

                if(x[lx][cx] != 0){ //Busca si existe una inconsistencia, si es asi, no existen soluciones
                    cout << "El sistema no tiene soluciones! " << endl;
                }

                else{ //De lo contrario, hay infinitas soluciones
                    cout << "El sistema tiene infinitas soluciones!" << endl;
                }
                system("pause");
                return 0;
            }
        }

        if(cc == i && x[i][cc] != 1){ // Verifico si la coordenada es 1, si no lo es, multiplico toda la fila por su inversa

            di = 1/x[i][cc]; //Inversa del punto de la matriz que debe convertirse en 1

            for(int j = 1; j <= cx; ++j){

                x[i][j] = x[i][j] * di; //Se multiplica toda la fila por esta inversa

            }
   
        }

        for (int n = 1;n <= lx; ++n ){ // Ahora reduzco el resto de elementos de la columna a 0 para obtener la forma escalonada completa

            if(n != i){
                nm = x[i][cc] * x[n][cc] * -1; //numero hecho para reducir el resto de elementos de la columna a 0

                for(int c = 1; c <= cx; ++c){
                    x[n][c] = (x[i][c] * nm) + x[n][c]; //nm veces la fila fi + la fila fn
                }             
            }
        }
    cc += 1; //Pasa a la siguiente columna clave, en resumen, hace que los 1 esten en diagonal, 
             //creando una matriz identidad con las constantes a la derecha

    string paso = string("Paso numero ") + to_string(i); //Muestra la matriz con la fila i despejada

    mostrar(x, cx, lx , paso);
    cout << endl;
    }


    mostrar(x, cx, lx); //Muestra la matriz resultado

    system("pause");
    return 0;
}