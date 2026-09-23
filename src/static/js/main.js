/**
 * Modern lightweight script for 机场推荐云 (jichangtuijian.cloud)
 * Zero dependencies, privacy-respecting, accessible
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Mobile Menu Toggle
  const menuToggle = document.querySelector('.mobile-menu-toggle');
  const navRow = document.querySelector('.header-nav-row');
  
  if (menuToggle && navRow) {
    menuToggle.addEventListener('click', () => {
      const isExpanded = menuToggle.getAttribute('aria-expanded') === 'true';
      menuToggle.setAttribute('aria-expanded', !isExpanded);
      navRow.classList.toggle('is-open');
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && navRow.classList.contains('is-open')) {
        menuToggle.setAttribute('aria-expanded', 'false');
        navRow.classList.remove('is-open');
        menuToggle.focus();
      }
    });
  }

  // 2. Coupon Copy Functionality
  document.querySelectorAll('.btn-copy').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      const code = btn.getAttribute('data-coupon');
      const provider = btn.getAttribute('data-provider') || 'unknown';
      if (!code) return;

      try {
        if (navigator.clipboard && window.isSecureContext) {
          await navigator.clipboard.writeText(code);
        } else {
          // Fallback selection
          const textarea = document.createElement('textarea');
          textarea.value = code;
          textarea.style.position = 'fixed';
          textarea.style.opacity = '0';
          document.body.appendChild(textarea);
          textarea.select();
          document.execCommand('copy');
          document.body.removeChild(textarea);
        }
        
        const origText = btn.textContent;
        btn.textContent = '已复制！';
        btn.style.color = '#10b981';
        btn.style.fontWeight = 'bold';
        
        // Track coupon_copy event
        trackEvent('coupon_copy', {
          provider: provider,
          coupon: code,
          page_path: window.location.pathname
        });

        setTimeout(() => {
          btn.textContent = origText;
          btn.style.color = '';
          btn.style.fontWeight = '';
        }, 2000);
      } catch (err) {
        console.error('Copy failed:', err);
      }
    });
  });

  // 3. Track Affiliate Link Clicks
  document.querySelectorAll('a[rel*="sponsored"]').forEach(link => {
    link.addEventListener('click', (e) => {
      const provider = link.getAttribute('data-provider') || 'unknown';
      const rank = link.getAttribute('data-rank') || '';
      const placement = link.getAttribute('data-placement') || 'card';
      
      trackEvent('affiliate_click', {
        provider: provider,
        rank: rank,
        placement: placement,
        page_path: window.location.pathname
      });
    });
  });

  // 4. Track Provider Detail Views
  const providerDetailElem = document.querySelector('[data-page-type="provider-detail"]');
  if (providerDetailElem) {
    const providerName = providerDetailElem.getAttribute('data-provider-name');
    trackEvent('provider_detail_view', {
      provider: providerName,
      page_path: window.location.pathname
    });
  }
});

/**
 * Privacy-friendly First-Party Event Tracker
 */
function trackEvent(eventName, eventParams) {
  // If window.gtag or custom analytics is configured, dispatch event
  if (typeof window.gtag === 'function') {
    window.gtag('event', eventName, eventParams);
  }
  // Console logging for verification in dev/local mode
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    console.log(`[Analytics Event] ${eventName}:`, eventParams);
  }
}
