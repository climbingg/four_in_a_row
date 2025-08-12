def one_to_two(n: int) -> tuple[int, int]:
    return n // 7, n % 7

def two_to_one(y: int, x: int) -> int:
    return y * 7 + x


content = [2] * 42
points = [0, 0, 0, 0, 0, 0, 0]
history_move = [None] * 42
history_point = [None] * 42
history = [0]
LJ = []
table = {}

print("載入中...")
with open("table.txt") as file:
    file = file.read().split("\n")
    if file == [""]:
        file.clear()
print("載入完成!!")

for one_of_table in file:
    key, val = one_of_table.split("  ")
    table[tuple(map(int, key.split()))] = list(map(lambda x: None if x == "None" else float("-inf") if x == "-inf" else int(x), val.split()))

for i in range(42):
    y, x = one_to_two(i)
    one_lj = []
    pair_lj = []
    one_one_lj = []
    for x_plus in range(-1, -4, -1):
        if 7 > x + x_plus >= 0:
            one_one_lj.append(two_to_one(y, x + x_plus))
    pair_lj.append(tuple(one_one_lj))
    one_one_lj = []
    for x_plus in range(1, 4):
        if 7 > x + x_plus >= 0:
            one_one_lj.append(two_to_one(y, x + x_plus))
    pair_lj.append(tuple(one_one_lj))
    one_lj.append(tuple(pair_lj))
    pair_lj = []
    one_one_lj = []
    for y_plus in range(-1, -4, -1):
        if 6 > y + y_plus >= 0:
            one_one_lj.append(two_to_one(y + y_plus, x))
    pair_lj.append(tuple(one_one_lj))
    pair_lj.append(())
    one_lj.append(tuple(pair_lj))
    one_one_lj = []
    pair_lj = []
    for x_y_plus in range(-1, -4, -1):
        if 7 > x + x_y_plus >= 0 and 6 > y + x_y_plus >= 0:
            one_one_lj.append(two_to_one(y + x_y_plus, x + x_y_plus))
    pair_lj.append(tuple(one_one_lj))
    one_one_lj = []
    for x_y_plus in range(1, 4):
        if 7 > x + x_y_plus >= 0 and 6 > y + x_y_plus >= 0:
            one_one_lj.append(two_to_one(y + x_y_plus, x + x_y_plus))
    pair_lj.append(tuple(one_one_lj))
    one_lj.append(tuple(pair_lj))
    pair_lj = []
    one_one_lj = []
    for plus in range(-1, -4, -1):
        if 7 > x + plus >= 0 and 6 > y - plus >= 0:
            one_one_lj.append(two_to_one(y - plus, x + plus))
    pair_lj.append(tuple(one_one_lj))
    one_one_lj = []
    for plus in range(1, 4):
        if 7 > x + plus >= 0 and 6 > y - plus >= 0:
            one_one_lj.append(two_to_one(y - plus, x + plus))
    pair_lj.append(tuple(one_one_lj))
    one_lj.append(tuple(pair_lj))
    pair_lj = []
    LJ.append(tuple(one_lj))

LJ = tuple(LJ)


def is_legal(move_num: int) -> bool:
    return points[move_num] != 6


def move(move_num: str) -> int:
    move_num = int(move_num) - 1
    history_move[history[0]] = move_num
    history_point[history[0]] = move_num + points[move_num] * 7
    history[0] += 1
    content[move_num + points[move_num] * 7] = history[0] % 2
    points[move_num] += 1
    return history_point[history[0] - 1]


def undo() -> None:
    history[0] -= 1
    points[history_move[history[0]]] -= 1
    content[history_point[history[0]]] = 2


def board_print() -> None:
    for i in range(6):
        for j in range(7):
            print(end=THREE[content[(5 - i) * 7 + j]])
        print()
    print("1234567")


def check_res(pre_point: int) -> int:
    for (one_t, two_t) in LJ[pre_point]:
        check_four = 1
        for one_of in one_t:
            if content[one_of] == content[pre_point]:
                check_four += 1
            else:
                break
        for one_of in two_t:
            if content[one_of] == content[pre_point]:
                check_four += 1
            else:
                break
        if check_four >= 4:
            return [-1, 1][content[pre_point]]
    return [2, 0][history[0] == 42]


def bfs() -> int | None:
    t_content = tuple(content)
    if t_content not in table:
        table[t_content] = [None] * 7
    table_res = table[t_content]
    for i in range(7):
        if table_res[i] is not None and table_res[i] != float("-inf") and history[0] % 2 != table_res[i] % 2:
            return table_res[i]
    for i in range(7):
        if table_res[i] is not None:
            if history[0] != 0 and history[0] % 2 == table_res[i] % 2:
                continue
        if not is_legal(i):
            table_res[i] = float("-inf")
            continue
        if history[0] == max_depth[0] - 1:
            table_res[i] = [0, max_depth[0], None][abs(check_res(move(str(i + 1))))]
            undo()
            if table_res[i] == max_depth[0]:
                return table_res[i]
        else:
            move(str(i + 1))
            table_res[i] = bfs()
            undo()
            if table_res[i] and table_res[i] == max_depth[0] and history[0] % 2 != max_depth[0] % 2:
                return table_res[i]
    table_res_2 = list(filter(lambda x: x != float("-inf"), table_res))
    return None if None in table_res_2 else 0 if 0 in table_res_2 else max(table_res_2)


def ai() -> list[str | None]:
    ret = [None] * 7
    for i in range(1, 8):
        if is_legal(int(i) - 1):
            if abs(check_res(move(str(i)))) == 1:
                ret[i - 1] = history[0]
                undo()
                continue
            for j in range(history[0], min(history[0] + user_depth - 1, 42)):
                max_depth[0] = j + 1
                score = bfs()
                print(i, j)
                if score:                   # 因為0是False
                    ret[i - 1] = score
                    break
            else:
                ret[i - 1] = "目前深度看不出來誰贏"
            undo()
    ret = list(map(lambda x: None if x is None else "平手" if x == 0 else "目前深度看不出來誰贏" if x == "目前深度看不出來誰贏" else f"{BLUE}到第{x}步藍獲勝!!{RESET}(再{x - history[0]}步!!)" if x % 2 == 0 else f"{RED}到第{x}步紅獲勝!!{RESET}(再{x - history[0]}步!!)", ret))
    return ret


def user_is_legal(move_num: str) -> bool:
    if move_num in {"1", "2", "3", "4", "5", "6", "7"}:
        return is_legal(int(move_num) - 1)
    return False


user_depth = int(input("你希望程式算未來幾步(建議8步)?:"))
max_depth = [None]
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"
THREE = [f"{BLUE}o{RESET}", f"{RED}o{RESET}", "o"]

board_print()


while True:
    if input("讓ai分析?(需要輸入yes):") == "yes":
        for i, ai_res in enumerate(ai(), 1):
            print(f"{i}:", ai_res)
    m = input("輸入1~7或undo:")
    while not user_is_legal(m):
        if m == "undo":
            undo()
            break
        print("error")
        m = input("輸入1~7或undo:")
    else:
        res = check_res(move(m))
        if res < 2:
            board_print()
            print(["平手!!", "紅方獲勝!!", "藍方獲勝!!"][res])
            break
    board_print()

print("game over!!")
