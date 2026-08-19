/* Process spine - progressive enhancement only.
   This file adds mode switching and deep links. It never renders content:
   with JavaScript disabled the page is already complete and readable. */
(function () {
  'use strict';

  var root = document.body;
  root.classList.add('has-js');

  /* ---- 1. Gate set switch -------------------------------------------------
     Toggles between the full gate set and a reduced one. Which gates belong to
     which set is org specific and is marked in the markup, not decided here. */

  var btnFull = document.getElementById('btn-full');
  var btnLean = document.getElementById('btn-lean');
  var note    = document.getElementById('modenote');

  var COPY = {
    full: 'Switch the gate set to see which decisions apply under each variant.',
    lean: 'Reduced gate set. Decisions marked as not applying are dimmed.'
  };

  function setMode(mode) {
    root.setAttribute('data-mode', mode);
    var lean = mode === 'lean';
    btnFull.setAttribute('aria-pressed', String(!lean));
    btnLean.setAttribute('aria-pressed', String(lean));
    note.textContent = COPY[mode];
  }

  if (btnFull && btnLean && note) {
    btnFull.addEventListener('click', function () { setMode('full'); });
    btnLean.addEventListener('click', function () { setMode('lean'); });
    setMode('full');
  }

  /* ---- 2. Deep links ------------------------------------------------------
     The tenant URL is not committed to this repository. The SharePoint Embed
     passes it in as ?base=<encoded site url>; only then do the nodes become
     links. Without it the page still shows every stage, gate, and question. */

  var base;
  try {
    base = new URLSearchParams(window.location.search).get('base');
  } catch (e) {
    base = null;
  }
  if (!base) return;

  base = base.replace(/\/+$/, '');
  if (!/^https:\/\/[^/]+\.sharepoint\.com\//i.test(base + '/')) return;

  Array.prototype.forEach.call(document.querySelectorAll('.node[data-sp]'), function (node) {
    var key = node.getAttribute('data-sp');
    node.setAttribute('href', base + '/SitePages/process-spine.aspx#' + encodeURIComponent(key));
    /* Escape the iframe so the intranet does not render inside itself. */
    node.setAttribute('target', '_parent');
    node.setAttribute('rel', 'noopener');
  });
})();
