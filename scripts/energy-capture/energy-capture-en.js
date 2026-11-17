(() => {
const $ = id => document.getElementById(id);
for (const [id,value] of Object.entries({postalCode:'10115',annualKwh:'3500',fixedCt:'32',fixedMonthly:'12','future-years':'5'})) $(id).value=value;
$('future-example').click();
for(let i=0;i<5;i++) $('wizard-next').click();
document.documentElement.lang='en';
window.scrollTo(0,0);
document.querySelector('#outlook .table-scroll').hidden=true;

$('outlook-status').textContent='Beispieldaten · 3.000 kWh Netzbezug/Jahr · Vertrag: 32 ct/kWh + 12 €/Monat · 5 Jahre. Preisverläufe frei angenommen.';

const translations={"DEINE NÄCHSTEN JAHRE": "YOUR NEXT FEW YEARS", "Wie könnte es weitergehen?": "What could the next few years cost?", "Drei Szenarien": "Three scenarios", "Drei angenommene Preisverläufe im Vergleich zu deinem heutigen Vertrag. So erkennst du, welchen Unterschied der Strompreis für deinen Haushalt macht.": "Compare three assumed price paths with your current contract. See how electricity prices could affect your household costs.", "Günstiger Verlauf": "Lower-price path", "Mittlerer Verlauf": "Mid-price path", "Hoher Preisverlauf": "Higher-price path", "Ø jährliche Bezugskosten": "Avg. annual grid electricity cost", " ct/kWh zu Beginn · ": " ct/kWh initially · ", " % pro Jahr. Insgesamt ": "% per year. Total: ", " über 5 Jahre.": " over 5 years.", " geringere Bezugskosten": " lower grid costs", " höhere Bezugskosten": " higher grid costs", "Bezugskosten über deinen Zeitraum": "Grid electricity costs over time", "Kumulierte Kosten in Euro, einschließlich Fixkosten": "Cumulative costs in euros, including fixed charges", "Heutiger Vertrag konstant": "Current contract, held constant", "Deine Preisverläufe": "Your price paths", "Günstig": "Lower", "Mittel": "Mid", "Hoch": "Higher", "Start": "Start", "J1": "Y1", "J2": "Y2", "J3": "Y3", "J4": "Y4", "J5": "Y5"};
const walker=document.createTreeWalker($('outlook'),NodeFilter.SHOW_TEXT);let node;
while(node=walker.nextNode()){
 let value=node.nodeValue;
 for(const [de,en] of Object.entries(translations))value=value.split(de).join(en);
 value=value.replace(/([\d.]+)\s*€/g,(_,n)=>new Intl.NumberFormat('en-GB',{style:'currency',currency:'EUR',maximumFractionDigits:0}).format(Number(n.replaceAll('.',''))));
 if(node.parentElement?.tagName.toLowerCase()==='text'&&!/Y\d|Start/.test(value))value=value.replace(/(\d)\.(\d{3})/g,'$1,$2');
 node.nodeValue=value;
}
$('outlook-status').textContent='Sample data · 3,000 kWh of grid electricity per year · Contract: 32 ct/kWh + €12/month · 5 years. Price paths are assumptions.';

const r=$('outlook').getBoundingClientRect(); const end=$('outlook-chart').parentElement.getBoundingClientRect();
const legend=document.querySelector('#outlook-chart .path-legend').getBoundingClientRect();
return {capture:{x:r.x-24,y:r.y-16,width:r.width+48,height:end.bottom-r.y+24},title:document.title,costs:['low','mid','high'].map(k=>$('outlook-'+k).textContent),status:$('outlook-status').textContent};
})();