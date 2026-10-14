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
    float r, l, b, h;

    cout << "Enter radius of circle: ";
    cin >> r;

    cout << "Area of Circle: " << AREA(r) << endl;

    cout << "\nEnter length and breadth of rectangle: ";
    cin >> l >> b;

    cout << "Area of Rectangle: " << AREA(l, b) << endl;

    cout << "\nEnter base and height of triangle: ";
    cin >> b >> h;

    cout << "Area of Triangle: " << AREA(b, h, 0) << endl;

    return 0;
}