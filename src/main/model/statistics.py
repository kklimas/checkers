import datetime

class Statistics:
    def save_result(self, name, result, difficulty = None):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open("wyniki.txt", "a") as file:
                file.write(f"Imię gracza: {name}\n")
                file.write(f"Wynik rozgrywki: {result}\n")
                if difficulty:
                    file.write(f"Trudność: {difficulty}\n")
                # else:
                #     czas_rozgrywki = result
                #     file.write(f"Czas rozgrywki: {czas_rozgrywki}\n")
                file.write(f"Czas zapisu: {timestamp}\n")
                file.write("----\n")
            print("Zapisano wynik w pliku.")
        except Exception as e:
            print(f"Wystąpił błąd podczas zapisu wyniku: {e}")
