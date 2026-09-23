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

  // 2. Real-time Search Box
  const searchInput = document.getElementById('header-search-input');
  const searchDropdown = document.getElementById('header-search-results');

  if (searchInput && searchDropdown) {
    searchInput.addEventListener('input', (e) => {
      const query = e.target.value.trim().toLowerCase();
      if (!query || !window.SITE_SEARCH_INDEX) {
        searchDropdown.classList.remove('is-active');
        searchDropdown.innerHTML = '';
        return;
      }

      const results = window.SITE_SEARCH_INDEX.filter(item => {
        return item.title.toLowerCase().includes(query) ||
               (item.keywords && item.keywords.toLowerCase().includes(query));
      }).slice(0, 8); // Top 8 results

      if (results.length === 0) {
        searchDropdown.innerHTML = '<div style="padding:14px;font-size:13px;color:var(--text-light);text-align:center;">未找到匹配文章或节点</div>';
      } else {
        searchDropdown.innerHTML = results.map(r => `
          <a href="${r.url}" class="search-result-item">
            <div class="search-result-title">${escapeHTML(r.title)}</div>
            <span class="search-result-badge">${escapeHTML(r.type || '文章')}</span>
          </a>
        `).join('');
      }
      searchDropdown.classList.add('is-active');
    });

    // Close search dropdown on click outside
    document.addEventListener('click', (e) => {
      if (!searchInput.contains(e.target) && !searchDropdown.contains(e.target)) {
        searchDropdown.classList.remove('is-active');
      }
    });

    // Keyboard navigation
    searchInput.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        searchDropdown.classList.remove('is-active');
      }
    });
  }

  // 3. Coupon Copy Functionality
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

  // 4. Track Affiliate Link Clicks
  document.querySelectorAll('a[rel*="sponsored"]').forEach(link => {
    link.addEventListener('click', () => {
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

  // 5. Track Provider Detail Views
  const providerDetailElem = document.querySelector('[data-page-type="provider-detail"]');
  if (providerDetailElem) {
    const providerName = providerDetailElem.getAttribute('data-provider-name');
    trackEvent('provider_detail_view', {
      provider: providerName,
      page_path: window.location.pathname
    });
  }
});

function escapeHTML(str) {
  if (!str) return '';
  return str.replace(/[&<>'"]/g, 
    tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag)
  );
}

function trackEvent(eventName, eventParams) {
  if (typeof window.gtag === 'function') {
    window.gtag('event', eventName, eventParams);
  }
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    console.log(`[Analytics Event] ${eventName}:`, eventParams);
  }
}
