import streamlit as st
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import folium
from streamlit_folium import folium_static

# Setup page config
st.set_page_config(page_title="Optimasi Rute Ambulans", layout="wide")

# Tambahkan CSS untuk mempercantik tampilan
st.markdown(
    """
    <style>
    body {
        background-color: #f4f7fc;
        font-family: 'Arial', sans-serif;
    }
    .main-title {
        text-align: left;
        font-size: 38px;
        color: #1f77b4;
        font-weight: bold;
        margin-bottom: 0px;
    }
    .description {
        text-align: left;
        font-size: 20px;
        color: #555;
        margin-bottom: 20px;
    }
    .main-title_menuRS {
        text-align: left;
        font-size: 40px;
        color: black;
        font-weight: bold;
        margin-bottom: 0px;
    }
    .description_menuRS {
        text-align: left;
        font-size: 20px;
        color: #555;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Data Rumah Sakit
rs_data = {

    "Rumah Sakit Bhayangkara": {
        "code": "Rumah Sakit Bhayangkara",
        "file": "Data Set/dataset_Rumah Sakit Bhayangkara.csv",
        "desc": "Rumah Sakit Bhayangkara merupakan salah satu fasilitas kesehatan terbaik di Surabaya yang dikenal dengan kelengkapan fasilitas medisnya dan pelayanan cepat untuk kebutuhan darurat. Rumah sakit ini menyediakan berbagai layanan kesehatan mulai dari unit gawat darurat, rawat inap, rawat jalan, hingga penanganan khusus untuk kasus-kasus kritis. Terletak di Jl. Ahmad Yani No.116, Surabaya, lokasi strategis ini membuat Rumah Sakit Bhayangkara menjadi pilihan utama masyarakat yang membutuhkan pelayanan medis yang profesional dan efisien. Dengan dukungan tenaga medis yang terlatih dan berpengalaman, rumah sakit ini terus berkomitmen untuk memberikan layanan kesehatan terbaik bagi pasien.",
        "image": "Tampilan Aplikasi/1 RS bhayangkara.jpg"
    },
    "Rumah Sakit Ramelan": {
        "code": "Rumah Sakit Ramelan",
        "file": "Data Set/dataset_Rumah Sakit Ramelan.csv",
        "desc": "Rumah Sakit Ramelan adalah rumah sakit terkemuka di Surabaya yang memiliki spesialisasi dalam bidang bedah dan perawatan intensif. Rumah sakit ini menawarkan layanan medis yang komprehensif dengan dukungan teknologi canggih dan tenaga ahli di berbagai bidang kesehatan. Dengan fokus pada penyediaan perawatan berkualitas tinggi, Rumah Sakit Ramelan melayani pasien dengan standar profesionalisme yang tinggi, baik untuk kebutuhan medis rutin maupun darurat. Berlokasi di Jl. Gadung No.1, Surabaya, rumah sakit ini mudah diakses oleh masyarakat yang membutuhkan layanan medis terbaik.",
        "image": "Tampilan Aplikasi/2 RS Ramelan.png"
    },
    "Rumah Sakit Islam": {
        "code": "Rumah Sakit Islam",
        "file": "Data Set/dataset_Rumah Sakit Islam.csv",
        "desc": "Rumah Sakit Islam Surabaya adalah rumah sakit yang mengutamakan prinsip Islami dalam memberikan layanan kesehatan kepada masyarakat. Dengan fasilitas modern dan tenaga medis yang kompeten, rumah sakit ini menawarkan berbagai jenis pelayanan kesehatan mulai dari konsultasi medis, rawat jalan, hingga rawat inap. Berlokasi di Jl. Achmad Jais No.56-58, Surabaya, Rumah Sakit Islam memberikan kenyamanan tambahan bagi pasien dengan pendekatan yang sesuai dengan nilai-nilai Islam.",
        "image": "Tampilan Aplikasi/3 RS Islam Surabaya.jpg"
    },
    "RSU Bakti Rahayu": {
        "code": "RSU Bakti Rahayu",
        "file": "Data Set/dataset_RSU Bakti Rahayu.csv",
        "desc": "RSU Bakti Rahayu adalah rumah sakit unggulan di Surabaya yang menawarkan layanan kesehatan berkualitas dengan harga yang terjangkau. Rumah sakit ini dikenal dengan pelayanan medis yang ramah, cepat, dan efisien untuk memenuhi kebutuhan kesehatan masyarakat. Terletak di Jl. Simpang Dukuh No.3, Surabaya, RSU Bakti Rahayu menyediakan akses mudah dengan fasilitas modern untuk menangani berbagai jenis kasus medis, baik yang bersifat umum maupun spesifik.",
        "image": "Tampilan Aplikasi/4 RSU Bhakti Rahayu.jpg"
    },
    "RS Wiyung Sejahtera": {
        "code": "RS Wiyung Sejahtera",
        "file": "Data Set/dataset_RS Wiyung Sejahtera.csv",
        "desc": "RS Wiyung Sejahtera adalah rumah sakit yang memberikan fokus pada pelayanan kesehatan umum dan penanganan pasien rawat inap. Rumah sakit ini dilengkapi dengan berbagai fasilitas medis yang dirancang untuk memberikan kenyamanan dan pelayanan berkualitas tinggi bagi pasien. Dengan lokasi di Jl. Raya Menganti No.248, Surabaya, RS Wiyung Sejahtera mudah dijangkau dan terus berkomitmen menjadi mitra kesehatan masyarakat Surabaya.",
        "image": "Tampilan Aplikasi/5 RS Wiyung Sejahtera.png"
    },
    "RSUD Soetomo": {
        "code": "RSUD Soetomo",
        "file": "Data Set/dataset RSUD Soetomo.csv",
        "desc": "RSUD Soetomo merupakan rumah sakit rujukan nasional yang dikenal dengan fasilitas medis yang sangat lengkap dan tenaga medis profesional. Rumah sakit ini menyediakan berbagai layanan kesehatan, termasuk penanganan kasus-kasus kritis, operasi kompleks, serta penelitian dan pendidikan di bidang kedokteran. Terletak di Jl. Mayjen Prof. Dr. Moestopo No.6-8, Surabaya, RSUD Soetomo menjadi salah satu institusi kesehatan terkemuka di Indonesia yang terus memberikan kontribusi dalam peningkatan kualitas kesehatan masyarakat.",
        "image": "Tampilan Aplikasi/6 RSUD Soetomo.jpeg"
    },
    "RS RSIA Pura Raharja": {
        "code": "RS RSIA Pura Raharja",
        "file": "Data Set/dataset_RS RSIA Pura Raharja.csv",
        "desc": "Rumah Sakit RSIA Pura Raharja adalah fasilitas kesehatan yang berfokus pada pelayanan ibu dan anak. Rumah sakit ini menawarkan layanan persalinan, pediatrik, dan perawatan kesehatan lainnya dengan standar kualitas tinggi. Dengan suasana yang nyaman dan dukungan tenaga medis yang berpengalaman, RSIA Pura Raharja menjadi pilihan utama bagi keluarga yang membutuhkan pelayanan kesehatan untuk ibu dan anak.",
        "image": "Tampilan Aplikasi/7 RS RSIA Pura Raharja.jpg"
    },
    "RS PHC Surabaya": {
        "code": "RS PHC Surabaya",
        "file": "Data Set/dataset_RS PHC Surabaya.csv",
        "desc": "RS PHC Surabaya adalah rumah sakit yang memiliki keunggulan dalam layanan kesehatan kelautan dan industri. Dengan fasilitas medis modern dan spesialisasi yang mendukung kebutuhan kesehatan tenaga kerja, RS PHC Surabaya memberikan solusi kesehatan yang efektif bagi masyarakat, khususnya yang bekerja di sektor industri dan kelautan. Rumah sakit ini juga dikenal dengan pelayanan yang cepat, efisien, dan berkualitas.",
        "image": "Tampilan Aplikasi/8 RS PHC Surabaya.jpg"
    },
    "Mitra Keluarga Kenjeran": {
        "code": "Mitra Keluarga Kenjeran",
        "file": "Data Set/dataset_RS Mitra Keluarga Kenjeran.csv",
        "desc": "Rumah Sakit Mitra Keluarga Kenjeran adalah fasilitas kesehatan swasta yang menawarkan layanan kesehatan keluarga modern. Rumah sakit ini menyediakan berbagai jenis perawatan medis dengan dukungan peralatan canggih dan tenaga medis yang profesional. Dengan fokus pada kenyamanan dan kepuasan pasien, Mitra Keluarga Kenjeran menjadi salah satu rumah sakit terbaik untuk perawatan keluarga di Surabaya.",
        "image": "Tampilan Aplikasi/9 Mitra Keluarga Kenjeren.jpg"
    },
    "RSI Darus Syifa": {
        "code": "RSI Darus Syifa",
        "file": "Data Set/Data RS DARUS SYIFA.csv",
        "desc": "RSI Darus Syifa adalah rumah sakit yang mengedepankan pelayanan kesehatan berbasis syariah. Rumah sakit ini menawarkan berbagai layanan kesehatan yang mengintegrasikan nilai-nilai Islami dengan teknologi medis modern. Dengan lingkungan yang nyaman dan pelayanan yang profesional, RSI Darus Syifa menjadi pilihan masyarakat yang membutuhkan layanan kesehatan yang sesuai dengan prinsip syariah.",
        "image": "Tampilan Aplikasi/11 RSI Darus Syifa.png"
    },
    "RS Bhakti Dharma Husada": {
        "code": "RS Bhakti Dharma Husada",
        "file": "Data Set/Data RS BDH.csv",
        "desc": "RS Bhakti Dharma Husada adalah rumah sakit dengan spesialisasi pada perawatan geriatri dan layanan rehabilitasi medis. Rumah sakit ini dikenal dengan pelayanan yang ramah dan fasilitas yang lengkap untuk memenuhi kebutuhan pasien, terutama yang memerlukan perawatan lanjutan atau rehabilitasi. Dengan lokasi yang mudah diakses, RS Bhakti Dharma Husada menjadi salah satu pilihan utama di Surabaya.",
        "image": "Tampilan Aplikasi/12 RS BDH.jpg"
    },
    "RS Bunda": {
        "code": "RS Bunda",
        "file": "Data Set/Data RS BUNDA.csv",
        "desc": "RS Bunda adalah rumah sakit yang berfokus pada pelayanan ibu dan anak. Rumah sakit ini menyediakan fasilitas persalinan modern serta perawatan khusus bagi ibu dan bayi. Dengan suasana yang nyaman dan didukung oleh tenaga medis yang berpengalaman, RS Bunda menjadi pilihan yang tepat untuk keluarga yang membutuhkan pelayanan kesehatan berkualitas.",
        "image": "Tampilan Aplikasi/13 RS BUNDA.jpg"
    },
    "RS Mitra Keluarga Darmo": {
        "code": "RS Mitra Keluarga Darmo",
        "file": "Data Set/Data RS MKD.csv",
        "desc": "Rumah Sakit Mitra Keluarga Darmo merupakan fasilitas kesehatan swasta di Surabaya yang menyediakan layanan kesehatan keluarga dengan kualitas terbaik. Rumah sakit ini dilengkapi dengan fasilitas modern dan tenaga medis profesional yang siap menangani berbagai kebutuhan kesehatan masyarakat. Lokasinya yang strategis di pusat kota menjadikan RS Mitra Keluarga Darmo pilihan utama untuk perawatan kesehatan keluarga.",
        "image": "Tampilan Aplikasi/14 RS MKD.jpg"
    },
    "RS Muji Rahayu": {
        "code": "RS Muji Rahayu",
        "file": "Data Set/Data RS MUJI RAHAYU.csv",
        "desc": "RS Muji Rahayu adalah rumah sakit umum yang dikenal dengan layanan kesehatan berkualitas dengan biaya yang terjangkau. Rumah sakit ini menyediakan berbagai jenis layanan kesehatan, mulai dari pemeriksaan rutin hingga penanganan kasus-kasus medis yang kompleks. Dengan fasilitas lengkap dan tenaga medis yang berpengalaman, RS Muji Rahayu menjadi pilihan yang andal untuk masyarakat Surabaya.",
        "image": "Tampilan Aplikasi/15 RS MUJI RAHAYU.jpg"
    },
    "RS Cempaka Putih": {
        "code": "RS Cempaka Putih",
        "file": "Data Set/Data RS Cempaka Putih.csv",
        "desc": "Rumah Sakit Cempaka Putih adalah salah satu fasilitas kesehatan di Surabaya yang menawarkan layanan medis berkualitas untuk masyarakat. Dengan fasilitas yang memadai dan tenaga medis profesional, rumah sakit ini menjadi pilihan masyarakat untuk memenuhi kebutuhan kesehatan dengan layanan yang ramah dan efisien.",
        "image": "Tampilan Aplikasi/10 RS Cempaka Putih.jpeg"
    },
}

node_positions = {
    "Rumah Sakit Bhayangkara": {
        "Klinik Unesa": (0, 0),
        "A1": (1, 0.5),
        "A2": (2, 0.5),
        "A3": (3, 0.5),
        "A4": (4, 0.5),
        "A5": (5, 0.5),
        "A6": (6, 0.5),
        "A7": (7, 0.5),
        "B1": (3, -0.5),
        "B2": (4, -0.5), 
        "B3": (5, -0.5),
        "Rumah Sakit Bhayangkara": (8, 0)
    },

    "Rumah Sakit Ramelan": {
        "Klinik Unesa": (2, 0),      
        "A1": (2.3, 0.8),                
        "A2": (5.2, 2),              
        "A3": (6.5, 1.7),             
        "A4": (7.4, 2.8),                
        "A5": (9.67, 5.8),               
        "A6": (9.2, 6),             
        "A7": (8.6, 2.7),              
        "B1": (5, 0.4),              
        "B2": (7.4, 0),              
        "B3": (7.87, 2),               
        "B4": (10.45, 6.9),              
        "B5": (9.4, 7),               
        "Rumah Sakit Ramelan": (11, 1.32)
    },

    "RS Cempaka Putih": {
    "Klinik Unesa": (190, 88),
    "A1": (201, 119),
    "A2": (86, 168),
    "A3": (48, 185),
    "A4": (-79, 146),
    "A5": (-114, -14),
    "A6": (-126, -62),
    "A7": (-155, -67),
    "RS Cempaka Putih": (-210, -181),
    "B1": (166, 47),
    "B2": (150, 6),
    "B3": (117, 17),
    "B4": (77, -80),
    "B5": (5, -53),
    "B6": (-10, -152),
    "B7": (-108, -126),
    "C1": (-83, -30)
    },


    "RSI Darus Syifa": {
        "Klinik Unesa": (830, -580),
        "A1": (810, -570),
        "A2": (780, -560),
        "A3": (750, -580),
        "A4": (730, -560),
        "A5": (710, -590),
        "A6": (700, -200),
        "A7": (700, -100),
        "A8": (400, -90),
        "A9": (380, -40),
        "A10": (250, -30),
        "A11": (120, -170),
        "A12": (100, -160),
        "A13": (90, -200),
        "RSI Darus Syifa": (110, -220),
        "B1": (650, -270),
    },

    "RS Bhakti Dharma Husada": {
    "Klinik Unesa": (201, -746),
    "A1": (206, -730),
    "A2": (173, -717),
    "A3": (142, -725),
    "A4": (139, -713),
    "A5": (91, -731),
    "A6": (85, -747),
    "A7": (-126, -723),
    "A8": (-120, -662),
    "A9": (-259, -650),
    "A10": (-276, -640),
    "A11": (-301, -519),
    "A12": (-330, -519),
    "A13": (-340, -510),
    "A14": (-327, -469),
    "A15": (-366, -436),
    "RS Bhakti Dharma Husada": (-359, -403),
    "B1": (80, -434),
    "B2": (68, -468),
    "B3": (-351, -349)
    },

    "RS Bunda": {
        "Klinik Unesa": (13.75, -136.75),
    "A1": (17, -129),
    "A2": (35, -129.25),
    "A3": (43.75, -114.75), 
    "A4": (55.75, -116.25),
    "A5": (68.75, -95.75),
    "A6": (81.25, -43.25),
    "A7": (16.75, 18.75),
    "A8": (-10.25, 25.75),
    "RS Bunda": (-92.75, 45.75),
    "B1": (-7.25, -110.75),
    "B2": (-20.75, -112.75),
    "B3": (-22.75, -105.25),
    "B4": (-28.25, -104.25),
    "B5": (-39.25, -81.75),
    "B6": (-12.25, -40.5),
    "B7": (-20.25, -36.25),
    "B8": (-5.75, -15.25),
    "B9": (-18.75, -4.75),
    "B10": (-26.25, 6.75),
    "B11": (-19.25, 18.25)
    },

    "RS Mitra Keluarga Darmo": {
        "Klinik Unesa": (243, -373),
    "A1": (256, -345),
    "A2": (191, -320),
    "A3": (135, -334),
    "A4": (126, -318),
    "A5": (107, -323),
    "A6": (38, -350),
    "A7": (-19, -325),
    "A8": (-106, -158),
    "A9": (10, -109),
    "A10": (50, 84),
    "A11": (-103, 109),
    "A12": (-185, 183),
    "A13": (-183, 213),
    "RS Mitra Keluarga Darmo": (-220, 215),
    "B1": (6, -299),
    "B2": (12, -234),
    "B3": (26, -235),
    "B4": (31, -111)
    },

    "RS Muji Rahayu": {
    "Klinik Unesa": (27.5, -297.5),
    "A1": (34, -282),
    "A2": (79.5, -282.5),
    "A3": (87.5, -253.5),
    "A4": (111.5, -256.5),
    "A5": (137.5, -215.5),
    "A6": (162.5, -110.5),
    "A7": (33.5, 13.5),
    "A8": (-20.5, 27.5),
    "A9": (-170, 65),
    "RS Muji Rahayu": (-149, 63),
    "B1": (-14.5, -245.5),
    "B2": (-41.5, -249.5),
    "B3": (-45.5, -234.5),
    "B4": (-56.5, -232.5),
    "B5": (-78.5, -187.5),
    "B6": (-24.5, -105),
    "B7": (-40.5, -96.5),
    "B8": (-11.5, -54.5),
    "B9": (-37.5, -33.5),
    "B10": (-52.5, -10.5),
    "B11": (-38.5, 12.5)
    }
} 


def load_graph_from_file(file_path):
    try:
        df = pd.read_csv(file_path)
        graph = {}

        all_nodes = pd.concat([df['Node Awal'], df['Node Tujuan']]).unique()
        for node in all_nodes:
            graph[node] = {}

        for _, row in df.iterrows():
            source, target, jarak = row['Node Awal'], row['Node Tujuan'], float(row['Jarak']) * 10
            graph[source][target] = jarak
            graph[target][source] = jarak

        return graph
    except Exception as e:
        st.error(f"Error loading graph: {str(e)}")
        return None


def dijkstra(graph, start, target):
    # Inisialisasi jarak
    distances = {node: float('inf') for node in graph}
    previous_nodes = {node: None for node in graph}
    distances[start] = 0
    
    # Set untuk menyimpan node yang sudah dikunjungi
    unvisited = list(graph.keys())
    
    while unvisited:
        # Pilih node yang belum dikunjungi dengan jarak terkecil
        current_node = min(unvisited, key=lambda node: distances[node])
        
        # Jika sudah mencapai target, bisa berhenti
        if current_node == target:
            break
        
        # Periksa semua tetangga node saat ini
        for neighbor, weight in graph[current_node].items():
            # Hitung jarak baru
            new_distance = distances[current_node] + weight
            
            # Update jarak jika jarak baru lebih pendek
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous_nodes[neighbor] = current_node
        
        # Hapus node saat ini dari daftar yang belum dikunjungi
        unvisited.remove(current_node)
    
    return distances, previous_nodes

def shortest_path(previous_nodes, start, target):
    path = []
    current_node = target
    
    while current_node and current_node != start:
        path.insert(0, current_node)
        current_node = previous_nodes[current_node]
    
    if current_node == start:
        path.insert(0, start)
        return path
    else:
        return None

def draw_graph(graph, path, hospital_name):
    # Create figure
    plt.figure(figsize=(15, 10))
    
    # Get node positions for the selected hospital
    pos = node_positions[hospital_name]
    
    # Draw edges first (so they appear behind nodes)
    for source, targets in graph.items():
        for target, jarak in targets.items():
            # Get positions for source and target nodes
            source_pos = pos[source]
            target_pos = pos[target]
            
            # Determine if this edge is part of the shortest path
            is_path_edge = False
            if path:
                if any((source == p1 and target == p2) or (target == p1 and source == p2) 
                       for p1, p2 in zip(path[:-1], path[1:])):
                    is_path_edge = True
            
            # Draw the edge
            color = 'red' if is_path_edge else 'gray'
            width = 3 if is_path_edge else 1
            plt.plot([source_pos[0], target_pos[0]], 
                    [source_pos[1], target_pos[1]], 
                    color=color, 
                    linewidth=width,
                    zorder=1)
            
            # Add edge jarak label
            mid_x = (source_pos[0] + target_pos[0]) / 2
            mid_y = (source_pos[1] + target_pos[1]) / 2
            plt.text(mid_x, mid_y, f"{int(graph[source][target])}m",
                    fontsize=6, 
                    horizontalalignment='center',
                    verticalalignment='center',
                    bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
    
    # Draw nodes
    for node, (x, y) in pos.items():
        # Determine node color
        if node == 'Klinik Unesa':
            color = 'green'
        elif node == rs_data[hospital_name]["code"]:
            color = 'red'
        else:
            color = 'lightblue'
        
        # Draw the node
        circle = plt.Circle((x, y), 0.2, 
                          color=color, 
                          alpha=0.6, 
                          zorder=2)
        plt.gca().add_patch(circle)
        
        # Add node label
        plt.text(x, y, node,
                fontsize=8,
                horizontalalignment='center',
                verticalalignment='center',
                zorder=3)
    
    # Set plot limits with some padding
    all_x = [x for x, y in pos.values()]
    all_y = [y for x, y in pos.values()]
    plt.xlim(min(all_x) - 1, max(all_x) + 1)
    plt.ylim(min(all_y) - 1, max(all_y) + 1)
    
    # Set title and remove axes
    plt.title(f"Peta Rute ke {hospital_name}", pad=20, size=16)
    plt.gca().set_aspect('equal')
    plt.axis('off')
    
    return plt

def format_distance(meters):
    """Format distance in meters to a readable string with both meters and kilometers"""
    km = meters / 1000
    return f"{meters:.1f} meter ({km:.2f} km)"

# Halaman Utama
def halaman_utama():
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<h1 class="main-title">Optimasi Rute Ambulans Ketintang</h1>', unsafe_allow_html=True)
        st.markdown(
            '<p class="description">Aplikasi ini membantu ambulans menuju pasien dan rumah sakit dengan rute tercepat, '
            'mempercepat penjemputan dalam situasi darurat di Klinik Unesa Ketintang Surabaya.</p>',
            unsafe_allow_html=True,
        )
        if st.button("Mulai", use_container_width=True):
            st.session_state["page"] = "menu_rs"

    with col2:
        try:
            image = Image.open("Tampilan Aplikasi/icon tampilan 1.png")
            st.image(image, use_container_width=True)
        except FileNotFoundError:
            st.error("Gambar tidak ditemukan!")

# Menu Pilihan Rumah Sakit
def menu_rs():
    st.markdown('<h2 class="main-title_menuRS">Pilih Rumah Sakit Tujuan</h2>', unsafe_allow_html=True)
    st.markdown('<p class="description_menuRS">Silakan pilih tujuan rumah sakit di bawah ini:</p>', unsafe_allow_html=True)

    for title, data in rs_data.items():
        col1, col2 = st.columns([1, 2])

        with col1:
            try:
                image = Image.open(data["image"])
                st.image(image, use_container_width=True, caption=title)
            except FileNotFoundError:
                st.error("Gambar tidak ditemukan")

        with col2:
            st.markdown(f"### {title}")
            st.markdown(data["desc"])
            if st.button(f"Pilih {title}", key=title):
                st.session_state["selected_rs"] = title
                st.session_state["page"] = "halaman_rs"

    if st.button("Kembali"):
        st.session_state["page"] = "halaman_utama"

# Halaman Hasil Rute
def halaman_rs():
    title = st.session_state["selected_rs"]
    col1, col2 = st.columns([2, 3])

    # Column 1 for displaying hospital info
    with col1:
        st.markdown(f'<h1>{title}</h1>', unsafe_allow_html=True)
        st.markdown('<p><b>Mulai:</b> Klinik Unesa Ketintang</p>', unsafe_allow_html=True)
        st.markdown(f'<p><b>Tujuan Akhir:</b> {title}</p>', unsafe_allow_html=True)
        st.markdown('<hr>', unsafe_allow_html=True)

        # Load graph and calculate route
        graph = load_graph_from_file(rs_data[title]["file"])
        if graph:
            distances, previous_nodes = dijkstra(graph, "Klinik Unesa", rs_data[title]["code"])
            path = shortest_path(previous_nodes, "Klinik Unesa", rs_data[title]["code"])

            if rs_data[title]["code"] in distances and distances[rs_data[title]["code"]] != float('inf'):
                st.success(f"Rute Terpendek:\n{' → '.join(path)}")
                st.info(f"Total Jarak: {format_distance(distances[rs_data[title]['code']])}")

                # Calculate estimated time (assuming average speed of 40 km/h)
                speed = 40  # km/h
                time_hours = (distances[rs_data[title]["code"]] / 1000) / speed
                time_minutes = time_hours * 60
                st.info(f"Estimasi Waktu: {time_minutes:.1f} menit")

        # Create buttons for navigating
        col1_buttons = st.columns([1, 1])  # creates two columns for buttons
        with col1_buttons[0]:
            if st.button("Kembali ke Menu Rumah Sakit"):
                st.session_state["page"] = "menu_rs"
        with col1_buttons[1]:
            if "view_mode" not in st.session_state:
                st.session_state["view_mode"] = "graph"
            if st.button(
                "Lihat dalam bentuk Graph" if st.session_state["view_mode"] == "route" else "Lihat dalam bentuk Rute"
            ):
                # Toggle view_mode between 'route' and 'graph'
                st.session_state["view_mode"] = "route" if st.session_state["view_mode"] == "graph" else "graph"

    # Column 2 for showing the route or graph
    with col2:
        if st.session_state.get("view_mode") == "route":
            # Define the path based on hospital title
            if title == "Rumah Sakit Ramelan":
                path = ["Klinik Unesa", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "Rumah Sakit Ramelan"]
            elif title == "Rumah Sakit Bhayangkara":
                path = ["Klinik Unesa", "A1", "A2", "A3", "A4", "A5", "Rumah Sakit Bhayangkara"]
            elif title == "RSI Darus Syifa":
                path = ["Klinik Unesa", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "RS Darus Syifa"]
            elif title == "RS Bunda":
                path = ["Klinik Unesa", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "RS Bunda"]
            elif title == "RS Bhakti Dharma Husada":
                path = ["Klinik Unesa", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "RS Bhakti Dharma Husada"]
            elif title == "RS Mitra Keluarga Darmo":
                path = ["Klinik Unesa", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "RS Mitra Keluarga Darmo"]
            elif title == "RS Muji Rahayu":
                path = ["Klinik Unesa", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "RS Muji Rahayu"]
            elif title == "RS Cempaka Putih":
                path = ["Klinik Unesa", "1", "2", "3", "4", "5", "6", "7", "8", "9", "RS Cempaka Putih"]

            # Create map with manually defined route
            map_object = create_map_with_manual_route(path, title)
            folium_static(map_object)

        elif st.session_state.get("view_mode") == "graph":
            # If view mode is 'graph', draw the graph
            if graph:
                fig = draw_graph(graph, path, title)
                st.pyplot(fig)
                plt.close()

node_coordinates  = {
    "Rumah Sakit Bhayangkara": {
        "Klinik Unesa": (-7.2839, 112.7413),
        "A1": (-7.2840, 112.7420),
        "A2": (-7.2850, 112.7430),
        "A3": (-7.2860, 112.7440),
        "A4": (-7.2870, 112.7450),
        "A5": (-7.2880, 112.7460),
        "A6": (-7.2890, 112.7470),
        "A7": (-7.2900, 112.7480),
        "B1": (-7.2845, 112.7405),
        "B2": (-7.2855, 112.7395),
        "B3": (-7.2865, 112.7385),
        "Rumah Sakit Bhayangkara": (-7.2910, 112.7500)
    },
    "Rumah Sakit Ramelan": {
        "Klinik Unesa": (-7.3112852394190355, 112.72943040972358),  
        "1": (-7.3100815796328025, 112.72987080180941),  
        "2": (-7.309728893743635, 112.73045472910741),  
        "3": (-7.309992078082717, 112.73254098592012),  
        "4": (-7.309356603697332, 112.73273508879385),
        "5":(-7.3093974543801075, 112.73292399715804),
        "6":(-7.3093712963739925, 112.7327345527389),
        "7":(-7.309409695058008, 112.73294102358494),
        "8":(-7.303319178349219, 112.7376910064642),
        "9":(-7.302910793866012, 112.7368831924013),
        "10":(-7.307148809999581, 112.73596076790388),
        "11":(-7.307195784446288, 112.73620808750326),
        '12':(-7.3073575852804415, 112.73619756326498),
        "13":(-7.307900400554115, 112.73852868204197),
        "Rumah Sakit Ramelan": (-7.308010007404354, 112.73846553661235)  
    },
    "RSI Darus Syifa": {
        "Klinik Unesa":(-7.3112852394190355, 112.72943040972358),
        "1": (-7.310074145443754, 112.7298720296243),
        "2": (-7.307608964349635, 112.72403254191602),
        "3": (-7.308999365009108, 112.71893063063882),
        "4": (-7.307417292501601, 112.71873996036662),
        "5": (-7.307254252950657, 112.71376531932367),
        "6": (-7.308967636429148, 112.71168660144255),
        "7": (-7.30888638996949, 112.7112516385413),
        "8": (-7.3074350784565505, 112.70757654454799),
        "9": (-7.308074508845883, 112.70610502234962),
        "10": (-7.306184016316744, 112.70061834660359),
        "11": (-7.304404721956728, 112.69913280990477),
        "12": (-7.302269333670001, 112.69860824364459),
        "13": (-7.293934328861173, 112.69802119387442),
        "14": (-7.290006949707702, 112.69956230524096),
        "15": (-7.284724457840447, 112.7064854669149),
        "16": (-7.280653195605427, 112.70825411066066),
        "17": (-7.261096295362021, 112.70941856561605),
        "18": (-7.2604515279328, 112.70801027679741),
        "19": (-7.2658230683381895, 112.70708345989482),
        "20": (-7.266633150890106, 112.70580850022223),
        "21": (-7.26733736373832, 112.70258380216426),
        "22": (-7.266413329817817, 112.70108743051082),
        "23": (-7.266383839350929, 112.7010279720128),
        "24": (-7.266324858396277, 112.70054239444264),
        "25": (-7.264642102517486, 112.69710824811793),
        "26": (-7.262869050627448, 112.69546961871579),
        "27": (-7.261826395451709, 112.69370379207776),
        "28": (-7.260978367407989, 112.69296102368796),
        "29": (-7.26018594634028, 112.68956951535093),
        "30": (-7.257794772577418, 112.67179913283721),
        "31": (-7.249646866002008, 112.6434708426378),
        "32": (-7.234571134840039, 112.61394771702406),
        "RS Darus Syifa": (-7.2348038111556185, 112.61269231809507),
    },

    "RS Bunda": {
        "Klinik Unesa": (-7.3112852394190355, 112.72943040972358),
        "1": (-7.310075639005821, 112.72986853000302),
        "2": (-7.309683649053946, 112.7307225793211),
        "3": (-7.309998940536553, 112.73257771854578),
        "4": (-7.3080305411274615, 112.73296426729907),
        "5": (-7.30819150198407, 112.73396614117722),
        "6": (-7.30699579014925, 112.73496658860684),
        "7": (-7.305395480696669, 112.73617313911345),
        "8": (-7.298378887634064, 112.73774271428401),
        "9": (-7.297103418432883, 112.73910239436776),
        "10": (-7.295937043590387, 112.73893549286127),
        "11": (-7.284482612066253, 112.73326823855044),
        "12": (-7.280788565314566, 112.73140819771987),
        "13": (-7.274966798011002, 112.72659812706063),
        "14": (-7.2747490467916895, 112.72606428807855),
        "15": (-7.273837806380136, 112.72503720403537),
        "16": (-7.272046960430397, 112.7236911497702),
        "17": (-7.2705661848832825, 112.72186026078475),
        "18": (-7.270294076027061, 112.71993368074753),
        "19": (-7.2682269827166675, 112.7136593735663),
        "20": (-7.266932599352387, 112.70801506760543),
        "21": (-7.266119845113534, 112.70702883136711),
        "22": (-7.267306461777536, 112.7024953536514),
        "23": (-7.2664184531810685, 112.70091737567007),
        "24": (-7.264561210726799, 112.6970355281194),
        "25": (-7.2618516099441415, 112.69363955334337),
        "26": (-7.261001409104566, 112.69292682799208),
        "27": (-7.260105416515036, 112.68934983157187),
        "28": (-7.257809649410535, 112.67176525979055),
        "29": (-7.251972850309799, 112.65047509946783),
        "RS Bunda": (-7.251727431164775, 112.65046287604127),
    },
    "RS Bhakti Dharma Husada": {
        "Klinik Unesa": (-7.3112852394190355, 112.72943040972358),
        "1": (-7.310074145443754, 112.7298720296243),
        "2": (-7.307608964349635, 112.72403254191602),
        "3": (-7.308758141122321, 112.72210647822573),
        "4": (-7.309056107619053, 112.71970321898941),
        "5": (-7.307225738857061, 112.71955301528713),
        "6": (-7.30749521919908, 112.71609470968575),
        "7": (-7.307351556303898, 112.71347687373189),
        "8": (-7.309117283535048, 112.71149203297983),
        "9": (-7.312821660468362, 112.70959703665622),
        "10": (-7.313730421153066, 112.69295675500412),
        "11": (-7.311497829225254, 112.68775121165122),
        "12": (-7.308890480737676, 112.67402264305439),
        "13": (-7.303917570634469, 112.67434289627262),
        "14": (-7.3012339287006895, 112.67569016849605),
        "15": (-7.300478124614919, 112.67559630117074),
        "16": (-7.298882436701148, 112.67562689440304),
        "17": (-7.298495369033317, 112.66837587481196),
        "18": (-7.300381073290231, 112.66553168819594),
        "19": (-7.299962995040292, 112.66181049038961),
        "20": (-7.29912333867766, 112.6614533414644),
        "21": (-7.296866600009457, 112.65743792869917),
        "22": (-7.296630097410529, 112.65173255525264),
        "23": (-7.295399632535234, 112.65138755623899),
        "24": (-7.295043045775646, 112.64911411825847),
        "25": (-7.274684490835846, 112.64506411867826),
        "26": (-7.274975608453503, 112.64338882773046),
        "27": (-7.274804840848616, 112.63992044237055),
        "28": (-7.274106702031196, 112.63993563237932),
        "29": (-7.273584352830449, 112.63854827820496),
        "30": (-7.269417785448771, 112.63920633086286),
        "31": (-7.266796795330911, 112.6405976366152),
        "32": (-7.26532146398357, 112.63804458186236),
        "33": (-7.264509133732679, 112.63809275270474),
        "34": (-7.263708748079576, 112.63746653172764),
        "35": (-7.26283071143978, 112.63738223275057),
        "36": (-7.262311056299873, 112.63749663850517),
        "37": (-7.2615226128437484, 112.63430532005374),
        "38": (-7.2609491985730905, 112.63408855125553),
        "39": (-7.260572951059922, 112.63456354223968),
        "RS Bhakti Dharma Husada": (-7.255249370318876, 112.63494289843585),

    },
    "RS Mitra Keluarga Darmo": {
        "Klinik Unesa": (-7.3112852394190355, 112.72943040972358),
        "1": (-7.310060358722841, 112.72986250241208),
        "2": (-7.307608726854946, 112.72402568158296),
        "3": (-7.30876150312453, 112.72208756265871),
        "4": (-7.309037281184761, 112.71969856744882),
        "5": (-7.307213770514296, 112.7148932434619),
        "6": (-7.306826802910874, 112.71503766048501),
        "7": (-7.3058734681529245, 112.71383222262475),
        "8": (-7.305784898154445, 112.70801072941825),
        "9": (-7.3045136200612335, 112.7080436399294),
        "10": (-7.301698076141181, 112.70708370863157),
        "11": (-7.301332074219214, 112.70731082887015),
        "12": (-7.28838538341577, 112.70706931529325),
        "13": (-7.288071341435355, 112.7069875860777),
        "14": (-7.28585014145491, 112.70504452186495),
        "15": (-7.2836377372973935, 112.70686297876375),
        "16": (-7.275795705729787, 112.70814146755302),
        "17": (-7.274910639038108, 112.70397176549805),
        "18": (-7.2745233300853585, 112.6998461315421),
        "19": (-7.2738821093551795, 112.69855328467008),
        "20": (-7.271828120242455, 112.69859295506933),
        "21": (-7.269191588219938, 112.6962312280532),
        "22": (-7.268904237817997, 112.69344709514124),
        "23": (-7.268826441781304, 112.69343011543138),
        "24": (-7.264752648988854, 112.69377184094645),
        "25": (-7.264530333220179, 112.69196489767486),
        "26": (-7.266257237604561, 112.69183282560071),
        "RS Mitra Keluarga Darmo": (-7.266218807101589, 112.69137567434895),
    },
    "RS Muji Rahayu": {
        "Klinik Unesa": (-7.3112852394190355, 112.72943040972358),
        "1": (-7.310075639005821, 112.72986853000302),
        "2": (-7.309683649053946, 112.7307225793211),
        "3": (-7.309998940536553, 112.73257771854578),
        "4": (-7.3080305411274615, 112.73296426729907),
        "5": (-7.30819150198407, 112.73396614117722),
        "6": (-7.30699579014925, 112.73496658860684),
        "7": (-7.305395480696669, 112.73617313911345),
        "8": (-7.298378887634064, 112.73774271428401),
        "9": (-7.297103418432883, 112.73910239436776),
        "10": (-7.295937043590387, 112.73893549286127),
        "11": (-7.284482612066253, 112.73326823855044),
        "12": (-7.280788565314566, 112.73140819771987),
        "13": (-7.274966798011002, 112.72659812706063),
        "14": (-7.2747490467916895, 112.72606428807855),
        "15": (-7.273837806380136, 112.72503720403537),
        "16": (-7.272046960430397, 112.7236911497702),
        "17": (-7.2705661848832825, 112.72186026078475),
        "18": (-7.270294076027061, 112.71993368074753),
        "19": (-7.2682269827166675, 112.7136593735663),
        "20": (-7.266932599352387, 112.70801506760543),
        "21": (-7.266119845113534, 112.70702883136711),
        "22": (-7.267306461777536, 112.7024953536514),
        "23": (-7.2664184531810685, 112.70091737567007),
        "24": (-7.264561210726799, 112.6970355281194),
        "25": (-7.2618516099441415, 112.69363955334337),
        "26": (-7.261001409104566, 112.69292682799208),
        "27": (-7.260105416515036, 112.68934983157187),
        "28": (-7.257809649410535, 112.67176525979055),
        "RS Muji Rahayu": (-7.257173833882126, 112.67096477053062),
    },
    "RS Cempaka Putih": {
        "Klinik Unesa": (-7.3112852394190355, 112.72943040972358),
        "1": (-7.3128606189599505, 112.72881508510271),
        "2": (-7.314369852332741, 112.72796682998685),
        "3": (-7.313931379352288, 112.72668572874913),
        "4": (-7.315052687171591, 112.71927188886959),
        "5": (-7.315671804196595, 112.71908611309408),
        "6": (-7.314793869419086, 112.71726164237592),
        "7": (-7.3158748636951305, 112.71712315119929),
        "8": (-7.316878215155274, 112.7174723898186),
        "9": (-7.317082246320721, 112.71637677301464),
        "RS Cempaka Putih": (-7.321641634176602, 112.71424780790743),
    },
}

def create_map_with_manual_route(path, hospital_name):
    # Memulai peta di koordinat Klinik Unesa (sebagai pusat peta)
    m = folium.Map(location=node_coordinates[hospital_name]["Klinik Unesa"], zoom_start=15)

    # Menambah marker untuk titik awal dan titik akhir
    if path:
        # Titik awal (node pertama) dan titik akhir (node terakhsir)
        start_node = path[0]
        end_node = path[-1]

        # Menambah marker untuk titik awal (warna hijau) dan titik akhir (warna merah)
        folium.Marker(location=node_coordinates[hospital_name][start_node], 
                      popup=start_node, icon=folium.Icon(color="green")).add_to(m)
        folium.Marker(location=node_coordinates[hospital_name][end_node], 
                      popup=end_node, icon=folium.Icon(color="red")).add_to(m)

        # Menambahkan rute sebagai PolyLine
        path_coords = [node_coordinates[hospital_name][node] for node in path]
        folium.PolyLine(locations=path_coords, color="blue", weight=5, opacity=0.8).add_to(m)

    return m

# Routing halaman
if "page" not in st.session_state:
    st.session_state["page"] = "halaman_utama"

if st.session_state["page"] == "halaman_utama":
    halaman_utama()
elif st.session_state["page"] == "menu_rs":
    menu_rs()
elif st.session_state["page"] == "halaman_rs":
    halaman_rs()