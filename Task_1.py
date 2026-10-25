import timeit


def boyer_moore(text, pattern):
    """Пошук підрядка алгоритмом Боєра-Мура."""

    if pattern == "":
        return 0

    pattern_length = len(pattern)
    text_length = len(text)

    if pattern_length > text_length:
        return -1

    shift_table = {}

    for index in range(pattern_length - 1):
        shift_table[pattern[index]] = pattern_length - index - 1

    text_index = pattern_length - 1

    while text_index < text_length:
        pattern_index = pattern_length - 1
        current_index = text_index

        while (
            pattern_index >= 0
            and text[current_index] == pattern[pattern_index]
        ):
            current_index -= 1
            pattern_index -= 1

        if pattern_index < 0:
            return current_index + 1

        shift = shift_table.get(
            text[text_index],
            pattern_length,
        )

        text_index += shift

    return -1


def create_lps(pattern):
    """Створення LPS-масиву для алгоритму КМП."""

    lps = [0] * len(pattern)

    prefix_length = 0
    index = 1

    while index < len(pattern):
        if pattern[index] == pattern[prefix_length]:
            prefix_length += 1
            lps[index] = prefix_length
            index += 1

        elif prefix_length > 0:
            prefix_length = lps[prefix_length - 1]

        else:
            lps[index] = 0
            index += 1

    return lps


def kmp_search(text, pattern):
    """Пошук підрядка алгоритмом Кнута-Морріса-Пратта."""

    if pattern == "":
        return 0

    if len(pattern) > len(text):
        return -1

    lps = create_lps(pattern)

    text_index = 0
    pattern_index = 0

    while text_index < len(text):
        if text[text_index] == pattern[pattern_index]:
            text_index += 1
            pattern_index += 1

            if pattern_index == len(pattern):
                return text_index - pattern_index

        elif pattern_index > 0:
            pattern_index = lps[pattern_index - 1]

        else:
            text_index += 1

    return -1


def rabin_karp(text, pattern):
    """Пошук підрядка алгоритмом Рабіна-Карпа."""

    if pattern == "":
        return 0

    pattern_length = len(pattern)
    text_length = len(text)

    if pattern_length > text_length:
        return -1

    pattern_hash = hash(pattern)

    for index in range(text_length - pattern_length + 1):
        current_substring = text[
            index:index + pattern_length
        ]

        if hash(current_substring) == pattern_hash:
            if current_substring == pattern:
                return index

    return -1


def read_file(file_name):
    """Читання текстового файлу."""

    with open(file_name, "r", encoding="utf-8") as file:
        return file.read().lower()


def compare_algorithms(
    text,
    existing_pattern,
    missing_pattern,
    article_name,
):
    """Порівняння часу роботи трьох алгоритмів."""

    algorithms = {
        "Боєра-Мура": boyer_moore,
        "Кнута-Морріса-Пратта": kmp_search,
        "Рабіна-Карпа": rabin_karp,
    }

    print()
    print(article_name)
    print("-" * 70)

    for algorithm_name, algorithm in algorithms.items():
        existing_index = algorithm(
            text,
            existing_pattern,
        )

        missing_index = algorithm(
            text,
            missing_pattern,
        )

        existing_time = timeit.timeit(
            lambda: algorithm(
                text,
                existing_pattern,
            ),
            number=100,
        )

        missing_time = timeit.timeit(
            lambda: algorithm(
                text,
                missing_pattern,
            ),
            number=100,
        )

        print(f"\nАлгоритм: {algorithm_name}")

        print(
            f"Існуючий підрядок: "
            f"індекс = {existing_index}, "
            f"час = {existing_time:.6f} с"
        )

        print(
            f"Неіснуючий підрядок: "
            f"індекс = {missing_index}, "
            f"час = {missing_time:.6f} с"
        )


text_1 = read_file("article1.txt")
text_2 = read_file("article2.txt")


existing_pattern_1 = "двійковий пошук"
missing_pattern_1 = "неіснуючий підрядок"

existing_pattern_2 = "рекомендаційної системи"
missing_pattern_2 = "вигадана структура даних"


compare_algorithms(
    text_1,
    existing_pattern_1,
    missing_pattern_1,
    "Стаття 1",
)

compare_algorithms(
    text_2,
    existing_pattern_2,
    missing_pattern_2,
    "Стаття 2",
)