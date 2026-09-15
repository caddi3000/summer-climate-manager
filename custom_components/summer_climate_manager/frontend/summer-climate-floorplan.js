const CARD_VERSION = "0.1.5";

class SummerClimateFloorplan extends HTMLElement {
  setConfig(config) {
    this.config = config || {};
    this.selected = this.selected || "open";
    if (!this.shadowRoot) this.attachShadow({mode:"open"});
  }
  set hass(hass) { this._hass = hass; this.render(); }
  getCardSize(){ return 12; }
  static getStubConfig(){ return {}; }

  findFrontend(){
    const states=this._hass?.states||{};
    return Object.values(states).find(
      s => s.entity_id.startsWith("sensor.") &&
           s.attributes?.card_config &&
           s.attributes?.card_version
    )?.attributes || null;
  }
  st(id){ return id ? this._hass?.states?.[id] : null; }
  val(id, fallback="—"){
    const s=this.st(id);
    return s && !["unknown","unavailable"].includes(s.state) ? s.state : fallback;
  }
  num(id){ const v=parseFloat(this.val(id,"")); return Number.isFinite(v)?v:null; }
  temp(zone,cfg){
    const n=this.num(cfg[zone]?.temp);
    if(n!==null) return `${n.toFixed(1)}°C`;
    const t=this.st(cfg[zone]?.climate)?.attributes?.current_temperature;
    return t==null ? "—" : `${Number(t).toFixed(1)}°C`;
  }
  humidity(zone,cfg){
    const n=this.num(cfg[zone]?.humidity);
    return n===null ? "—" : `${Math.round(n)}%`;
  }
  climate(zone,cfg){
    const s=this.st(cfg[zone]?.climate);
    return (s?.state||"—").replace("heat_cool","auto").toUpperCase();
  }
  manager(suffix){
    const states=this._hass?.states||{};
    const hit=Object.values(states).find(
      s=>s.entity_id.startsWith("sensor.summer_climate_manager_") &&
         s.entity_id.endsWith(suffix)
    );
    return hit?.state || "—";
  }
  action(zone){
    const map={kids:"kids_proposed_action",nursery:"nursery_proposed_action",
               master:"master_proposed_action",open:"open_plan_proposed_action"};
    return this.manager(map[zone]);
  }
  reason(zone){
    const map={kids:"kids_reason",nursery:"nursery_reason",
               master:"master_reason",open:"open_plan_reason"};
    return this.manager(map[zone]);
  }
  fireMoreInfo(entityId){
    if(!entityId) return;
    const ev=new Event("hass-more-info",{bubbles:true,composed:true});
    ev.detail={entityId}; this.dispatchEvent(ev);
  }
  call(domain,service,data){ this._hass.callService(domain,service,data); }

  render(){
    if(!this.shadowRoot || !this._hass) return;
    const f=this.findFrontend();
    if(!f){
      this.shadowRoot.innerHTML=`<ha-card><div style="padding:20px">
      Summer Climate Manager is waiting for the <b>Frontend Config</b> entity.
      </div></ha-card>`;
      return;
    }
    const cfg=f.card_config, z=this.selected||"open";
    const labels={kids:"Bed 2 (Kids)",nursery:"Bed 3 (Nursery)",
                  master:"Bed 1 (Master)",open:"Open Plan"};
    const img="/summer_climate_manager_static/floorplan.png?v=015";
    const gridImport=this.manager("grid_import");
    const gridExport=this.manager("grid_export");
    const evPower=this.manager("ev_charger_power");
    const solar=this.manager("solar_level");
    const strategy=this.manager("strategy");
    const eco=cfg.open?.eco ? this.val(cfg.open.eco).toUpperCase() :
      this.manager("open_plan_eco_recommendation");
    const quiet=cfg.open?.quiet ? this.val(cfg.open.quiet).toUpperCase() :
      this.manager("open_plan_quiet_recommendation");

    this.shadowRoot.innerHTML=`
<style>
:host{display:block;width:100%}
ha-card{overflow:hidden;background:#091722;color:#eef7ff;border-radius:16px}
.top{display:grid;grid-template-columns:minmax(250px,1.5fr) repeat(5,minmax(120px,.7fr));
gap:10px;padding:14px}
.brand{font-size:25px;font-weight:750}.sub,.muted{color:#a9bbca}
.metric,.panel,.room,.evpanel{background:#102231;border:1px solid #294154;border-radius:12px}
.metric{padding:9px 12px}.metric small{color:#9fb1c1;display:block}.metric b{font-size:17px}
.body{display:grid;grid-template-columns:minmax(620px,3fr) minmax(300px,1fr);gap:12px;padding:0 14px 14px}
.plan{position:relative;aspect-ratio:1092/734;background:#06121b;border-radius:12px;overflow:hidden}
.plan img{width:100%;height:100%;object-fit:cover;display:block}
.hot,.evhot{position:absolute;border:1px solid rgba(72,190,255,.75);background:rgba(8,25,38,.88);
color:white;border-radius:9px;padding:7px 9px;cursor:pointer;box-shadow:0 3px 14px #0008;font-size:12px;line-height:1.45}
.hot:hover,.hot.sel,.evhot:hover{outline:2px solid #27b7ff;background:rgba(8,32,49,.96)}
.kids{left:16%;top:24%}.nursery{left:16%;top:48%}.master{left:16%;top:70%}.open{left:48%;top:45%}
.evhot{right:4%;bottom:12%;border-color:#55d98b}.panel{padding:16px}.panel h2{margin:0 0 4px}
.big{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:16px 0}
.box,.reason{background:#142838;border-radius:10px;padding:12px}.box strong{font-size:22px}
.reason{margin-top:12px}.controls{display:grid;grid-template-columns:repeat(3,1fr);gap:7px;margin-top:12px}
.controls button{border:1px solid #36536a;background:#162b3b;color:white;border-radius:8px;padding:10px;cursor:pointer}
.controls button:hover{background:#1d3b50}.cool{color:#4fc3ff}.ok{color:#54d67b}
.rooms{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;padding:0 14px 14px}
.room{padding:12px;cursor:pointer}.room.sel{border:2px solid #26b8ff}.room b{display:block;margin-bottom:6px}
.room .t{font-size:19px;font-weight:700}.evpanel{padding:12px;cursor:pointer;border-color:#315d50}
.evpanel:hover{border-color:#55d98b}
@media(max-width:1100px){
 .top{grid-template-columns:1fr 1fr 1fr}.brand{grid-column:1/-1}
 .body{grid-template-columns:1fr}.rooms{grid-template-columns:1fr 1fr}
}
</style>
<ha-card>
<div class="top">
 <div><div class="brand">☀️ Summer Climate Manager</div>
 <div class="sub">Solar-aware comfort for your home · GUI v${CARD_VERSION}</div></div>
 <div class="metric"><small>Solar level</small><b>${solar}</b></div>
 <div class="metric"><small>Grid export</small><b>${gridExport} W</b></div>
 <div class="metric"><small>Grid import</small><b>${gridImport} W</b></div>
 <div class="metric"><small>EV charger</small><b>${evPower} W</b></div>
 <div class="metric"><small>Strategy</small><b>${strategy}</b></div>
</div>
<div class="body">
 <div class="plan"><img src="${img}">
 ${["kids","nursery","master","open"].map(k=>`
   <button class="hot ${k} ${z===k?'sel':''}" data-zone="${k}">
   <b>${labels[k]}</b><br>🌡 ${this.temp(k,cfg)} &nbsp; 💧 ${this.humidity(k,cfg)}<br>
   ❄ ${this.climate(k,cfg)}</button>`).join("")}
 <button class="evhot" id="evhot"><b>⚡ Delta AC Max / EVCC</b><br>${evPower} W · click to open</button>
 </div>
 <div class="panel">
   <h2>${labels[z]}</h2><div class="muted">Live Home Assistant data</div>
   <div class="big"><div class="box"><span class="muted">Temperature</span><br>
   <strong>${this.temp(z,cfg)}</strong></div><div class="box"><span class="muted">Humidity</span><br>
   <strong>${this.humidity(z,cfg)}</strong></div></div>
   <div class="box"><span class="muted">Current AC</span><br><strong>${this.climate(z,cfg)}</strong></div>
   <div class="box" style="margin-top:10px"><span class="muted">Manager recommends</span><br>
   <strong class="cool">${this.action(z)}</strong></div>
   <div class="reason"><b>💡 Reason</b><br>${this.reason(z)}</div>
   <div class="controls"><button id="more">AC controls</button><button id="off">Turn off</button>
   <button id="cool">Cool</button></div>
   ${z==='open'?`<div class="reason"><b>Hisense optimisation</b><br>🌿 Eco: <b>${eco}</b><br>
   🔇 Quiet: <b>${quiet}</b></div>`:''}
 </div>
</div>
<div class="rooms">
 ${["kids","nursery","master","open"].map(k=>`<div class="room ${z===k?'sel':''}" data-zone="${k}">
 <b>${labels[k]}</b><span class="t">${this.temp(k,cfg)}</span> &nbsp; 💧 ${this.humidity(k,cfg)}<br>
 <span class="muted">${this.climate(k,cfg)} · ${this.action(k)}</span></div>`).join("")}
 <div class="evpanel" id="evcard"><b>⚡ EV Charger (Garage)</b><br>
 <span class="t">${evPower} W</span><br><span class="muted">Delta AC Max / EVCC · click to open</span></div>
</div>
</ha-card>`;

    this.shadowRoot.querySelectorAll('[data-zone]').forEach(
      el=>el.onclick=()=>{this.selected=el.dataset.zone;this.render();}
    );
    this.shadowRoot.getElementById('more').onclick=()=>this.fireMoreInfo(cfg[z]?.climate);
    this.shadowRoot.getElementById('off').onclick=()=>this.call('climate','turn_off',{entity_id:cfg[z]?.climate});
    this.shadowRoot.getElementById('cool').onclick=()=>this.call('climate','set_hvac_mode',
      {entity_id:cfg[z]?.climate,hvac_mode:'cool'});

    const openEV=()=>{
      const entity=cfg.energy?.ev_charging || cfg.energy?.ev_power;
      this.fireMoreInfo(entity);
    };
    this.shadowRoot.getElementById('evhot').onclick=openEV;
    this.shadowRoot.getElementById('evcard').onclick=openEV;
  }
}
if(!customElements.get("summer-climate-floorplan")){
  customElements.define("summer-climate-floorplan",SummerClimateFloorplan);
}
window.customCards=window.customCards||[];
if(!window.customCards.some(c=>c.type==="summer-climate-floorplan")){
  window.customCards.push({type:"summer-climate-floorplan",name:"Summer Climate Floorplan",
    description:"Interactive companion GUI for Summer Climate Manager"});
}
