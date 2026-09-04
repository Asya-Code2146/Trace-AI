const API_BASE_URL = "http://127.0.0.1:8000";
const apiUrl = `${API_BASE_URL}/api/investigate`;

let imagesBase64 = []; // Menampung array banyak gambar dalam format base64
let historyData = JSON.parse(localStorage.getItem('trace_history') || "[]");
let startTime = 0;

document.addEventListener("DOMContentLoaded", () => {
    checkAuthStatus();
    renderHistory();
    setupSidebarToggle();
    setupThemeToggle();
    setupImagePreview();
    setupExportFeatures(); 
    setupQuickTemplates();
    setupHistorySearchAndFilter();
});

/* SYSTEM TOAST NOTIFICATION */
function showToast(message, type = "info") {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerText = message;

    container.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 3000);
}

/* 1. QUICK TEMPLATE BUTTONS */
function setupQuickTemplates() {
    const chipButtons = document.querySelectorAll('.chip-btn');
    chipButtons.forEach(button => {
        button.addEventListener('click', () => {
            const type = button.getAttribute('data-type');
            const text = button.getAttribute('data-text');
            
            const caseTypeEl = document.getElementById('caseType');
            const textInputEl = document.getElementById('textInput');

            if (caseTypeEl) caseTypeEl.value = type;
            if (textInputEl) textInputEl.value = text;
            showToast("Template dimuat!", "success");
        });
    });
}

/* 2. EXPORT & COPY REPORT LOGIC */
function setupExportFeatures() {
    const btnCopy = document.getElementById('btnCopyReport');
    const btnPDF = document.getElementById('btnDownloadPDF');

    btnCopy?.addEventListener('click', () => {
        const riskPercent = document.getElementById('riskPercent')?.innerText || '-';
        const riskLevel = document.getElementById('riskLevel')?.innerText || '-';
        const caseType = document.getElementById('caseType')?.value || '-';
        const summary = document.getElementById('summaryText')?.innerText || '-';
        
        let emoji = '⚠️';
        if (riskLevel.includes('HIGH')) emoji = '🚨';
        if (riskLevel.includes('LOW')) emoji = '✅';

        const waMessage = `${emoji} *LAPORAN INVESTIGASI TRACE AI* ${emoji}\n` +
            `-----------------------------------------\n` +
            `📌 *Tingkat Risiko:* ${riskPercent} (${riskLevel})\n` +
            `📂 *Kategori:* ${formatTitle(caseType)}\n\n` +
            `📝 *Ringkasan Kasus:*\n${summary}\n\n` +
            `🔍 *Dianalisis oleh:* TRACE AI Digital Investigation Engine`;

        navigator.clipboard.writeText(waMessage).then(() => {
            showToast("Ringkasan berhasil disalin ke clipboard!", "success");
        }).catch(err => {
            showToast("Gagal menyalin teks", "error");
        });
    });

    btnPDF?.addEventListener('click', () => {
        const element = document.getElementById('pdfContent');
        if (!element) return;

        element.classList.add('pdf-render-mode');

        const opt = {
            margin:       [8, 8, 8, 8],
            filename:     `TRACE_AI_Report_${Date.now()}.pdf`,
            image:        { type: 'jpeg', quality: 0.98 },
            html2canvas:  { scale: 2, useCORS: true, logging: false, letterRendering: true },
            jsPDF:        { unit: 'mm', format: 'a4', orientation: 'portrait' }
        };

        showToast("Memproses pembuatan PDF...", "info");
        html2pdf().set(opt).from(element).save().then(() => {
            element.classList.remove('pdf-render-mode');
            showToast("PDF berhasil diunduh!", "success");
        });
    });
}

/* 3. THEME TOGGLE */
function setupThemeToggle() {
    const btnTheme = document.getElementById('btnThemeToggle');
    const sunIcon = document.getElementById('themeIconSun');
    const moonIcon = document.getElementById('themeIconMoon');
    
    const savedTheme = localStorage.getItem('trace_theme') || 'dark';
    applyTheme(savedTheme);

    btnTheme?.addEventListener('click', () => {
        const isLight = document.body.classList.contains('light-mode');
        applyTheme(isLight ? 'dark' : 'light');
    });

    function applyTheme(theme) {
        if (theme === 'light') {
            document.body.classList.add('light-mode');
            if (sunIcon) sunIcon.style.display = 'none';
            if (moonIcon) moonIcon.style.display = 'block';
        } else {
            document.body.classList.remove('light-mode');
            if (sunIcon) sunIcon.style.display = 'block';
            if (moonIcon) moonIcon.style.display = 'none';
        }
        localStorage.setItem('trace_theme', theme);
    }
}

/* 4. MULTI-IMAGE PREVIEW LOGIC */
function setupImagePreview() {
    const input = document.getElementById('imageInput');
    const container = document.getElementById('imagePreviewContainer');

    input?.addEventListener('change', function (e) {
        const files = Array.from(e.target.files);
        
        files.forEach(file => {
            const reader = new FileReader();
            reader.onload = function (event) {
                const base64Data = event.target.result.split(',')[1];
                imagesBase64.push(base64Data);

                // Buat thumbnail preview per gambar
                const thumbBox = document.createElement('div');
                thumbBox.className = 'preview-thumb-box';

                const img = document.createElement('img');
                img.src = event.target.result;

                const btnRemove = document.createElement('button');
                btnRemove.className = 'btn-remove-thumb';
                btnRemove.innerHTML = '&times;';
                btnRemove.title = 'Hapus gambar ini';
                
                btnRemove.onclick = function () {
                    const index = imagesBase64.indexOf(base64Data);
                    if (index > -1) imagesBase64.splice(index, 1);
                    thumbBox.remove();
                    if (imagesBase64.length === 0 && container) {
                        container.style.display = 'none';
                    }
                };

                thumbBox.appendChild(img);
                thumbBox.appendChild(btnRemove);
                container?.appendChild(thumbBox);
            };
            reader.readAsDataURL(file);
        });

        if (files.length > 0 && container) {
            container.style.display = 'flex';
        }
        input.value = ""; // Reset value agar bisa menambah file baru lagi
    });
}

function resetImageInput() {
    const input = document.getElementById('imageInput');
    const container = document.getElementById('imagePreviewContainer');

    if (input) input.value = "";
    if (container) {
        container.innerHTML = "";
        container.style.display = 'none';
    }
    imagesBase64 = [];
}

/* 5. SIDEBAR LOGIC */
function setupSidebarToggle() {
    const layout = document.getElementById('appLayout');
    const btnToggle = document.getElementById('btnToggleSidebar');
    const btnOpen = document.getElementById('btnOpenSidebar');
    const overlay = document.getElementById('sidebarOverlay');

    btnToggle?.addEventListener('click', () => {
        layout?.classList.add('sidebar-closed');
        if (btnOpen) btnOpen.style.display = 'flex';
    });

    btnOpen?.addEventListener('click', () => {
        layout?.classList.remove('sidebar-closed');
        if (btnOpen) btnOpen.style.display = 'none';
    });

    overlay?.addEventListener('click', () => {
        layout?.classList.add('sidebar-closed');
        if (btnOpen) btnOpen.style.display = 'flex';
    });
}

/* 6. AUTH CHECK */
async function checkAuthStatus() {
    try {
        const res = await fetch(`${API_BASE_URL}/api/auth/status`);
        const data = await res.json();

        if (data.is_logged_in) {
            document.getElementById('loggedOutView').style.display = 'none';
            document.getElementById('loggedInView').style.display = 'flex';
            document.getElementById('userName').innerText = data.name;

            const emailEl = document.getElementById('userEmail');
            if (emailEl && data.email) emailEl.innerText = data.email;

            const avatarEl = document.getElementById('userAvatar');
            if (avatarEl) {
                avatarEl.src = (data.pic && data.pic !== "not_available") ? data.pic : "https://lh3.googleusercontent.com/a/default-user=s96-c";
                avatarEl.onerror = function () {
                    this.onerror = null;
                    this.src = "https://lh3.googleusercontent.com/a/default-user=s96-c";
                };
            }
            return data;
        } else {
            document.getElementById('loggedOutView').style.display = 'block';
            document.getElementById('loggedInView').style.display = 'none';
            return { is_logged_in: false };
        }
    } catch (err) {
        console.error("Gagal memeriksa status login:", err);
        return { is_logged_in: false };
    }
}

/* 7. INVESTIGATION & NEW CHAT */
document.getElementById('btnNewChat')?.addEventListener('click', () => {
    const textInput = document.getElementById('textInput');
    const results = document.getElementById('results');
    const formCard = document.querySelector('.form-card');
    const scrollContainer = document.querySelector('.content-scroll');

    if (textInput) textInput.value = "";
    resetImageInput();
    if (results) results.style.display = "none";
    if (formCard) formCard.style.display = "block";
    if (scrollContainer) scrollContainer.scrollTo({ top: 0, behavior: 'smooth' });
});

document.getElementById('btnInvestigate')?.addEventListener('click', runInvestigation);

async function runInvestigation() {
    const btn = document.getElementById('btnInvestigate');
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    const caseType = document.getElementById('caseType')?.value;
    const textInput = document.getElementById('textInput')?.value;

    if (!textInput && imagesBase64.length === 0) {
        showToast("Masukkan teks atau upload minimal 1 gambar terlebih dahulu!", "error");
        return;
    }

    startTime = performance.now();

    btn.disabled = true;
    btn.innerText = "PROCESSING...";
    if (loading) loading.style.display = "flex";
    if (results) results.style.display = "none";

    const payload = {
        case_type: caseType,
        raw_text: textInput || null,
        images_base64: imagesBase64.length > 0 ? imagesBase64 : null // Mengirim array gambar
    };

    try {
        const response = await fetch(apiUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const data = await response.json();
        const report = data.investigation_report;

        const endTime = performance.now();
        const duration = ((endTime - startTime) / 1000).toFixed(2);
        
        renderReport(report, duration);
        saveToHistory(caseType, textInput, report);

    } catch (error) {
        showToast("Gagal terhubung ke TRACE AI Engine.", "error");
        console.error("Error Detail:", error);
    } finally {
        btn.disabled = false;
        btn.innerText = "RUN INVESTIGATION";
        if (loading) loading.style.display = "none";
    }
}

function renderReport(report, duration = null) {
    if (duration !== null) {
        const timeEl = document.getElementById('processTime');
        if (timeEl) timeEl.innerText = `${duration}s`;
    }

    document.getElementById('riskPercent').innerText = report.risk_score + "%";

    const rlEl = document.getElementById('riskLevel');
    rlEl.innerText = report.risk_level;
    rlEl.className = "score-value text-" + report.risk_level.toLowerCase();

    document.getElementById('summaryText').innerText = report.evidence_summary;
    document.getElementById('reasoning-text').innerText = report.reasoning;

    const flagContainer = document.getElementById('redFlagsContainer');
    flagContainer.innerHTML = "";
    if (!report.red_flags || report.red_flags.length === 0) {
        flagContainer.innerHTML = "<p style='color:var(--text-muted); font-size:13px;'>Tidak ada red flags terdeteksi.</p>";
    } else {
        report.red_flags.forEach(flag => {
            flagContainer.innerHTML += `
                <div class="flag-card" style="margin-bottom:8px;">
                    <div style="color:#ef4444; font-size:12px; font-weight:600; margin-bottom:4px;">[ ${flag.severity.toUpperCase()} ] ${flag.type}</div>
                    <div style="font-size:13px; color:var(--text-main); line-height:1.5;">${flag.description}</div>
                </div>
            `;
        });
    }

    const recList = document.getElementById('recList');
    recList.innerHTML = "";
    if (report.recommendation) {
        report.recommendation.forEach(rec => {
            const li = document.createElement('li');
            li.textContent = rec;
            recList.appendChild(li);
        });
    }

    // Auto-Scroll Mulus
    const resultsEl = document.getElementById('results');
    if (resultsEl) {
        resultsEl.style.display = "block";
        resultsEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

/* 8. HISTORY MANAGEMENT WITH FILTER & SEARCH */
function formatTitle(text) {
    if (!text) return "";
    return text.replace(/_/g, ' ').replace(/\b\w/g, char => char.toUpperCase());
}

function saveToHistory(caseType, textInput, report) {
    const rawTitle = textInput 
        ? textInput.substring(0, 30) + (textInput.length > 30 ? "..." : "") 
        : caseType;

    const item = {
        id: Date.now(),
        title: formatTitle(rawTitle),
        riskLevel: report.risk_level || 'LOW',
        report: report
    };

    historyData.unshift(item);
    if (historyData.length > 50) historyData = historyData.slice(0, 50);
    localStorage.setItem('trace_history', JSON.stringify(historyData));
    renderHistory();
}

function deleteHistoryItem(id, e) {
    e.stopPropagation();
    historyData = historyData.filter(item => item.id !== id);
    localStorage.setItem('trace_history', JSON.stringify(historyData));
    renderHistory();
    showToast("Riwayat dihapus", "info");
}

document.getElementById('btnClearHistory')?.addEventListener('click', () => {
    if (confirm("Apakah Anda yakin ingin menghapus semua riwayat?")) {
        historyData = [];
        localStorage.removeItem('trace_history');
        renderHistory();
        showToast("Semua riwayat dibersihkan", "info");
    }
});

function renderHistory() {
    const listEl = document.getElementById('historyList');
    if (!listEl) return;

    listEl.innerHTML = "";

    if (historyData.length === 0) {
        listEl.innerHTML = '<li class="history-empty">Belum ada riwayat</li>';
        return;
    }

    historyData.forEach(item => {
        const li = document.createElement('li');
        li.className = "history-item";
        li.setAttribute('data-title', item.title.toLowerCase());
        li.setAttribute('data-risk', (item.riskLevel || 'LOW').toUpperCase());

        const titleSpan = document.createElement('span');
        titleSpan.className = "history-title";
        titleSpan.textContent = item.title;

        const riskBadge = document.createElement('span');
        const level = (item.riskLevel || 'LOW').toUpperCase();
        let badgeClass = 'badge-low';
        if (level.includes('HIGH')) badgeClass = 'badge-high';
        if (level.includes('MEDIUM')) badgeClass = 'badge-medium';

        riskBadge.className = `risk-badge-sm ${badgeClass}`;
        riskBadge.textContent = level;

        const delBtn = document.createElement('button');
        delBtn.className = "btn-del-item";
        delBtn.innerHTML = "&times;";
        delBtn.addEventListener('click', (e) => deleteHistoryItem(item.id, e));

        li.appendChild(titleSpan);
        li.appendChild(riskBadge);
        li.appendChild(delBtn);

        li.addEventListener('click', () => {
            renderReport(item.report);
            listEl.querySelectorAll('li').forEach(l => l.classList.remove('active'));
            li.classList.add('active');
        });

        listEl.appendChild(li);
    });
}

function setupHistorySearchAndFilter() {
    const searchInput = document.getElementById('historySearchInput');
    const filterSelect = document.getElementById('historyFilterSelect');

    function applyFilter() {
        const query = searchInput?.value.toLowerCase() || "";
        const filterVal = filterSelect?.value || "ALL";
        const historyItems = document.querySelectorAll('#historyList .history-item');

        historyItems.forEach(item => {
            const title = item.getAttribute('data-title') || "";
            const risk = item.getAttribute('data-risk') || "";

            const matchesSearch = title.includes(query);
            const matchesRisk = (filterVal === "ALL") || risk.includes(filterVal);

            if (matchesSearch && matchesRisk) {
                item.style.display = 'flex';
            } else {
                item.style.display = 'none';
            }
        });
    }

    searchInput?.addEventListener('input', applyFilter);
    filterSelect?.addEventListener('change', applyFilter);
}

async function googleLogin() {
    const status = await checkAuthStatus();
    if (status.is_logged_in) {
        showToast(`Anda terautentikasi sebagai ${status.name}`, "info");
        return;
    }
    window.location.href = `${API_BASE_URL}/auth/login`;
}