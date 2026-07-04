
async function main(){
  const r = await fetch('data/project_status.json');
  const data = await r.json();
  document.getElementById('version').textContent = data.version;
  document.getElementById('crs').textContent = data.crs;
  const grid = document.getElementById('modules');
  for(const m of data.modules){
    const div = document.createElement('article');
    div.className='card';
    div.innerHTML = `<h2>${m.name}</h2>
      <span class="badge ${m.status}">${m.status}</span>
      <div class="progress"><div class="bar" style="width:${m.progress}%"></div></div>
      <div><b>${m.progress}%</b></div>
      <p class="small">${m.note}</p>`;
    grid.appendChild(div);
  }
  document.getElementById('steps').textContent = data.next_steps.map((s,i)=>`${i+1}. ${s}`).join('\n');
}
main();
