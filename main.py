# main.py
from transaction import Transaction
from file_manager import FileManager
import re


def main() -> None:
    """
    Основная функция программы, управляющая интерфейсом и вызывающая соответствующие методы FileManager.

    Returns:
        None
    """
    file_path = "data/transactions.txt"
    file_manager = FileManager(file_path)

    while True:
        print("1. Добавить запись")
        print("2. Вывести баланс")
        print("3. Редактировать запись")
        print("4. Поиск по записям")
        print("5. Удалить данные о транзакции")
        print("6. Выход")
        print()

        choice = input("Выберите действие: ")

        if choice == "1":
            add_transaction(file_manager)
        elif choice == "2":
            print_balance(file_manager)
        elif choice == "3":
            edit_transaction(file_manager)
        elif choice == "4":
            search_criteria = {}
            category = input(
                "Введите категорию (для пропуска введите пустую строку): "
            ).capitalize()
            if category:
                search_criteria["category"] = category
            date = input("Введите дату (для пропуска введите пустую строку): ")
            if date:
                search_criteria["date"] = date
            amount = input("Введите сумму (для пропуска введите пустую строку): ")
            if amount:
                search_criteria["amount"] = str(float(amount))
            description = input(
                "Введите описание (для пропуска введите пустую строку): "
            )
            if description:
                search_criteria["description"] = description

            found_transactions = file_manager.search_transactions(search_criteria)
            if found_transactions:
                print("Найденные транзакции:")
                for transaction_info in found_transactions:
                    transaction = Transaction(**transaction_info)
                    print_transaction_info(transaction)
            else:
                print("Транзакции не найдены")
        elif choice == "5":
            delete_transaction(file_manager)
        elif choice == "6":
            break
        else:
            print("Неверный ввод. Попробуйте снова.")


def print_transaction_info(transaction: Transaction) -> None:
    """
    Выводит информацию о транзакции в консоль.

    Args:
        transaction (Transaction): Транзакция, информацию о которой нужно вывести.

    Returns:
        None
    """
    print(f"ID: {transaction.transaction_id}")
    print(f"Дата: {transaction.date}")
    print(f"Категория: {transaction.category}")
    print(f"Сумма: {transaction.amount}")
    print(f"Описание: {transaction.description}\n")


def add_transaction(file_manager: FileManager) -> None:
    """
    Добавляет новую транзакцию в файл с помощью менеджера файлов.

    Args:
        file_manager (FileManager): Менеджер файлов для работы с транзакциями.

    Returns:
        None
    """
    while True:
        date = input("Введите дату транзакции (гггг-мм-дд): ")
        if not is_valid_date(date):
            print(
                "Неверный формат даты. Пожалуйста, введите дату в формате гггг-мм-дд."
            )
            continue

        category = input("Введите категорию (Доход/Расход): ").capitalize()
        if not is_valid_category(category):
            print("Неверная категория. Категория должна быть 'Доход' или 'Расход'.")
            continue

        amount_str = input("Введите сумму транзакции: ")
        if not is_valid_amount(amount_str):
            print("Неверный формат суммы. Пожалуйста, введите число.")
            continue
        amount = float(amount_str)

        description = input("Введите описание транзакции (не более 100 символов): ")
        if not is_valid_description(description):
            print("Неверное описание. Описание не должно превышать 100 символов.")
            continue

        file_manager.add_transaction(date, category, amount, description)

        print()
        print("Новая транзакция успешно добавлена!")
        print()
        break


def print_balance(file_manager: FileManager) -> None:
    """
    Выводит текущий баланс, а также сумму доходов и расходов отдельно.

    Args:
        file_manager (FileManager): Менеджер файлов для работы с транзакциями.

    Returns:
        None
    """
    balance, total_income, total_expense = file_manager.get_balance()
    print()
    print(f"Текущий баланс: {balance}")
    print(f"Текущий доход: {total_income}")
    print(f"Текущий расход: {total_expense}")
    print()


def edit_transaction(file_manager: FileManager) -> None:
    """
    Редактирует транзакцию с помощью менеджера файлов.

    Args:
        file_manager (FileManager): Менеджер файлов для работы с транзакциями.

    Returns:
        None
    """
    transaction_id = input("Введите ID транзакции для редактирования: ")
    transaction_info = file_manager.get_transaction_info_by_id(transaction_id)
    if transaction_info:
        print("Текущая информация о транзакции:")
        print_transaction_info(Transaction(**transaction_info))
        print("Введите новые значения (оставьте пустым, чтобы оставить без изменений):")

        while True:
            date_input = input(f"Дата ({transaction_info['date']}): ").strip()
            if date_input == "":
                date = transaction_info["date"]
                break
            elif not is_valid_date(date_input):
                print(
                    "Неверный формат даты. Пожалуйста, введите дату в формате гггг-мм-дд."
                )
                continue
            else:
                date = date_input
                break

        while True:
            category_input = (
                input(f"Категория ({transaction_info['category']}): ")
                .capitalize()
                .strip()
            )
            if category_input == "":
                category = transaction_info["category"]
                break
            elif not is_valid_category(category_input):
                print("Неверная категория. Категория должна быть 'Доход' или 'Расход'.")
                continue
            else:
                category = category_input
                break

        while True:
            amount_input = input(f"Сумма ({transaction_info['amount']}): ").strip()
            if amount_input == "":
                amount = transaction_info["amount"]
                break
            elif not is_valid_amount(amount_input):
                print("Неверный формат суммы. Пожалуйста, введите число.")
                continue
            else:
                amount = float(amount_input)
                break

        description_input = input(
            f"Описание ({transaction_info['description']}): "
        ).strip()
        if description_input == "":
            description = transaction_info["description"]
        else:
            description = description_input
            if not is_valid_description(description):
                print("Неверное описание. Описание не должно превышать 100 символов.")
                return

        file_manager.edit_transaction(
            transaction_id, date, category, amount, description
        )

        new_transaction_info = file_manager.get_transaction_info_by_id(transaction_id)

        print("Транзакция успешно отредактирована!")
        print()
        print("Текущая информация о транзакции:")
        print_transaction_info(Transaction(**new_transaction_info))
    else:
        print("Транзакция с указанным ID не найдена.")


def delete_transaction(file_manager: FileManager) -> None:
    """
    Удаляет транзакцию с помощью менеджера файлов.

    Args:
        file_manager (FileManager): Менеджер файлов для работы с транзакциями.

    Returns:
        None
    """
    transaction_id = input("Введите ID транзакции для удаления: ")
    transaction_info = file_manager.get_transaction_info_by_id(transaction_id)
    if transaction_info:
        print("Информация о транзакции:")
        print_transaction_info(Transaction(**transaction_info))
        confirmation = input(
            "Вы уверены, что хотите удалить эту транзакцию? (yes/no): "
        )
        if confirmation.lower() == "yes":
            file_manager.delete_transaction(transaction_id)
            print("Транзакция успешно удалена!")
        else:
            print("Удаление отменено.")
    else:
        print("Транзакция с указанным ID не найдена.")


def is_valid_date(date: str) -> bool:
    """
    Проверяет дату на валидность.

    Returns:
        bool
    """
    return bool(re.match(r"^\d{4}-\d{2}-\d{2}$", date))


def is_valid_category(category: str) -> bool:
    """
    Проверяет дату на валидность.

    Returns:
        bool
    """
    return category.capitalize() in ["Доход", "Расход"]


def is_valid_amount(amount_str: str) -> bool:
    """
    Проверяет сумму транзакции на валидность.

    Returns:
        bool
    """
    try:
        float(amount_str)
        return True
    except ValueError:
        return False


def is_valid_description(description: str) -> bool:
    """
    Проверяет что длина описания не больше 100 символов.

    Returns:
        bool
    """
    return len(description) <= 100


if __name__ == "__main__":
    main()
