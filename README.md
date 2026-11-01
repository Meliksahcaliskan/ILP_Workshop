# ILP & Optimizasyon Workshop'u

Bilgisayar mühendisliği öğrencilerine yönelik, **Tamsayılı Doğrusal Programlama (ILP)** kavramlarını uygulamalı olarak tanıtan ~2 saatlik bir workshop.

---

## 📅 Tarih / Yer / Bağlantı

> *(Tarih, yer ve uzaktan katılım bağlantısı buraya eklenecek)*

---

## 🎯 Amaç

- Decision variable, objective function, constraint kavramlarını somut problemler üzerinden anlamak
- LP ile ILP arasındaki farkı görmek
- Infeasible ve unbounded durumları deneyimlemek
- Hazır modelleri değiştirerek sonuçları gözlemlemek

---

## ⚙️ Kurulum

### 1. Repoyu klonla

```bash
git clone https://github.com/Meliksahcaliskan/ILP_Workshop.git
cd ILP_Workshop
```

### 2. Sanal ortam oluştur ve aktifleştir

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate
```

### 3. Paketleri yükle

```bash
pip install -r requirements.txt
```

### 4. Jupyter'ı başlat

```bash
jupyter notebook
```

> ⚠️ **Workshop'tan önce `00_setup_check.ipynb`'yi çalıştırarak kurulumunuzu doğrulayın!**

---

## 📓 Notebook'lar

| # | Notebook | Konu | Süre | Colab |
|---|----------|------|------|-------|
| 0 | `00_setup_check.ipynb` | Kurulum kontrolü | 5 dk | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Meliksahcaliskan/ILP_Workshop/blob/main/00_setup_check.ipynb) |
| 1 | `01_giris_bulut_sunucusu.ipynb` | Giriş: decision variable, LP vs ILP | 30 dk | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Meliksahcaliskan/ILP_Workshop/blob/main/01_giris_bulut_sunucusu.ipynb) |
| 2 | `02_sinav_takvimi.ipynb` | Ana problem: binary değişkenler, graph coloring | 35 dk | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Meliksahcaliskan/ILP_Workshop/blob/main/02_sinav_takvimi.ipynb) |
| 3 | `03_alistirma_knapsack.ipynb` | Alıştırma: knapsack, kendin modelle | 25 dk | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Meliksahcaliskan/ILP_Workshop/blob/main/03_alistirma_knapsack.ipynb) |
| 4 | `04_bonus_task_assignment.ipynb` | Bonus: MILP, makespan minimizasyonu | ev ödevi | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Meliksahcaliskan/ILP_Workshop/blob/main/04_bonus_task_assignment.ipynb) |

### Colab'da kullanım notu

Notebook'ların ilk hücresi Colab ortamını otomatik olarak algılar ve `pulp` paketini kurar. Ayrıca `utils/plotting.py` dosyasına erişmek için repoyu Colab'a klonlar:

```python
import sys
if "google.colab" in sys.modules:
    !pip install -q pulp
    !git clone https://github.com/Meliksahcaliskan/ILP_Workshop.git
    sys.path.insert(0, "ILP_Workshop")
```

---

## 🗓️ Workshop Akışı

| Süre | Bölüm | Notebook |
|------|-------|----------|
| 0:00 – 0:10 | Açılış, kurulum kontrolü | `00_setup_check` |
| 0:10 – 0:40 | Giriş problemi: kavramlar, grafik, LP vs ILP | `01_giris_bulut_sunucusu` |
| 0:40 – 1:15 | Sınav takvimi: graph coloring, değiştir-gözlemle | `02_sinav_takvimi` |
| 1:15 – 1:25 | Mola | — |
| 1:25 – 1:50 | Knapsack alıştırması (15 dk bireysel + 10 dk çözüm) | `03_alistirma_knapsack` |
| 1:50 – 2:00 | Kapanış: NP-hardness, kaynaklar, bonus | `kaynaklar.md`, `04_bonus` |

---

## 📚 Kaynaklar

Bkz. [kaynaklar.md](kaynaklar.md)

---

## 🌿 Branch Yapısı

- **`main`** — Workshop materyalleri (çözümsüz alıştırmalar)
- **`solutions`** — Çözümlü notebook'lar (`solutions/` klasörü altında)
