function showToast(message){const t=document.getElementById('toast');if(!t)return;t.textContent=message;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),3000)}
async function refreshAuthLink(){const r=await fetch('/session-info');if(!r.ok)return;const d=await r.json();const a=document.getElementById('authLink');if(a&&d.logged_in){a.textContent='Dashboard';a.href='/dashboard'}}
refreshAuthLink();
