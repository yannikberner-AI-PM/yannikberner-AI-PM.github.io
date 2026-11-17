(() => {
const $ = id => document.getElementById(id);
for (const [id,value] of Object.entries({postalCode:'10115',annualKwh:'3500',fixedCt:'32',fixedMonthly:'12','future-years':'5'})) $(id).value=value;
$('future-example').click();
for(let i=0;i<5;i++) $('wizard-next').click();
document.querySelector('.local').textContent='Beispieldaten · lokaler Prototyp';
window.scrollTo(0,0);
document.querySelector('#outlook .table-scroll').hidden=true;
const r=$('outlook').getBoundingClientRect(); const end=$('outlook-chart').parentElement.getBoundingClientRect();
const legend=document.querySelector('#outlook-chart .path-legend').getBoundingClientRect();
$('outlook-status').textContent='Beispieldaten · 3.000 kWh Netzbezug/Jahr · Vertrag: 32 ct/kWh + 12 €/Monat · 5 Jahre. Preisverläufe frei angenommen.';
return {capture:{x:r.x-24,y:r.y-16,width:r.width+48,height:end.bottom-r.y+24},title:document.title,costs:['low','mid','high'].map(k=>$('outlook-'+k).textContent),status:$('outlook-status').textContent};
})();