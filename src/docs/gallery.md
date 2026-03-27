---
hide:
  - navigation
  - toc
---

# Daily Baseline Gallery

A temporal record of the garden's state, captured daily. This provides the primary visual baseline to track macro-growth and canopy health.

<style>
.gallery-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
}
.gallery-item {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    overflow: hidden;
    transition: transform 0.2s, border-color 0.2s;
}
.gallery-item:hover {
    transform: translateY(-5px);
    border-color: #4ade80;
}
.gallery-item img {
    width: 100%;
    aspect-ratio: 4/3;
    object-fit: cover;
    display: block;
}
.gallery-info {
    padding: 1rem;
    background: #1e293b;
    border-top: 1px solid #334155;
}
.gallery-date {
    font-weight: 700;
    color: #f8fafc;
    font-size: 0.9rem;
}
</style>

<div id="gallery-root" class="gallery-grid">
    Loading visual history...
</div>

<script>
    async function loadGallery() {
        try {
            const GITHUB_RAW = "https://raw.githubusercontent.com/surendranb/gardenbot/main/";
            const res = await fetch(GITHUB_RAW + "data/gallery.json");
            const data = await res.json();
            
            const root = document.getElementById('gallery-root');
            root.innerHTML = '';
            
            data.forEach(item => {
                const div = document.createElement('div');
                div.className = 'gallery-item';
                div.innerHTML = `
                    <img src="${GITHUB_RAW}${item.path}" alt="${item.date}">
                    <div class="gallery-info">
                        <div class="gallery-date">${item.date}</div>
                    </div>
                `;
                root.appendChild(div);
            });
        } catch(e) { 
            document.getElementById('gallery-root').textContent = "Failed to load gallery.";
            console.error(e); 
        }
    }
    loadGallery();
</script>