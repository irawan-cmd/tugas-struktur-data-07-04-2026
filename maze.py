"""
====================================================
  MAZE PATHFINDING - Tugas Praktikum
  Algoritma: BFS, DFS, A*
  Maze: 15x15 (sesuai tugas)
====================================================
"""

import time
from collections import deque
import heapq

# ============================================================
# MAZE 15x15
# S = Start (titik awal)
# E = Exit  (titik keluar)
# # = Dinding
# . = Jalur kosong
# ============================================================
MAZE = [
    "###############",
    "#S..#...#.....#",
    "###.#.#.#.###.#",
    "#.....#...#.#.#",
    "#.#######.#...#",
    "#.#.....#.#####",
    "#.#.###.#....##",
    "#...#.#.####.##",
    "###.#.#....#..#",
    "#.#.#.####.##.#",
    "#.#......#..#.#",
    "#.######.####.#",
    "#.....#.......#",
    "#####.#######E#",
    "###############",
]

ROWS = len(MAZE)
COLS = len(MAZE[0])

# Arah gerak: kanan, bawah, kiri, atas
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
DIR_NAMES  = ["→", "↓", "←", "↑"]

# ============================================================
# FUNGSI UTILITAS
# ============================================================

def find_start_end(maze):
    """Cari posisi Start (S) dan End (E) di maze."""
    start = end = None
    for r in range(len(maze)):
        for c in range(len(maze[r])):
            if maze[r][c] == 'S':
                start = (r, c)
            elif maze[r][c] == 'E':
                end = (r, c)
    return start, end


def is_valid(r, c, maze):
    """Cek apakah posisi valid (tidak dinding, tidak out of bound)."""
    return (0 <= r < len(maze) and
            0 <= c < len(maze[0]) and
            maze[r][c] != '#')


def reconstruct_path(parent, start, end):
    """Rekonstruksi jalur dari End ke Start menggunakan parent map."""
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()
    return path


def print_maze(maze, visited=None, path=None, current=None):
    """
    Tampilkan maze dengan warna di terminal.
    - Hijau  : jalur yang ditemukan
    - Kuning : sel yang sudah dikunjungi
    - Cyan   : posisi current
    - Merah  : dinding
    - Putih  : jalur kosong
    """
    # ANSI color codes
    RESET  = "\033[0m"
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    CYAN   = "\033[96m"
    WHITE  = "\033[97m"
    BOLD   = "\033[1m"

    visited  = visited  or set()
    path_set = set(path) if path else set()

    print()
    for r in range(len(maze)):
        row_str = ""
        for c in range(len(maze[r])):
            cell = maze[r][c]
            pos  = (r, c)

            if cell == '#':
                row_str += RED + "██" + RESET
            elif pos == current:
                row_str += CYAN + BOLD + " ●" + RESET
            elif cell == 'S':
                row_str += GREEN + BOLD + " S" + RESET
            elif cell == 'E':
                row_str += YELLOW + BOLD + " E" + RESET
            elif pos in path_set:
                row_str += GREEN + " *" + RESET
            elif pos in visited:
                row_str += YELLOW + " x" + RESET
            else:
                row_str += WHITE + " ." + RESET
        print(row_str)
    print()


def print_header(title):
    print("\n" + "=" * 50)
    print(f"  {title}")
    print("=" * 50)


def print_result(algorithm, path, visited_count, elapsed):
    """Tampilkan hasil pencarian."""
    print(f"\n{'─'*50}")
    print(f"  Algoritma  : {algorithm}")
    if path:
        print(f"  Status     : ✅ JALUR DITEMUKAN!")
        print(f"  Panjang    : {len(path)} langkah")
        print(f"  Dieksplorasi: {visited_count} sel")
        print(f"  Waktu      : {elapsed*1000:.2f} ms")
        print(f"\n  Urutan langkah:")
        steps = []
        for i in range(1, len(path)):
            dr = path[i][0] - path[i-1][0]
            dc = path[i][1] - path[i-1][1]
            for j, (dr2, dc2) in enumerate(DIRECTIONS):
                if dr == dr2 and dc == dc2:
                    steps.append(DIR_NAMES[j])
        print(f"  {' '.join(steps)}")
    else:
        print(f"  Status     : ❌ Tidak ada jalur!")
        print(f"  Dieksplorasi: {visited_count} sel")
        print(f"  Waktu      : {elapsed*1000:.2f} ms")
    print(f"{'─'*50}")


# ============================================================
# ALGORITMA 1: BFS (Breadth-First Search)
# - Menjamin jalur TERPENDEK
# - Menggunakan Queue (FIFO)
# - Eksplorasi melebar ke segala arah
# ============================================================

def bfs(maze, show_steps=False):
    """
    Breadth-First Search
    Time Complexity  : O(V + E)
    Space Complexity : O(V)
    Optimal          : Ya (jalur terpendek)
    """
    print_header("BFS - Breadth First Search")

    start, end = find_start_end(maze)
    if not start or not end:
        print("Error: Start atau End tidak ditemukan!")
        return None, 0

    # Queue berisi posisi saat ini
    queue = deque([start])

    # Parent map untuk rekonstruksi jalur
    parent = {start: None}

    # Set visited
    visited = set([start])

    t_start = time.time()

    while queue:
        current = queue.popleft()

        if show_steps:
            print_maze(maze, visited, current=current)
            time.sleep(0.05)

        # Cek apakah sudah sampai tujuan
        if current == end:
            elapsed = time.time() - t_start
            path = reconstruct_path(parent, start, end)
            print_maze(maze, visited, path=path)
            print_result("BFS", path, len(visited), elapsed)
            return path, len(visited)

        # Eksplorasi tetangga
        for dr, dc in DIRECTIONS:
            nr, nc = current[0] + dr, current[1] + dc
            neighbor = (nr, nc)

            if is_valid(nr, nc, maze) and neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    elapsed = time.time() - t_start
    print_result("BFS", None, len(visited), elapsed)
    return None, len(visited)


# ============================================================
# ALGORITMA 2: DFS (Depth-First Search)
# - TIDAK menjamin jalur terpendek
# - Menggunakan Stack (LIFO)
# - Eksplorasi sedalam mungkin dulu
# ============================================================

def dfs(maze, show_steps=False):
    """
    Depth-First Search
    Time Complexity  : O(V + E)
    Space Complexity : O(V)
    Optimal          : Tidak (bukan jalur terpendek)
    """
    print_header("DFS - Depth First Search")

    start, end = find_start_end(maze)
    if not start or not end:
        print("Error: Start atau End tidak ditemukan!")
        return None, 0

    # Stack berisi posisi saat ini
    stack = [start]

    # Parent map untuk rekonstruksi jalur
    parent = {start: None}

    # Set visited
    visited = set()

    t_start = time.time()

    while stack:
        current = stack.pop()

        if current in visited:
            continue
        visited.add(current)

        if show_steps:
            print_maze(maze, visited, current=current)
            time.sleep(0.05)

        # Cek apakah sudah sampai tujuan
        if current == end:
            elapsed = time.time() - t_start
            path = reconstruct_path(parent, start, end)
            print_maze(maze, visited, path=path)
            print_result("DFS", path, len(visited), elapsed)
            return path, len(visited)

        # Eksplorasi tetangga (terbalik agar urutan konsisten)
        for dr, dc in reversed(DIRECTIONS):
            nr, nc = current[0] + dr, current[1] + dc
            neighbor = (nr, nc)

            if is_valid(nr, nc, maze) and neighbor not in visited:
                if neighbor not in parent:
                    parent[neighbor] = current
                stack.append(neighbor)

    elapsed = time.time() - t_start
    print_result("DFS", None, len(visited), elapsed)
    return None, len(visited)


# ============================================================
# ALGORITMA 3: A* (A-Star)
# - Menjamin jalur TERPENDEK (dengan heuristik yang tepat)
# - Menggunakan Priority Queue (Min-Heap)
# - Lebih efisien dari BFS karena pakai heuristik
# ============================================================

def heuristic(pos, end):
    """
    Manhattan Distance sebagai heuristik.
    h(n) = |row_n - row_end| + |col_n - col_end|
    """
    return abs(pos[0] - end[0]) + abs(pos[1] - end[1])


def astar(maze, show_steps=False):
    """
    A* Search Algorithm
    Time Complexity  : O(E log V) dengan priority queue
    Space Complexity : O(V)
    Optimal          : Ya (dengan heuristik admissible)

    f(n) = g(n) + h(n)
    - g(n) = biaya dari start ke n
    - h(n) = estimasi biaya dari n ke end (Manhattan distance)
    """
    print_header("A* - A-Star Search")

    start, end = find_start_end(maze)
    if not start or not end:
        print("Error: Start atau End tidak ditemukan!")
        return None, 0

    # g_score: biaya dari start ke setiap node
    g_score = {start: 0}

    # f_score: g + h
    f_score = {start: heuristic(start, end)}

    # Priority queue: (f_score, posisi)
    open_heap = [(f_score[start], start)]

    # Parent map untuk rekonstruksi jalur
    parent = {start: None}

    # Set closed (sudah dievaluasi)
    closed = set()

    # Set visited untuk visualisasi
    visited = set()

    t_start = time.time()

    while open_heap:
        _, current = heapq.heappop(open_heap)

        if current in closed:
            continue

        closed.add(current)
        visited.add(current)

        if show_steps:
            print_maze(maze, visited, current=current)
            time.sleep(0.05)

        # Cek apakah sudah sampai tujuan
        if current == end:
            elapsed = time.time() - t_start
            path = reconstruct_path(parent, start, end)
            print_maze(maze, visited, path=path)
            print_result("A*", path, len(visited), elapsed)
            return path, len(visited)

        # Eksplorasi tetangga
        for dr, dc in DIRECTIONS:
            nr, nc = current[0] + dr, current[1] + dc
            neighbor = (nr, nc)

            if not is_valid(nr, nc, maze) or neighbor in closed:
                continue

            # g_score baru = g_score current + 1 (setiap langkah cost = 1)
            tentative_g = g_score[current] + 1

            if tentative_g < g_score.get(neighbor, float('inf')):
                parent[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, end)
                heapq.heappush(open_heap, (f_score[neighbor], neighbor))

    elapsed = time.time() - t_start
    print_result("A*", None, len(visited), elapsed)
    return None, len(visited)


# ============================================================
# PERBANDINGAN KETIGA ALGORITMA
# ============================================================

def compare_all(maze):
    """Jalankan dan bandingkan ketiga algoritma."""
    print("\n" + "=" * 50)
    print("  PERBANDINGAN ALGORITMA")
    print("=" * 50)

    results = {}

    # BFS
    path_bfs, visited_bfs = bfs(maze, show_steps=False)
    results['BFS'] = (path_bfs, visited_bfs)

    # DFS
    path_dfs, visited_dfs = dfs(maze, show_steps=False)
    results['DFS'] = (path_dfs, visited_dfs)

    # A*
    path_astar, visited_astar = astar(maze, show_steps=False)
    results['A*'] = (path_astar, visited_astar)

    # Tabel perbandingan
    print("\n" + "=" * 50)
    print("  TABEL PERBANDINGAN")
    print("=" * 50)
    print(f"  {'Algoritma':<10} {'Panjang Jalur':<16} {'Sel Dieksplorasi':<18} {'Optimal'}")
    print(f"  {'─'*9} {'─'*15} {'─'*17} {'─'*8}")
    for algo, (path, visited) in results.items():
        panjang  = len(path) if path else "Tidak ada"
        optimal  = "✅ Ya" if algo in ['BFS', 'A*'] else "❌ Tidak"
        print(f"  {algo:<10} {str(panjang):<16} {str(visited):<18} {optimal}")
    print("=" * 50)
    print()
    print("  Keterangan:")
    print("  - BFS  : Menjamin jalur terpendek, eksplorasi lebar")
    print("  - DFS  : Cepat tapi tidak selalu jalur terpendek")
    print("  - A*   : Paling efisien, pakai heuristik Manhattan")
    print()


# ============================================================
# MENU UTAMA
# ============================================================

def main():
    print("\033[2J\033[H")  # Clear screen
    print("=" * 50)
    print("  MAZE PATHFINDING - Tugas Praktikum")
    print("  Maze 15x15 | BFS | DFS | A*")
    print("=" * 50)

    # Tampilkan maze awal
    print("\nMaze awal:")
    print_maze(MAZE)

    while True:
        print("\nPilih aksi:")
        print("  [1] Jalankan BFS")
        print("  [2] Jalankan DFS")
        print("  [3] Jalankan A*")
        print("  [4] Bandingkan semua algoritma")
        print("  [0] Keluar")
        print()

        pilihan = input("  Pilihan: ").strip()

        if pilihan == '1':
            bfs(MAZE, show_steps=False)
        elif pilihan == '2':
            dfs(MAZE, show_steps=False)
        elif pilihan == '3':
            astar(MAZE, show_steps=False)
        elif pilihan == '4':
            compare_all(MAZE)
        elif pilihan == '0':
            print("\n  Sampai jumpa!\n")
            break
        else:
            print("  Pilihan tidak valid, coba lagi.")


if __name__ == "__main__":
    main()
