#include <iostream>
#include <string>
using namespace std;

// Простая структура для хранения информации о студенте
struct Student {
    string name;
    int age;
    float averageGrade;
};

// Функция для вывода информации о студенте
void printStudentInfo(Student s) {
    cout << "Имя: " << s.name << endl;
    cout << "Возраст: " << s.age << " лет" << endl;
    cout << "Средний балл: " << s.averageGrade << endl;
    cout << "-------------------" << endl;
}

// Функция для проверки успеваемости
string checkPerformance(float grade) {
    if (grade >= 4.5) {
        return "Отличник";
    } else if (grade >= 3.5) {
        return "Хорошист";
    } else if (grade >= 2.5) {
        return "Троечник";
    } else {
        return "Неуспевающий";
    }
}



// Функция для вычисления факториала
int factorial(int n) {
    int result = 1;
    for (int i = 1; i <= n; i++) {
        result = result * i;
    }
    return result;
}

// Функция для работы с массивом
void processArray() {
    const int SIZE = 5;
    int numbers[SIZE];

    cout << "Введите " << SIZE << " чисел:" << endl;
    for (int i = 0; i < SIZE; i++) {
        cout << "Число " << (i + 1) << ": ";
        cin >> numbers[i];
    }

    int sum = 0;
    int max = numbers[0];
    int min = numbers[0];

    for (int i = 0; i < SIZE; i++) {
        sum += numbers[i];
        if (numbers[i] > max) {
            max = numbers[i];
        }
        if (numbers[i] < min) {
            min = numbers[i];
        }
    }

    cout << "Сумма элементов: " << sum << endl;
    cout << "Максимальный элемент: " << max << endl;
    cout << "Минимальный элемент: " << min << endl;
    cout << "Среднее значение: " << (float)sum / SIZE << endl;
}

int main() {
    cout << "=== ПРОГРАММА ДЛЯ УПРАВЛЕНИЯ СТУДЕНТАМИ ===" << endl;
    cout << endl;

    // Работа с переменными разных типов
    int num1, num2;
    cout << "Введите первое число: ";
    cin >> num1;
    cout << "Введите второе число: ";
    cin >> num2;

    cout << "Результаты операций:" << endl;
    cout << num1 << " + " << num2 << " = " << (num1 + num2) << endl;
    cout << num1 << " - " << num2 << " = " << (num1 - num2) << endl;
    cout << num1 << " * " << num2 << " = " << (num1 * num2) << endl;

    if (num2 != 0) {
        cout << num1 << " / " << num2 << " = " << (float)num1 / num2 << endl;
    } else {
        cout << "Деление на ноль!" << endl;
    }

    cout << endl;

    // Работа со структурой Student
    Student student1 = {"Иван Петров", 20, 4.8};
    Student student2 = {"Мария Сидорова", 19, 3.7};
    Student student3 = {"Алексей Иванов", 21, 2.9};

    cout << "Информация о студентах:" << endl;
    cout << "=======================" << endl;

    printStudentInfo(student1);
    printStudentInfo(student2);
    printStudentInfo(student3);

    // Проверка успеваемости
    cout << "Проверка успеваемости:" << endl;
    cout << student1.name << ": " << checkPerformance(student1.averageGrade) << endl;
    cout << student2.name << ": " << checkPerformance(student2.averageGrade) << endl;
    cout << student3.name << ": " << checkPerformance(student3.averageGrade) << endl;

    cout << endl;

    // Вычисление факториала
    int factNum;
    cout << "Введите число для вычисления факториала (до 10): ";
    cin >> factNum;

    if (factNum >= 0 && factNum <= 10) {
        int factResult = factorial(factNum);
        cout << "Факториал " << factNum << "! = " << factResult << endl;
    } else {
        cout << "Число должно быть от 0 до 10" << endl;
    }

    cout << endl;

    // Работа с массивом
    cout << "Работа с массивом чисел" << endl;
    cout << "========================" << endl;
    processArray();

    cout << endl;

    // Пример работы со строками
    string firstName, lastName;
    cout << "Введите ваше имя: ";
    cin.ignore(); // Очищаем буфер
    getline(cin, firstName);

    cout << "Введите вашу фамилию: ";
    getline(cin, lastName);

    string fullName = firstName + " " + lastName;
    cout << "Привет, " << fullName << "!" << endl;
    cout << "Длина вашего полного имени: " << fullName.length() << " символов" << endl;

    cout << endl;

    // Простой цикл for
    cout << "Таблица умножения для " << num1 << ":" << endl;
    for (int i = 1; i <= 10; i++) {
        cout << num1 << " x " << i << " = " << (num1 * i) << endl;
    }

    return 0;
}