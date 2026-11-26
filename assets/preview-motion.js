/* GSAP is local; all content remains visible if the library cannot load. */
(() => {
  const art = document.querySelector('#heroArt');
  if (!art) return;
  const en = document.documentElement.lang === 'en';
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'motion-toggle';
  art.after(button);
  let paused = reduced.matches, visible = true, rev;
  const speed = {rate: 1};
  const animations = () => [...document.querySelectorAll('.chain-tooth')].flatMap(el => el.getAnimations());
  function sync() {
    const stopped = paused || !visible || document.hidden;
    if (stopped && rev) {
      rev.kill();
      rev = undefined;
      speed.rate = 1;
      updateSpeed();
    }
    animations().forEach(animation => stopped ? animation.pause() : animation.play());
    button.hidden = reduced.matches;
    art.disabled = paused || reduced.matches;
    button.textContent = paused ? (en ? 'Play chainsaws' : '播放电锯动画') : (en ? 'Pause chainsaws' : '暂停电锯动画');
  }
  function updateSpeed() { animations().forEach(a => a.updatePlaybackRate(speed.rate)); }
  button.addEventListener('click', () => { paused = !paused; sync(); });
  reduced.addEventListener('change', () => { paused = reduced.matches; sync(); });
  document.addEventListener('visibilitychange', sync);
  const observer = new IntersectionObserver(([entry]) => { visible = entry.isIntersecting; sync(); });
  observer.observe(art);
  art.addEventListener('click', () => {
    if (paused || !visible || reduced.matches || !window.gsap) return;
    rev?.kill();
    rev = gsap.timeline().to(speed, {rate:4,duration:.18,ease:'power2.out',onUpdate:updateSpeed})
      .to(speed,{rate:1,duration:1.1,ease:'power2.inOut',onUpdate:updateSpeed},'+=.35');
  });
  sync();
  if (!window.gsap) return;
  const media = gsap.matchMedia();
  media.add('(prefers-reduced-motion: no-preference)', () => {
    gsap.timeline({defaults:{duration:.65,ease:'power3.out',clearProps:'transform,opacity'}})
      .from('.hero h1 > *',{y:24,opacity:0,stagger:.09})
      .from('.hero p, .hero-actions',{y:14,opacity:0,stagger:.08},'-.35')
      .from('.hero .art',{y:20,opacity:0,duration:.85},.18);

    const chapters = new IntersectionObserver((entries) => {
      for (const {target, isIntersecting} of entries) {
        if (!isIntersecting) continue;
        chapters.unobserve(target);
        gsap.from(target, {scaleX:.14, duration:.55, ease:'power3.out', clearProps:'transform'});
      }
    }, {threshold:.75});
    document.querySelectorAll('[data-chapter-rule]').forEach(rule => chapters.observe(rule));
    return () => {
      chapters.disconnect();
      gsap.killTweensOf('[data-chapter-rule]');
      gsap.set('[data-chapter-rule]', {clearProps:'transform'});
    };
  });
  addEventListener('pagehide', (event) => {
    if (event.persisted) return;
    rev?.kill();
    media.revert();
    observer.disconnect();
  });
  addEventListener('pageshow', () => { observer.observe(art); sync(); });
})();
