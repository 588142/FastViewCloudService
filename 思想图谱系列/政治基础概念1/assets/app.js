(function () {
  var input = document.getElementById('termSearch');
  var counter = document.getElementById('resultCount');
  var terms = Array.prototype.slice.call(document.querySelectorAll('.term'));
  var chapters = Array.prototype.slice.call(document.querySelectorAll('.chapter'));
  var tocLinks = Array.prototype.slice.call(document.querySelectorAll('.toc a'));
  var total = terms.length;

  function applyFilter(q) {
    var visible = 0;
    terms.forEach(function (t) {
      var hay = (t.getAttribute('data-term') || '') + ' ' +
                (t.getAttribute('data-en') || '') + ' ' +
                (t.textContent || '');
      var show = !q || hay.toLowerCase().indexOf(q) !== -1;
      t.style.display = show ? '' : 'none';
      if (show) visible++;
    });
    chapters.forEach(function (c) {
      var visInSec = Array.prototype.some.call(c.querySelectorAll('.term'), function (t) {
        return t.style.display !== 'none';
      });
      c.style.display = visInSec ? '' : 'none';
    });
    if (counter) counter.textContent = visible + ' / ' + total + ' 条';
  }

  if (input) {
    input.addEventListener('input', function () {
      applyFilter(input.value.trim().toLowerCase());
    });
  }

  var spy = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) {
        var id = e.target.getAttribute('id');
        tocLinks.forEach(function (a) {
          a.classList.toggle('active', a.getAttribute('href') === '#' + id);
        });
      }
    });
  }, { rootMargin: '-20% 0px -70% 0px' });

  chapters.forEach(function (c) { spy.observe(c); });
})();
