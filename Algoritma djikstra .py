import pandas as pd
import customtkinter as ctk

# Fungsi untuk menemukan node dengan jarak minimum yang belum dikunjungi
def find_min_distance_node(distances, visited):
    min_distance = float('inf')
    min_node = None
    for node, distance in distances.items():
        if not visited[node] and distance < min_distance:
            min_distance = distance
            min_node = node
    return min_node

# Fungsi utama algoritma Dijkstra
def dijkstra(graph, start, end):
    # Validasi jika start atau end tidak ada di graf
    if start not in graph or end not in graph:
        return float('inf'), []

    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous_nodes = {node: None for node in graph}
    visited = {node: False for node in graph}

    while True:
        current_node = find_min_distance_node(distances, visited)
        
        if current_node is None:
            break
        if current_node == end:
            break
        
        visited[current_node] = True

        for neighbor, distance in graph[current_node]:
            if not visited[neighbor]:
                new_distance = distances[current_node] + distance
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous_nodes[neighbor] = current_node

    path = []
    current_node = end
    while current_node is not None:
        path.insert(0, current_node)
        current_node = previous_nodes[current_node]

    if distances[end] == float('inf'):
        return float('inf'), []
    return distances[end], path

# Membaca data dari file CSV
file_path = 'Data Set/Data RSU bakti rahayu.csv'
data = pd.read_csv(file_path)


source_col = 'Node Awal'
target_col = 'Node Tujuan'
distance_col = 'Jarak'

# Membangun graf
graph = {}
for _, row in data.iterrows():
    source = row[source_col]
    target = row[target_col]
    distance = row[distance_col]
    
    if source not in graph:
        graph[source] = []
    if target not in graph:
        graph[target] = []
        
    graph[source].append((target, distance))
    graph[target].append((source, distance))

# Fungsi untuk menampilkan hasil di GUI
def show_result():
    start_node = entry_start.get()
    end_node = entry_end.get()
    
    if not start_node or not end_node:
        result_label.configure(text="Harap masukkan node awal dan tujuan.")
        return
    
    distance, path = dijkstra(graph, start_node, end_node)
    
    if path:
        result_text = f"Rute terpendek dari {start_node} ke {end_node}:\n" \
                      f"{' -> '.join(path)}\n" \
                      f"Total jarak: {distance} unit"
    else:
        result_text = f"Rute dari {start_node} ke {end_node} tidak ditemukan."
    
    result_label.configure(text=result_text)

# GUI dengan customtkinter
ctk.set_appearance_mode("dark")  # Mode dark atau light
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Jalur Terpendek dengan Dijkstra")
app.geometry("500x400")

# Input untuk node awal dan tujuan
label_start = ctk.CTkLabel(app, text="Node Awal:")
label_start.pack(pady=(10, 0))
entry_start = ctk.CTkEntry(app, placeholder_text="Masukkan node awal (misal: Klinik Unesa)")
entry_start.pack(pady=(0, 10), padx=10)

label_end = ctk.CTkLabel(app, text="Node Tujuan:")
label_end.pack(pady=(10, 0))
entry_end = ctk.CTkEntry(app, placeholder_text="Masukkan node tujuan (misal: RSU Bakti Rahayu)")
entry_end.pack(pady=(0, 10), padx=10)

# Tombol untuk mencari jalur terpendek
search_button = ctk.CTkButton(app, text="Cari Jalur Terpendek", command=show_result)
search_button.pack(pady=10)

# Label untuk menampilkan hasil
result_label = ctk.CTkLabel(app, text="", justify="left", wraplength=450)
result_label.pack(pady=10, padx=10)

# Menjalankan aplikasi
app.mainloop()
