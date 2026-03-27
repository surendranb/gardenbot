---
hide:
  - navigation
  - toc
---

# 📖 Botanical Baseline Gallery

A temporal record of the garden's state, captured daily. This provides the primary visual baseline to track macro-growth and canopy health.

<!-- SimpleLightbox CSS -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/simplelightbox/2.14.3/simple-lightbox.min.css" />

<style>
.gallery-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}
.gallery-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 16px;
    overflow: hidden;
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.2s;
    text-decoration: none !important;
}
.gallery-card:hover {
    transform: translateY(-8px);
    border-color: #4ade80;
    box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.3);
}
.img-wrapper {
    position: relative;
    width: 100%;
    aspect-ratio: 4/3;
    overflow: hidden;
}
.gallery-card img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.5s ease;
}
.gallery-card:hover img {
    transform: scale(1.08);
}
.gallery-info {
    padding: 1.2rem;
    background: #1e293b;
}
.date-badge {
    display: inline-block;
    padding: 4px 10px;
    background: rgba(74, 222, 128, 0.1);
    color: #4ade80;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 700;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.gallery-title {
    color: #f8fafc;
    font-weight: 600;
    font-size: 1rem;
    display: block;
}
</style>

<div id="gallery-root" class="gallery-container">
    Scanning historical visual ledger...
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/simplelightbox/2.14.3/simple-lightbox.min.js"></script>

<script>
    async function initGallery() {
        // Cache bust the JSON to always get latest even if GitHub raw is slow
        const GITHUB_RAW = "https://raw.githubusercontent.com/surendranb/gardenbot/main/";
        const root = document.getElementById('gallery-root');
        
        try {
            const res = await fetch(GITHUB_RAW + "data/gallery.json?t=" + Date.now());
            const data = await res.json();
            
            if (data.length === 0) {
                root.innerHTML = "<p>No entries found in the archive.</p>";
                return;
            }

            root.innerHTML = '';
            data.forEach(item => {
                const anchor = document.createElement('a');
                anchor.href = GITHUB_RAW + item.path;
                anchor.className = 'gallery-card item';
                
                // Date formatting for UI
                const dateParts = item.date.split('-');
                const dateObj = new Date(dateParts[0], dateParts[1] - 1, dateParts[2]);
                const displayDate = dateObj.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });

                anchor.innerHTML = `
                    <div class="img-wrapper">
                        <img src="${GITHUB_RAW}${item.path}" alt="${displayDate}" loading="lazy" />
                    </div>
                    <div class="gallery-info">
                        <span class="date-badge">${item.date}</span>
                        <span class="gallery-title">${displayDate}</span>
                    </div>
                `;
                root.appendChild(anchor);
            });

            // Init SimpleLightbox for that sweet UX
            new SimpleLightbox('.gallery-container a.item', {
                overlayOpacity: 0.9,
                className: 'garden-lightbox'
            });

        } catch (e) {
            root.innerHTML = `<p style="color: #ef4444;">Gallery Sync Failed: ${e.message}</p>`;
        }
    }

    initGallery();
</script>