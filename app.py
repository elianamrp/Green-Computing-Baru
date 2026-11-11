from flask import Flask, render_template_string, request, redirect, url_for
import os

app = Flask(__name__)

# Database Mock / In-Memory Storage
assets = [
    {
        "id": "AST-001",
        "name": "PC Lab Komputer 01",
        "category": "Komputer",
        "unit": "Fakultas Teknik",
        "purchase_date": "2023-01-15",
        "status": "Aktif",
        "health_score": 85,
        "recommendation": "Pertahankan / Layak Pakai",
        "history": [{"date": "2024-06-10", "desc": "Pembersihan debu & ganti pasta termal", "cost": 50000}]
    },
    {
        "id": "AST-002",
        "name": "Core Switch Ruang Server",
        "category": "Jaringan",
        "unit": "Pusat TIK",
        "purchase_date": "2021-05-20",
        "status": "Perlu Perhatian",
        "health_score": 48,
        "recommendation": "Rekomendasi Pensiun / E-Waste",
        "history": [
            {"date": "2023-08-12", "desc": "Penggantian modul power supply", "cost": 750000},
            {"date": "2025-01-10", "desc": "Perbaikan port LAN terbakar", "cost": 300000}
        ]
    }
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart IT Asset Lifecycle - Universitas</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-light">
    <nav class="navbar navbar-dark bg-dark shadow-sm">
        <div class="container-fluid">
            <a class="navbar-brand" href="/"><i class="fas fa-server me-2"></i>Smart IT Asset Lifecycle (Universitas)</a>
        </div>
    </nav>

    <div class="container my-4">
        {% with messages = get_flashed_messages() %}
          {% if messages %}
            <div class="alert alert-success alert-dismissible fade show" role="alert">
              {{ messages[0] }}
              <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
          {% endif %}
        {% endwith %}

        <div class="row mb-4">
            <div class="col-md-12">
                <div class="card shadow-sm border-0">
                    <div class="card-body bg-white rounded">
                        <h4 class="card-title mb-3 text-primary"><i class="fas fa-chart-line me-2"></i>Dashboard Monitoring Aset IT</h4>
                        <p class="text-muted">Sistem pemantauan umur, kondisi, riwayat perawatan, dan rekomendasi perpanjangan masa pakai berbasis AI.</p>
                        <hr>
                        <div class="row text-center">
                            <div class="col-md-4">
                                <div class="p-3 border bg-light rounded">
                                    <h5 class="text-secondary">Total Aset</h5>
                                    <h3>{{ assets|length }} Unit</h3>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="p-3 border bg-light rounded">
                                    <h5 class="text-success">Layak Pakai</h5>
                                    <h3>{{ assets | selectattr("health_score", "ge", 60) | list | length }} Unit</h3>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="p-3 border bg-light rounded">
                                    <h5 class="text-danger">Perlu Perhatian / Afkir</h5>
                                    <h3>{{ assets | selectattr("health_score", "lt", 60) | list | length }} Unit</h3>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="card shadow-sm border-0 mb-4">
            <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
                <h5 class="mb-0"><i class="fas fa-list me-2"></i>Daftar Aset IT & Rekomendasi Siklus Hidup</h5>
                <button class="btn btn-light btn-sm" data-bs-toggle="modal" data-bs-target="#addAssetModal">
                    <i class="fas fa-plus me-1"></i> Tambah Aset
                </button>
            </div>
            <div class="card-body bg-white">
                <div class="table-responsive">
                    <table class="table table-hover align-middle">
                        <thead class="table-dark">
                            <tr>
                                <th>ID & Nama</th>
                                <th>Kategori / Unit</th>
                                <th>Umur (Beli)</th>
                                <th>Skor Kesehatan (AI)</th>
                                <th>Rekomendasi Keputusan</th>
                                <th>Aksi</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for asset in assets %}
                            <tr>
                                <td>
                                    <strong>{{ asset.id }}</strong><br>
                                    <span class="text-muted">{{ asset.name }}</span>
                                </td>
                                <td>
                                    <span class="badge bg-secondary">{{ asset.category }}</span><br>
                                    <small class="text-muted">{{ asset.unit }}</small>
                                </td>
                                <td>{{ asset.purchase_date }}</td>
                                <td>
                                    <div class="progress" style="height: 20px;">
                                        <div class="progress-bar {% if asset.health_score > 75 %}bg-success{% elif asset.health_score > 50 %}bg-warning{% else %}bg-danger{% endif %}" 
                                             role="progressbar" style="width: {{ asset.health_score }}%;">
                                            {{ asset.health_score }}%
                                        </div>
                                    </div>
                                </td>
                                <td>
                                    <span class="badge {% if asset.health_score > 75 %}bg-success{% elif asset.health_score > 50 %}bg-warning text-dark{% else %}bg-danger{% endif %}">
                                        {{ asset.recommendation }}
                                    </span>
                                </td>
                                <td>
                                    <button class="btn btn-sm btn-outline-info" data-bs-toggle="modal" data-bs-target="#detailModal{{ asset.id }}">
                                        <i class="fas fa-info-circle"></i> Detail
                                    </button>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <!-- Modal Tambah Aset -->
    <div class="modal fade" id="addAssetModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <form action="/add" method="POST">
                    <div class="modal-header bg-primary text-white">
                        <h5 class="modal-title">Tambah Aset IT Baru</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <label class="form-label">ID Aset</label>
                            <input type="text" class="form-control" name="id" placeholder="Cth: AST-003" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Nama Perangkat</label>
                            <input type="text" class="form-control" name="name" placeholder="Cth: PC Lab Jaringan" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Kategori</label>
                            <select class="form-select" name="category">
                                <option value="Komputer">Komputer / PC</option>
                                <option value="Laptop">Laptop</option>
                                <option value="Jaringan">Perangkat Jaringan (Switch/Router)</option>
                                <option value="Server">Server</option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Unit / Fakultas</label>
                            <input type="text" class="form-control" name="unit" placeholder="Cth: Fakultas Ilmu Komputer" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Tanggal Pembelian</label>
                            <input type="date" class="form-control" name="purchase_date" required>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Batal</button>
                        <button type="submit" class="btn btn-primary">Simpan Aset</button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <!-- Modal Detail & Perawatan -->
    {% for asset in assets %}
    <div class="modal fade" id="detailModal{{ asset.id }}" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header bg-dark text-white">
                    <h5 class="modal-title">Detail Aset: {{ asset.name }} ({{ asset.id }})</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <p><strong>Kategori:</strong> {{ asset.category }}</p>
                            <p><strong>Unit Penempatan:</strong> {{ asset.unit }}</p>
                            <p><strong>Tanggal Beli:</strong> {{ asset.purchase_date }}</p>
                        </div>
                        <div class="col-md-6">
                            <p><strong>Skor Kesehatan AI:</strong> {{ asset.health_score }}%</p>
                            <p><strong>Rekomendasi Siklus:</strong> <span class="text-primary fw-bold">{{ asset.recommendation }}</span></p>
                        </div>
                    </div>
                    <hr>
                    <h6 class="text-secondary"><i class="fas fa-tools me-1"></i> Riwayat Perawatan & Servis</h6>
                    {% if asset.history %}
                    <ul class="list-group mb-3">
                        {% for h in asset.history %}
                        <li class="list-group-item d-flex justify-content-between align-items-center">
                            <div>
                                <small class="text-muted"><i class="far fa-calendar-alt me-1"></i> {{ h.date }}</small><br>
                                <span>{{ h.desc }}</span>
                            </div>
                            <span class="badge bg-secondary">Rp {{ "{:,}".format(h.cost) }}</span>
                        </li>
                        {% endfor %}
                    </ul>
                    {% else %}
                    <p class="text-muted">Belum ada riwayat perawatan tercatat.</p>
                    {% endif %}

                    <!-- Form Tambah Perawatan -->
                    <form action="/maintenance/{{ asset.id }}" method="POST" class="card card-body bg-light">
                        <h6 class="mb-2">Tambah Catatan Perawatan / Servis</h6>
                        <div class="row g-2">
                            <div class="col-md-6">
                                <input type="date" class="form-control form-control-sm" name="date" required>
                            </div>
                            <div class="col-md-6">
                                <input type="number" class="form-control form-control-sm" name="cost" placeholder="Biaya Servis (Rp)" required>
                            </div>
                            <div class="col-12 mt-2">
                                <input type="text" class="form-control form-control-sm" name="desc" placeholder="Deskripsi perbaikan (Cth: Ganti SSD 512GB & Kipas)" required>
                            </div>
                            <div class="col-12 mt-2">
                                <button type="submit" class="btn btn-sm btn-success">Simpan Perawatan & Update AI</button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
    {% endfor %}

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, assets=assets)

@app.route('/add', methods=['POST'])
def add_asset():
    new_id = request.form.get('id')
    name = request.form.get('name')
    category = request.form.get('category')
    unit = request.form.get('unit')
    purchase_date = request.form.get('purchase_date')
    
    health_score = 90
    recommendation = "Pertahankan / Layak Pakai"
    
    assets.append({
        "id": new_id,
        "name": name,
        "category": category,
        "unit": unit,
        "purchase_date": purchase_date,
        "status": "Aktif",
        "health_score": health_score,
        "recommendation": recommendation,
        "history": []
    })
    return redirect(url_for('index'))

@app.route('/maintenance/<asset_id>', methods=['POST'])
def add_maintenance(asset_id):
    date = request.form.get('date')
    desc = request.form.get('desc')
    cost = int(request.form.get('cost', 0))
    
    for asset in assets:
        if asset['id'] == asset_id:
            asset['history'].append({"date": date, "desc": desc, "cost": cost})
            asset['health_score'] = max(15, asset['health_score'] - 15)
            if asset['health_score'] > 75:
                asset['recommendation'] = "Pertahankan / Layak Pakai"
            elif asset['health_score'] > 45:
                asset['recommendation'] = "Rekomendasi Upgrade Komponen (RAM/SSD)"
            else:
                asset['recommendation'] = "Rekomendasi Pensiun / E-Waste"
            break
            
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)