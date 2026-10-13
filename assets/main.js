/* Settings live in assets/config.js (loaded before this file), so updates to main.js never wipe them. */
const FORM_ENDPOINT = (window.FS_CONFIG && window.FS_CONFIG.formEndpoint) || "";
const CONTACT_EMAIL = (window.FS_CONFIG && window.FS_CONFIG.contactEmail) || "hello@freesummitpt.com";

document.getElementById('yr').textContent = new Date().getFullYear();
const mailLink = document.getElementById('mailLink');
mailLink.href = 'mailto:' + CONTACT_EMAIL; mailLink.textContent = CONTACT_EMAIL;

/* --- Language toggle (EN in markup, PT in data-pt) --- */
let lang = 'en';
try { lang = localStorage.getItem('fs-lang') || ((navigator.language||'').toLowerCase().startsWith('pt') ? 'pt' : 'en'); } catch(e){}
function setLang(l){
  lang = l;
  document.documentElement.lang = l === 'pt' ? 'pt-PT' : 'en';
  document.querySelectorAll('[data-pt]').forEach(el=>{
    if(el.dataset.en === undefined) el.dataset.en = el.textContent;
    el.textContent = l === 'pt' ? el.dataset.pt : el.dataset.en;
  });
  document.querySelectorAll('[data-pt-placeholder]').forEach(el=>{
    if(el.dataset.enPlaceholder === undefined) el.dataset.enPlaceholder = el.placeholder;
    el.placeholder = l === 'pt' ? el.dataset.ptPlaceholder : el.dataset.enPlaceholder;
  });
  document.querySelectorAll('img[data-pt-alt]').forEach(img=>{
    if(img.dataset.enAlt === undefined) img.dataset.enAlt = img.alt;
    img.alt = l === 'pt' ? img.dataset.ptAlt : img.dataset.enAlt;
  });
  document.querySelectorAll('td[data-label-pt]').forEach(td=>{
    if(td.dataset.labelEn === undefined) td.dataset.labelEn = td.dataset.label;
    td.dataset.label = l === 'pt' ? td.dataset.labelPt : td.dataset.labelEn;
  });
  const b = document.getElementById('langBtn');
  b.textContent = l === 'pt' ? 'EN' : 'PT';
  b.setAttribute('aria-label', l === 'pt' ? 'Switch to English' : 'Mudar para português');
  try { localStorage.setItem('fs-lang', l); } catch(e){}
}
document.getElementById('langBtn').addEventListener('click', ()=> setLang(lang === 'pt' ? 'en' : 'pt'));
setLang(lang);

/* --- Topographic hero (contour lines, like the logo) --- */
(function(){
  const svg = document.getElementById('topo');
  if(!svg) return;
  const W = 1600, H = 1000; svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
  const peaks = [{x:1180,y:330,s:1},{x:300,y:880,s:.7},{x:1500,y:900,s:.5}];
  const ns = 'http://www.w3.org/2000/svg';
  let seed = 7; const rnd = ()=> (seed = (seed*16807)%2147483647, seed/2147483647);
  const paths = [];
  peaks.forEach((p,pi)=>{
    const harm = [1,2,3,5].map(k=>({k, a:rnd()*2*Math.PI, m:(.10+rnd()*.12)/k*1.6}));
    const rings = Math.round(22*p.s);
    for(let i=1;i<=rings;i++){
      const r = i*34*p.s + 10;
      const pts = [];
      for(let t=0;t<=96;t++){
        const th = t/96*2*Math.PI;
        let f = 1; harm.forEach(h=> f += h.m*Math.sin(h.k*th + h.a + i*.045*h.k));
        pts.push([p.x + Math.cos(th)*r*f*1.25, p.y + Math.sin(th)*r*f*.85]);
      }
      const d = pts.map((q,j)=>(j?'L':'M')+q[0].toFixed(1)+' '+q[1].toFixed(1)).join('')+'Z';
      const el = document.createElementNS(ns,'path');
      el.setAttribute('d', d);
      if(i%5===0) el.setAttribute('class','idx');
      svg.appendChild(el); paths.push(el);
    }
  });
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(!reduce && 'getTotalLength' in paths[0]){
    paths.forEach((el,i)=>{
      const L = el.getTotalLength();
      el.style.strokeDasharray = L; el.style.strokeDashoffset = L;
      el.style.transition = `stroke-dashoffset 1.8s cubic-bezier(.3,.6,.2,1) ${Math.min(i*28,900)}ms`;
    });
    requestAnimationFrame(()=>requestAnimationFrame(()=>paths.forEach(el=> el.style.strokeDashoffset = 0)));
  }
})();

/* --- Booking form --- */
const form = document.getElementById('bookForm');
// Activity pages pre-select their activity: <form data-activity="...">
// Links with data-select="<activity>" pick that activity in the form (e.g. "Know more" before a page exists)
document.querySelectorAll('[data-select]').forEach(a=>a.addEventListener('click',()=>{ const sel=document.getElementById('f-activity'); if(sel) sel.value=a.dataset.select; }));
if(form.dataset.activity){ const sel = document.getElementById('f-activity'); if(sel) sel.value = form.dataset.activity; }
const msg = document.getElementById('formMsg');
const T = {
  en:{missing:'Add your name, a valid email and the activity, then send again.', sending:'Sending…', ok:'Request sent. We will reply within 24 hours.', fail:'The request did not go through. Email us at '},
  pt:{missing:'Preenche o nome, um email válido e a actividade, e envia de novo.', sending:'A enviar…', ok:'Pedido enviado. Respondemos em 24 horas.', fail:'O pedido não foi enviado. Escreve-nos para '}
};
form.addEventListener('submit', async (e)=>{
  e.preventDefault();
  const t = T[lang]; msg.className = 'form-msg';
  const data = new FormData(form);
  if(data.get('website')) return; // spam trap
  const email = (data.get('email')||'').trim();
  if(!data.get('name').trim() || !/^\S+@\S+\.\S+$/.test(email) || !data.get('activity')){
    msg.textContent = t.missing; msg.classList.add('err'); return;
  }
  data.append('lang', lang);
  data.append('source', document.body.dataset.page || 'home');
  if(!FORM_ENDPOINT){
    // Fallback until the Google Sheet endpoint is connected: open an email draft.
    const body = [...data.entries()].filter(([k])=>k!=='website').map(([k,v])=>`${k}: ${v}`).join('\n');
    location.href = `mailto:${CONTACT_EMAIL}?subject=${encodeURIComponent('Booking request – '+data.get('activity'))}&body=${encodeURIComponent(body)}`;
    return;
  }
  const btn = document.getElementById('sendBtn'); btn.disabled = true;
  msg.textContent = t.sending;
  try{
    await fetch(FORM_ENDPOINT, {method:'POST', mode:'no-cors', body:new URLSearchParams(data)});
    form.reset(); if(form.dataset.activity) document.getElementById('f-activity').value = form.dataset.activity; msg.textContent = t.ok; msg.classList.add('ok');
  }catch(err){
    msg.textContent = t.fail + CONTACT_EMAIL; msg.classList.add('err');
  }finally{ btn.disabled = false; }
});
