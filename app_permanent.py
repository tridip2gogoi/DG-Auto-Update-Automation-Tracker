import os
import json
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)
DATA_FILE = 'telecom_records.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return [
        {
            "saipId": "SAIP90211", "jc": "JC-7712", "state": "Assam", "supervisorName": "Bikash Gogoi",
            "trtName": "TRT-Guwahati", "contactNo": "9876543210", "siteType": "Ground", "facility5g": "Yes",
            "dgMake": "Kirloskar", "dgRating": "25 KVA", "oemVendor": "Indus", "ebNonEb": "EB",
            "dependentSite": "None", "fuelSensorStatus": "Working", "docketNo": "DOC-40192",
            "openDate": "2026-05-01", "bucket": "Critical", "presentDocketNo": "PDOC-9981",
            "presentDocketRaiseDate": "2026-05-10", "agingDays": "5", "timeline": "24 Hrs",
            "presentRemarks": "DG battery low voltage issue", "previousRemarks": "Resolved previously",
            "previousDocketNo": "PDOC-8812", "previousDocketRaiseDate": "2026-04-10",
            "lastClosedDate": "2026-04-15", "batteryBackupMin": "120"
        }
    ]

def save_data(records):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/records', methods=['GET'])
def get_records():
    return jsonify(load_data())

@app.route('/api/records', methods=['POST'])
def add_record():
    records = load_data()
    new_item = request.json
    records.insert(0, new_item)
    save_data(records)
    return jsonify({"status": "success", "records": records})

@app.route('/api/records', methods=['PUT'])
def update_record():
    records = load_data()
    data = request.json
    idx = int(data.get('id', -1))
    if 0 <= idx < len(records):
        records[idx] = data
        save_data(records)
    return jsonify({"status": "success", "records": records})

@app.route('/api/records/<int:idx>', methods=['DELETE'])
def delete_record(idx):
    records = load_data()
    if 0 <= idx < len(records):
        records.pop(idx)
        save_data(records)
    return jsonify({"status": "success", "records": records})

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Telecom NOC Portal - Permanent Storage</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #f0f2f5; color: #333; }
        .navbar { background: linear-gradient(135deg, #071952, #0b2447); }
        .card-stat { border: none; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); transition: transform 0.2s; }
        .card-stat:hover { transform: translateY(-3px); }
        .portal-container { background: #ffffff; border-radius: 14px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); padding: 20px; }
        .table-responsive { max-height: 650px; overflow: auto; }
        .table thead th {
            background-color: #071952; color: #ffffff; font-weight: 600; text-transform: uppercase;
            font-size: 0.7rem; letter-spacing: 0.4px; white-space: nowrap; vertical-align: middle; position: sticky; top: 0; z-index: 10;
        }
        .table thead th.hl-yellow { background-color: #ffcc00; color: #000; }
        .table thead th.hl-red { background-color: #dc3545; color: #fff; }
        .table tbody td { vertical-align: middle; font-size: 0.8rem; white-space: nowrap; }
        .badge-aging-critical { background-color: #dc3545; color: white; font-weight: bold; }
        .badge-aging-normal { background-color: #198754; color: white; }
        .btn-primary { background-color: #0b2447; border-color: #0b2447; }
        .btn-primary:hover { background-color: #071952; border-color: #071952; }
    </style>
</head>
<body>
    <nav class="navbar navbar-dark shadow-sm">
        <div class="container-fluid px-4">
            <span class="navbar-brand mb-0 h1 fw-bold"><i class="fa-solid fa-tower-cell me-2"></i>Telecom NOC Portal (Permanent Server Storage)</span>
            <span class="text-light small"><i class="fa-regular fa-calendar-days me-1"></i> <span id="currentDate"></span></span>
        </div>
    </nav>
    <div class="container-fluid px-4 py-4">
        <div class="row g-3 mb-4">
            <div class="col-xl-3 col-md-6">
                <div class="card card-stat bg-white p-3 border-start border-4 border-primary">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <p class="text-muted mb-1 small fw-semibold">Total Sites / SAIP IDs</p>
                            <h3 class="fw-bold mb-0" id="totalSites">0</h3>
                        </div>
                        <div class="text-primary fs-2"><i class="fa-solid fa-server"></i></div>
                    </div>
                </div>
            </div>
            <div class="col-xl-3 col-md-6">
                <div class="card card-stat bg-white p-3 border-start border-4 border-danger">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <p class="text-muted mb-1 small fw-semibold">Open Dockets</p>
                            <h3 class="fw-bold mb-0 text-danger" id="openDocketsCount">0</h3>
                        </div>
                        <div class="text-danger fs-2"><i class="fa-solid fa-triangle-exclamation"></i></div>
                    </div>
                </div>
            </div>
            <div class="col-xl-3 col-md-6">
                <div class="card card-stat bg-white p-3 border-start border-4 border-warning">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <p class="text-muted mb-1 small fw-semibold">Active Supervisors</p>
                            <h3 class="fw-bold mb-0" id="totalSupervisors">0</h3>
                        </div>
                        <div class="text-warning fs-2"><i class="fa-solid fa-user-shield"></i></div>
                    </div>
                </div>
            </div>
            <div class="col-xl-3 col-md-6">
                <div class="card card-stat bg-white p-3 border-start border-4 border-success">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <p class="text-muted mb-1 small fw-semibold">Active States</p>
                            <h3 class="fw-bold mb-0" id="totalStates">0</h3>
                        </div>
                        <div class="text-success fs-2"><i class="fa-solid fa-map"></i></div>
                    </div>
                </div>
            </div>
        </div>

        <div class="portal-container mb-4">
            <div class="row g-3 align-items-center mb-3">
                <div class="col-md-3">
                    <div class="input-group">
                        <span class="input-group-text bg-light"><i class="fa-solid fa-magnifying-glass"></i></span>
                        <input type="text" id="searchInput" class="form-control" placeholder="Search SAIP ID, Docket, Supervisor...">
                    </div>
                </div>
                <div class="col-md-2">
                    <select id="filterState" class="form-select"><option value="">All States</option></select>
                </div>
                <div class="col-md-2">
                    <select id="filterBucket" class="form-select"><option value="">All Buckets</option></select>
                </div>
                <div class="col-md-5 text-md-end">
                    <button class="btn btn-outline-secondary me-2" onclick="exportToCSV()"><i class="fa-solid fa-file-excel me-1"></i> Export CSV</button>
                    <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#recordModal" onclick="openAddModal()"><i class="fa-solid fa-plus me-1"></i> Add Portal Record</button>
                </div>
            </div>

            <div class="table-responsive">
                <table class="table table-hover align-middle mb-0" id="portalTable">
                    <thead>
                        <tr>
                            <th>SAIP ID</th><th>JC</th><th>State</th><th>Supervisor Name</th><th>TRT Name</th><th>Contact No.</th>
                            <th>Site Type</th><th>5G Facility</th><th>DG Make</th><th>DG Rating</th><th>OEM Vendor</th><th>EB/Non EB</th>
                            <th>Dependent Site</th><th>Fuel Sensor Status</th><th class="hl-red">Docket no.</th><th class="hl-red">Open Date</th>
                            <th>DG Automation Status</th><th>Present Remarks</th><th>Bucket</th><th class="hl-yellow">Present Docket No.</th>
                            <th class="hl-yellow">Present Docket raise Date</th><th class="hl-yellow">Aging (Day's)</th><th class="hl-yellow">Timeline</th>
                            <th>Previous Remarks</th><th class="hl-yellow">Previous Docket No.</th><th class="hl-yellow">Previous Docket raise Date</th>
                            <th>Last Closed date</th><th>F. Battery Backup (Min)</th><th class="text-center">Actions</th>
                        </tr>
                    </thead>
                    <tbody id="tableBody"></tbody>
                </table>
            </div>
            <div id="noDataMessage" class="text-center py-5 text-muted d-none">
                <i class="fa-regular fa-folder-open fs-2 mb-2"></i>
                <p class="mb-0">No records found matching your criteria.</p>
            </div>
        </div>
    </div>

    <div class="modal fade" id="recordModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-xl modal-dialog-centered modal-dialog-scrollable">
            <div class="modal-content">
                <div class="modal-header bg-dark text-white">
                    <h5 class="modal-title" id="modalTitle"><i class="fa-solid fa-pen-to-square me-2"></i>Add Portal Record</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form id="portalForm">
                        <input type="hidden" id="recordIndex">
                        <div class="d-flex justify-content-between align-items-center mb-3 border-bottom pb-2">
                            <h6 class="text-primary fw-bold mb-0">Site & Personnel Details</h6>
                            <button type="button" class="btn btn-sm btn-outline-success" onclick="fillSampleSitePersonnel()"><i class="fa-solid fa-bolt me-1"></i> Auto-Fill Sample Site Data</button>
                        </div>
                        <div class="row g-3 mb-4">
                            <div class="col-md-3"><label class="form-label small fw-semibold">SAIP ID *</label><input type="text" class="form-control" id="saipId" required></div>
                            <div class="col-md-3"><label class="form-label small fw-semibold">JC *</label><input type="text" class="form-control" id="jc" required></div>
                            <div class="col-md-3"><label class="form-label small fw-semibold">State *</label><input type="text" class="form-control" id="state" required></div>
                            <div class="col-md-3"><label class="form-label small fw-semibold">Supervisor Name *</label><input type="text" class="form-control" id="supervisorName" required></div>
                            <div class="col-md-3"><label class="form-label small fw-semibold">TRT Name</label><input type="text" class="form-control" id="trtName"></div>
                            <div class="col-md-3"><label class="form-label small fw-semibold">Contact No.</label><input type="text" class="form-control" id="contactNo"></div>
                            <div class="col-md-3"><label class="form-label small fw-semibold">Site Type</label><input type="text" class="form-control" id="siteType"></div>
                            <div class="col-md-3"><label class="form-label small fw-semibold">5G Facility</label><select class="form-select" id="facility5g"><option value="Yes">Yes</option><option value="No">No</option></select></div>
                        </div>

                        <h6 class="text-primary fw-bold mb-3 border-bottom pb-2">Hardware & Power Configuration</h6>
                        <div class="row g-3 mb-4">
                            <div class="col-md-3"><label class="form-label small fw-semibold">DG Make</label><input type="text" class="form-control" id="dgMake"></div>
                            <div class="col-md-3"><label class="form-label small fw-semibold">DG Rating</label><input type="text" class="form-control" id="dgRating"></div>
                            <div class="col-md-3"><label class="form-label small fw-semibold">OEM Vendor</label><input type="text" class="form-control" id="oemVendor"></div>
                            <div class="col-md-3"><label class="form-label small fw-semibold">EB/Non EB</label><select class="form-select" id="ebNonEb"><option value="EB">EB</option><option value="Non EB">Non EB</option></select></div>
                            <div class="col-md-3"><label class="form-label small fw-semibold">Dependent Site</label><input type="text" class="form-control" id="dependentSite"></div>
                            <div class="col-md-3"><label class="form-label small fw-semibold">Fuel Sensor Status</label><input type="text" class="form-control" id="fuelSensorStatus"></div>
                            <div class="col-md-3"><label class="form-label small fw-semibold">DG Automation Status</label><input type="text" class="form-control" id="dgAutomationStatus"></div>
                            <div class="col-md-3"><label class="form-label small fw-semibold">F. Battery Backup (Min)</label><input type="number" class="form-control" id="batteryBackupMin"></div>
                        </div>

                        <h6 class="text-danger fw-bold mb-3 border-bottom pb-2">Current Docket & Aging Details</h6>
                        <div class="row g-3 mb-4">
                            <div class="col-md-3"><label class="form-label small fw-semibold">Docket no.</label><input type="text" class="form-control" id="docketNo"></div>
                            <div class="col-md-3"><label class="form-label small fw-semibold">Open Date</label><input type="date" class="form-control" id="openDate"></div>
                            <div class="col-md-3"><label class="form-label small fw-semibold">Bucket</label><input type="text" class="form-control" id="bucket"></div>
                            <div class="col-md-3"><label class="form-label small fw-semibold">Present Docket No.</label><input type="text" class="form-control" id="presentDocketNo"></div>
                            <div class="col-md-3"><label class="form-label small fw-semibold">Present Docket raise Date</label><input type="date" class="form-control" id="presentDocketRaiseDate"></div>
                            <div class="col-md-3"><label class="form-label small fw-semibold">Aging (Day's)</label><input type="number" class="form-control" id="agingDays"></div>
                            <div class="col-md-3"><label class="form-label small fw-semibold">Timeline</label><input type="text" class="form-control" id="timeline"></div>
                            <div class="col-md-3"><label class="form-label small fw-semibold">Present Remarks</label><input type="text" class="form-control" id="presentRemarks"></div>
                        </div>

                        <h6 class="text-secondary fw-bold mb-3 border-bottom pb-2">Historical & Previous Dockets</h6>
                        <div class="row g-3">
                            <div class="col-md-3"><label class="form-label small fw-semibold">Previous Remarks</label><input type="text" class="form-control" id="previousRemarks"></div>
                            <div class="col-md-3"><label class="form-label small fw-semibold">Previous Docket No.</label><input type="text" class="form-control" id="previousDocketNo"></div>
                            <div class="col-md-3"><label class="form-label small fw-semibold">Previous Docket raise Date</label><input type="date" class="form-control" id="previousDocketRaiseDate"></div>
                            <div class="col-md-3"><label class="form-label small fw-semibold">Last Closed date</label><input type="date" class="form-control" id="lastClosedDate"></div>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-light" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-primary" onclick="saveRecord()">Save Portal Record</button>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        document.getElementById('currentDate').innerText = new Date().toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });
        let records = [];

        async function fetchRecords() {
            try {
                const response = await fetch('/api/records');
                records = await response.json();
                initApp();
            } catch (e) {
                console.error("Error loading records", e);
            }
        }

        function initApp() {
            renderTable(records);
            updateDashboardMetrics();
            populateFilters();
        }

        function fillSampleSitePersonnel() {
            document.getElementById('saipId').value = "SAIP" + Math.floor(10000 + Math.random() * 90000);
            document.getElementById('jc').value = "JC-" + Math.floor(1000 + Math.random() * 9000);
            document.getElementById('state').value = "Assam";
            document.getElementById('supervisorName').value = "Pranjal Saikia";
            document.getElementById('trtName').value = "TRT-Jorhat";
            document.getElementById('contactNo').value = "9864" + Math.floor(100000 + Math.random() * 900000);
            document.getElementById('siteType').value = "Ground Tower";
            document.getElementById('facility5g').value = "Yes";
        }

        function renderTable(data) {
            const tbody = document.getElementById('tableBody');
            const noData = document.getElementById('noDataMessage');
            tbody.innerHTML = '';
            if (data.length === 0) {
                noData.classList.remove('d-none');
                return;
            } else {
                noData.classList.add('d-none');
            }

            data.forEach((item, index) => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td class="fw-bold text-primary">${item.saipId}</td>
                    <td>${item.jc}</td>
                    <td><span class="badge bg-secondary">${item.state}</span></td>
                    <td>${item.supervisorName}</td>
                    <td>${item.trtName || '-'}</td>
                    <td>${item.contactNo || '-'}</td>
                    <td>${item.siteType || '-'}</td>
                    <td>${item.facility5g || '-'}</td>
                    <td>${item.dgMake || '-'}</td>
                    <td>${item.dgRating || '-'}</td>
                    <td>${item.oemVendor || '-'}</td>
                    <td>${item.ebNonEb || '-'}</td>
                    <td>${item.dependentSite || '-'}</td>
                    <td>${item.fuelSensorStatus || '-'}</td>
                    <td class="fw-bold text-danger">${item.docketNo || '-'}</td>
                    <td>${item.openDate || '-'}</td>
                    <td>${item.dgAutomationStatus || '-'}</td>
                    <td>${item.presentRemarks || '-'}</td>
                    <td><span class="badge bg-dark">${item.bucket || 'General'}</span></td>
                    <td class="fw-bold">${item.presentDocketNo || '-'}</td>
                    <td>${item.presentDocketRaiseDate || '-'}</td>
                    <td><span class="badge ${item.agingDays > 3 ? 'badge-aging-critical' : 'badge-aging-normal'}">${item.agingDays || 0} Days</span></td>
                    <td>${item.timeline || '-'}</td>
                    <td>${item.previousRemarks || '-'}</td>
                    <td>${item.previousDocketNo || '-'}</td>
                    <td>${item.previousDocketRaiseDate || '-'}</td>
                    <td>${item.lastClosedDate || '-'}</td>
                    <td>${item.batteryBackupMin || '-'} Min</td>
                    <td class="text-center">
                        <button class="btn btn-sm btn-outline-primary me-1" onclick="editRecord(${index})" title="Edit"><i class="fa-solid fa-pen"></i></button>
                        <button class="btn btn-sm btn-outline-danger" onclick="deleteRecord(${index})" title="Delete"><i class="fa-solid fa-trash"></i></button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }

        function updateDashboardMetrics() {
            document.getElementById('totalSites').innerText = records.length;
            const openDockets = records.filter(r => r.docketNo && r.docketNo !== '').length;
            document.getElementById('openDocketsCount').innerText = openDockets;
            const supervisors = [...new Set(records.map(r => r.supervisorName))].length;
            document.getElementById('totalSupervisors').innerText = supervisors;
            const states = [...new Set(records.map(r => r.state))].length;
            document.getElementById('totalStates').innerText = states;
        }

        function populateFilters() {
            const stateFilter = document.getElementById('filterState');
            const bucketFilter = document.getElementById('filterBucket');
            const states = [...new Set(records.map(r => r.state))];
            const buckets = [...new Set(records.map(r => r.bucket))];

            stateFilter.innerHTML = '<option value="">All States</option>';
            states.forEach(s => { if(s) stateFilter.innerHTML += `<option value="${s}">${s}</option>`; });

            bucketFilter.innerHTML = '<option value="">All Buckets</option>';
            buckets.forEach(b => { if(b) bucketFilter.innerHTML += `<option value="${b}">${b}</option>`; });
        }

        function openAddModal() {
            document.getElementById('modalTitle').innerHTML = '<i class="fa-solid fa-pen-to-square me-2"></i>Add Portal Record';
            document.getElementById('portalForm').reset();
            document.getElementById('recordIndex').value = '';
        }

        function editRecord(index) {
            const item = records[index];
            document.getElementById('modalTitle').innerHTML = '<i class="fa-solid fa-pen-to-square me-2"></i>Edit Portal Record';
            document.getElementById('recordIndex').value = index;

            document.getElementById('saipId').value = item.saipId || '';
            document.getElementById('jc').value = item.jc || '';
            document.getElementById('state').value = item.state || '';
            document.getElementById('supervisorName').value = item.supervisorName || '';
            document.getElementById('trtName').value = item.trtName || '';
            document.getElementById('contactNo').value = item.contactNo || '';
            document.getElementById('siteType').value = item.siteType || '';
            document.getElementById('facility5g').value = item.facility5g || 'Yes';
            document.getElementById('dgMake').value = item.dgMake || '';
            document.getElementById('dgRating').value = item.dgRating || '';
            document.getElementById('oemVendor').value = item.oemVendor || '';
            document.getElementById('ebNonEb').value = item.ebNonEb || 'EB';
            document.getElementById('dependentSite').value = item.dependentSite || '';
            document.getElementById('fuelSensorStatus').value = item.fuelSensorStatus || '';
            document.getElementById('docketNo').value = item.docketNo || '';
            document.getElementById('openDate').value = item.openDate || '';
            document.getElementById('bucket').value = item.bucket || '';
            document.getElementById('presentDocketNo').value = item.presentDocketNo || '';
            document.getElementById('presentDocketRaiseDate').value = item.presentDocketRaiseDate || '';
            document.getElementById('agingDays').value = item.agingDays || '';
            document.getElementById('timeline').value = item.timeline || '';
            document.getElementById('presentRemarks').value = item.presentRemarks || '';
            document.getElementById('previousRemarks').value = item.previousRemarks || '';
            document.getElementById('previousDocketNo').value = item.previousDocketNo || '';
            document.getElementById('previousDocketRaiseDate').value = item.previousDocketRaiseDate || '';
            document.getElementById('lastClosedDate').value = item.lastClosedDate || '';
            document.getElementById('batteryBackupMin').value = item.batteryBackupMin || '';

            const myModal = new bootstrap.Modal(document.getElementById('recordModal'));
            myModal.show();
        }

        async function saveRecord() {
            const form = document.getElementById('portalForm');
            if (!form.checkValidity()) {
                form.reportValidity();
                return;
            }

            const index = document.getElementById('recordIndex').value;
            const newItem = {
                saipId: document.getElementById('saipId').value,
                jc: document.getElementById('jc').value,
                state: document.getElementById('state').value,
                supervisorName: document.getElementById('supervisorName').value,
                trtName: document.getElementById('trtName').value,
                contactNo: document.getElementById('contactNo').value,
                siteType: document.getElementById('siteType').value,
                facility5g: document.getElementById('facility5g').value,
                dgMake: document.getElementById('dgMake').value,
                dgRating: document.getElementById('dgRating').value,
                oemVendor: document.getElementById('oemVendor').value,
                ebNonEb: document.getElementById('ebNonEb').value,
                dependentSite: document.getElementById('dependentSite').value,
                fuelSensorStatus: document.getElementById('fuelSensorStatus').value,
                docketNo: document.getElementById('docketNo').value,
                openDate: document.getElementById('openDate').value,
                bucket: document.getElementById('bucket').value,
                presentDocketNo: document.getElementById('presentDocketNo').value,
                presentDocketRaiseDate: document.getElementById('presentDocketRaiseDate').value,
                agingDays: document.getElementById('agingDays').value,
                timeline: document.getElementById('timeline').value,
                presentRemarks: document.getElementById('presentRemarks').value,
                previousRemarks: document.getElementById('previousRemarks').value,
                previousDocketNo: document.getElementById('previousDocketNo).value,
                previousDocketRaiseDate: document.getElementById('previousDocketRaiseDate').value,
                lastClosedDate: document.getElementById('lastClosedDate').value,
                batteryBackupMin: document.getElementById('batteryBackupMin').value
            };

            try {
                let url = '/api/records';
                let method = 'POST';
                if (index !== '') {
                    newItem.id = index;
                    method = 'PUT';
                }

                const response = await fetch(url, {
                    method: method,
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(newItem)
                });
                const result = await response.json();
                records = result.records;
                initApp();
            } catch (e) {
                console.error("Save failed", e);
            }

            const modalEl = document.getElementById('recordModal');
            const modal = bootstrap.Modal.getInstance(modalEl);
            modal.hide();
        }

        async function deleteRecord(index) {
            if (confirm('Are you sure you want to delete this record from permanent storage?')) {
                try {
                    const response = await fetch(`/api/records/${index}`, {method: 'DELETE'});
                    const result = await response.json();
                    records = result.records;
                    initApp();
                } catch (e) {
                    console.error("Delete failed", e);
                }
            }
        }

        document.getElementById('searchInput').addEventListener('input', filterTable);
        document.getElementById('filterState').addEventListener('change', filterTable);
        document.getElementById('filterBucket').addEventListener('change', filterTable);

        function filterTable() {
            const query = document.getElementById('searchInput').value.toLowerCase();
            const selectedState = document.getElementById('filterState').value;
            const selectedBucket = document.getElementById('filterBucket').value;

            const filtered = records.filter(item => {
                const matchesSearch = Object.values(item).some(val => String(val).toLowerCase().includes(query));
                const matchesState = selectedState === '' || item.state === selectedState;
                const matchesBucket = selectedBucket === '' || item.bucket === selectedBucket;
                return matchesSearch && matchesState && matchesBucket;
            });
            renderTable(filtered);
        }

        function exportToCSV() {
            let csvContent = "data:text/csv;charset=utf-8,";
            const headers = [
                "SAIP ID", "JC", "State", "Supervisor Name", "TRT Name", "Contact No.", "Site Type", 
                "5G Facility", "DG Make", "DG Rating", "OEM Vendor", "EB/Non EB", "Dependent Site", 
                "Fuel Sensor Status", "Docket no.", "Open Date", "DG Automation Status", "Present Remarks", 
                "Bucket", "Present Docket No.", "Present Docket raise Date", "Aging (Day's)", "Timeline", 
                "Previous Remarks", "Previous Docket No.", "Previous Docket raise Date", "Last Closed date", "F. Battery Backup (Min)"
            ];
            csvContent += headers.join(",") + "\r\n";
            records.forEach(r => {
                const row = [
                    r.saipId, r.jc, r.state, r.supervisorName, r.trtName, r.contactNo, r.siteType,
                    r.facility5g, r.dgMake, r.dgRating, r.oemVendor, r.ebNonEb, r.dependentSite,
                    r.fuelSensorStatus, r.docketNo, r.openDate, r.dgAutomationStatus, r.presentRemarks,
                    r.bucket, r.presentDocketNo, r.presentDocketRaiseDate, r.agingDays, r.timeline,
                    r.previousRemarks, r.previousDocketNo, r.previousDocketRaiseDate, r.lastClosedDate, r.batteryBackupMin
                ];
                csvContent += row.map(e => `"${e || ''}"`).join(",") + "\r\n";
            });
            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", "permanent_telecom_noc_records.csv");
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }

        fetchRecords();
    </script>
</body>
</html>
"""
