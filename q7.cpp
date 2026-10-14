#include <iostream>
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

// Area of triangle
float AREA(float b, float h, int t)
{
    return 0.5 * b * h;
}

int main()
{
    int choice;
    float r, l, b, h;

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
                cout << "Enter base and height: ";
                cin >> b >> h;
                cout << "Area of Triangle: "
                     << AREA(b, h, 0) << endl;
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