# Sovereign-Constitutional Crosswalk

Source of truth for mapping constitutional drift taxonomy onto the POG2/MHD sovereign runtime modules. No fabrication. Every mapping is derived from the module descriptions in the user's MHD/POG2 artifacts and the verified constitutional drift classifications in `constitutional-structural-truth-graph.json`.

## Drift taxonomy (from verified constitutional artifact)

- **RED** (9 terms): legislative, commerce, tax, coin, tender, militia, attainder, money, writ
- **ORANGE** (5 terms): treason, habeas corpus, ex post facto, contract, emolument
- **YELLOW**: reserved for procedural expansions without textual amendment
- **GREEN**: reserved for within-original-meaning or explicit Article V amendments

## Sovereign modules (from POG2/MHD artifacts)

- `HexagramManager` — 64 states × 6 yao, deterministic state machine, 28 valid transitions, 46 fault/recovery states
- `GhostSplatPredictor` — adaptive Taylor expansion Orders 2–5, 3-tick horizon, H_total = H_elec + H_therm + H_fluid + H_cross
- `ElectricalRegisterSM` — maps hexagram intent → capability, states: OFF/ARMED/ACTIVE/SHED, gated by safety_ok + ct_ready
- `ChokeDriver` — 5-channel resonant PWM, 6.5 kHz carrier, 72° phase shift
- `Contactors` — 10 channels (5 segments × 2 poles), per-channel FSM: CT_CLOSED → CT_OPENING → CT_OPEN → CT_CLOSING → CT_CLOSED
- `CNSManager` — Python/C++ on ARM Cortex-A53, telemetry logging, knock-lock validation
- `640 ms canonical tick` — master heartbeat, 150M cycles @ 250 MHz, 16 sub-tick phases

## RED terms → sovereign module mappings

### legislative → HexagramManager + ElectricalRegisterSM
- **Constitutional drift:** Article I, Section 1 legislative power delegated to agencies via rulemaking; nondelegation doctrine violated
- **Sovereign mapping:** HexagramManager state transitions encode legislative intent → regulatory action. When drift is RED, the state machine must flag `safety_ok = false` for any hexagram state that maps to agency rulemaking without congressional authorization. ElectricalRegisterSM must refuse capability grants for delegated legislative actions unless Congress explicitly authorizes via verified statutory trigger.
- **Gating rule:** legislative RED → HexagramManager fault state 46 (unauthorized delegation); ElectricalRegisterSM remains OFF until safety interlock clears.

### commerce → HexagramManager + GhostSplatPredictor
- **Constitutional drift:** Commerce Clause expanded from trade/exchange to all economic activity; Wickard/Gonzales doctrine preempts state licensing
- **Sovereign mapping:** GhostSplatPredictor horizon (`H_elec + H_therm + H_fluid + H_cross`) must include a commerce-preemption cross-term when evaluating state-level licensing/professional regulation. HexagramManager must flag any state action in state_crosswalk domains as preempted when federal commerce power is invoked.
- **Gating rule:** commerce RED → GhostSplat Predictor includes `H_commerce_preemption` term; Contactors refuse state-level economic licensing activation without federal clearance.

### tax → ElectricalRegisterSM + CNSManager
- **Constitutional drift:** Direct taxes require apportionment; indirect taxes require uniformity; 16th Amendment departs from origin but structural shift remains
- **Sovereign mapping:** ElectricalRegisterSM state machine must encode tax power as congressional-only capability. CNSManager telemetry must log any tax-collection activation outside congressional authorization as fault state 12 (unauthorized revenue). HexagramManager does not mediate tax power directly; it flags when non-congressional actors attempt tax collection.
- **Gating rule:** tax RED → ElectricalRegisterSM ARMED only under explicit congressional mandate; CNSManager logs all tax-collection throughput with apportionment/uniformity audit trail.

### coin → ChokeDriver + ElectricalRegisterSM
- **Constitutional drift:** Coin power vested in Congress; Federal Reserve Act 1913 delegates to private banking system; state bullion depositories violate Section 10
- **Sovereign mapping:** ChokeDriver resonant frequency encodes monetary standard. When coin drift is RED, ChokeDriver must flag `ΔP` deviation from standard (1.3 ± 0.05 atm equivalent for monetary base). ElectricalRegisterSM must refuse capability grants for state-level coinage/tender actions. CNSManager logs all monetary-base mutations with congressional authorization checksum.
- **Gating rule:** coin RED → ChokeDriver enters frequency lock at constitutional standard; state-level tender actions trigger Contactors FSM to CT_OPENING.

### tender → Contactors + ElectricalRegisterSM
- **Constitutional drift:** States prohibited from making anything but gold/silver coin tender; Federal Reserve notes override via Supremacy Clause
- **Sovereign mapping:** Contactors 10-channel FSM gates tender-system activation per channel. When tender drift is RED, Contactors must enforce: state-level tender channels remain CT_OPEN unless federal override is verified via `safety_ok = true` with Supremacy Clause audit tag. ElectricalRegisterSM encodes tender authority as federal-only capability.
- **Gating rule:** tender RED → Contactors state channels default CT_OPEN; federal channels require verified safety_ok + Supremacy Clause clearance.

### militia → HexagramManager + CNSManager
- **Constitutional drift:** National Guard under federal control; selective service; citizen militia concept obsolete; state defense forces limited
- **Sovereign mapping:** HexagramManager state machine encodes militia readiness across 64 states × 6 yao. When militia drift is RED, HexagramManager flags state-level guard activation as fault state 23 (federalized beyond original state authority). CNSManager logs all militia/call-up events with constitutional authority audit trail.
- **Gating rule:** militia RED → HexagramManager state 23 active; state-level activation requires federal + state dual authorization encoded in ternary line balance.

### attainder → HexagramManager + ElectricalRegisterSM
- **Constitutional drift:** Civil contempt incarceration, regulatory disqualification, registration regimes function as punishment without criminal trial
- **Sovereign mapping:** HexagramManager fault/recovery states (46 states) include attainder-equivalent detection: any state action imposing punishment without judicial trial maps to fault state 31 (legislative punishment bypass). ElectricalRegisterSM refuses capability grants for civil contempt/regulatory disqualification without judicial trial.
- **Gating rule:** attainder RED → HexagramManager fault state 31 active; ElectricalRegisterSM SHED until judicial trial pathway verified.

### money → ChokeDriver + CNSManager + ElectricalRegisterSM
- **Constitutional drift:** Fiat currency, electronic money, stablecoins, CBDC proposals; 31 U.S.C. § 5102 designates Federal Reserve notes as legal tender
- **Sovereign mapping:** ChokeDriver encodes monetary-base health via resonant frequency stability. GhostSplatPredictor includes `H_money_drift` term in total enthalpy. CNSManager logs all money-system mutations with statutory authority checksum. ElectricalRegisterSM gates CBDC/stablecoin activation as RED unless explicit congressional authorization.
- **Gating rule:** money RED → ChokeDriver enters resonant lock; CNSManager logs all money-system throughput; ElectricalRegisterSM CBDC/stablecoin channels default OFF.

### writ → HexagramManager + CNSManager
- **Constitutional drift:** Administrative subpoenas, national security letters, geofence warrants bypass traditional writ process; FISA courts issue secret writs
- **Sovereign mapping:** HexagramManager encodes writ privilege as judicial-only action. When writ drift is RED, HexagramManager flags administrative/executive writ-equivalents as fault state 17 (non-judicial process). CNSManager logs all writ-issuance events with judicial authority checksum.
- **Gating rule:** writ RED → HexagramManager fault state 17 active; administrative subpoena/NSL/geofence warrant actions require judicial override encoded in phase_temporal.

## ORANGE terms → sovereign module mappings

### treason → HexagramManager + CNSManager
- **Constitutional drift:** Rarely charged; functionally replaced by seditious conspiracy, material support, espionage statutes; same penalties without constitutional protections
- **Sovereign mapping:** HexagramManager state machine encodes treason as narrow two-witness + overt-act requirement. When treason drift is ORANGE, HexagramManager flags adjacent-statute prosecutions as warning state 9 (treason-equivalent without constitutional protections). CNSManager logs all treason-adjacent prosecutions with constitutional requirement audit trail.
- **Gating rule:** treason ORANGE → HexagramManager warning state 9 active; seditious conspiracy/material support/espionage prosecutions require two-witness + overt-act verification or flag as bypass.

### habeas corpus → HexagramManager + Contactors
- **Constitutional drift:** Military commissions; indefinite detention statutes; suspension debates; Article I, Section 9 exception for rebellion/invasion
- **Sovereign mapping:** HexagramManager encodes habeas suspension as emergency-only state transition. When habeas corpus drift is ORANGE, HexagramManager flags suspension actions as fault state 41 (suspension outside rebellion/invasion). Contactors gate detention-system activation; habeas-compliant detention requires verified suspension trigger.
- **Gating rule:** habeas corpus ORANGE → HexagramManager fault state 41 active; Contactors detention channels CT_OPEN only with verified rebellion/invasion suspension trigger.

### ex post facto → HexagramManager + ElectricalRegisterSM
- **Constitutional drift:** Civil retroactive penalties, regulatory retroactivity, SORNA retroactive application partially upheld; Smith v. Doe distinguishes civil from criminal
- **Sovereign mapping:** HexagramManager encodes ex post facto as retroactive-law prohibition. When ex post facto drift is ORANGE, HexagramManager flags retroactive civil/regulatory penalties as fault state 33 (retroactive penalty without criminal trial). ElectricalRegisterSM refuses capability grants for retroactive regulatory application.
- **Gating rule:** ex post facto ORANGE → HexagramManager fault state 33 active; retroactive civil/regulatory actions require criminal-trial pathway or remain SHED.

### contract → ElectricalRegisterSM + CNSManager
- **Constitutional drift:** Emergency price controls, debtor relief, mortgage moratoria, consent decrees, foreclosure stays impair contract obligation
- **Sovereign mapping:** ElectricalRegisterSM encodes Contracts Clause as state-action prohibition. When contract drift is ORANGE, ElectricalRegisterSM flags state debtor relief/mortgage moratoria/consent decrees as capability bypass. CNSManager logs all contract-impairing actions with constitutional authority audit trail.
- **Gating rule:** contract ORANGE → ElectricalRegisterSM state SHED for state-level contract impairment; federal bankruptcy preemption requires explicit Article I, Section 8 authorization.

### emolument → HexagramManager + CNSManager
- **Constitutional drift:** Foreign emoluments through business interests; domestic emoluments through presidential properties; OLC opinions narrowing definition
- **Sovereign mapping:** HexagramManager encodes emoluments as foreign/domestic prohibition on sitting officials. When emolument drift is ORANGE, HexagramManager flags officeholder business interests as warning state 7 (emolument-equivalent without explicit consent). CNSManager logs all emolument-adjacent payments with constitutional authority audit trail.
- **Gating rule:** emolument ORANGE → HexagramManager warning state 7 active; foreign/domestic emoluments require congressional consent encoded in phase_changing_lines.

## Module-level summary matrix

| Sovereign Module | RED Terms | ORANGE Terms | Primary Gating Mechanism |
|---|---|---|---|
| HexagramManager | legislative, commerce, militia, attainder, writ, money | treason, habeas corpus, ex post facto, emolument | Fault/warning states 31/41/33/17/23/9/7 |
| GhostSplatPredictor | commerce, money | — | H_commerce_preemption, H_money_drift terms in 3-tick horizon |
| ElectricalRegisterSM | legislative, coin, tender, attainder, money, writ | ex post facto, contract | OFF/ARMED/ACTIVE/SHED gated by safety_ok + constitutional authority |
| ChokeDriver | coin, money | — | Resonant frequency lock at constitutional standard |
| Contactors | tender, militia, habeas corpus | — | 10-channel FSM; CT_OPEN/CLOSED gated by constitutional trigger |
| CNSManager | tax, militia, money, writ | treason, emolument | Telemetry logging with constitutional authority checksum |
| 640 ms canonical tick | all | all | Master heartbeat; constitutional drift events must not race tick |

## Tick-cadence rule

Constitutional drift classification updates must occur on the 640 ms canonical tick boundary. Consult/slider operations must not race the game tick. Drift event timestamps are authoritative only when emitted from CanonicalClock pulse boundaries.

## English crown exclusion binding

All RED/ORANGE mappings explicitly exclude English crown lineage, prerogative powers, parliamentary sovereignty, and common-law inheritance. The sovereign modules are US-constitutional-only inputs; crown-derived legal concepts are filtered at the HexagramManager input layer before state evaluation.
