import time
import random


def one_to_two(n: int) -> tuple[int, int]:
    return n // 7, n % 7

def two_to_one(y: int, x: int) -> int:
    return y * 7 + x


board_red = [0]
board_blue = [0]
history_point = [None] * 42
history = [0]
depth = [8]
table = {}
is_win = [None]
win = [0]
win_lose = [0]
LJ = []

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


def is_legal(move_num: int) -> int:
    while move_num < 42:
        if board_red[0] >> move_num & 1 == 0 and board_blue[0] >> move_num & 1 == 0:
            return move_num
        move_num += 7
    return -1


def move(move_point: int) -> None:
    history_point[history[0]] = move_point
    history[0] += 1
    if history[0] % 2 == 1:
        board_red[0] |= 1 << move_point
    else:
        board_blue[0] |= 1 << move_point


def undo() -> None:
    history[0] -= 1
    if history[0] % 2 == 0:
        board_red[0] ^= 1 << history_point[history[0]]
        history_point[history[0]] = None
    else:
        board_blue[0] ^= 1 << history_point[history[0]]
        history_point[history[0]] = None

def board_print() -> None:
    for i in range(6):
        for j in range(7):
            temp_point = (5 - i) * 7 + j
            if board_red[0] >> temp_point & 1:
                print(end=THREE[1])
            elif board_blue[0] >> temp_point & 1:
                print(end=THREE[0])
            else:
                print(end=THREE[2])
        print()
    print("1234567")


def check_res(pre_point: int) -> int:
    check = [board_blue[0], board_red[0]][history[0] % 2]
    for (one_t, two_t) in LJ[pre_point]:
        check_four = 1
        for one_of in one_t:
            if check >> one_of & 1:
                check_four += 1
            else:
                break
        for one_of in two_t:
            if check >> one_of & 1:
                check_four += 1
            else:
                break
        if check_four >= 4:
            return history[0]
    return [-1, 0][history[0] == 42]


def user_is_legal(move_num: str) -> int:
    if move_num in {"1", "2", "3", "4", "5", "6", "7"}:
        return is_legal(int(move_num) - 1)
    return -1


def bfs() -> int | None:
    if (board_red[0], board_blue[0]) not in table:
        table[(board_red[0], board_blue[0])] = [None] * 7
    table_res = table[(board_red[0], board_blue[0])]
    for i in range(7):
        if table_res[i] is not None and table_res[i] != float("-inf") and history[0] % 2 != table_res[i] % 2:
            return table_res[i]
    for i in range(7):
        if table_res[i] is not None:
            if history[0] != 0 and history[0] % 2 == table_res[i] % 2:
                continue
        res_point = is_legal(i)
        if res_point == -1:
            table_res[i] = float("-inf")
            continue
        if history[0] == max_depth[0] - 1:
            move(res_point)
            res = check_res(res_point)
            table_res[i] = None if res == -1 else res
            undo()
            if table_res[i] == max_depth[0]:
                win_lose[0] += 1
                if is_win[0] == (history[0] + 1) % 2:
                    win[0] += 1
                return table_res[i]
        else:
            move(res_point)
            table_res[i] = bfs()
            undo()
            if table_res[i] and table_res[i] == max_depth[0] and history[0] % 2 != max_depth[0] % 2:
                return table_res[i]
    table_res_2 = list(filter(lambda x: x != float("-inf"), table_res))
    return None if None in table_res_2 else 0 if 0 in table_res_2 else max(table_res_2)


def analyze_ai(user_depth: int) -> list[str | None]:
    is_win[0] = (history[0] + 1) % 2
    ret = [None] * 7
    for i in range(7):
        res_point = is_legal(int(i))
        if res_point == -1:
            ret[i] = float("-inf")
            continue
        move(res_point)
        if check_res(res_point) != -1:
            ret[i] = history[0]
            undo()
            continue
        for j in range(history[0], min(history[0] + user_depth - 1, 42)):
            max_depth[0] = j + 1
            score = bfs()
            print(i + 1, j)
            if score:                   # 因為0是False
                ret[i] = score
                break
        else:
            if win_lose[0] == 0:
                ret[i] = 0.5
            else:
                ret[i] = win[0] / win_lose[0]
        win[0] = 0
        win_lose[0] = 0
        undo()
    ret = list(map(lambda x: "非法棋步" if x == float("-inf") else f"勝率{x * 100}%" if type(x) == float else "平手" if x == 0 else f"{BLUE}到第{x}步藍獲勝!!{RESET}(再{x - history[0]}步!!)" if x % 2 == 0 else f"{RED}到第{x}步紅獲勝!!{RESET}(再{x - history[0]}步!!)", ret))
    table.clear()
    return ret


def ai_play(ai: str) -> int:
    is_win[0] = (history[0] + 1) % 2
    best_moves_val = None
    best_moves = []
    for i in range(7):
        if (board_red[0], board_blue[0]) in table and table[(board_red[0], board_blue[0])][i] is not None and table[(board_red[0], board_blue[0])][i] != float("-inf") and table[(board_red[0], board_blue[0])][i] % 2 != history[0] % 2:
            return i
        res_point = is_legal(i)
        if res_point == -1:
            continue
        move(res_point)
        res = check_res(res_point)
        if res != -1:
            undo()
            print("你輸了!!!!")
            return i
        for j in range(history[0], min(history[0] + depth[-1] - 1, 42)):
            max_depth[0] = j + 1
            score = bfs()
            if score:                   # 因為0是False
                if score % 2 == {"red": 1, "blue": 0}[ai]:
                    undo()
                    print("你輸定了!!!!")
                    return i
                if best_moves_val is None:
                    best_moves_val = score
                    best_moves = [i]
                if type(best_moves_val) != float:
                    if best_moves_val < score:
                        best_moves_val = score
                        best_moves = [i]
                    elif best_moves_val == score:
                        best_moves.append(i)
                break
        else:
            if best_moves_val is None:
                if win_lose[0] == 0:
                    best_moves_val = 0.5
                else:
                    best_moves_val = win[0] / win_lose[0]
                best_moves = [i]
            elif type(best_moves_val) == int:
                if win_lose[0] == 0:
                    best_moves_val = 0.5
                else:
                    best_moves_val = win[0] / win_lose[0]
                best_moves = [i]
            elif type(best_moves_val) == float:
                if win_lose[0] == 0:
                    rate = 0.5
                else:
                    rate = win[0] / win_lose[0]
                if best_moves_val < rate:
                    best_moves_val = rate
                    best_moves = [i]
        win[0] = 0
        win_lose[0] = 0
        undo()
    table.clear()
    return random.choice(best_moves)


max_depth = [None]
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"
THREE = [f"{BLUE}o{RESET}", f"{RED}o{RESET}", "o"]


def double() -> None:
    board_print()
    while True:
        m = input("輸入1~7或undo:")
        point = user_is_legal(m)
        while point == -1:
            if m == "undo":
                undo()
                break
            print("error")
            m = input("輸入1~7或undo:")
            point = user_is_legal(m)
        else:
            move(point)
            res = check_res(point)
            if res != -1:
                board_print()
                if res == 0:
                    print("平手!!")
                    break
                if res % 2 == 1:
                    print("紅方獲勝!!")
                else:
                    print("藍方獲勝!!")
                break
        board_print()


def analyze() -> None:
    depth[0] = int(input("你希望程式算未來幾步(建議初始8步)(ai會自動調節)?:"))
    board_print()
    while True:
        if input("讓ai分析?(需要輸入yes):") == "yes":
            t = time.time()
            for i, ai_res in enumerate(analyze_ai(depth[0]), 1):
                print(f"{i}:", ai_res)
            if time.time() - t < 2:
                depth.append(depth[-1] + 1)
                print("加深！！！")
            else:
                depth.append(depth[-1])
        else:
            depth.append(depth[-1])
        m = input("輸入1~7或undo:")
        point = user_is_legal(m)
        while point == -1:
            if m == "undo":
                depth.pop()
                undo()
                break
            print("error")
            m = input("輸入1~7或undo:")
            point = user_is_legal(m)
        else:
            move(point)
            res = check_res(point)
            if res != -1:
                board_print()
                if res == 0:
                    print("平手!!")
                    break
                if res % 2 == 1:
                    print("紅方獲勝!!")
                else:
                    print("藍方獲勝!!")
                break
        board_print()


def play_red() -> None:
    board_print()
    pre_undo = False
    while True:
        m = input("輸入1~7或undo:")
        res_point = user_is_legal(m)
        while res_point == -1:
            if m == "undo":
                depth.pop()
                undo()
                undo()
                pre_undo = True
                break
            print("error")
            m = input("輸入1~7或undo:")
            res_point = user_is_legal(m)
        else:
            move(res_point)
            res = check_res(res_point)
            if res != -1:
                board_print()
                if res == 0:
                    print("平手!!")
                    break
                if res % 2 == 1:
                    print("紅方獲勝!!")
                else:
                    print("藍方獲勝!!")
                break
        board_print()
        if not pre_undo:
            t = time.time()
            res_point = is_legal(ai_play("blue"))
            if time.time() - t < 2:
                print("加深！！！")
                depth.append(depth[-1] + 1)
            else:
                depth.append(depth[-1])
            move(res_point)
            res = check_res(res_point)
            if res != -1:
                board_print()
                if res == 0:
                    print("平手!!")
                    break
                if res % 2 == 1:
                    print("紅方獲勝!!")
                else:
                    print("藍方獲勝!!")
                break
            board_print()
        else:
            pre_undo = False


def play_blue() -> None:
    board_print()
    pre_undo = False
    while True:
        if not pre_undo:
            t = time.time()
            res_point = is_legal(ai_play("red"))
            if time.time() - t < 2:
                print("加深！！！")
                depth.append(depth[-1] + 1)
            else:
                depth.append(depth[-1])
            move(res_point)
            res = check_res(res_point)
            if res != -1:
                board_print()
                if res == 0:
                    print("平手!!")
                    break
                if res % 2 == 1:
                    print("紅方獲勝!!")
                else:
                    print("藍方獲勝!!")
                break
            board_print()
        else:
            pre_undo = False
        m = input("輸入1~7或undo:")
        res_point = user_is_legal(m)
        while res_point == -1:
            if m == "undo":
                depth.pop()
                undo()
                undo()
                pre_undo = True
                break
            print("error")
            m = input("輸入1~7或undo:")
            res_point = user_is_legal(m)
        else:
            move(res_point)
            res = check_res(res_point)
            if res != -1:
                board_print()
                if res == 0:
                    print("平手!!")
                    break
                if res % 2 == 1:
                    print("紅方獲勝!!")
                else:
                    print("藍方獲勝!!")
                break
        board_print()


def main() -> None:
    num = input("請選擇模式...\n1:雙人對戰\n2:分析\n3:拿紅\n4:拿藍\n輸入模式:")
    while num not in ["1", "2", "3", "4"]:
        num = input("請選擇模式...\n1:雙人對戰\n2:分析\n3:拿紅\n4:拿藍\n輸入模式(只能輸入1~4):")
    [double, analyze, play_red, play_blue][int(num) - 1]()
    print("game over!!")


main()
