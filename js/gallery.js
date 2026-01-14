/**
 * Anh Khôi Portfolio - Instagram Vibe
 * View Transitions + Swiper Coverflow + Video Autoplay
 */

import { ALL_MEDIA, MEDIA_DATA } from './media-data.js';

class PortfolioApp {
    constructor() {
        this.currentView = 'hero'; // 'hero' or 'gallery'
        this.currentFilter = 'image'; // 'image' or 'video'
        this.filteredMedia = ALL_MEDIA.filter(m => m.type === 'image');
        this.swiper = null;
        this.init();
    }

    init() {
        this.cacheDOM();
        this.hideLoader();
        this.bindEvents();
    }

    cacheDOM() {
        // Loader
        this.loader = document.getElementById('loader');

        // Views
        this.heroCover = document.getElementById('heroCover');
        this.galleryView = document.getElementById('galleryView');

        // Buttons
        this.enterGalleryBtn = document.getElementById('enterGalleryBtn');
        this.backToHeroBtn = document.getElementById('backToHeroBtn');

        // Gallery
        this.swiperWrapper = document.getElementById('swiperWrapper');
        this.tabButtons = document.querySelectorAll('.tab-btn');
        this.currentIndexEl = document.getElementById('currentIndex');
        this.totalItemsEl = document.getElementById('totalItems');

        // Lightbox
        this.lightbox = document.getElementById('lightbox');
        this.lightboxContent = document.getElementById('lightboxContent');
        this.lightboxClose = document.getElementById('lightboxClose');
        this.lightboxPrev = document.getElementById('lightboxPrev');
        this.lightboxNext = document.getElementById('lightboxNext');
    }

    hideLoader() {
        const progressBar = document.getElementById('progressBar');
        let progress = 0;

        const interval = setInterval(() => {
            progress += Math.random() * 20 + 10;
            if (progress >= 100) {
                progress = 100;
                clearInterval(interval);
                setTimeout(() => {
                    this.loader?.classList.add('hidden');
                }, 400);
            }
            if (progressBar) progressBar.style.width = `${progress}%`;
        }, 150);
    }

    bindEvents() {
        // View transitions
        this.enterGalleryBtn?.addEventListener('click', () => this.showGallery());
        this.backToHeroBtn?.addEventListener('click', () => this.showHero());

        // Tab switching
        this.tabButtons.forEach(btn => {
            btn.addEventListener('click', () => this.handleTabSwitch(btn));
        });

        // Lightbox controls
        this.lightboxClose?.addEventListener('click', () => this.closeLightbox());
        this.lightboxPrev?.addEventListener('click', () => this.navigateLightbox(-1));
        this.lightboxNext?.addEventListener('click', () => this.navigateLightbox(1));
        this.lightbox?.addEventListener('click', (e) => {
            if (e.target === this.lightbox) this.closeLightbox();
        });

        // Keyboard navigation
        document.addEventListener('keydown', (e) => this.handleKeyboard(e));
    }

    // === View Transitions ===
    showGallery() {
        this.currentView = 'gallery';

        // Animate hero out
        this.heroCover.classList.add('hidden');

        // Animate gallery in
        setTimeout(() => {
            this.galleryView.classList.remove('hidden');

            // Init Swiper if not already
            if (!this.swiper) {
                this.renderSlides();
                this.initSwiper();
            }
        }, 300);
    }

    showHero() {
        this.currentView = 'hero';

        // Animate gallery out
        this.galleryView.classList.add('hidden');

        // Animate hero in
        setTimeout(() => {
            this.heroCover.classList.remove('hidden');
        }, 300);

        // Pause any playing videos
        this.pauseAllVideos();
    }

    // === Tab Switching ===
    handleTabSwitch(btn) {
        const filter = btn.dataset.filter;

        // Update active state
        this.tabButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        // Update filter
        this.currentFilter = filter;
        this.filteredMedia = ALL_MEDIA.filter(m => m.type === filter);

        // Rebuild slides
        this.renderSlides();

        // Reinitialize Swiper
        if (this.swiper) {
            this.swiper.destroy(true, true);
        }
        this.initSwiper();
    }

    // === Swiper ===
    renderSlides() {
        if (!this.swiperWrapper) return;

        this.swiperWrapper.innerHTML = '';

        this.filteredMedia.forEach((media, index) => {
            const slide = document.createElement('div');
            slide.className = 'swiper-slide';
            slide.dataset.index = index;

            if (media.type === 'video') {
                slide.innerHTML = `
          <div class="slide-content video-slide">
            <video src="${media.src}" muted loop playsinline preload="metadata"></video>
            <div class="video-overlay">
              <svg viewBox="0 0 24 24" fill="white"><path d="M8 5v14l11-7z"/></svg>
            </div>
          </div>
        `;
            } else {
                slide.innerHTML = `
          <div class="slide-content">
            <img src="${media.src}" alt="Photo ${index + 1}" loading="lazy">
          </div>
        `;
            }

            this.swiperWrapper.appendChild(slide);
        });

        this.updateCounter(0);
    }

    initSwiper() {
        this.swiper = new Swiper('.gallery-swiper', {
            effect: 'coverflow',
            grabCursor: true,
            centeredSlides: true,
            slidesPerView: 'auto',
            loop: this.filteredMedia.length > 3,
            speed: 600,

            coverflowEffect: {
                rotate: 0,
                stretch: 80,
                depth: 200,
                modifier: 1,
                slideShadows: true,
            },

            pagination: {
                el: '.swiper-pagination',
                clickable: true,
                dynamicBullets: true,
            },

            keyboard: {
                enabled: true,
            },

            mousewheel: {
                enabled: true,
                sensitivity: 1.5,
            },

            on: {
                slideChange: (swiper) => {
                    this.updateCounter(swiper.realIndex);
                    this.handleVideoAutoplay();
                },
                click: (swiper, e) => {
                    const slide = e.target.closest('.swiper-slide');
                    if (slide && slide.classList.contains('swiper-slide-active')) {
                        const index = parseInt(slide.dataset.index);
                        this.openLightbox(index);
                    }
                },
            },
        });

        // Initial video autoplay check
        this.handleVideoAutoplay();
    }

    handleVideoAutoplay() {
        // Pause all videos first
        this.pauseAllVideos();

        // Play video in active slide
        const activeSlide = document.querySelector('.swiper-slide-active');
        if (activeSlide) {
            const video = activeSlide.querySelector('video');
            if (video) {
                video.play().catch(() => { });
                // Hide overlay when playing
                const overlay = activeSlide.querySelector('.video-overlay');
                if (overlay) overlay.style.opacity = '0';
            }
        }
    }

    pauseAllVideos() {
        document.querySelectorAll('.gallery-swiper video').forEach(v => {
            v.pause();
            v.currentTime = 0;
        });
        // Show all overlays
        document.querySelectorAll('.video-overlay').forEach(o => o.style.opacity = '1');
    }

    updateCounter(index) {
        if (this.currentIndexEl) this.currentIndexEl.textContent = index + 1;
        if (this.totalItemsEl) this.totalItemsEl.textContent = this.filteredMedia.length;
    }

    // === Lightbox ===
    openLightbox(index) {
        this.lightboxIndex = index;
        const media = this.filteredMedia[index];

        this.lightboxContent.innerHTML = '';

        if (media.type === 'video') {
            const video = document.createElement('video');
            video.src = media.src;
            video.controls = true;
            video.autoplay = true;
            this.lightboxContent.appendChild(video);
        } else {
            const img = document.createElement('img');
            img.src = media.src;
            img.alt = `Photo ${index + 1}`;
            this.lightboxContent.appendChild(img);
        }

        this.lightbox.classList.add('active');
        document.body.style.overflow = 'hidden';

        // Pause swiper videos
        this.pauseAllVideos();
    }

    closeLightbox() {
        this.lightbox.classList.remove('active');
        document.body.style.overflow = '';

        const video = this.lightboxContent.querySelector('video');
        if (video) video.pause();

        // Resume video autoplay in swiper
        this.handleVideoAutoplay();
    }

    navigateLightbox(direction) {
        const total = this.filteredMedia.length;
        this.lightboxIndex = (this.lightboxIndex + direction + total) % total;
        this.openLightbox(this.lightboxIndex);
    }

    handleKeyboard(e) {
        if (this.lightbox?.classList.contains('active')) {
            if (e.key === 'Escape') this.closeLightbox();
            if (e.key === 'ArrowLeft') this.navigateLightbox(-1);
            if (e.key === 'ArrowRight') this.navigateLightbox(1);
        } else if (this.currentView === 'hero' && e.key === 'Enter') {
            this.showGallery();
        } else if (this.currentView === 'gallery' && e.key === 'Escape') {
            this.showHero();
        }
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    new PortfolioApp();
});
