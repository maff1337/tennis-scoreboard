(() => {
  'use strict';

  const forms = document.querySelectorAll('form[data-once]');

  const unlock = (form) => {
    delete form.dataset.sent;
    form.classList.remove('is-sent');
  };

  forms.forEach((form) => {
    form.addEventListener('submit', (event) => {
      if (form.dataset.sent === '1') {
        event.preventDefault();
        return;
      }
      form.dataset.sent = '1';
      form.classList.add('is-sent');
      
      setTimeout(() => unlock(form), 8000);
    });
  });

  window.addEventListener('pageshow', (event) => {
    if (event.persisted) forms.forEach(unlock);
  });

  const board = document.querySelector('[data-match]');
  if (!board) return;

  const storageKey = `score:${board.dataset.match}`;
  let previous = {};
  try {
    previous = JSON.parse(sessionStorage.getItem(storageKey) || '{}');
  } catch (e) {
    previous = {};
  }

  const current = {};
  board.querySelectorAll('[data-tile]').forEach((tile) => {
    const name = tile.dataset.tile;
    const value = tile.textContent.trim();
    current[name] = value;
    if (name in previous && previous[name] !== value) {
      tile.classList.add('is-flipping');
    }
  });

  try {
    sessionStorage.setItem(storageKey, JSON.stringify(current));
  } catch (e) {
    /* хранилище недоступно: просто без анимации */
  }
})();