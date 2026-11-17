/**
 * NewsBlog — Main JavaScript Application
 * Reading Progress Tracker & Laravel-style Session Toast Manager
 */

(function () {
    'use strict';

    // 1. Reading Progress Bar Indicator
    function initReadingProgressBar() {
        const bar = document.getElementById('readingProgress');
        if (!bar) return;

        window.addEventListener('scroll', function () {
            const docHeight = document.documentElement.scrollHeight - window.innerHeight;
            if (docHeight > 0) {
                const progress = (window.scrollY / docHeight) * 100;
                bar.style.width = Math.min(100, Math.max(0, progress)) + '%';
            }
        }, { passive: true });
    }

    // 2. Dismiss Toast with smooth slide-up animation
    window.dismissToast = function (toastEl) {
        if (!toastEl) return;
        toastEl.classList.add('session-toast--hiding');
        setTimeout(() => {
            toastEl.remove();
        }, 300);
    };

    // 3. Auto-dismiss timer for toasts with hover pause
    function setupToastTimer(toast, duration = 4500) {
        let timer = setTimeout(() => {
            window.dismissToast(toast);
        }, duration);

        toast.addEventListener('mouseenter', () => clearTimeout(timer));
        toast.addEventListener('mouseleave', () => {
            timer = setTimeout(() => window.dismissToast(toast), 2000);
        });
    }

    // 4. Global function to trigger a Laravel-style Toast dynamically
    window.showToast = function (message, type = 'success', title = null) {
        const container = document.getElementById('toastContainer');
        if (!container) return;

        const iconClass = type === 'success' ? 'bi-check-lg'
            : (type === 'error' || type === 'danger') ? 'bi-exclamation-triangle-fill'
            : type === 'warning' ? 'bi-exclamation-circle-fill'
            : 'bi-info-circle-fill';

        const defaultTitle = type === 'success' ? 'Success'
            : (type === 'error' || type === 'danger') ? 'Attention'
            : type === 'warning' ? 'Warning'
            : 'Notice';

        const toast = document.createElement('div');
        toast.className = `session-toast session-toast--${type}`;
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <div class="session-toast__inner">
                <div class="session-toast__icon">
                    <i class="bi ${iconClass}"></i>
                </div>
                <div class="session-toast__content">
                    <div class="session-toast__title">${title || defaultTitle}</div>
                    <div class="session-toast__message">${message}</div>
                </div>
                <button type="button" class="session-toast__close" aria-label="Dismiss notification" onclick="dismissToast(this.closest('.session-toast'))">
                    <i class="bi bi-x"></i>
                </button>
            </div>
            <div class="session-toast__progress">
                <div class="session-toast__progress-bar"></div>
            </div>
        `;

        container.appendChild(toast);
        setupToastTimer(toast, 4500);
    };

    // Initialize on DOM Ready
    document.addEventListener('DOMContentLoaded', function () {
        initReadingProgressBar();

        // Attach timers to existing server-rendered session toasts
        const existingToasts = document.querySelectorAll('.session-toast');
        existingToasts.forEach(toast => setupToastTimer(toast, 4500));
    });

})();
