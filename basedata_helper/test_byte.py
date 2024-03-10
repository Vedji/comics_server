genre_works = {
    "Mandy":                                int(b'1010000000000010', 2),
    "Tokidoki":                             int(b'1100010000000100', 2),
    "I_want_my_hat_back":                   int(b'0010000000000000', 2),
    "The_Amazing_Spider_Man":               int(b'0010100000101000', 2),
    "Iron_Man":                             int(b'0000100010101000', 2),
    "One_Piece":                            int(b'0111100101000000', 2),
    "Three_Days_of_Happiness":              int(b'1100010100000010', 2),
    "Gabriel_Dropout_Shcool":               int(b'0011010001000010', 2),
    "DemonSlayer":                          int(b'0101100000001010', 2),
    "test_work":                            int(b'1000100010101010', 2),
    "Test_work_two":                        int(b'1100010000000100', 2)
}


def genre_check(field, mask) -> bool:
    return (field & mask) == mask


def genres_filter(list_search: dict, temp: int):
    for key, value in list_search.items():
        if genre_check(value, temp):
            print(f"temp: {value:<10}-   {key}")


genres_filter(genre_works, int(b"0010000000000000", 2))
print("Genre: ", int(b"1000000000000000", 2))
