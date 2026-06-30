/**
 * Blog filters and search for static HTML
 */
function filterPosts(category) {
  const posts = document.querySelectorAll('.blog-card');
  const searchTerm = (document.getElementById('blog-search')?.value || '').toLowerCase();

  posts.forEach(post => {
    const postCategory = post.getAttribute('data-category') || 
      (post.querySelector('.blog-badge')?.textContent?.toLowerCase().replace(/\s+/g, '_') || '');
    const title = post.querySelector('.card-title')?.textContent?.toLowerCase() || '';
    const excerpt = post.querySelector('.blog-excerpt')?.textContent?.toLowerCase() || '';
    const matchesSearch = !searchTerm || title.includes(searchTerm) || excerpt.includes(searchTerm);
    const matchesCategory = category === 'all' || postCategory === category || postCategory.includes(category);
    post.style.display = (matchesSearch && matchesCategory) ? '' : 'none';
  });

  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.classList.remove('active');
    const btnCategory = btn.getAttribute('onclick')?.match(/filterPosts\('([^']+)'\)/);
    if (btnCategory && btnCategory[1] === category) {
      btn.classList.add('active');
    }
  });
}

document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('blog-search')?.addEventListener('input', function() {
    const activeBtn = document.querySelector('.filter-btn.active');
    const category = activeBtn ? (activeBtn.getAttribute('onclick')?.match(/filterPosts\('([^']+)'\)/)?.[1] || 'all') : 'all';
    filterPosts(category);
  });
});
