# Daily Baseline Gallery

A temporal record of the garden's state, captured daily at 06:00 AM. This provides the primary visual baseline to track macro-growth and canopy health.

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

<div class="gallery-grid">

    <div class="gallery-item">
        <img src="../media/baselines/2026-03-25.jpg" alt="Mar 25">
        <div class="gallery-info"><div class="gallery-date">March 25, 2026</div></div>
    </div>

    <div class="gallery-item">
        <img src="../media/baselines/2026-03-24.jpg" alt="Mar 24">
        <div class="gallery-info"><div class="gallery-date">March 24, 2026</div></div>
    </div>

    <div class="gallery-item">
        <img src="../media/baselines/2026-03-23.jpg" alt="Mar 23">
        <div class="gallery-info"><div class="gallery-date">March 23, 2026</div></div>
    </div>

    <div class="gallery-item">
        <img src="../media/baselines/2026-03-22.jpg" alt="Mar 22">
        <div class="gallery-info"><div class="gallery-date">March 22, 2026</div></div>
    </div>

    <div class="gallery-item">
        <img src="../media/baselines/2026-03-21.jpg" alt="Mar 21">
        <div class="gallery-info"><div class="gallery-date">March 21, 2026</div></div>
    </div>

    <div class="gallery-item">
        <img src="../media/baselines/2026-03-20.jpg" alt="Mar 20">
        <div class="gallery-info"><div class="gallery-date">March 20, 2026</div></div>
    </div>

</div>
