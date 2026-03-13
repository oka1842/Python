"""
3D図形回転アニメーション - Tkinterを使用（拡張版）
複数の図形を選択して回転させるインタラクティブなアニメーション
"""

import tkinter as tk
import math
try:
    import numpy as np
except ModuleNotFoundError:
    np = None


class Shape3D:
    """3D図形の基底クラス"""

    def __init__(self):
        self.vertices = []
        self.edges = []
        self.faces = []  # 面（オプション）

    def get_vertices(self):
        return self.vertices

    def get_edges(self):
        return self.edges

    def get_faces(self):
        return self.faces


class 立方体(Shape3D):
    """立方体"""

    def __init__(self):
        super().__init__()
        self.vertices = [
            [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],  # 背面
            [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]       # 前面
        ]
        self.edges = [
            [0, 1], [1, 2], [2, 3], [3, 0],  # 背面
            [4, 5], [5, 6], [6, 7], [7, 4],  # 前面
            [0, 4], [1, 5], [2, 6], [3, 7]   # 側面
        ]
        self.faces = [
            [0, 1, 2, 3],  # 背面
            [4, 5, 6, 7],  # 前面
            [0, 1, 5, 4],  # 下
            [1, 2, 6, 5],  # 右
            [2, 3, 7, 6],  # 上
            [3, 0, 4, 7]   # 左
        ]


class 四面体(Shape3D):
    """四面体"""

    def __init__(self):
        super().__init__()
        # 正四面体の頂点
        a = 1.0
        self.vertices = [
            [a, a, a], [-a, -a, a], [-a, a, -a], [a, -a, -a]
        ]
        self.edges = [
            [0, 1], [1, 2], [2, 0],  # 底面
            [0, 3], [1, 3], [2, 3]   # 側面
        ]
        self.faces = [
            [0, 1, 2],
            [0, 3, 1],
            [0, 2, 3],
            [1, 3, 2]
        ]


class 八面体(Shape3D):
    """八面体"""

    def __init__(self):
        super().__init__()
        self.vertices = [
            [1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]
        ]
        self.edges = [
            [0, 2], [2, 1], [1, 3], [3, 0],  # 赤道
            [0, 4], [2, 4], [1, 4], [3, 4],  # 上半球
            [0, 5], [2, 5], [1, 5], [3, 5]   # 下半球
        ]
        self.faces = [
            [4, 0, 2], [4, 2, 1], [4, 1, 3], [4, 3, 0],
            [5, 2, 0], [5, 1, 2], [5, 3, 1], [5, 0, 3]
        ]


class 正三角形(Shape3D):
    """3枚の三角形を辺でつないだ3D形状"""

    def __init__(self):
        super().__init__()
        # 底面に正三角形、上に1頂点を置いて3枚の三角形を構成
        h = math.sqrt(3) / 2
        self.vertices = [
            [0, -0.7, 0],              # 頂点（上）
            [0, 0.35, 2 * h / 3],      # 底面 前
            [-0.5, 0.35, -h / 3],      # 底面 左
            [0.5, 0.35, -h / 3]        # 底面 右
        ]

        # 三角形3枚: (0,1,2), (0,2,3), (0,3,1)
        self.edges = [
            [0, 1], [0, 2], [0, 3],
            [1, 2], [2, 3], [3, 1]
        ]
        self.faces = [
            [0, 1, 2],
            [0, 2, 3],
            [0, 3, 1]
        ]


class 円柱(Shape3D):
    """円柱（高解像度ワイヤーフレーム）"""

    def __init__(self):
        super().__init__()
        # 上円と下円の頂点
        radius = 1.0
        height = 2.0
        segments = 16  # 解像度を向上

        self.vertices = []
        self.edges = []
        self.faces = []

        # 上円
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            x = radius * math.cos(angle)
            z = radius * math.sin(angle)
            self.vertices.append([x, height/2, z])

        # 下円
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            x = radius * math.cos(angle)
            z = radius * math.sin(angle)
            self.vertices.append([x, -height/2, z])

        # 上円の辺
        for i in range(segments):
            self.edges.append([i, (i + 1) % segments])

        # 下円の辺
        for i in range(segments):
            self.edges.append([i + segments, ((i + 1) % segments) + segments])

        # 縦の辺
        for i in range(segments):
            self.edges.append([i, i + segments])

        # 上面・下面
        self.faces.append([i for i in range(segments)])
        self.faces.append([i + segments for i in range(segments - 1, -1, -1)])

        # 側面（四角形）
        for i in range(segments):
            next_i = (i + 1) % segments
            self.faces.append([i, next_i, next_i + segments, i + segments])


class 円錐(Shape3D):
    """円錐（高解像度ワイヤーフレーム）"""

    def __init__(self):
        super().__init__()
        # 頂点と底面円
        radius = 1.0
        height = 2.0
        segments = 16  # 解像度を向上

        self.vertices = [[0, height/2, 0]]  # 頂点
        self.edges = []
        self.faces = []

        # 底面円
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            x = radius * math.cos(angle)
            z = radius * math.sin(angle)
            self.vertices.append([x, -height/2, z])

        # 底面の辺
        for i in range(segments):
            self.edges.append([i + 1, ((i + 1) % segments) + 1])

        # 側面の辺（頂点から底面へ）
        for i in range(segments):
            self.edges.append([0, i + 1])

        # 側面（三角形）
        for i in range(segments):
            next_i = ((i + 1) % segments) + 1
            self.faces.append([0, i + 1, next_i])

        # 底面
        self.faces.append([i for i in range(segments, 0, -1)])


class 球(Shape3D):
    """球（高解像度ワイヤーフレーム）"""

    def __init__(self):
        super().__init__()
        radius = 1.0
        segments = 16  # 解像度を大幅に向上

        self.vertices = []
        self.edges = []
        self.faces = []

        # 緯度線（水平方向の分割を増やす）
        lat_segments = segments // 2  # 緯度方向の分割
        for lat in range(lat_segments + 1):
            phi = math.pi * lat / lat_segments
            for lon in range(segments):
                theta = 2 * math.pi * lon / segments
                x = radius * math.sin(phi) * math.cos(theta)
                y = radius * math.cos(phi)
                z = radius * math.sin(phi) * math.sin(theta)
                self.vertices.append([x, y, z])

        points_per_lat = segments

        # 緯度線（同じ緯度上の点をつなぐ）
        for lat in range(lat_segments):
            for lon in range(segments):
                current = lat * points_per_lat + lon
                next_lon = lat * points_per_lat + ((lon + 1) % segments)
                self.edges.append([current, next_lon])

        # 経度線（同じ経度上の点をつなぐ）
        for lon in range(segments):
            for lat in range(lat_segments):
                current = lat * points_per_lat + lon
                next_lat = (lat + 1) * points_per_lat + lon
                self.edges.append([current, next_lat])

        # 面（緯度経度グリッドの四角形）
        for lat in range(lat_segments):
            for lon in range(segments):
                next_lon = (lon + 1) % segments
                a = lat * points_per_lat + lon
                b = lat * points_per_lat + next_lon
                c = (lat + 1) * points_per_lat + next_lon
                d = (lat + 1) * points_per_lat + lon
                self.faces.append([a, b, c, d])


class トーラス(Shape3D):
    """トーラス（高解像度ドーナツ形）"""

    def __init__(self):
        super().__init__()
        major_radius = 1.5  # 外径
        minor_radius = 0.5  # 内径
        major_segments = 12  # 外周の分割を増加
        minor_segments = 8   # 内周の分割を増加
        self.major_segments = major_segments
        self.minor_segments = minor_segments

        self.vertices = []
        self.edges = []
        self.faces = []

        for i in range(major_segments):
            major_angle = 2 * math.pi * i / major_segments
            center_x = major_radius * math.cos(major_angle)
            center_z = major_radius * math.sin(major_angle)

            for j in range(minor_segments):
                minor_angle = 2 * math.pi * j / minor_segments
                x = center_x + minor_radius * math.cos(minor_angle) * math.cos(major_angle)
                y = minor_radius * math.sin(minor_angle)
                z = center_z + minor_radius * math.cos(minor_angle) * math.sin(major_angle)
                self.vertices.append([x, y, z])

        # 辺を作成
        for i in range(major_segments):
            for j in range(minor_segments):
                current = i * minor_segments + j
                # 同じリング内の次の点
                next_j = (j + 1) % minor_segments
                self.edges.append([current, i * minor_segments + next_j])
                # 次のリングの同じ位置
                next_i = (i + 1) % major_segments
                self.edges.append([current, next_i * minor_segments + j])

                # 面（四角形）
                self.faces.append([
                    current,
                    i * minor_segments + next_j,
                    next_i * minor_segments + next_j,
                    next_i * minor_segments + j
                ])


class 正十二面体(Shape3D):
    """正十二面体"""

    def __init__(self):
        super().__init__()
        phi = (1 + math.sqrt(5)) / 2  # 黄金比
        inv_phi = 1 / phi
        scale = 0.85

        # 正十二面体の標準頂点
        self.vertices = []

        # (±1, ±1, ±1)
        for sx in (-1, 1):
            for sy in (-1, 1):
                for sz in (-1, 1):
                    self.vertices.append([sx, sy, sz])

        # (0, ±1/φ, ±φ)
        for sy in (-1, 1):
            for sz in (-1, 1):
                self.vertices.append([0, sy * inv_phi, sz * phi])

        # (±1/φ, ±φ, 0)
        for sx in (-1, 1):
            for sy in (-1, 1):
                self.vertices.append([sx * inv_phi, sy * phi, 0])

        # (±φ, 0, ±1/φ)
        for sx in (-1, 1):
            for sz in (-1, 1):
                self.vertices.append([sx * phi, 0, sz * inv_phi])

        # サイズ調整
        self.vertices = [[x * scale, y * scale, z * scale] for x, y, z in self.vertices]

        # 最短距離の頂点ペアを辺として採用（正十二面体は30辺）
        dist2_table = {}
        min_dist2 = float("inf")
        for i in range(len(self.vertices)):
            for j in range(i + 1, len(self.vertices)):
                x1, y1, z1 = self.vertices[i]
                x2, y2, z2 = self.vertices[j]
                d2 = (x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2
                dist2_table[(i, j)] = d2
                if d2 < min_dist2 and d2 > 1e-12:
                    min_dist2 = d2

        tolerance = min_dist2 * 0.02
        self.edges = [
            [i, j]
            for (i, j), d2 in dist2_table.items()
            if abs(d2 - min_dist2) <= tolerance
        ]

        # 辺グラフから五角形サイクルを抽出して面を構成
        adjacency = [set() for _ in range(len(self.vertices))]
        for i, j in self.edges:
            adjacency[i].add(j)
            adjacency[j].add(i)

        def canonical_cycle(cycle):
            n = len(cycle)
            candidates = []
            for offset in range(n):
                candidates.append(tuple(cycle[offset:] + cycle[:offset]))
            reversed_cycle = list(reversed(cycle))
            for offset in range(n):
                candidates.append(tuple(reversed_cycle[offset:] + reversed_cycle[:offset]))
            return min(candidates)

        cycles = set()

        def dfs(start, path, remaining_depth):
            current = path[-1]
            if remaining_depth == 0:
                if start in adjacency[current]:
                    cycles.add(canonical_cycle(path))
                return
            for nxt in adjacency[current]:
                if nxt in path:
                    continue
                dfs(start, path + [nxt], remaining_depth - 1)

        for start in range(len(self.vertices)):
            dfs(start, [start], 4)

        self.faces = [list(cycle) for cycle in sorted(cycles)]


class 正二十面体(Shape3D):
    """正二十面体"""

    def __init__(self):
        super().__init__()
        phi = (1 + math.sqrt(5)) / 2
        scale = 0.75

        self.vertices = []

        # (0, ±1, ±φ)
        for sy in (-1, 1):
            for sz in (-1, 1):
                self.vertices.append([0, sy, sz * phi])

        # (±1, ±φ, 0)
        for sx in (-1, 1):
            for sy in (-1, 1):
                self.vertices.append([sx, sy * phi, 0])

        # (±φ, 0, ±1)
        for sx in (-1, 1):
            for sz in (-1, 1):
                self.vertices.append([sx * phi, 0, sz])

        self.vertices = [[x * scale, y * scale, z * scale] for x, y, z in self.vertices]

        # 最短距離の頂点ペアを辺として採用（正二十面体は30辺）
        dist2_table = {}
        min_dist2 = float("inf")
        for i in range(len(self.vertices)):
            for j in range(i + 1, len(self.vertices)):
                x1, y1, z1 = self.vertices[i]
                x2, y2, z2 = self.vertices[j]
                d2 = (x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2
                dist2_table[(i, j)] = d2
                if d2 < min_dist2 and d2 > 1e-12:
                    min_dist2 = d2

        tolerance = min_dist2 * 0.02
        self.edges = [
            [i, j]
            for (i, j), d2 in dist2_table.items()
            if abs(d2 - min_dist2) <= tolerance
        ]

        # 辺グラフから三角形面を抽出（正二十面体は20面）
        adjacency = [set() for _ in range(len(self.vertices))]
        for i, j in self.edges:
            adjacency[i].add(j)
            adjacency[j].add(i)

        triangles = set()
        for i in range(len(self.vertices)):
            neighbors = sorted(adjacency[i])
            for idx_j in range(len(neighbors)):
                j = neighbors[idx_j]
                for idx_k in range(idx_j + 1, len(neighbors)):
                    k = neighbors[idx_k]
                    if k in adjacency[j]:
                        triangles.add(tuple(sorted((i, j, k))))

        self.faces = [list(face) for face in sorted(triangles)]


class 三角柱(Shape3D):
    """三角柱"""

    def __init__(self):
        super().__init__()
        h = math.sqrt(3) / 2
        y_top = 0.7
        y_bottom = -0.7

        self.vertices = [
            [0, y_top, 2 * h / 3],      # 上 前
            [-0.5, y_top, -h / 3],      # 上 左
            [0.5, y_top, -h / 3],       # 上 右
            [0, y_bottom, 2 * h / 3],   # 下 前
            [-0.5, y_bottom, -h / 3],   # 下 左
            [0.5, y_bottom, -h / 3]     # 下 右
        ]

        self.edges = [
            [0, 1], [1, 2], [2, 0],
            [3, 4], [4, 5], [5, 3],
            [0, 3], [1, 4], [2, 5]
        ]

        self.faces = [
            [0, 1, 2],          # 上面
            [5, 4, 3],          # 下面
            [0, 1, 4, 3],
            [1, 2, 5, 4],
            [2, 0, 3, 5]
        ]


class 五角錐(Shape3D):
    """五角錐"""

    def __init__(self):
        super().__init__()
        radius = 0.9
        apex_y = 1.0
        base_y = -0.6
        sides = 5

        self.vertices = [[0, apex_y, 0]]

        for i in range(sides):
            angle = -math.pi / 2 + 2 * math.pi * i / sides
            x = radius * math.cos(angle)
            z = radius * math.sin(angle)
            self.vertices.append([x, base_y, z])

        self.edges = []
        self.faces = []

        # 側面の辺
        for i in range(1, sides + 1):
            self.edges.append([0, i])

        # 底面の辺
        for i in range(1, sides + 1):
            next_i = 1 + (i % sides)
            self.edges.append([i, next_i])

        # 側面（三角形）
        for i in range(1, sides + 1):
            next_i = 1 + (i % sides)
            self.faces.append([0, i, next_i])

        # 底面（五角形）
        self.faces.append([i for i in range(sides, 0, -1)])


class RotatingShape3D:
    """3D回転図形のアニメーション"""

    def __init__(self, root):
        self.root = root
        self.root.title("3D図形回転アニメーション - 拡張版")
        self.canvas_width = 900
        self.canvas_height = 620
        self.root.geometry(f"{self.canvas_width}x800")
        self.root.minsize(860, 760)
        self.theme = {
            "root_bg": "#0e131c",
            "panel_bg": "#151c27",
            "canvas_bg": "#05070a",
            "text": "#e7edf7",
            "button_bg": "#253246",
            "button_active": "#32435f",
            "menu_bg": "#1b2432",
            "trough": "#2a364b",
            "accent": "#3a4f72"
        }
        self.root.configure(bg=self.theme["root_bg"])

        # キャンバス作成
        self.canvas = tk.Canvas(
            root,
            width=self.canvas_width,
            height=self.canvas_height,
            bg=self.theme["canvas_bg"],
            highlightthickness=0
        )
        self.canvas.pack(padx=12, pady=(12, 8), fill="both", expand=True)

        # コントロールパネル
        self.control_frame = tk.Frame(root, bg=self.theme["panel_bg"], padx=10, pady=8)
        self.control_frame.pack(fill="x", padx=12, pady=(0, 6))
        for col in range(8):
            self.control_frame.grid_columnconfigure(col, pad=4)
        label_style = {"bg": self.theme["panel_bg"], "fg": self.theme["text"]}
        scale_style = {
            "bg": self.theme["panel_bg"],
            "fg": self.theme["text"],
            "highlightthickness": 0,
            "troughcolor": self.theme["trough"],
            "activebackground": self.theme["accent"],
            "bd": 0,
            "length": 135,
            "sliderlength": 18
        }
        button_style = {
            "bg": self.theme["button_bg"],
            "fg": self.theme["text"],
            "activebackground": self.theme["button_active"],
            "activeforeground": self.theme["text"],
            "highlightthickness": 0,
            "bd": 0
        }

        # 図形選択
        tk.Label(self.control_frame, text="図形:", **label_style).grid(row=0, column=0, padx=5)
        self.shape_var = tk.StringVar(value="立方体")
        self.shape_menu = tk.OptionMenu(self.control_frame, self.shape_var,
                                       "立方体", "三角形", "四面体", "八面体",
                                       "円柱", "円錐", "球", "トーラス", "十二面体",
                                       "正二十面体", "三角柱", "五角錐",
                                       command=self.change_shape)
        self.shape_menu.config(
            bg=self.theme["button_bg"],
            fg=self.theme["text"],
            activebackground=self.theme["button_active"],
            activeforeground=self.theme["text"],
            highlightthickness=0,
            bd=0,
            width=12
        )
        self.shape_menu["menu"].config(
            bg=self.theme["menu_bg"],
            fg=self.theme["text"],
            activebackground=self.theme["accent"],
            activeforeground=self.theme["text"]
        )
        self.shape_menu.grid(row=0, column=1, padx=6, pady=(0, 4), sticky="w")

        self.show_faces_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            self.control_frame,
            text="面を貼る",
            variable=self.show_faces_var,
            bg=self.theme["panel_bg"],
            fg=self.theme["text"],
            activebackground=self.theme["panel_bg"],
            activeforeground=self.theme["text"],
            selectcolor=self.theme["panel_bg"],
            highlightthickness=0
        ).grid(row=0, column=2, padx=12, pady=(0, 4), sticky="w")

        # 回転速度コントロール（デフォルト値）
        self.default_speed_x = 0.01
        self.default_speed_y = 0.01
        self.default_speed_z = 0.01

        tk.Label(self.control_frame, text="X速度:", **label_style).grid(row=1, column=0, padx=5)
        self.speed_x_var = tk.DoubleVar(value=self.default_speed_x)
        self.speed_x_scale = tk.Scale(self.control_frame, from_=-0.2, to=0.2,
                                     resolution=0.01, orient=tk.HORIZONTAL,
                                     variable=self.speed_x_var, **scale_style)
        self.speed_x_scale.grid(row=1, column=1, padx=6, pady=2)

        tk.Label(self.control_frame, text="Y速度:", **label_style).grid(row=1, column=2, padx=5)
        self.speed_y_var = tk.DoubleVar(value=self.default_speed_y)
        self.speed_y_scale = tk.Scale(self.control_frame, from_=-0.2, to=0.2,
                                     resolution=0.01, orient=tk.HORIZONTAL,
                                     variable=self.speed_y_var, **scale_style)
        self.speed_y_scale.grid(row=1, column=3, padx=6, pady=2)

        tk.Label(self.control_frame, text="Z速度:", **label_style).grid(row=1, column=4, padx=5)
        self.speed_z_var = tk.DoubleVar(value=self.default_speed_z)
        self.speed_z_scale = tk.Scale(self.control_frame, from_=-0.2, to=0.2,
                                     resolution=0.01, orient=tk.HORIZONTAL,
                                     variable=self.speed_z_var, **scale_style)
        self.speed_z_scale.grid(row=1, column=5, padx=6, pady=2)
        self.active_speed_axis = "x"
        self._bind_speed_scale(self.speed_x_scale, self.speed_x_var, "x")
        self._bind_speed_scale(self.speed_y_scale, self.speed_y_var, "y")
        self._bind_speed_scale(self.speed_z_scale, self.speed_z_var, "z")

        # リセットボタン
        tk.Button(
            self.control_frame, text="リセット", command=self.reset_rotation, **button_style
        ).grid(row=1, column=6, padx=12, pady=2)
        tk.Button(
            self.control_frame, text="終了", command=self.exit_app, **button_style
        ).grid(row=1, column=7, padx=(0, 8), pady=2)

        # 情報表示
        self.info_label = tk.Label(
            root,
            text="キーボード: 1-0,Q,Wで図形切り替え, 矢印キーで速度調整, Fで面ON/OFF(面ONで影), Rで回転リセット, Eで終了, F11で全画面, ESCで全画面解除",
            bg=self.theme["root_bg"],
            fg=self.theme["text"]
        )
        self.info_label.pack(pady=(0, 10))

        # 図形の初期化
        self.shapes = {
            "立方体": 立方体(),
            "三角形": 正三角形(),
            "四面体": 四面体(),
            "八面体": 八面体(),
            "円柱": 円柱(),
            "円錐": 円錐(),
            "球": 球(),
            "トーラス": トーラス(),
            "十二面体": 正十二面体(),
            "正二十面体": 正二十面体(),
            "三角柱": 三角柱(),
            "五角錐": 五角錐()
        }
        self.current_shape = self.shapes["立方体"]

        # 回転角度
        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0
        self.is_fullscreen = False

        # キーボードイベント
        self.root.bind('<Key>', self.on_key_press)
        self.root.bind('<F11>', self.toggle_fullscreen)

        # アニメーション開始
        self.animate()

    def rotate_point_x(self, point, angle):
        """X軸回転"""
        x, y, z = point
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return [x, y * cos_a - z * sin_a, y * sin_a + z * cos_a]

    def rotate_point_y(self, point, angle):
        """Y軸回転"""
        x, y, z = point
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return [x * cos_a + z * sin_a, y, -x * sin_a + z * cos_a]

    def rotate_point_z(self, point, angle):
        """Z軸回転"""
        x, y, z = point
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return [x * cos_a - y * sin_a, x * sin_a + y * cos_a, z]

    def project_3d_to_2d(self, point_3d, focal_length=3):
        """3D座標を2D画面座標に投影"""
        x, y, z = point_3d
        # 透視投影
        denom = focal_length + z
        if abs(denom) < 1e-6:
            denom = 1e-6 if denom >= 0 else -1e-6
        factor = focal_length / denom
        x_2d = x * factor
        y_2d = y * factor
        return x_2d, y_2d

    def normalize_vector(self, vec):
        """ベクトル正規化"""
        x, y, z = vec
        length = math.sqrt(x * x + y * y + z * z)
        if length < 1e-9:
            return [0.0, 0.0, 0.0]
        return [x / length, y / length, z / length]

    def get_face_normal(self, vertices, face):
        """面法線を計算"""
        if len(face) < 3:
            return [0.0, 1.0, 0.0]
        p0 = vertices[face[0]]
        p1 = vertices[face[1]]
        p2 = vertices[face[2]]
        ux, uy, uz = p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2]
        vx, vy, vz = p2[0] - p0[0], p2[1] - p0[1], p2[2] - p0[2]
        nx = uy * vz - uz * vy
        ny = uz * vx - ux * vz
        nz = ux * vy - uy * vx
        return self.normalize_vector([nx, ny, nz])

    def get_face_center(self, vertices, face):
        """面重心を計算"""
        count = len(face)
        if count == 0:
            return [0.0, 0.0, 0.0]
        cx = sum(vertices[idx][0] for idx in face) / count
        cy = sum(vertices[idx][1] for idx in face) / count
        cz = sum(vertices[idx][2] for idx in face) / count
        return [cx, cy, cz]

    def expand_polygon_points(self, points, scale):
        """ポリゴンを重心基準で拡大縮小"""
        if len(points) < 6:
            return points
        xs = points[0::2]
        ys = points[1::2]
        cx = sum(xs) / len(xs)
        cy = sum(ys) / len(ys)
        expanded = []
        for i in range(0, len(points), 2):
            expanded.append(cx + (points[i] - cx) * scale)
            expanded.append(cy + (points[i + 1] - cy) * scale)
        return expanded

    def convex_hull_2d(self, points):
        """単調連鎖法で2D凸包を取得"""
        unique_points = sorted(set(points))
        if len(unique_points) <= 2:
            return unique_points

        def cross(o, a, b):
            return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

        lower = []
        for p in unique_points:
            while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
                lower.pop()
            lower.append(p)

        upper = []
        for p in reversed(unique_points):
            while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
                upper.pop()
            upper.append(p)

        return lower[:-1] + upper[:-1]

    def _bind_speed_scale(self, scale_widget, speed_var, axis):
        """速度スライダーのマウス/フォーカス操作を設定"""
        scale_widget.configure(takefocus=1)
        scale_widget.bind(
            "<Button-1>",
            lambda event, s=scale_widget, v=speed_var, a=axis: self._on_speed_scale_pointer(event, s, v, a)
        )
        scale_widget.bind(
            "<B1-Motion>",
            lambda event, s=scale_widget, v=speed_var, a=axis: self._on_speed_scale_pointer(event, s, v, a)
        )
        scale_widget.bind("<FocusIn>", lambda _event, a=axis: self._set_active_speed_axis(a))

    def _set_active_speed_axis(self, axis):
        """矢印キー操作対象の軸を更新"""
        self.active_speed_axis = axis

    def _set_speed_scale_value_from_pointer(self, event, scale_widget, speed_var):
        """マウス位置からスライダー値を算出して設定"""
        width = max(1, scale_widget.winfo_width())
        from_value = float(scale_widget.cget("from"))
        to_value = float(scale_widget.cget("to"))
        resolution = float(scale_widget.cget("resolution"))

        ratio = min(max(event.x / width, 0.0), 1.0)
        value = from_value + (to_value - from_value) * ratio

        if resolution > 0:
            steps = round((value - from_value) / resolution)
            value = from_value + steps * resolution

        low, high = sorted((from_value, to_value))
        speed_var.set(min(max(value, low), high))

    def _on_speed_scale_pointer(self, event, scale_widget, speed_var, axis):
        """クリック位置に直接ジャンプし、ドラッグでも追従"""
        self._set_active_speed_axis(axis)
        self._set_speed_scale_value_from_pointer(event, scale_widget, speed_var)
        scale_widget.focus_set()
        return "break"

    def _adjust_active_speed_with_arrow(self, keysym):
        """矢印キーで選択中スライダー値を増減"""
        axis_to_var = {
            "x": self.speed_x_var,
            "y": self.speed_y_var,
            "z": self.speed_z_var
        }
        axis_to_scale = {
            "x": self.speed_x_scale,
            "y": self.speed_y_scale,
            "z": self.speed_z_scale
        }
        axis = self.active_speed_axis if self.active_speed_axis in axis_to_var else "x"
        speed_var = axis_to_var[axis]
        scale_widget = axis_to_scale[axis]

        step = float(scale_widget.cget("resolution"))
        if step <= 0:
            step = 0.01
        from_value = float(scale_widget.cget("from"))
        to_value = float(scale_widget.cget("to"))
        low, high = sorted((from_value, to_value))
        delta = step if keysym in ("Right", "Up") else -step
        next_value = speed_var.get() + delta
        next_value = min(max(next_value, low), high)
        if step > 0:
            snapped = from_value + round((next_value - from_value) / step) * step
            next_value = min(max(snapped, low), high)
        speed_var.set(next_value)

    def _rotate_and_project_without_numpy(self, vertices, center_x, center_y, scale, focal_length):
        """NumPy未導入時の回転・投影"""
        rotated_vertices = []
        screen_points = []

        for vertex in vertices:
            rotated = self.rotate_point_x(vertex, self.angle_x)
            rotated = self.rotate_point_y(rotated, self.angle_y)
            rotated = self.rotate_point_z(rotated, self.angle_z)
            rotated_vertices.append(rotated)

            x_2d, y_2d = self.project_3d_to_2d(rotated, focal_length=focal_length)
            screen_points.append((center_x + x_2d * scale, center_y - y_2d * scale))

        return rotated_vertices, screen_points

    def _draw_simple_faces_without_numpy(self, rotated_vertices, screen_points):
        """NumPy未導入時の簡易面描画"""
        face_draw_items = []

        for face in self.current_shape.get_faces():
            if len(face) < 3:
                continue

            z_depth = sum(rotated_vertices[idx][2] for idx in face) / len(face)
            points = []
            for idx in face:
                x_pos, y_pos = screen_points[idx]
                points.extend([x_pos, y_pos])

            shade = int(max(65, min(205, 145 + z_depth * 28)))
            color = f"#{shade:02x}{min(255, shade + 14):02x}{min(255, shade + 32):02x}"
            face_draw_items.append((z_depth, points, color))

        face_draw_items.sort(key=lambda item: item[0], reverse=True)
        for _, points, color in face_draw_items:
            self.canvas.create_polygon(points, fill=color, outline="")

    def change_shape(self, shape_name):
        """図形を変更"""
        self.current_shape = self.shapes[shape_name]
        self.reset_angles()

    def reset_angles(self):
        """回転角度のみリセット"""
        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0

    def reset_rotation(self):
        """回転をデフォルト状態にリセット"""
        self.reset_angles()
        self.speed_x_var.set(self.default_speed_x)
        self.speed_y_var.set(self.default_speed_y)
        self.speed_z_var.set(self.default_speed_z)

    def toggle_fullscreen(self, event=None):
        """全画面表示を切り替え"""
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes("-fullscreen", self.is_fullscreen)
        return "break"

    def exit_app(self):
        """アプリを終了"""
        if self.is_fullscreen:
            self.root.attributes("-fullscreen", False)
            self.is_fullscreen = False
        self.root.quit()

    def on_key_press(self, event):
        """キーボードイベント"""
        if event.keysym in ("Left", "Right", "Up", "Down"):
            if not isinstance(event.widget, tk.Scale):
                self._adjust_active_speed_with_arrow(event.keysym)
                return "break"
            return

        key = event.char.lower() if event.char else ""
        shape_mapping = {
            '1': "立方体",
            '2': "三角形",
            '3': "四面体",
            '4': "八面体",
            '5': "円柱",
            '6': "円錐",
            '7': "球",
            '8': "トーラス",
            '9': "十二面体",
            '0': "正二十面体",
            'q': "三角柱",
            'w': "五角錐"
        }
        if key in shape_mapping:
            self.change_shape(shape_mapping[key])
            self.shape_var.set(shape_mapping[key])
        elif key == 'f':
            self.show_faces_var.set(not self.show_faces_var.get())
        elif key == 'r':
            self.reset_rotation()
        elif key == 'e':
            self.exit_app()
        elif event.keysym == 'Escape':
            if self.is_fullscreen:
                self.is_fullscreen = False
                self.root.attributes("-fullscreen", False)

    def animate(self):
        """アニメーション実行"""
        # キャンバスをクリア
        self.canvas.delete("all")

        # 回転角度を更新
        self.angle_x += self.speed_x_var.get()
        self.angle_y += self.speed_y_var.get()
        self.angle_z += self.speed_z_var.get()

        vertices = self.current_shape.get_vertices()
        if not vertices:
            self.root.after(16, self.animate)
            return

        # 画面座標に変換
        canvas_w = max(1, self.canvas.winfo_width())
        canvas_h = max(1, self.canvas.winfo_height())
        center_x, center_y = canvas_w / 2, canvas_h / 2
        scale = min(canvas_w, canvas_h) * 0.16
        focal_length = 3.0

        show_faces = bool(self.show_faces_var.get() and self.current_shape.get_faces())
        if np is None:
            rotated_vertices, screen_points = self._rotate_and_project_without_numpy(
                vertices, center_x, center_y, scale, focal_length
            )

            if show_faces:
                self._draw_simple_faces_without_numpy(rotated_vertices, screen_points)

            for edge in self.current_shape.get_edges():
                start, end = edge
                x1, y1 = screen_points[start]
                x2, y2 = screen_points[end]
                self.canvas.create_line(x1, y1, x2, y2, fill='white', width=2)

            self.canvas.create_text(
                350, 30, text=f"現在の図形: {self.shape_var.get()}",
                fill='white', font=('Arial', 12)
            )
            self.root.after(16, self.animate)
            return

        vertices_np = np.asarray(vertices, dtype=np.float64)

        # NumPyで回転行列を適用（X -> Y -> Z）
        cx, sx = math.cos(self.angle_x), math.sin(self.angle_x)
        cy, sy = math.cos(self.angle_y), math.sin(self.angle_y)
        cz, sz = math.cos(self.angle_z), math.sin(self.angle_z)
        rx = np.array([[1.0, 0.0, 0.0], [0.0, cx, -sx], [0.0, sx, cx]], dtype=np.float64)
        ry = np.array([[cy, 0.0, sy], [0.0, 1.0, 0.0], [-sy, 0.0, cy]], dtype=np.float64)
        rz = np.array([[cz, -sz, 0.0], [sz, cz, 0.0], [0.0, 0.0, 1.0]], dtype=np.float64)
        rotated_np = vertices_np @ rx.T @ ry.T @ rz.T

        def project_to_screen(points_3d):
            z = points_3d[:, 2]
            denom = focal_length + z
            denom = np.where(np.abs(denom) < 1e-6, np.where(denom >= 0, 1e-6, -1e-6), denom)
            factor = focal_length / denom
            x_2d = points_3d[:, 0] * factor
            y_2d = points_3d[:, 1] * factor
            screen = np.empty((points_3d.shape[0], 2), dtype=np.float64)
            screen[:, 0] = center_x + x_2d * scale
            screen[:, 1] = center_y - y_2d * scale
            return screen

        screen_np = project_to_screen(rotated_np)

        # 固定光源（オブジェクトの真上から）
        light_direction = np.array([0.0, -1.0, 0.0], dtype=np.float64)
        light_direction /= np.linalg.norm(light_direction)
        incoming_light = -light_direction
        shadow_plane_y = -2.0

        # 面を貼っているときだけ影を描画
        object_center = None
        if show_faces:
            object_center = rotated_np.mean(axis=0)

            # トーラスは穴を残すため面投影、その他はシルエット影で自然化
            if self.shape_var.get() == "トーラス":
                dy = light_direction[1]
                if abs(dy) < 1e-6:
                    dy = -1e-6
                t = (shadow_plane_y - rotated_np[:, 1]) / dy
                t = np.clip(t, 0.0, 20.0)
                shadow_points = rotated_np + t[:, None] * light_direction[None, :]
                shadow_screen = project_to_screen(shadow_points)

                major_segments = getattr(self.current_shape, "major_segments", 12)
                minor_segments = getattr(self.current_shape, "minor_segments", 8)
                center = shadow_screen.mean(axis=0)

                outer_loop = []
                inner_loop = []
                for i in range(major_segments):
                    start = i * minor_segments
                    ring = shadow_screen[start:start + minor_segments]
                    if len(ring) < 3:
                        continue
                    distances = np.linalg.norm(ring - center, axis=1)
                    outer_loop.append(tuple(ring[np.argmax(distances)]))
                    inner_loop.append(tuple(ring[np.argmin(distances)]))

                if len(outer_loop) >= 3 and len(inner_loop) >= 3:
                    outer_points = []
                    for x, y in outer_loop:
                        outer_points.extend([x, y])
                    mid_points = self.expand_polygon_points(outer_points, 1.025)
                    outer_soft_points = self.expand_polygon_points(outer_points, 1.055)

                    bg_color = self.canvas.cget("bg")
                    self.canvas.create_polygon(outer_soft_points, fill="#263145", outline="")
                    self.canvas.create_polygon(mid_points, fill="#1a2434", outline="")
                    self.canvas.create_polygon(outer_points, fill="#111a28", outline="")

                    inner_points = []
                    for x, y in reversed(inner_loop):
                        inner_points.extend([x, y])
                    inner_soft_points = self.expand_polygon_points(inner_points, 1.015)
                    self.canvas.create_polygon(inner_soft_points, fill=bg_color, outline="")
                    self.canvas.create_polygon(inner_points, fill=bg_color, outline="")
            else:
                dy = light_direction[1]
                if abs(dy) < 1e-6:
                    dy = -1e-6
                t = (shadow_plane_y - rotated_np[:, 1]) / dy
                t = np.clip(t, 0.0, 20.0)
                shadow_points = rotated_np + t[:, None] * light_direction[None, :]
                shadow_screen = project_to_screen(shadow_points)
                hull = self.convex_hull_2d([tuple(pt) for pt in shadow_screen.tolist()])
                if len(hull) >= 3:
                    core_points = []
                    for x, y in hull:
                        core_points.extend([x, y])
                    mid_points = self.expand_polygon_points(core_points, 1.035)
                    outer_points = self.expand_polygon_points(core_points, 1.075)
                    self.canvas.create_polygon(outer_points, fill="#2a3445", outline="")
                    self.canvas.create_polygon(mid_points, fill="#1d2736", outline="")
                    self.canvas.create_polygon(core_points, fill="#121b28", outline="")

        # 面を描画（自然な拡散反射）
        if show_faces:
            face_draw_items = []
            if object_center is None:
                object_center = np.zeros(3, dtype=np.float64)
            camera_position = np.array([0.0, 0.0, -4.0], dtype=np.float64)

            for face in self.current_shape.get_faces():
                if len(face) < 3:
                    continue

                idx = np.asarray(face, dtype=np.int64)
                face_points = rotated_np[idx]
                face_center = face_points.mean(axis=0)
                normal = np.cross(face_points[1] - face_points[0], face_points[2] - face_points[0])
                normal_len = np.linalg.norm(normal)
                if normal_len < 1e-9:
                    continue
                normal /= normal_len
                if np.dot(normal, face_center - object_center) < 0:
                    normal = -normal

                diffuse = max(0.0, float(np.dot(normal, incoming_light)))
                view_dir = camera_position - face_center
                view_len = np.linalg.norm(view_dir)
                if view_len > 1e-9:
                    view_dir /= view_len
                reflected = 2.0 * diffuse * normal - incoming_light
                ref_len = np.linalg.norm(reflected)
                if ref_len > 1e-9:
                    reflected /= ref_len
                specular = max(0.0, float(np.dot(reflected, view_dir))) ** 18

                ambient = 0.22
                intensity = max(0.0, min(1.2, ambient + 0.70 * diffuse + 0.12 * specular))

                # マテリアルを1種類に固定
                shadow_rgb = np.array([50.0, 62.0, 78.0])
                light_rgb = np.array([176.0, 196.0, 218.0])
                t = min(1.0, intensity)
                rgb = shadow_rgb + (light_rgb - shadow_rgb) * t
                if intensity > 1.0:
                    rgb += (intensity - 1.0) * 55.0
                rgb = np.clip(rgb, 0.0, 255.0).astype(np.uint8)
                color = f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

                points = screen_np[idx].reshape(-1).tolist()
                face_draw_items.append((float(face_center[2]), points, color))

            face_draw_items.sort(key=lambda item: item[0], reverse=True)
            for _, points, color in face_draw_items:
                self.canvas.create_polygon(points, fill=color, outline="")

        # 辺を描画
        for edge in self.current_shape.get_edges():
            start, end = edge
            x1, y1 = screen_np[start]
            x2, y2 = screen_np[end]
            self.canvas.create_line(x1, y1, x2, y2, fill='white', width=2)

        # 図形名を表示
        self.canvas.create_text(350, 30, text=f"現在の図形: {self.shape_var.get()}",
                               fill='white', font=('Arial', 12))

        # 次のフレームをスケジュール（約60FPS）
        self.root.after(16, self.animate)


def main():
    """メイン関数"""
    if np is None:
        print("NumPy が見つからないため簡易描画モードで起動します。`pip install numpy` で高品質描画になります。")
    root = tk.Tk()
    app = RotatingShape3D(root)
    root.mainloop()


if __name__ == "__main__":
    main()
