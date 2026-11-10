#include <iostream>

// awwalun commit fi gitbush

void printCrescent() {
    std::cout << "\n";
    std::cout << "           ████           \n";
    std::cout << "         ██ █             \n";
    std::cout << "        █  ██               \n";
    std::cout << "       ██  █             \n";
    std::cout << "       ██  ██               \n";
    std::cout << "       ██   ██               \n";
    std::cout << "        ██    ███  █      \n";
    std::cout << "         ██      ██         \n";
    std::cout << "           ██████           \n";
    std::cout << "\n";
}
int main() {
    std::string answer;
    std::string name;
    
    std::cout << "أهلاً وسهلاً! (Добро пожаловать!)\n";
    std::cout << "Как тебя зовут? ";
    std::getline(std::cin, name);
    
    std::cout << "\n" << name << ", ты мусульманин? (да / нет): ";
    std::getline(std::cin, answer);

    std::cout << "\n------------------------------------------------\n";
    
    if (answer == "да" || answer == "Да" || answer == "YES") {
        std::cout << "ما شاء الله! (МашаАллах!)\n";
    } 
	else {
        std::cout << "Мир тебе и твоему дому!\n";
        std::cout << "скорее принимай ислам!\n";
    }

    printCrescent();

    return 0;
}
