# file_manager.py
from transaction import Transaction


class FileManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def add_transaction(self, date, category, amount, description):
        transaction_id = self.get_next_transaction_id()
        transaction = Transaction(date, category, amount, description, transaction_id)

        with open(self.file_path, "a") as file:
            file.write(f"ID: {transaction.transaction_id}\n")
            file.write(f"Дата: {transaction.date}\n")
            file.write(f"Категория: {transaction.category}\n")
            file.write(f"Сумма: {transaction.amount}\n")
            file.write(f"Описание: {transaction.description}\n\n")

    def get_next_transaction_id(self):
        last_id = 0
        with open(self.file_path, "r") as file:
            for line in file:
                if line.startswith("ID:"):
                    last_id = int(line.split(":")[1])

        return last_id + 1

    def get_balance(self) -> tuple:
        """
        Возвращает общий баланс, а также сумму доходов и расходов отдельно.

        Returns:
            tuple(float, float, float) кортеж из балланса, дохода и расходов.
        """
        total_income = 0
        total_expense = 0
        with open(self.file_path, "r") as file:
            for line in file:
                if line.startswith("Категория:"):
                    category = line.split(":")[1].strip()
                elif line.startswith("Сумма:"):
                    amount = float(line.split(":")[1].strip())
                    if category == "Доход":
                        total_income += amount
                    elif category == "Расход":
                        total_expense += amount
        balance = total_income - total_expense
        return balance, total_income, total_expense

    def search_transactions(
        self, search_criteria: dict[str, str]
    ) -> list[dict[str, str]]:
        """
        Ищет транзакции в файле на основе заданных критериев.

        Args:
            search_criteria (dict[str, str]): Словарь с критериями поиска, где ключ - это имя поля,
                                                а значение - требуемое значение для этого поля.

        Returns:
            list[dict[str, str]]: Список словарей с информацией о найденных транзакциях.
        """
        found_transactions = []
        with open(self.file_path, "r") as file:
            transaction_info = {}
            for line in file:
                if line.strip():
                    key, value = line.split(":")
                    key = key.strip()
                    if key == "Дата":
                        key = "date"
                    elif key == "Категория":
                        key = "category"
                    elif key == "Сумма":
                        key = "amount"
                    elif key == "Описание":
                        key = "description"
                    transaction_info[key] = value.strip()

                if line.strip() == "" and transaction_info:
                    if search_criteria:
                        match = True
                        for key, value in search_criteria.items():
                            if key in transaction_info:
                                if transaction_info[key].lower() != value.lower():
                                    match = False
                                    break
                            else:
                                match = False
                                break
                        if match:
                            transaction_info["transaction_id"] = int(
                                transaction_info.pop("ID", 0)
                            )
                            found_transactions.append(transaction_info.copy())
                    transaction_info.clear()
        return found_transactions

    def edit_transaction(
        self,
        transaction_id: int,
        date: str,
        category: str,
        amount: float,
        description: str,
    ) -> None:
        """
        Редактирует транзакцию с указанным ID.

        Args:
            transaction_id (int): ID транзакции, которую необходимо отредактировать.
            date (str): Новая дата транзакции.
            category (str): Новая категория транзакции.
            amount (float): Новая сумма транзакции.
            description (str): Новое описание транзакции.

        Returns:
            None
        """
        with open(self.file_path, "r") as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if line.startswith("ID:") and int(line.split(":")[1].strip()) == int(
                    transaction_id
                ):
                    lines[i + 1] = f"Дата: {date}\n"
                    lines[i + 2] = f"Категория: {category}\n"
                    lines[i + 3] = f"Сумма: {amount}\n"
                    lines[i + 4] = f"Описание: {description}\n\n"
                    break
            else:
                print("Транзакция с указанным ID не найдена.")
                return

        with open(self.file_path, "w") as file:
            file.writelines(lines)

    def get_transaction_info_by_id(self, transaction_id: int) -> dict:
        """
        Возвращает информацию о транзакции по её ID.

        Args:
            transaction_id (int): ID транзакции, информацию о которой нужно получить.

        Returns:
            dict: Словарь с информацией о транзакции.
        """
        transaction_info = {}
        with open(self.file_path, "r") as file:
            current_id = None
            for line in file:
                if line.startswith("ID:"):
                    current_id = int(line.split(":")[1].strip())
                    if current_id == int(transaction_id):
                        transaction_info["transaction_id"] = current_id
                elif current_id == int(transaction_id):
                    if ":" in line:
                        key, value = line.split(":", 1)  # Split only once
                        key = key.strip()
                        if key == "Дата":
                            key = "date"
                        elif key == "Категория":
                            key = "category"
                        elif key == "Сумма":
                            key = "amount"
                        elif key == "Описание":
                            key = "description"
                        transaction_info[key] = value.strip()
        return transaction_info

    def delete_transaction(self, transaction_id: int) -> None:
        """
        Удаляет транзакцию с указанным ID.

        Args:
            transaction_id (int): ID транзакции, которую необходимо удалить.

        Returns:
            None
        """
        with open(self.file_path, "r") as file:
            lines = file.readlines()

        with open(self.file_path, "w") as file:
            for i, line in enumerate(lines):
                if line.startswith("ID:") and int(line.split(":")[1].strip()) == int(
                    transaction_id
                ):
                    del lines[i : i + 6]
                    break
            else:
                print("Транзакция с указанным ID не найдена.")
                return

            file.writelines(lines)
