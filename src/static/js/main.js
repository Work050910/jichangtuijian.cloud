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

  // 6. Article Table of Contents (TOC), Scrollspy & Dynamic URL Hash
  initArticleTocAndScrollspy();
});

/**
 * Automatically extracts H2 & H3 headings in article, generates IDs,
 * creates a hierarchical Table of Contents (TOC) in the sidebar,
 * implements smooth scrolling, and uses IntersectionObserver for scrollspy
 * with silent URL hash updates.
 */
function initArticleTocAndScrollspy() {
  const articleMain = document.querySelector('.article-main') || document.querySelector('article');
  if (!articleMain) return;

  const articleBody = articleMain.querySelector('.article-body') || articleMain;
  // Extract all H2 and H3 headings inside the article body
  const headings = Array.from(articleBody.querySelectorAll('h2, h3')).filter(h => {
    return !h.closest('.article-header') && 
           !h.closest('.article-sidebar') && 
           !h.closest('.site-footer') &&
           !h.closest('.hero-section');
  });

  if (headings.length < 2) return;

  // 1. Auto-generate unique IDs from heading text
  const existingIds = new Set();
  document.querySelectorAll('[id]').forEach(el => {
    if (el.id) existingIds.add(el.id);
  });

  headings.forEach(heading => {
    if (!heading.id) {
      let slug = heading.textContent
        .trim()
        .toLowerCase()
        .replace(/[^\w\u4e00-\u9fa5\s\-_]/g, '')
        .replace(/\s+/g, '-')
        .replace(/-+/g, '-')
        .replace(/^-|-$/g, '');

      if (!slug) slug = 'section';

      let uniqueId = slug;
      let counter = 1;
      while (existingIds.has(uniqueId)) {
        uniqueId = `${slug}-${counter++}`;
      }
      heading.id = uniqueId;
    }
    existingIds.add(heading.id);
  });

  // 2. Generate Sidebar Table of Contents (TOC)
  const sidebar = document.querySelector('.article-sidebar');
  if (!sidebar) return;

  const tocWidget = document.createElement('div');
  tocWidget.className = 'sidebar-widget toc-widget';
  tocWidget.id = 'article-toc-widget';

  const titleDiv = document.createElement('div');
  titleDiv.className = 'widget-title';
  titleDiv.innerHTML = '<span>📑 文章目录</span>';
  tocWidget.appendChild(titleDiv);

  const nav = document.createElement('nav');
  nav.className = 'toc-nav';
  nav.setAttribute('aria-label', '文章目录');

  const ul = document.createElement('ul');
  ul.className = 'toc-list';

  headings.forEach(heading => {
    const level = heading.tagName.toLowerCase(); // 'h2' or 'h3'
    const li = document.createElement('li');
    li.className = `toc-item toc-${level}`;

    const a = document.createElement('a');
    a.href = `#${heading.id}`;
    a.className = 'toc-link';
    a.textContent = heading.textContent.trim();
    a.setAttribute('data-target', heading.id);

    li.appendChild(a);
    ul.appendChild(li);
  });

  nav.appendChild(ul);
  tocWidget.appendChild(nav);

  // Prepend TOC as the first widget in sidebar
  sidebar.insertBefore(tocWidget, sidebar.firstChild);

  // 3. Smooth Scrolling on TOC click
  let isManualScrolling = false;
  let scrollTimeout = null;

  tocWidget.querySelectorAll('.toc-link').forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const targetId = link.getAttribute('data-target');
      const target = document.getElementById(targetId);
      if (!target) return;

      isManualScrolling = true;
      if (scrollTimeout) clearTimeout(scrollTimeout);

      const headerOffset = 85;
      const elementPosition = target.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
      });

      // Silently update URL hash without page reload or history pollution
      history.replaceState(null, null, `#${targetId}`);

      // Highlight active TOC item
      setActiveTocItem(targetId);

      // Re-enable scrollspy tracking after smooth scroll completes
      scrollTimeout = setTimeout(() => {
        isManualScrolling = false;
      }, 800);
    });
  });

  function setActiveTocItem(id) {
    if (!id) return;
    const allLinks = tocWidget.querySelectorAll('.toc-link');
    const allItems = tocWidget.querySelectorAll('.toc-item');
    allLinks.forEach(l => l.classList.remove('active'));
    allItems.forEach(i => i.classList.remove('active'));

    const safeId = (window.CSS && CSS.escape) ? CSS.escape(id) : id.replace(/"/g, '\\"');
    const targetLink = tocWidget.querySelector(`.toc-link[data-target="${safeId}"]`);
    if (targetLink) {
      targetLink.classList.add('active');
      const parentItem = targetLink.closest('.toc-item');
      if (parentItem) parentItem.classList.add('active');

      // Keep active TOC link within visible range of its scrollable container without moving window
      const tocNav = tocWidget.querySelector('.toc-nav');
      if (tocNav) {
        const itemTop = targetLink.offsetTop;
        const itemBottom = itemTop + targetLink.offsetHeight;
        if (itemTop < tocNav.scrollTop) {
          tocNav.scrollTop = itemTop - 10;
        } else if (itemBottom > tocNav.scrollTop + tocNav.clientHeight) {
          tocNav.scrollTop = itemBottom - tocNav.clientHeight + 10;
        }
      }
    }
  }

  // 4. Scrollspy with Intersection Observer API (Core)
  let activeHeadingId = '';

  const observerOptions = {
    root: null,
    rootMargin: '-80px 0px -70% 0px',
    threshold: 0
  };

  const observer = new IntersectionObserver((entries) => {
    if (isManualScrolling) return;
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.id;
        if (id && id !== activeHeadingId) {
          activeHeadingId = id;
          setActiveTocItem(id);
          history.replaceState(null, null, `#${id}`);
        }
      }
    });
  }, observerOptions);

  headings.forEach(h => observer.observe(h));

  // Fluid bidirectional scroll fallback with requestAnimationFrame
  let ticking = false;
  window.addEventListener('scroll', () => {
    if (isManualScrolling) return;
    if (!ticking) {
      window.requestAnimationFrame(() => {
        let currentId = null;
        for (let i = 0; i < headings.length; i++) {
          const rect = headings[i].getBoundingClientRect();
          if (rect.top <= 120) {
            currentId = headings[i].id;
          } else {
            break;
          }
        }
        if (!currentId && headings.length > 0) {
          const firstRect = headings[0].getBoundingClientRect();
          if (firstRect.top < window.innerHeight && firstRect.top > 0) {
            currentId = headings[0].id;
          }
        }

        if (currentId && currentId !== activeHeadingId) {
          activeHeadingId = currentId;
          setActiveTocItem(activeHeadingId);
          history.replaceState(null, null, `#${activeHeadingId}`);
        }
        ticking = false;
      });
      ticking = true;
    }
  }, { passive: true });

  // 5. Initial positioning when loaded with #xxx hash
  if (window.location.hash) {
    const rawHash = window.location.hash.slice(1);
    let targetId = rawHash;
    try {
      targetId = decodeURIComponent(rawHash);
    } catch (err) {}

    const targetElement = document.getElementById(targetId) || document.getElementById(rawHash);
    if (targetElement) {
      setTimeout(() => {
        const headerOffset = 85;
        const elementPosition = targetElement.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

        window.scrollTo({
          top: offsetPosition,
          behavior: 'smooth'
        });

        activeHeadingId = targetElement.id;
        setActiveTocItem(targetElement.id);
      }, 250);
    }
  }
}


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
