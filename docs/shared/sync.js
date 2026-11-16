// sync.js: a demo on a Slidev slide (<LiveFrame src="…"> of the presenter addon) follows
// its twin in the other window: a slider moved in the presenter view moves on the projector too.
// Standalone (not in an iframe) it does nothing; the demo works as before.
//
// Use: <script src="./shared/sync.js"></script> before the demo's own script. Every
// <input>/<select>/<textarea> with an id is synced by itself. State outside the form fields
// (data, drags, animation step) the demo gives with two hooks, in its own script:
//   LiveSync.get = () => ({ xData, yData })        // plain JSON
//   LiveSync.set = s => { xData = s.xData; …; render() }
// and calls LiveSync.send() when that state changes without a click, key or pointer
// (an animation step). After a user action (input, click, key, drag) it sends by itself.
//
// Messages: to the parent { type: 'oli-frame', state, hello? } (hello once after load, with
// the start state), from the parent { type: 'oli-frame-set', state }.
(function () {
  const api = { get: null, set: null, send () {} };
  window.LiveSync = api;
  const parent = window.parent;
  if (parent === window) return;

  let applying = false, timer = 0, lastSent = '';
  const fields = () => [...document.querySelectorAll('input[id], select[id], textarea[id]')]
    .filter(el => el.type !== 'file' && el.type !== 'password');
  const isCheck = el => el.type === 'checkbox' || el.type === 'radio';

  function snapshot () {
    const f = {};
    for (const el of fields()) f[el.id] = isCheck(el) ? el.checked : el.value;
    return { f, x: api.get ? api.get() : null };
  }
  function post (hello) {
    const state = snapshot();
    const json = JSON.stringify(state);
    if (!hello && json === lastSent) return;
    lastSent = json;
    parent.postMessage({ type: 'oli-frame', state, hello }, '*');
  }
  // after the demo's own handlers ran; at most every 40 ms while dragging
  api.send = () => {
    if (applying || timer) return;
    timer = setTimeout(() => { timer = 0; post(false); }, 40);
  };

  function apply (s) {
    applying = true;
    try {
      for (const el of fields()) {
        if (!s.f || !(el.id in s.f)) continue;
        const v = s.f[el.id];
        if (isCheck(el)) {
          if (el.checked === v) continue;
          el.checked = v;
          if (el.type === 'radio' && !v) continue; // only the radio that becomes checked fires
        } else {
          if (el.value === String(v)) continue;
          el.value = v;
        }
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
      }
      if (s.x != null && api.set) api.set(s.x);
    } finally {
      applying = false;
    }
    lastSent = JSON.stringify(snapshot());
  }

  window.addEventListener('message', e => {
    if (e.source === parent && e.data && e.data.type === 'oli-frame-set' && e.data.state) apply(e.data.state);
  });
  // only what a person did here, not what apply() set
  const user = e => { if (e.isTrusted) api.send(); };
  for (const t of ['input', 'change', 'click', 'keyup', 'pointerup']) document.addEventListener(t, user, true);
  document.addEventListener('pointermove', e => { if (e.buttons) user(e); }, true);
  window.addEventListener('load', () => post(true));
})();
