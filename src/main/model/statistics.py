import datetime


class Statistics:
    def __init__(self):
        self.file_path = "wyniki.txt"

    def save_result(self, name, result, difficulty=None):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(self.file_path, "a") as file:
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

    def get_latest_results(self):
        with open(self.file_path, 'r') as result_file:
            result = [line for line in result_file]
            return result
