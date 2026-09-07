(function () {
  if (window.mermaid) {
    mermaid.initialize({
      startOnLoad: true,
      theme: 'neutral',
      securityLevel: 'loose',
      flowchart: { curve: 'basis', htmlLabels: true },
      fontFamily: 'WorkSans, PingFang SC, Microsoft YaHei, sans-serif'
    });
  }

  var input = document.getElementById('searchInput');
  var sections = Array.prototype.slice.call(document.querySelectorAll('section.sec'));
  var tocLinks = Array.prototype.slice.call(document.querySelectorAll('#toc a'));

  function applyFilter() {
    var q = (input.value || '').trim().toLowerCase();
    sections.forEach(function (sec) {
      var hit = !q || sec.textContent.toLowerCase().indexOf(q) !== -1;
      sec.classList.toggle('hidden-by-search', !hit);
    });
    tocLinks.forEach(function (a) {
      var id = a.getAttribute('href').slice(1);
      var sec = document.getElementById(id);
      var visible = sec && !sec.classList.contains('hidden-by-search');
      a.style.opacity = visible ? '' : '0.35';
    });
  }

  if (input) {
    input.addEventListener('input', applyFilter);
  }
})();
