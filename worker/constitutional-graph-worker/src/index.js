export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === '/graph_data.json') {
      const data = {
        nodes: [
          {id:'preamble',label:'Preamble',group:'constitution',sub:'Popular sovereignty, general welfare'},
          {id:'art1',label:'Article I',group:'constitution',sub:'Legislative Powers'},
          {id:'art2',label:'Article II',group:'constitution',sub:'Executive Powers'},
          {id:'art3',label:'Article III',group:'constitution',sub:'Judicial Powers'},
          {id:'art4',label:'Article IV',group:'constitution',sub:'State Relations'},
          {id:'art6',label:'Article VI',group:'constitution',sub:'Supremacy Clause + Oath'},
          {id:'amend1',label:'1st Amendment',group:'constitution',sub:'Establishment/Speech/Press/Assembly/Petition'},
          {id:'amend4',label:'4th Amendment',group:'constitution',sub:'Search and Seizure'},
          {id:'amend5',label:'5th Amendment',group:'constitution',sub:'Due Process and Takings'},
          {id:'amend6',label:'6th Amendment',group:'constitution',sub:'Right to Counsel'},
          {id:'amend8',label:'8th Amendment',group:'constitution',sub:'Excessive Bail/Fines and Cruel and Unusual Punishment'},
          {id:'amend13',label:'13th Amendment',group:'constitution',sub:'Abolition of Slavery'},
          {id:'amend14',label:'14th Amendment',group:'constitution',sub:'Citizenship, Privileges/Immunities, Due Process, Equal Protection'},
          {id:'amend15',label:'15th Amendment',group:'constitution',sub:'Race-based Voting Discrimination'},
          {id:'amend19',label:"Women's Suffrage",group:'constitution',sub:"Women's Suffrage"},
          {id:'amend26',label:'26th Amendment',group:'constitution',sub:'Voting Age'},
          {id:'judiciary_act',label:'Judiciary Act of 1789',group:'law',sub:'Federal court structure'},
          {id:'civil_rights_1866',label:'Civil Rights Act of 1866',group:'law',sub:'Equal rights under 13th/14th'},
          {id:'vra',label:'Voting Rights Act of 1965',group:'law',sub:'Race-based voting discrimination under 15th'},
          {id:'civil_rights_1964',label:'Civil Rights Act of 1964',group:'law',sub:'Public accommodations and employment'},
          {id:'fha',label:'Fair Housing Act of 1968',group:'law',sub:'Housing discrimination'},
          {id:'adha',label:'ADA of 1990',group:'law',sub:'Disability access and equal protection'},
          {id:'usc18',label:'18 U.S.C.',group:'law',sub:'Federal crimes'},
          {id:'usc42',label:'42 U.S.C.',group:'law',sub:'Public health and civil rights'},
          {id:'usc52',label:'52 U.S.C.',group:'law',sub:'Voting and elections'},
          {id:'ins_act',label:'INA',group:'law',sub:'Naturalization and aliens'},
          {id:'csa',label:'Controlled Substances Act',group:'law',sub:'Drug scheduling under commerce power'},
          {id:'nsa_fisa',label:'FISA Amendments',group:'law',sub:'Programmatic surveillance tension with 4th'},
          {id:'marbury',label:'Marbury v. Madison',group:'scotus',sub:'Judicial review under Article III'},
          {id:'mcculloch',label:'McCulloch v. Maryland',group:'scotus',sub:'Implied powers and Necessary and Proper'},
          {id:'gibbons',label:'Gibbons v. Ogden',group:'scotus',sub:'Commerce Clause breadth'},
          {id:'plessy',label:'Plessy v. Ferguson',group:'scotus',sub:'Separate but equal'},
          {id:'brown',label:'Brown v. Board',group:'scotus',sub:'Segregation violates Equal Protection'},
          {id:'mapp',label:'Mapp v. Ohio',group:'scotus',sub:'Exclusionary rule'},
          {id:'gideon',label:'Gideon v. Wainwright',group:'scotus',sub:'Right to counsel'},
          {id:'miranda',label:'Miranda v. Arizona',group:'scotus',sub:'Custodial warnings'},
          {id:'loving',label:'Loving v. Virginia',group:'scotus',sub:'Anti-miscegenation bans violate 14th'},
          {id:'roe',label:'Roe v. Wade',group:'scotus',sub:'Abortion right; overruled by Dobbs'},
          {id:'heller',label:'District of Columbia v. Heller',group:'scotus',sub:'2nd Amendment individual right'},
          {id:'mcdonald',label:'McDonald v. Chicago',group:'scotus',sub:'2nd Amendment incorporation'},
          {id:'obergefell',label:'Obergefell v. Hodges',group:'scotus',sub:'Same-sex marriage'},
          {id:'shelby',label:'Shelby County v. Holder',group:'scotus',sub:'VRA preclearance formula invalidated'},
          {id:'dobbs',label:'Dobbs v. Jackson Women\'s Health',group:'scotus',sub:'Returned abortion to states'},
          {id:'bruen',label:'Bruen',group:'scotus',sub:'2nd Amendment historical tradition test'},
          {id:'grant_hoist',label:'Trump v. Anderson',group:'scotus',sub:'Section 3 and presidential eligibility'},
          {id:'tx_sb8',label:'Texas S.B. 8 architecture',group:'state',sub:'13th/14th Amend. tension',conflict:'RED'},
          {id:'al_hb56',label:'Alabama HB 56',group:'state',sub:'INS preemption and Supremacy Clause',conflict:'RED'},
          {id:'ok_ten',label:'Oklahoma Ten Commandments',group:'state',sub:'Establishment Clause',conflict:'RED'},
          {id:'ny_safe',label:'New York SAFE Act',group:'state',sub:'2nd Amend. tension',conflict:'PARTIAL'},
          {id:'ca_ammo',label:'California ammunition checks',group:'state',sub:'2nd Amend. and preemption tension',conflict:'PARTIAL'},
          {id:'fl_voting',label:'Florida 2021 election laws',group:'state',sub:'15th Amend. and VRA',conflict:'PARTIAL'},
          {id:'tx_gerry',label:'Texas redistricting',group:'state',sub:'14th/15th Amend. and VRA',conflict:'PARTIAL'},
          {id:'nj_sbf',label:'New Jersey admissions diversity',group:'state',sub:'14th Amend. Equal Protection',conflict:'PARTIAL'},
          {id:'pa_debtor',label:'Pennsylvania debtor protection',group:'state',sub:'1776/1790 template; modern contempt evades',conflict:'RED'},
          {id:'tx_debtor',label:'Texas debtor protection',group:'state',sub:'1845 outright ban',conflict:'RED'},
          {id:'fl_debtor',label:'Florida debtor protection',group:'state',sub:'State ban; contempt reclassifies obligation',conflict:'RED'},
          {id:'oh_debtor',label:'Ohio debtor protection',group:'state',sub:'State ban; family court exception',conflict:'RED'},
          {id:'in_debtor',label:'Indiana debtor protection',group:'state',sub:'State ban; judicial exception',conflict:'RED'},
          {id:'nc_debtor',label:'North Carolina debtor protection',group:'state',sub:'1867 abolition; modern contempt evades',conflict:'RED'},
          {id:'vt_huth',label:'Vermont State v. Huth',group:'state',sub:'Debtor ban; support contempt carve-out',conflict:'RED'},
          {id:'sc_turner',label:'South Carolina Turner pathway',group:'state',sub:'Indigent parent jailed',conflict:'RED'},
          {id:'ga_bearden',label:'Georgia Bearden pathway',group:'state',sub:'Imprisonment for inability to pay',conflict:'PARTIAL'},
          {id:'state_debtor_bans',label:'State Debtors\' Prison Bans',group:'state',sub:'41/50 state bans; fraud exception'},
          {id:'child_support_contempt',label:'Child Support Civil Contempt',group:'state',sub:'Functional debt imprisonment; Turner safeguards'},
          {id:'aba',label:'ABA',group:'registry',sub:'U.S. national association; no direct national practicing register'},
          {id:'ncbe',label:'NCBE',group:'registry',sub:'Multistate exam and score portability'},
          {id:'state_bars',label:'U.S. State Bars',group:'registry',sub:'50+ admission authorities; public lookups'},
          {id:'barenroll',label:'U.S. Enrollment Pathway',group:'registry',sub:'JD or non-JD route to bar and state roll'},
          {id:'federal_admission',label:'Federal Admissions',group:'registry',sub:'Separate federal court admission registries'},
          {id:'bsb',label:'BSB',group:'registry',sub:'England/Wales bar regulator; practising certificate and Barristers\' Register'},
          {id:'barcouncil',label:'Bar Council',group:'registry',sub:'Barristers\' representative and standard-setting body'},
          {id:'inns',label:'Inns of Court',group:'registry',sub:"Gray's Inn, Lincoln's Inn, Inner Temple, Middle Temple"},
          {id:'sra',label:'SRA',group:'registry',sub:'England/Wales solicitor regulator; separate register'},
          {id:'lawcabs',label:'Bar Training Framework',group:'registry',sub:'Academic, vocational, pupillage, tenancy/employed practice'},
          {id:'bar_monopoly',label:'Mandatory State Bar Monopoly',group:'practice',sub:'Compulsory licensing and dues; First Amendment tension'},
          {id:'judicial_councils',label:'Judicial Councils',group:'practice',sub:'Court policy and budgeting insulated from legislature'},
          {id:'contempt_practice',label:'Contempt of Court Practice',group:'practice',sub:'Self-executing coercion without criminal process'},
          {id:'judicial_immunity_practice',label:'Absolute Judicial Immunity Practice',group:'practice',sub:'Civil damages immunity; no Article III text; common-law inheritance'},
          {id:'self_pardon_practice',label:'Self-Pardon Practice',group:'practice',sub:'No textual Article II limit; prerogaive descent'},
          {id:'administrative_state_practice',label:'Administrative State Practice',group:'practice',sub:'Nondelegation and intelligible principle bypass'},
          {id:'foreign_law_practice',label:'Foreign Law Citation Practice',group:'practice',sub:'Persuasive international norms; no Article III/VI authorization'},
          {id:'crown_rule_governance',label:'Crown-Rule Governance Model',group:'history',sub:'Royal prerogative and legislative supremacy rejected by Framers'},
          {id:'prerogative_courts',label:'Prerogative Courts',group:'history',sub:'Star Chamber, High Commission, Admiralty'},
          {id:'parliamentary_sovereignty',label:'Parliamentary Sovereignty',group:'history',sub:'No judicial review over statute'},
          {id:'magna_carta_constraint',label:'Magna Carta Constraint',group:'history',sub:"Coke's common-law limit on Crown"},
          {id:'amend2_textual_scope',label:'2nd Amendment Textual Scope',group:'constitution',sub:'Unqualified operative clause; no textual self-extension'},
          {id:'article_v',label:'Article V',group:'constitution',sub:'Sole amendment mechanism'},
          {id:'militia_fines',label:'Founding-Era Militia Disarmament',group:'history',sub:'Temporary militia-based disarmament'},
          {id:'loyalist_disarmament',label:'Loyalist Disarmament',group:'history',sub:'Status-based temporary disarmament'},
          {id:'treason_disarmament',label:'Treason Disarmament',group:'history',sub:'Offense-specific, not categorical felon class'}
        ],
        edges: [
          ["amend13","art6","ENFORCES"],["amend14","art6","ENFORCES"],["amend15","art6","ENFORCES"],["amend19","art6","ENFORCES"],["amend26","art6","ENFORCES"],
          ["art1","judiciary_act","AUTHORIZES"],["art1","usc42","AUTHORIZES"],["art1","usc52","AUTHORIZES"],["art1","usc18","AUTHORIZES"],
          ["amend13","civil_rights_1866","MANDATES"],["amend14","civil_rights_1964","MANDATES"],["amend14","fha","MANDATES"],["amend14","adha","MANDATES"],["amend14","usc42","MANDATES"],
          ["amend15","vra","MANDATES"],["amend1","civil_rights_1964","LIMITS"],["amend1","nsa_fisa","TENSIONS"],["amend4","nsa_fisa","TENSIONS"],["amend4","usc18","CONSTRAINS"],
          ["amend2","ny_safe","CHALLENGES"],["amend2","ca_ammo","CHALLENGES"],["amend14","ca_ammo","TENSION"],["usc922g","bruen","LITIGATION UNDER"],
          ["art1","csa","AUTHORIZES"],["art2","ins_act","IMPLEMENTS"],["art2","al_hb56","BORDERS"],["marbury","mcculloch","FOLLOWS"],["mcculloch","gibbons","FOLLOWS"],["gibbons","civil_rights_1964","UNDERLIES"],
          ["plessy","brown","OVERRULED BY"],["brown","civil_rights_1964","UNDERLIES"],["mapp","usc18","CONSTRAINS"],["gideon","usc42","STRENGTHENS"],["miranda","usc42","STRENGTHENS"],["loving","fha","UNDERLIES"],["roe","dobbs","OVERRULED BY"],["heller","mcdonald","INCORPORATED IN"],["shelby","vra","LIMITS"],["shelby","fl_voting","ENABLES CHALLENGES"],
          ["vra","fl_voting","DIRECT CONFLICT"],["vra","tx_gerry","DIRECT CONFLICT"],["amend15","fl_voting","DIRECT CONFLICT"],["amend15","tx_gerry","DIRECT CONFLICT"],
          ["civil_rights_1964","ok_ten","DIRECT CONFLICT"],["amend1","ok_ten","DIRECT CONFLICT"],["ins_act","al_hb56","DIRECT CONFLICT"],["csa","ca_ammo","CONFLICT"],["amend2","ny_safe","DIRECT CHALLENGE"],["amend2","ca_ammo","DIRECT CHALLENGE"],
          ["state_debtor_bans","child_support_contempt","HOLLOWED OUT BY"],["amend5","child_support_contempt","TURNER PROCEDURAL SAFEGUARDS"],["amend14","child_support_contempt","DUE PROCESS TENSION"],
          ["pa_debtor","child_support_contempt","DIRECT CONFLICT: state text vs. practice"],["tx_debtor","child_support_contempt","DIRECT CONFLICT: outright ban circumvented"],["fl_debtor","child_support_contempt","DIRECT CONFLICT: judicial reclassification"],["oh_debtor","child_support_contempt","DIRECT CONFLICT: family court exception"],["in_debtor","child_support_contempt","DIRECT CONFLICT: constitutional ban ignored"],["nc_debtor","child_support_contempt","DIRECT CONFLICT: 1867 abolition evaded"],["vt_huth","child_support_contempt","DIRECT CONFLICT: carve-out"],["sc_turner","child_support_contempt","DIRECT CONFLICT: indigent parent jailed"],["ga_bearden","child_support_contempt","PARTIAL: due process limit, not textual ban"],
          ["bar_monopoly","amend1","COMPELLED SPEECH / PETITION TENSION"],["bar_monopoly","state_bars","PRACTICE: mandatory dues"],["judicial_councils","art3","CASE-OR-CONTROVERSY BYPASS"],["judicial_councils","amend1","RULEMAKING WITHOUT LEGISLATURE"],["contempt_practice","amend6","SELF-EXECUTING INCARCERATION"],["contempt_practice","prerogative_courts","INHERITED COERCIVE POWER"],["judicial_immunity_practice","art3","NO TEXTUAL IMMUNITY CLAUSE"],["judicial_immunity_practice","crown_rule_governance","COMMON-LAW JUDGE IMMUNITY INHERITED"],["self_pardon_practice","art2","NO TEXTUAL LIMIT ON SELF-PARDON"],["self_pardon_practice","crown_rule_governance","ROYAL PREROGATIVE OF MERCY DESCENT"],["administrative_state_practice","art1","NONDELEGATION BYPASS"],["foreign_law_practice","art6","NO AUTHORIZATION TO ADOPT FOREIGN LAW"],["foreign_law_practice","crown_rule_governance","ENGLISH COURTS USED FOREIGN/CHURCH LAW; U.S. text does not authorize"],["crown_rule_governance","parliamentary_sovereignty","REJECTED BY FRAMERS"],["crown_rule_governance","prerogative_courts","REJECTED EXCEPT RESIDUAL PRACTICE"],["crown_rule_governance","magna_carta_constraint","PARTIALLY ADOPTED AS COMMON LAW"],["crown_rule_governance","judicial_immunity_practice","CROWN INFLUENCE ON AMERICAN JUDICIAL IMMUNITY"],["crown_rule_governance","contempt_practice","CROWN INFLUENCE ON AMERICAN CONTEMPT POWER"],
          ["state_bars","ncbe","USES EXAMINATION SCORES"],["state_bars","federal_admission","FEEDS FEDERAL ADMISSION"],["state_bars","bsb","COMPARISON: centralized registry"],["state_bars","sra","COMPARISON: split profession"],["barenroll","barcouncil","COMPARISON: rolls vs practising certificate"],["bsb","barcouncil","COMPARISON: regulatory unification"],["inns","barcouncil","CALL TO BAR PATHWAY"],["bsb","lawcabs","EDUCATES AGAINST STANDARDS"]
        ],
        stateRows: [
          ["Texas","S.B. 8 architecture","13th/14th Amend. tension","RED","https://supreme.justia.com/cases/federal/us/23/2023/"],
          ["Alabama","HB 56 / immigration-state crimes","INS preemption","RED","https://supreme.justia.com/cases/federal/us/567/2012/"],
          ["Oklahoma","Ten Commandments monument","Establishment Clause","RED","https://supreme.justia.com/cases/federal/us/545/1011/"],
          ["Pennsylvania","1776/1790 debtor protection","State constitution vs. modern contempt","RED","https://www.paconstitution.org/"],
          ["Texas","1845 debtor ban","Tex. Const. Art. I 15","RED","https://tarlton.law.utexas.edu/"],
          ["Florida","State debtor ban","State constitution vs. contempt","RED","https://www.floridaconstitutioncenter.org/"],
          ["Ohio","State debtor ban","State constitution vs. contempt","RED","https://www.supremecourt.ohio.gov/"],
          ["Indiana","State debtor ban","State constitution vs. contempt","RED","https://www.in.gov/judiciary/"],
          ["North Carolina","1867 abolition","State abolition vs. modern contempt","RED","https://www.nccourts.gov/"],
          ["Vermont","State v. Huth","Vermont Supreme Court carve-out","RED","https://www.vermontjudiciary.org/"],
          ["South Carolina","Turner pathway","Indigent parent jailed","RED","https://supreme.justia.com/cases/federal/us/564/431/"],
          ["Georgia","Bearden pathway","Imprisonment for inability to pay","PARTIAL","https://supreme.justia.com/cases/federal/us/461/660/"],
          ["New York","SAFE Act","2nd Amend. tension","PARTIAL","https://supreme.justia.com/cases/federal/us/597/20-843/"],
          ["California","Ammunition background checks","2nd Amend./preemption tension","PARTIAL","https://supreme.justia.com/cases/federal/us/561/742/"],
          ["Florida","2021 election laws","15th Amend./VRA","PARTIAL","https://www.law.cornell.edu/uscode/text/52/10301"],
          ["Texas","Partisan redistricting","14th/15th Amend./VRA","PARTIAL","https://www.law.cornell.edu/uscode/text/52/10301"],
          ["Federal","922(g)","2nd Amend. text/history/tradition","PARTIAL","https://supreme.justia.com/cases/federal/us/597/20-843/"],
          ["41 States","Debtors' prison bans vs. contempt","State constitutions plus Turner","PARTIAL","https://supreme.justia.com/cases/federal/us/564/431/"],
          ["Federal","Mandatory state bar monopolies","1st Amend. Petition/Compelled Speech","PARTIAL","https://supreme.justia.com/cases/federal/us/496/1/"],
          ["Federal","Judicial council governance","Article III case-or-controversy","PARTIAL","https://www.uscourts.gov/about-federal-courts/educational-resources/about-educational-outreach/activity-resources/about"],
          ["Federal","Absolute judicial immunity","Article III; no textual immunity","PARTIAL","https://www.law.cornell.edu/supremecourt/text/10/436"],
          ["Federal","Self-pardon scope","Article II; no textual limit","PARTIAL","https://supreme.justia.com/cases/federal/us/343/579/"],
          ["Federal","Foreign law citation","Article III/VI; no authorization","PARTIAL","https://supreme.justia.com/cases/federal/us/543/551/"],
          ["Federal","Administrative state nondelegation","Article I Section 1 vesting clause","PARTIAL","https://www.law.cornell.edu/uscode/text/5/706"]
        ],
        sourceMap: Object.fromEntries([
          ["preamble","https://constitution.congress.gov/constitution/"],["art1","https://constitution.congress.gov/constitution/article-1/"],["art2","https://constitution.congress.gov/constitution/article-2/"],["art3","https://constitution.congress.gov/constitution/article-3/"],["art4","https://constitution.congress.gov/constitution/article-4/"],["art6","https://constitution.congress.gov/constitution/article-6/"],["amend1","https://constitution.congress.gov/constitution/amendment-1/"],["amend4","https://constitution.congress.gov/constitution/amendment-4/"],["amend5","https://constitution.congress.gov/constitution/amendment-5/"],["amend6","https://constitution.congress.gov/constitution/amendment-6/"],["amend8","https://constitution.congress.gov/constitution/amendment-8/"],["amend13","https://constitution.congress.gov/constitution/amendment-13/"],["amend14","https://constitution.congress.gov/constitution/amendment-14/"],["amend15","https://constitution.congress.gov/constitution/amendment-15/"],["amend19","https://constitution.congress.gov/constitution/amendment-19/"],["amend26","https://constitution.congress.gov/constitution/amendment-26/"],
          ["judiciary_act","https://www.law.cornell.edu/uscode/text/28/1"],["vra","https://www.law.cornell.edu/uscode/text/52/10301"],["civil_rights_1964","https://www.law.cornell.edu/uscode/text/42/2000e"],["csa","https://www.law.cornell.edu/uscode/text/21/812"],["nsa_fisa","https://www.law.cornell.edu/uscode/text/50/1881a"],["ins_act","https://www.law.cornell.edu/uscode/text/8/1325"],["usc18","https://www.law.cornell.edu/uscode/text/18/1"],["usc42","https://www.law.cornell.edu/uscode/text/42/1"],["usc52","https://www.law.cornell.edu/uscode/text/52/1"],["usc922g","https://www.law.cornell.edu/uscode/text/18/922"],["nfra","https://www.law.cornell.edu/uscode/text/26/5801"],
          ["marbury","https://supreme.justia.com/cases/federal/us/5/137/"],["mcculloch","https://supreme.justia.com/cases/federal/us/17/316/"],["gibbons","https://supreme.justia.com/cases/federal/us/22/1/"],["brown","https://supreme.justia.com/cases/federal/us/347/483/"],["mapp","https://supreme.justia.com/cases/federal/us/367/643/"],["gideon","https://supreme.justia.com/cases/federal/us/372/335/"],["miranda","https://supreme.justia.com/cases/federal/us/384/436/"],["loving","https://supreme.justia.com/cases/federal/us/388/1/"],["roe","https://supreme.justia.com/cases/federal/us/410/113/"],["heller","https://supreme.justia.com/cases/federal/us/554/570/"],["mcdonald","https://supreme.justia.com/cases/federal/us/561/742/"],["obergefell","https://supreme.justia.com/cases/federal/us/576/644/"],["shelby","https://supreme.justia.com/cases/federal/us/570/529/"],["dobbs","https://supreme.justia.com/cases/federal/us/597/19-1392/"],["bruen","https://supreme.justia.com/cases/federal/us/597/20-843/"],["grant_hoist","https://supreme.justia.com/cases/federal/us/23-1979/"],["keller","https://supreme.justia.com/cases/federal/us/496/1/"],["turner","https://supreme.justia.com/cases/federal/us/564/431/"],["bearden","https://supreme.justia.com/cases/federal/us/461/660/"],["hicks","https://supreme.justia.com/cases/federal/us/485/624/"],["youngstown","https://supreme.justia.com/cases/federal/us/343/579/"],["pa1776","https://www.paconstitution.org/"],["tx1845","https://tarlton.law.utexas.edu/"],["vtHuth","https://www.vermontjudiciary.org/"],["bsb","https://www.barstandardsboard.org.uk/"],["aba","https://www.americanbar.org/"],["englishBill1689","https://avalon.law.yale.edu/17th_century/england.asp"],["magnaCarta","https://avalon.law.yale.edu/medieval/magnamenu.asp"],["starChamber","https://www.britannica.com/topic/Star-Chamber"]
        ])
      };
      return new Response(JSON.stringify(data), {
        headers: {
          'content-type': 'application/json;charset=utf-8',
          'cache-control': 'no-store',
        },
      });
    }
    if (url.pathname === '/favicon.ico') {
      return new Response('', { status: 204 });
    }
    const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Constitutional Law Semantic Graph</title>
<style>
  :root { --bg:#0b1220; --border:#1f2937; --text:#e5e7eb; --muted:#94a3b8; }
  * { box-sizing: border-box; }
  html, body { height: 100%; }
  body { margin:0; background:radial-gradient(circle at top left,#0f1c33,#0b1220 40%); color:var(--text); font-family:ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial; }
  .wrap { max-width:1400px; margin:0 auto; padding:24px; }
  h1 { margin:0 0 4px; font-size:26px; }
  .sub { color:var(--muted); margin:0 0 14px; font-size:14px; }
  .legend { display:flex; flex-wrap:wrap; gap:14px; margin:10px 0 18px; }
  .legend .item { display:inline-flex; align-items:center; gap:8px; font-size:12px; color:#d1d5db; }
  .dot { width:10px; height:10px; border-radius:50%; box-shadow:0 0 0 1px rgba(0,0,0,0.4); }
  .grid { display:grid; grid-template-columns:1.2fr 1fr; gap:18px; }
  @media (max-width:980px) { .grid { grid-template-columns:1fr; } }
  .card { background:linear-gradient(180deg,rgba(17,24,39,0.7),rgba(17,24,39,0.4)); border:1px solid var(--border); border-radius:14px; padding:14px; }
  .card h2 { margin:0 0 10px; font-size:15px; color:#cbd5e1; }
  .canvas-wrap { position:relative; width:100%; height:520px; }
  canvas { display:block; width:100%; height:100%; }
  table { width:100%; border-collapse:collapse; font-size:12px; color:#e5e7eb; }
  th, td { text-align:left; padding:8px 9px; border-bottom:1px solid #1f2937; vertical-align:top; }
  thead th { color:#9ca3af; font-weight:600; }
  .source-link { color:#7dd3fc; text-decoration:underline; }
  .badge { display:inline-block; padding:3px 7px; border-radius:999px; font-size:11px; border:1px solid rgba(255,255,255,0.08); background:rgba(17,24,39,0.6); }
  .badge-red { color:#fca5a5; border-color:#7f1d1d; background:#2a0f0f; }
  .badge-partial { color:#fde68a; border-color:#78350f; background:#271e0d; }
  .note { margin-top:10px; color:var(--muted); font-size:12px; font-style:italic; }
</style>
</head>
<body>
<div class="wrap">
  <h1>Constitutional Law Semantic Graph</h1>
  <p class="sub">U.S. constitutional sources -> constitutionally mandated federal law -> Supreme Court interpretive nodes -> state/practice conflict topology</p>
  <div class="legend" id="legend"></div>
  <div class="grid">
    <div class="card">
      <h2>Graph - Federal Mandate &amp; Judicial Interpretation Topology</h2>
      <div class="canvas-wrap"><canvas id="g"></canvas></div>
      <div class="note">Read: green yields valid federal mandate under constitutional text; purple yields judicial enforcement; red yields state direct conflict under Supremacy Clause.</div>
    </div>
    <div class="card">
      <h2>Source-Indexed State &amp; Practice Conflict Map</h2>
      <div style="overflow:auto; max-height:520px;">
        <table>
          <thead>
            <tr><th>Jurisdiction / Domain</th><th>Nature of Conflict</th><th>Constitutional Basis</th><th>Status</th><th>Source / Citation</th></tr>
          </thead>
          <tbody id="state-table"></tbody>
        </table>
      </div>
      <div class="note">Scope note: each row is tied to a node/edge pair in the graph with a clickable source where available.</div>
    </div>
  </div>
</div>
<script>
let loadErr;
fetch('/graph_data.json').then(r=>{ if(!r.ok){ throw new Error('HTTP ' + r.status); } return r.json(); }).then(data=>{
  window.__G=1;
  const nodes=data.nodes, edges=data.edges, stateRows=data.stateRows, sourceMap=data.sourceMap;
  const legend=[{color:'#a78bfa',label:'US Constitution Source'},{color:'#60a5fa',label:'Federal Law / Statute'},{color:'#34d399',label:'SCOTUS Interpretation'},{color:'#fbbf24',label:'State Constitutional Provision'},{color:'#f87171',label:'Direct Conflict / Preemption Risk'},{color:'#4ade80',label:'Compliant / Struck Down'},{color:'#e879f9',label:'US Bar Practice Registry'},{color:'#f472b6',label:'British Bar Registry / BSB'},{color:'#fb923c',label:'Founding / Historical Analogue'},{color:'#22d3ee',label:'Practice / Governance Lineage'}];
  const el=document.getElementById('legend'); legend.forEach(item=>{ const span=document.createElement('span'); span.className='item'; span.innerHTML='<span class="dot" style="background:'+item.color+'"></span>'+item.label; el.appendChild(span); });

  function sourceFor(nodeId){ return sourceMap[nodeId] || null; }

  const canvas=document.getElementById('g');
  if(!canvas) throw new Error('missing canvas');
  const ctx=canvas.getContext('2d');
  const colors={constitution:'#a78bfa',law:'#60a5fa',scotus:'#34d399',state:'#fbbf24',conflict:'#f87171',compliant:'#4ade80',registry:'#e879f9',history:'#fb923c',practice:'#22d3ee'};
  const fit=()=>{ const wrap=canvas.parentElement; const w=wrap?wrap.clientWidth:canvas.clientWidth; const h=wrap?wrap.clientHeight:canvas.clientHeight; canvas.width=Math.max(320,w); canvas.height=Math.max(320,h); return {w:canvas.width,h:canvas.height}; };
  const coords=(i,total,w,h)=>{ const margin=64; const cx=w/2,cy=h/2; const rx=w/2-margin,ry=h/2-margin; const angle=(i/total)*Math.PI*2; return {x:cx+Math.cos(angle)*rx*0.9,y:cy+Math.sin(angle)*ry*0.9}; };
  let positions=nodes.map((n,i)=>coords(i,nodes.length,fit().w,fit().h));
  const nodeMap=new Map(nodes.map((n,i)=>[n.id,i]));
  const links=edges.map(([a,b,type])=>({from:nodeMap.get(a),to:nodeMap.get(b),type})).filter(e=>e.from!=null&&e.to!=null);
  const linkStroke={AUTHORIZES:'#334155',MANDATES:'#0ea5e9',TENSIONS:'#f59e0b',DIRECT_CONFLICT:'#ef4444',PREEMPTION_RISK:'#f97316',OVERRULED_BY:'#f43f5e',ENFORCES:'#10b981',GIVES_RISE_TO:'#8b5cf6',UNDERLIES:'#14b8a6',CONSTRAINS:'#6366f1',STRENGTHENS:'#22c55e',OVERLAPS:'#eab308',BORDERS:'#fb923c',LIMITS:'#fbbf24',ENABLES_CHALLENGES:'#fb923c',TENSION:'#f59e0b',FOLLOWS:'#64748b',IMPLEMENTS:'#0ea5e9',APPLIES_TO:'#22d3ee',STATE_CONSTITUTIONAL_FAITH_ISSUE:'#facc15',CHALLENGES:'#f97316',INCORPORATED_IN:'#34d399',LIMITS_STATE_ENFORCEMENT:'#ef4444',CONFLICT:'#ef4444'};

  function draw(){
    const {w,h}=fit();
    ctx.clearRect(0,0,w,h);
    ctx.fillStyle='#0b1220'; ctx.fillRect(0,0,w,h);
    ctx.strokeStyle='#111f3a'; ctx.lineWidth=1;
    const step=36;
    for(let x=0;x<w;x+=step){ ctx.beginPath(); ctx.moveTo(x,0); ctx.lineTo(x,h); ctx.stroke(); }
    for(let y=0;y<h;y+=step){ ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(w,y); ctx.stroke(); }
    links.forEach(l=>{
      const a=positions[l.from],b=positions[l.to];
      ctx.strokeStyle=linkStroke[l.type]||'#475569';
      ctx.lineWidth = String(l.type).includes('DIRECT') ? 1.8 : (String(l.type).includes('TENSIONS') ? 1.4 : 1);
      ctx.setLineDash(String(l.type).includes('TENSIONS') ? [6,4] : []);
      ctx.beginPath(); ctx.moveTo(a.x,a.y); ctx.lineTo(b.x,b.y); ctx.stroke(); ctx.setLineDash([]);
      const mx=(a.x+b.x)/2, my=(a.y+b.y)/2;
      ctx.fillStyle='#7dd3fc'; ctx.font='9px ui-sans-serif, system-ui';
      ctx.fillText(l.type, mx+4, my-4);
    });
    positions.forEach((p,i)=>{
      const n = nodes[i];
      ctx.fillStyle = colors[n.group] || '#64748b';
      ctx.strokeStyle='#0b1220'; ctx.lineWidth=2;
      ctx.beginPath(); ctx.arc(p.x,p.y,7,0,Math.PI*2); ctx.fill(); ctx.stroke();
      if(n.conflict && n.conflict==='RED'){ ctx.strokeStyle='#ef4444'; ctx.lineWidth=2; ctx.beginPath(); ctx.arc(p.x,p.y,10,0,Math.PI*2); ctx.stroke(); }
      const src = sourceFor(n.id);
      ctx.fillStyle='#f8fafc'; ctx.font='10px ui-sans-serif, system-ui'; ctx.fillText(n.label, p.x+12, p.y+4);
      ctx.fillStyle='#7dd3fc'; ctx.font='9px ui-sans-serif, system-ui'; ctx.fillText(src || n.sub, p.x+12, p.y+15);
    });
  }
  draw();

  let dragging=false, dragIdx=-1;
  canvas.addEventListener('mousedown', e=>{
    const r=canvas.getBoundingClientRect();
    const mx=e.clientX-r.left, my=e.clientY-r.top;
    let best=-1, bestD=18;
    positions.forEach((p,i)=>{const d=Math.hypot(p.x-mx,p.y-my); if(d<bestD){bestD=d;best=i;}});
    if(best>=0){dragging=true;dragIdx=best;canvas.style.cursor='grabbing';}
  });
  window.addEventListener('mousemove', e=>{
    if(!dragging) return;
    const r=canvas.getBoundingClientRect();
    positions[dragIdx]={x:e.clientX-r.left, y:e.clientY-r.top};
    draw();
  });
  window.addEventListener('mouseup', ()=>{ dragging=false; dragIdx=-1; canvas.style.cursor='grab'; });

  const tbody=document.querySelector('#state-table tbody');
  const rowLegend={RED:'<span class="badge badge-red">Direct Conflict</span>',PARTIAL:'<span class="badge badge-partial">Partial / Challenge</span>',COMPLIANT:'<span class="badge badge-compliant">Compliant / Struck</span>',UNVERIFIED:'<span class="badge badge-unverified">Unverified</span>'};
  stateRows.forEach(r=>{
    const tr=document.createElement('tr');
    const raw=r[4]||'';
    const src=raw && raw.startsWith('http') ? '<a class="source-link" href="' + raw + '" target="_blank" rel="noopener">' + raw + '</a>' : raw;
    tr.innerHTML='<td>' + r[0] + '</td><td>' + r[1] + '</td><td>' + r[2] + '</td><td>' + (rowLegend[r[3]] || r[3]) + '</td><td>' + src + '</td>';
    tbody.appendChild(tr);
  });
}).catch(err=>{
  loadErr=err;
  console.error('graph load error', err);
  document.body.insertAdjacentHTML('beforeend','<pre style="color:#fca5a5;padding:12px;">' + err + '</pre>');
});
</script>
</body>
</html>`;
    return new Response(html, {
      headers: {
        'content-type': 'text/html;charset=utf-8',
        'cache-control': 'no-store',
      },
    });
  }
};
