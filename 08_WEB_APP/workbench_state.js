const URLE_STATE_KEY='urle_gcp_workbench_v3_2';

window.URLEState={
  load(base){
    try{
      const raw=localStorage.getItem(URLE_STATE_KEY);
      if(!raw)return base;
      const saved=JSON.parse(raw);
      if(!saved||!Array.isArray(saved.gcps))return base;
      const map=new Map(saved.gcps.map(g=>[g.gcp_id,g]));
      base.gcps=base.gcps.map(g=>map.has(g.gcp_id)?Object.assign({},g,map.get(g.gcp_id)):g);
      return base;
    }catch(e){console.warn('URLE state load failed',e);return base}
  },
  save(data){
    const payload={version:'3.2',saved_at:new Date().toISOString(),gcps:data.gcps};
    localStorage.setItem(URLE_STATE_KEY,JSON.stringify(payload));
    return payload.saved_at;
  },
  clear(){localStorage.removeItem(URLE_STATE_KEY)},
  exportJson(data){
    const payload={version:'3.2',saved_at:new Date().toISOString(),gcps:data.gcps};
    const a=document.createElement('a');
    a.href=URL.createObjectURL(new Blob([JSON.stringify(payload,null,2)],{type:'application/json'}));
    a.download='URLE_GCP_WORKBENCH_BACKUP.json';
    a.click();
  }
};
