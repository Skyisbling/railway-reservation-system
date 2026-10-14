#include <iostream>
#include <cmath>
using namespace std;

// Area of circle
float AREA(float r)
{
    return 3.14 * r * r;
}

// Area of rectangle
float AREA(float l, float b)
{
    return l * b;
}

// Area of triangle using Heron's formula
float AREA(float a, float b, float c)
{
    float s = (a + b + c) / 2;
    return sqrt(s * (s - a) * (s - b) * (s - c));
}

int main()
{
    int choice;
    float r, l, b, a, c;

    do
    {
        cout << "\n===== AREA MENU =====\n";
        cout << "1. Circle\n";
        cout << "2. Rectangle\n";
        cout << "3. Triangle\n";
        cout << "4. Exit\n";
        cout << "Enter your choice: ";
        cin >> choice;

        switch (choice)
        {
            case 1:
                cout << "Enter radius: ";
                cin >> r;
                cout << "Area of Circle: " << AREA(r) << endl;
                break;

            case 2:
                cout << "Enter length and breadth: ";
                cin >> l >> b;
                cout << "Area of Rectangle: "
                     << AREA(l, b) << endl;
                break;

            case 3:
                cout << "Enter three sides of triangle: ";
                cin >> a >> b >> c;

                if (a + b > c && a + c > b && b + c > a)
                    cout << "Area of Triangle: "
                         << AREA(a, b, c) << endl;
                else
                    cout << "Invalid triangle sides!\n";
                break;

            case 4:
                cout << "Exiting program...\n";
                break;

            default:
                cout << "Invalid choice!\n";
        }

    } while (choice != 4);

    return 0;
}