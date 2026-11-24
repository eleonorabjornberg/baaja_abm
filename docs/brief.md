# What BAAJA would do to US electricity supply: a simulation of permitting, courts and the interconnection queue

*Methods and results brief, 24 November 2026. Model, data and code: this repository. Full model description:
[`docs/ODD.md`](ODD.md). Section map of the bill: [`docs/bill_question_map.md`](bill_question_map.md).*

## Summary

The Bipartisan American Affordability and Jobs Act (BAAJA) was introduced as S.5653 on 30 September 2026 and adopted
with changes as S.Amdt. 6883 to H.R. 2347, which the Senate passed on 19 November 2026 by 62 to 33. The House has
not yet acted on it, so it is not law; the model assumes enactment in November 2026, and later enactment moves every
date below by the same amount. This brief asks how much generating and storage capacity the Senate-passed text would
bring online in the United States by 2041,
in which regions, and what that does to regional reserve margins.

By November 2041 the bill adds 6.7 GW of new capacity if no RTO/ISO changes its interconnection process under
Sec.2106, and 37.0 GW if every one does, against about 954 GW that comes online under current law. Where between the
two it lands depends on how many RTOs change their process, which nothing in the record predicts. The central case,
with each RTO changing with probability one half, gives 21.9 GW; it is close to the midpoint of the two bounds and is
a convention. Of the 21.9 GW, 14.9 GW are renewables, 5.0 GW gas and 2.0 GW storage. About 4 GW of
the 6.7 GW comes from the extra hosting room the model credits to Sec.2109 (advanced transmission technologies); the
permitting, court and permit-certainty provisions on their own add 2.9 GW. Existing hydro whose new licence comes
sooner accounts for a further 1.8 GW; this is existing capacity kept in service and is not counted as new
capacity.

The size of the Sec.2106 effect rests on three assumptions the statute does not settle. The first is whether an
RTO's process changes at all (FERC may find existing processes compliant under Sec.2106(d)). The second is what the
single decision point removes. In the model it removes a re-study round that under current law adds six months
before an agreement and raises the costs of the requests that stay when others withdraw; both are assumptions. With
no such round under current law, Sec.2106 adds between -2.6 and +0.5 GW even if every RTO changes its process
(section 4.5). The third is the entry screen that stands for the non-refundable security. With every RTO changing its
process, the bill adds 44.2 GW with no screen, 37.0 GW with the relative screen used here, and -4.4 GW with the
absolute threshold I first specified. I changed from the absolute to the relative version after seeing those results
(section 2). Drawing the assumption ranges of section 5 together, with the relative screen and the calibration held
fixed, gives a median of 26.5 GW [4.9, 64.0] (5th-95th percentile of 400 joint samples).

Little changes before the early 2030s. The model assumes reformed interconnection studies start about three years
after enactment (range two to four; the bill gives FERC 18 months for the rule and RTOs two years from enactment to file), and that
requests already in the queue keep their current terms. By 2030 the bill has added 0.3 GW; by 2035, 10.8 GW.

The gain is concentrated in MISO, with 12.4 of the 21.9 GW, and MISO accounts for about three quarters of what
Sec.2106 adds, so the result is close to a question about whether MISO's process changes. MISO gains because its
fitted study capacity falls short of the requests arriving; with PJM's ratio of study capacity to arrivals, MISO's
gain with every RTO changing falls from 23.5 to 13.6 GW. PJM gains almost nothing (0.7 GW with every RTO changing).
That result is a property of the model: there, most PJM solar and storage that completes
pays no upgrade cost, so the entry screen removes completers, and without the screen PJM gains 9.0 GW. In LBNL's PJM
cost data, completed solar projects are no more likely to have zero upgrade cost than withdrawn ones (sections 4.3
and 6). ERCOT is outside FERC's rate and interconnection
jurisdiction, and the Southeast and most of the non-ISO West have no RTO, so Sec.2106 does not reach them. ERCOT gains
from the permitting and court provisions only; the Southeast and the non-ISO West also gain from Sec.2109, which
applies to FERC-jurisdictional public utilities, not only to RTOs.

Under current law the national shortfall below NERC's Reference Margin Levels reaches about 69 GW in 2035 (70 GW
[25, 132] when demand growth, retirements and accreditation are drawn jointly) and 122 GW in 2041, most of it in PJM, whose installed reserve margin, as reported by NERC, rises from 18.6% in 2026 to 35.1% in
2034. NERC's forecast ends in 2035; the 2041 figure extends demand at its 2030-35 growth rate and holds margins at
their 2035 levels. BAAJA reduces the 2035 shortfall by 3.1 GW
[0.3, 6.4]. The shortfall is a benchmark against NERC's planning margins and says nothing about outages. The bill does
not close it, with or without the entry screen.

The published estimates measure different things. Resources for the Future reports about 60 GW more clean capacity
in 2028 (Rennert and Bergman 2026); this model's gain by 2028 is zero, because reformed studies start about three
years after enactment. Rhodium Group reports 17 to 249 GW more clean capacity through 2040, a range across technology
costs and fuel prices (King et al. 2026); this model's gain in renewables and storage by November 2041 runs from
5.9 GW if no RTO changes its process to 27.8 GW if all do. Both studies are capacity-expansion models that report net
changes in a fleet that meets demand, and both expand transmission under the bill; this model counts gross additions
from the queue and plans no transmission. RFF names permit certainty and faster interconnection as the primary
drivers of its near-term gain, and each study, including this one, sets the extent of interconnection relief by
assumption.

![Headline: BAAJA minus current law by 2041](../figures/brief_1_headline.png)

## 1. The bill and the question

BAAJA is a permitting and transmission bill. The provisions that bear on generating capacity fall into four groups
(full map, with each section's status, in `docs/bill_question_map.md`):

| group | main sections modelled | what changes in the model |
|---|---|---|
| Permitting | 1105 and 1108 (level of review), 1106 (enforcement of the existing one-year EA and two-year EIS deadlines, new deadlines for decisions after the review), 1202 (tighter rules on the existing one-year Clean Water Act s.401 clock), 1302 (ESA consultation timeline), 2213 (clocks for renewable and storage rights-of-way on federal land), 2229 | months to a federal permit |
| Courts | 1110 (150-day limit, comment exhaustion and remand without vacatur for NEPA claims) and 2201 (150-day limit and expedited review for energy authorizations); 1134 sets a 150-day limit for FAST-41 claims (1205 and 1305, for s.404 approvals and ESA opinions, are listed but not modelled separately) | how many suits are filed and how many halt a project |
| Permit certainty | 1401 | whether a permit can be revoked or suspended after issue |
| Grid access | 2106 (interconnection reform in RTOs/ISOs), 2110 (study automation), 2109 (advanced transmission technologies), 2101, 2102(a) and 2214 (transmission permitting) | who enters the interconnection queue, who leaves it, how long studies take, how much hosting room the grid has |

Sections 1203 and 1204 (NPDES permit term and Clean Water Act s.404) are listed but not modelled, because they act
on existing plants and on wetlands permits the model cannot attach to generation projects.

The model asks how much capacity comes online by region and year with and without the bill, and what that does to
each region's reserve margin. It does not estimate prices, emissions or customer bills.

Several provisions that bear on supply are outside the model. Sec.2107(b) confirms that states may condition retail service to a
data center on new generation it procures, which acts on the demand behind the adequacy gap. Sec.2108 bars RTOs from
blocking aggregations of behind-the-meter storage, fuel cells and generators of 5 kW to 5 MW each from wholesale markets,
which is capacity outside the interconnection queue. Sec.2102(b) exempts interstate gas pipeline looping and
compression in existing corridors from NEPA review. Sec.2109 also requires public utilities to evaluate advanced
technologies on existing lines and deploy them where benefits exceed costs; the model credits only extra hosting room
on lines finished after month 36, later than the one year the statute gives FERC for its order.
Sec.2103 (new interregional planning with cost allocation; regional planning is deemed met by Order No. 1920) is, in
my reading, the bill's main route to new transmission, and the model does not plan transmission. Sec.1501-1504 (nuclear licensing) are listed
because no new reactor reaches operation through the queue data by 2041.

## 2. The model

The full description, in the ODD form of Grimm et al. (2020), is in `docs/ODD.md`. In short, it is a model of the
interconnection queue with decision rules for grid operators and developers, coupled to a permitting and litigation
pipeline and to a supply-and-adequacy account.

Projects. Every generation, storage and transmission request from 2026 to 2041, plus the queue standing at the end
of 2025, is drawn from LBNL interconnection-queue data by technology and region (Rand et al. 2026). Each goes through
federal permitting if it has a federal hook, possible litigation, possible federal halt, interconnection and
construction. Permitting and litigation are sized from CEQ, BLM, Army Corps and NEPA-litigation data.

Grid operators, one per region, study requests in clusters (ERCOT one at a time) with a throughput fitted to LBNL
request-to-agreement times. They allocate network-upgrade costs drawn from LBNL's regional cost studies; costs rise
with the capacity signed in a region (by a rate fitted to LBNL cost data for requests made since 2018 against 2010-17; zero in ERCOT, which did not allocate network upgrades to generators through 2025) and fall as transmission is finished.

Developers enter on the published wait and on their region's projected capacity shortfall. At each study result they
compare the allocated upgrade cost with the project's value and stay or leave. The shape of the value distribution
comes from LBNL cost and completion data; its level is one scale per technology and region, fitted so that
completion matches LBNL's rates. The scales run from 0.007 to 3.9, so value here stands for every reason a project
completes or not that the model does not otherwise represent; it is not revenue, and the model has no prices.
Developers also withdraw over time at background rates fitted by region.

Supply. What comes online is added to the EIA-860 fleet, less announced and age-based retirements, and compared with
NERC's 2025 peak-demand forecast and reference margin levels (NERC 2026). Wind, solar and batteries count at on-peak
shares that start at NERC's national values and fall halfway to PJM's 2041/42 ELCC class ratings by 2041 (on-peak
accredited capacity below).

The bill enters as mechanisms. Under Sec.2106 a reformed RTO publishes planned interconnection locations
with "an upfront, fixed, subregional, per-megawatt fee" (new FPA s.228(a)(2)(B)), holds a single decision point, and
requires "meaningful and nonrefundable financial security" and "withdrawal penalties after the determination of total
costs of interconnection ... are provided to the customer" (s.228(a)(3)(B) and (C)). Four choices here are model
assumptions, not statute. The single decision point removes the current-law re-study round for every request made
after the rule in an RTO whose process changes: requests that stay sign at the cost in their first study result, six
months sooner, and the cost that other requests' withdrawals would have shifted onto them is assumed to be covered by
forfeited security and penalties, which the model does not check. The fee is set at the region's expected upgrade
cost, so requests at a published location face no cost shock at the study result; those requests are exempt from the
screen; and the security
in (B) is represented as an entry screen, applied before costs are known, while the penalty in (C), which applies once
costs are known, is not modelled separately. Within each technology and region, the quarter of new
requests least likely to complete (range a tenth to a half) do not enter; requests using a published location are
exempt. Johnston, Liu and Yang (2023, revised 2026) find, for PJM, that higher queue-entry costs have little effect
on completed capacity (-1.2% to +0.8%) or on waiting time, because they mainly deter requests that would have left
quickly. The modelled screen is harsher than that: it removes 8.3 GW of completions in PJM and shortens the queue in
MISO, so their result is closer to the no-screen case in section 4.4 than to my central case.
Each RTO's process changes with probability 0.5 in the central case.

The screen was first specified as an absolute threshold: requests whose modelled chance of completing was below
0.25 did not enter. After the calibration was refitted, that threshold kept out nearly all new storage requests in PJM.
The refit had put developer values for storage in PJM, SPP and ERCOT, solar in SPP and offshore wind at the bottom of
their allowed range, where few requests clear an absolute threshold.
An absolute threshold on the modelled chance of completing depends on those fitted scales, and where a scale sits at
its bound the modelled chance carries little information. A screen defined as a share does not depend on the scale:
under the calibration before the refit, with every RTO changing its process, the relative screen gives +42.9 GW
against +37.0 now, and the absolute one +9.5 against -4.4. I changed to the relative screen after seeing the results;
I should have specified it that way before running. The relative screen is a quota, though: it fixes the share kept
out instead of deriving it from the size of the deposit, and where value says little about completing it is close to
a random cut (in PJM storage, 133 of the 135 requests per run that sign after the rule pay no upgrade cost). Both
versions, and no screen, are reported in section 4.4. Sec.2110 is a study-throughput
gain, zero in the central case because the bill sets no target. Sec.2109 adds hosting room per transmission line
finished after the rule.

Each bill scenario is run against current law with the same random numbers, so differences come from the bill and
not from sampling noise. There are 100 paired runs per scenario and 400 joint Latin-hypercube samples of every
assumption range for the uncertainty analysis (Saltelli et al. 2008).

A simpler version of the model (Sims 1-6) draws interconnection time from the historical distribution instead of
from the queue. Its results appear alongside as a check and are labelled as such.

## 3. Data

All inputs are public. Sources, retrieval dates and file hashes are in `data/SOURCES.md`.

- Interconnection: LBNL *Queued Up* workbook (requests through 2025) and LBNL interconnection-cost studies for MISO,
  PJM, SPP, NYISO, ISO-NE and non-ISO balancing areas (used for the Southeast and West). The CAISO, MISO and NYISO queue files were downloaded for cross-checks but are not
  used.
- Permitting: CEQ EIS timelines, BLM MLRS rights-of-way cases, Army Corps permit data.
- Courts: a case-level export of 1,821 NEPA cases filed 2001-22 (supplied; publisher to be recorded in `data/SOURCES.md`); Sabin Center renewable-opposition database.
- Fleet, retirements and generation: EIA-860 (2015-2025), EIA-860M, EIA-923.
- Demand and adequacy: NERC 2025 Long-Term Reliability Assessment; PJM ELCC class ratings.
- Bill text: the Senate floor copy of S.Amdt. 6883 (KAT26804 V62), checked against the engrossed Senate amendment to
  H.R. 2347 (GovInfo, BILLS-119hr2347eas). All 83 sections are identical in letters and digits, apart from two section
  labels in Sec.2301-2302 and the attestation at the end.

## 4. Results

All numbers in this section are from the grid-agent model (Sim 7, `results/sim7_grid_agents.json`): means across
100 paired runs, with the 5th and 95th percentiles in brackets, for capacity online by November 2041. New capacity
excludes relicensed hydro, which is reported separately.

### 4.1 How much, and under which assumption about Sec.2106

| scenario | new capacity GW | renewables GW | gas GW | storage GW |
|---|---|---|---|---|
| BAAJA, no RTO changes its process (Sec.2106 off) | +6.7 [+5.0, +8.8] | +4.8 | +0.9 | +1.1 |
| BAAJA, each RTO changes its process with probability 0.5 (central) | +21.9 [+7.5, +37.2] | +14.9 | +5.0 | +2.0 |
| BAAJA, every RTO changes its process | +37.0 [+32.0, +42.8] | +24.7 | +9.2 | +3.1 |
| BAAJA, central, plus a 25% study-throughput gain under Sec.2110 | +37.4 [+26.1, +49.3] | +23.3 | +8.4 | +5.8 |

Current law brings about 954 GW of new capacity online by November 2041 [939, 972]. The bill adds 0.7% to 3.9% to that
(2.3% in the central case), depending on how many RTOs change their process. The first row, which keeps every provision except Sec.2106, contains
the permitting, court and permit-certainty provisions (Division A, Titles I-IV; Division B, Title II), Sec.2109, and
Sec.2110 at zero; Sec.2109's extra hosting room adds about 4 GW
to the central case (+17.8 GW without it). With Sec.2106 and Sec.2109 both off, the remaining provisions add
2.9 GW [1.6, 4.5] (`results/sec2106_decomposition.json`). Existing hydro whose new licence comes sooner accounts for a
further 1.8 GW in every bill scenario; it is existing capacity kept in service.

The interval on the central row is wide because it mostly records which RTOs happen to change their process in each
run. The two rows around it bound it, and the probability of one half is an assumption: Sec.2106(d) lets FERC find an
existing process compliant, and nothing in the record says how often it will. Adoption is drawn independently for
each RTO, although one FERC rule sets the standard for all six, so the central row's spread understates the chance of
all-or-nothing outcomes. The simpler model, with study times drawn from history and Sec.2106 and Sec.2110 set to
zero, gives +8.0 GW [+6.1, +9.6] for the permitting, court and certainty provisions, and has no Sec.2109. With the
grid agents the same provisions give 2.9 GW. The first row's total is close to the simpler model's by coincidence;
on the provisions the two models share they differ by a factor of almost three.

Part of the gain is timing. With every RTO changing its process, new requests in RTO regions add 33.6 GW online by
November 2041, but only 29.2 GW more of them ever complete; the difference, about 4.5 GW, would have come online after
2041 anyway and arrives earlier under the bill (`results/sec2106_decomposition.json`).

### 4.2 When

| year (to November) | current law: new GW that year | BAAJA central: cumulative GW vs current law | no RTO changes | every RTO changes |
|---|---|---|---|---|
| 2028 | 91 | +0.0 | +0.0 | +0.0 |
| 2030 | 114 | +0.3 | +0.3 | +0.3 |
| 2032 | 56 | +0.6 | +0.6 | +0.6 |
| 2033 | 62 | +2.3 | +1.1 | +3.3 |
| 2035 | 53 | +10.8 [+3.4, +18.4] | +1.9 | +18.8 |
| 2038 | 48 | +17.0 | +4.0 | +29.7 |
| 2041 | 44 | +21.9 | +6.7 | +37.0 |

The bill adds under 1 GW before 2033. The permitting and court provisions add a little each year from the start.
The model applies Sec.2106 only to requests made after reformed studies start (late 2029 in the central case, an
assumption; the statute is silent on requests already queued), and the first of those come online in 2033. Current-law additions peak at 118 GW in 2029, while the queue standing at the end of 2025
is being built, then settle at 44 to 62 GW a year. The peak is about twice the largest year in EIA-860 for these
technologies (57.5 GW in 2025); the model puts no supply-chain or labor limit on construction.

### 4.3 Where

![New capacity by region](../figures/brief_2_regions.png)

Of the 21.9 GW in the central case, 12.4 GW is in MISO; if every RTO changes its process, MISO gains 23.5 of the 37.0
GW. ERCOT, the Southeast and the non-ISO West gain 0.5 to 1.9 GW each from the provisions that apply everywhere.

PJM gains almost nothing from Sec.2106: 0.5 GW in the central case and 0.7 GW if every RTO changes its process, the
same as with Sec.2106 off. If every RTO changes its process, Sec.2106 does shorten PJM's studies (from 30 to 28 months to
agreement, median for requests made in the first five years) and raise the share of requests that sign, but the
entry screen offsets it. The screen keeps out the requests least likely to complete, ranked by value within
technology and region, and in PJM that ranking carries little information. In LBNL's cost study 13.7% of PJM requests
pay no upgrade cost, as many as the 13.7% of PJM solar requests that complete and more than the 7.5% of storage
requests. The calibration therefore sets low values for both, and completing in the model depends mostly on drawing a
zero cost: per run, 216 of the 427 PJM solar requests and 133 of the 135 storage requests that sign after the rule pay
nothing. A screen on value then removes completers almost in proportion.

The numbers below are from `results/sec2106_decomposition.json` (every RTO changes its process, 100 paired runs).
Without the screen PJM gains 9.0 GW (MISO 18.3). Giving PJM MISO's zero-cost share of 2.5% raises PJM's gain with the
screen from 0.7 to 5.6 GW; giving it MISO's narrower cost spread changes nothing (0.9 GW). The screen lowers the gain
in every RTO except MISO: PJM by 8.3 GW, SPP 1.7, CAISO 1.1, NYISO 1.0 and ISO-NE 0.5. In MISO it adds 5.3 GW,
because MISO's fitted study capacity at the end of 2025 is 0.59 of the requests arriving, so fewer entrants shorten
the queue. With PJM's ratio of 0.97, MISO's gain falls from 23.5 to 13.6 GW and the screen costs MISO capacity too.
The PJM result is a property of the modelled screen and of how the calibration reads PJM's cost data, and LBNL's PJM
data do not show zero cost as the route to completion (section 6).

### 4.4 The entry screen

| entry screen | BAAJA central vs current law | every RTO changes |
|---|---|---|
| no entry screen | +26.5 [+11.6, +42.0] | +44.2 [+39.9, +48.8] |
| Sec.2106 keeps out the bottom quarter within technology and region (central) | +21.9 [+7.5, +37.2] | +37.0 [+32.0, +42.8] |
| Sec.2106 keeps out requests whose chance of completing is below 0.25 (previous specification) | -0.1 [-17.7, +18.8] | -4.4 [-11.4, +1.0] |

These rows are from `results/sec2106_decomposition.json`, 100 paired runs. The relative screen is not the most
favorable of the three; no screen gives more. Under the previous, absolute specification the bill reduces capacity,
because the screen removes most storage requests in regions where the fitted developer value is at its lower bound
(section 2). Which specification is right is not something the data here can settle, and the result depends on it.
Assuming current law already screens out a tenth of requests, as FERC Order No. 2023's readiness deposits may, raises
the bill's effect slightly (+19.4 GW central and +39.8 GW with every RTO, against +17.4 and +37.3 in the same 20 paired
runs, `results/sim7_grid_agents.json`), because fewer marginal requests are left for Sec.2106 to remove.

A stricter relative screen also matters: keeping out half of new requests instead of a quarter brings the central
case to +6.4 GW, below the +7.3 GW with Sec.2106 off in the same 20 runs, so a strict enough screen cancels the rest of
Sec.2106. Keeping out a tenth gives +21.0 GW.

### 4.5 What the single decision point does

Taking Sec.2106 apart, with every RTO changing its process (`results/sec2106_decomposition.json`, 100 paired runs),
the single decision point alone adds 35.0 GW over the bill without Sec.2106, published locations add 2.5 GW more, and
the relative screen takes 7.2 GW away, for 30.3 GW in all. Published locations add little because the fee is set at
the region's expected upgrade cost, which with skewed costs is more than most requests would pay, so few use them; a
published location is presumably one with room, and its fee could be lower.

The single decision point is worth so much because of what it removes. Under current law in cluster regions the
model has one re-study round: when requests withdraw at the first study result, the costs of those who stay rise by
0.3 times the share of capacity that withdrew, and the agreement comes six months after the first result. Both
numbers are assumptions, with no data behind them. The table changes them in current law and in the bill alike.

| current-law re-study round (law and bill) | current law GW | no RTO changes | every RTO, single decision point only | every RTO, full Sec.2106 | central (p = 0.5) |
|---|---|---|---|---|---|
| cost rise 0.3, 6 months (central) | 954 | +6.7 | +41.7 | +37.0 | +21.9 |
| cost rise 0 | 988 | +7.2 | +27.7 | +22.9 | +14.8 |
| 1 month | 955 | +6.7 | +24.2 | +21.7 | +13.9 |
| cost rise 0, 1 month | 988 | +7.2 | +10.2 | +7.7 | +6.7 |
| no re-study round | 988 | +7.2 | +7.2 | +4.6 | +5.1 |

About half of the effect comes from the cost shift and half from the six months. With neither the cost shift nor more
than a month of re-study, Sec.2106 adds 0.5 GW with every RTO changing its process; with no re-study round at all it
lowers capacity by 2.6 GW, because the screen's cost then outweighs what is left. The sensitivity ranges in section 5
(0.1 to 0.6 for the cost shift, 3 to 12 months) stop short of these values. The model also lets the requests that
stay at the single decision point sign at their first-result cost; who pays for upgrades that withdrawn requests
would have shared is not modelled.

### 4.6 Adequacy

![Shortfall below NERC reference margin levels](../figures/brief_3_shortfall.png)

The adequacy account compares on-peak accredited capacity with NERC's 2025 peak-demand forecast plus each region's
Reference Margin Level, the reserve margin NERC uses as its planning benchmark. Under current law the national
shortfall below those levels is 9 GW in 2027, 69 GW [66, 73] in 2035 and 122 GW [118, 127] in 2041; those brackets are
the spread across runs, and drawing demand growth, retirements and accreditation jointly gives 70 GW [25, 132] in 2035
(median, `results/uncertainty.json`). In 2035, 57 GW of
the shortfall is in PJM, whose Reference Margin Level, an installed reserve margin, rises in NERC's assessment from
18.6% in 2026 to 35.1% in 2034. PJM explains the rise by resources added having lower accredited value than those
retiring (PJM 2026). PJM's own October 2026 study projects a lower path, 24.4% for 2034/35; on NERC's 2035 PJM peak of
199 GW that difference is about 21 GW of the 57. CAISO (7 GW) and MISO (5 GW) account for most of the rest. NERC's
forecast ends in 2035: for 2036-41 the model extends demand at its 2030-35 growth rate and holds each region's margin
at its 2035 level, so the 2041 figures rest on that extension.

BAAJA reduces the 2035 shortfall by 3.1 GW [0.3, 6.4] in the central case and by 5.8 GW if every RTO changes its
process; by 2041 the reductions are 5.7 and 10.3 GW. The bill does not close the gap. Most of the shortfall is in PJM,
where the bill adds little (section 4.3); without the entry screen PJM gains 9.0 GW of nameplate capacity, mostly solar
and storage, against a 57 GW gap there, so this conclusion does not rest on the screen. MISO's 2035 shortfall is 5 GW,
so MISO capacity beyond that does not reduce the national figure. The simpler model, with historical study times (Sim 6,
`results/sim6_supply.md`), shows MISO and ISO-NE first falling below their margins in 2027 (median first year across
runs; MISO's margin is 0.8% against 8.3% that year) and close to them by 2035: MISO's reserve margin is then 8.4%
against a Reference Margin Level of 8.9%, and ISO-NE's 11.8% against 13.0%, below the level in 66% and 71% of runs.
With the grid agents the 2035 margins are lower, 5.2% in MISO and 11.0% in ISO-NE.

These figures are a benchmark against planning margins. They are not a forecast of outages: apart from developers entering faster where a shortfall is projected,
the model has no response from prices, no demand response beyond NERC's forecast and no delayed retirements, all of
which narrow a shortfall in practice.

Under the joint uncertainty analysis below, the 2035 shortfall reduction is 2.0 GW [0.1, 8.8] (median, 5th-95th
percentile across 400 samples).

## 5. What drives the result

Two analyses answer this. The first moves one assumption at a time to the low and high end of its range, holding the
others central (20 paired runs each, `results/sim7_grid_agents.json`, central case +17.4 GW in these runs). The second
draws every assumption at once, 400 Latin-hypercube samples, and splits the variance of the result by rank regression
(`results/uncertainty.json`).

| assumption (range) | BAAJA minus current law, new GW, low / high |
|---|---|
| probability an RTO changes its process (0 / 1) | +7.3 / +37.3 |
| Sec.2110 study-throughput gain (0 / 25%) | +17.4 / +34.8 |
| Sec.2109 hosting room per new line (0 / 30%) | +13.3 / +25.8 |
| share of requests the entry screen keeps out (0.5 / 0.1) | +6.4 / +21.0 |
| growth of upgrade cost with capacity signed (5.14 / 0) | +13.5 / +24.2 |
| months of re-study after the first result (3 / 12) | +13.3 / +24.2 |
| cost rise for remaining requests per withdrawn MW (0.1 / 0.6) | +13.6 / +21.5 |
| share able to use a published location (0.25 / 0.9) | +16.9 / +18.3 |
| fee as a multiple of expected upgrade cost (1.5 / 0.8) | +16.8 / +18.4 |
| hosting room added per transmission project, GW (0.5 / 3.0) | +14.4 / +22.0 |
| entry response to the region's projected shortfall (0 / 3) | +18.0 / +14.7 |
| entry response to the published wait (0 / 1) | +16.7 / +18.4 |
| hold after an adverse study result under Sec.2106, relative to current law (0 / 1) | +17.4 / +17.4 |

The bill's effect is most sensitive to the assumptions about how Sec.2106 and Sec.2110 are carried out, none of which
the statute sizes; section 4.5 takes the two re-study assumptions below these ranges. The hold row has no effect by
construction, since the hold only delays when a withdrawal is recorded. Upgrade-cost growth (`kappa`) matters more for the level of current law than for the bill's
effect: at zero, current law brings 1,118 GW online, against 842 GW at the high end.

![What drives the result](../figures/brief_4_drivers.png)

Drawing every range in the table together, with the relative screen and the calibration held fixed, gives a median
of +26.5 GW [+4.9, +64.0] of new capacity. The median is above the
central +21.9 GW because the joint draw includes Sec.2110 gains above zero, while the central case sets them to zero.
Rank regression explains 67% of the variance. The largest share, 23% [14, 31], is how much of the RTOs' capacity sits
in RTOs that changed their process in that sample, followed by the Sec.2110 gain (12%), the screen's share (7%),
upgrade-cost growth (6%) and Sec.2109 hosting room (6%). Split by the adoption that happened, the median is +13.3 GW
when no RTO changed its process, +26.5 GW when some did and +39.3 GW when all did. The probability that an RTO
changes is drawn uniformly from 0 to 1, so the joint samples hold more cases with no RTO or every RTO changing than the
central case does. The joint draw leaves out the screen's specification (section 4.4), re-study values below the
ranges in the table (section 4.5), every fitted parameter (value scales, withdrawal hazards, the hold, study
throughput, among them MISO's shortfall of study capacity), the structural errors the backcast shows (section 6) and
any correlation in adoption across RTOs. No drawn assumption makes the effect negative, so the lower bound of +4.9 GW
is positive by construction.

In the simpler model, with Sec.2106 and Sec.2110 at zero, the result is a median of +8.0 GW [+4.6, +13.1], and 52% of its
variance comes from one assumption: the share of new applications for rights-of-way on federal land whose Sec.2213
intake deadlines are met. When that model's study-time cut for Sec.2106 is instead drawn from zero to ERCOT's pace, the range becomes
+33.5 GW [+6.5, +188.7], with 76% of the variance from that cut alone. The grid-agent model replaces that single assumed
cut with operators and developers whose current-law behavior is fitted to queue data. The bill's effect on them is
still set by assumption, so the narrower range (64 against 189 GW at the upper end) reflects the ranges I chose for
those assumptions.

## 6. Validation

The model was run from January 2010 to December 2025 under current law and compared with what happened
(`results/backcast.md`, `results/calibration.json`). Following the pattern-oriented approach (Grimm et al. 2005;
Windrum et al. 2007), it is checked against several patterns at once, some of them left out of the fit. It passes some
tests and fails others, and the failures bear on the result.

What was fitted, and to what. Grid operators' study throughput was fitted to LBNL request-to-agreement times for
2010-19 cohorts; CAISO, ERCOT and MISO have their own fit, and the other six regions, which lack reliable agreement
dates, use the pooled MISO and CAISO fit. Developers' background withdrawal rates were fitted to the shares of
2015-19 requests withdrawn by 12, 36 and 60 months in each region, three parameters for three targets. Developer
value scales were fitted to LBNL completion rates for 2010-19 requests by technology and region. The NEPA EIS
probabilities and overdue windows were refitted with the agents on, and the storage settings were chosen with the
backcast in view, so the backcast is not fully independent of the fit.

National additions, 2018-25 (EIA-860, not used in fitting). The agents produce 68% of EIA's solar additions (86.9 vs
127.2 GW), 82% of onshore wind, 80% of gas and 45% of storage (19.5 vs 43.1 GW). The simpler model with historical
study times does better (82%, 100%, 84% and 108%). Both miss the 2024-25 jump in solar (31 and 30 GW in EIA); the agents also miss the jump in storage. By region, the
weighted mean absolute log ratio of model to EIA additions is 0.51 for the agents and 0.42 for the simpler model;
MISO, where much of the Sec.2106 effect sits, builds 0.51 of EIA's additions (24.0 against 46.8 GW), and storage in PJM is 3.9 GW in the model against
0.4 GW in EIA.

![Backcast: model vs EIA-860 additions, 2018-25](../figures/brief_5_backcast.png)

Completion by technology and region. Of the 28 cells with an LBNL completion rate of at least 5%, all but two are
within 35% of it. ERCOT storage completes at 18.4% in the model against 11.7% in the data: its value scale is at the
lower bound of its range, and 17% of requests in the pooled ISO cost sample that stands in for ERCOT (LBNL has no
ERCOT cost study) have no upgrade cost, so even the lowest value leaves too many completing. Geothermal outside the
West completes at 25.3% against 13.7%. Below 5%, storage in SPP and MISO and offshore wind miss by more than a third,
each by under 2 points. Five value scales
sit at that lower bound (solar in SPP; storage in ERCOT, PJM and SPP; offshore wind), so in those cells the fitted
value is a corner of the search range.

Completion by upgrade cost. Sec.2106 acts on how completion responds to the allocated cost. Across cost bins from
$0-10/kW to over $400/kW, the model completes 0.30, 0.16, 0.12, 0.08, 0.04 and 0.01 of the requests that receive a study
result, against 0.80, 0.67, 0.59, 0.42, 0.18 and 0.07 of LBNL's resolved requests (`results/sim7_grid_agents.md`).
LBNL counts only resolved requests, so the levels are not comparable, but the model's completion halves between the
first two bins and LBNL's falls by a sixth. In PJM, completion in the model runs mostly through zero-cost draws
(section 4.3). In LBNL's PJM cost study, 12% of completed solar projects queued since 2010 have no upgrade cost,
against 14% of withdrawn ones (my tabulation of the latest study for each project; 15% and 16% for requests since
2018), so in the data zero cost is not the route to completion. Waiting longer also does not raise withdrawal in the
agents, which leaves out one route by which a faster process raises completion.

Withdrawal timing. In the fitted cohorts the 24-month shares, which were left out of the fit, differ from the data
by at most 0.05 in every region. The 2020-23 cohorts, used in no fit, are a different matter. The model's 12-month withdrawal shares are
0.59 in CAISO against 0.12 in the data, 0.30 in PJM against 0.13, 0.40 in NYISO against 0.72 and 0.09 in the West
against 0.33. The data's withdrawal rates for these cohorts differ from 2015-19 in both directions, and the model's
hazards, fixed at their 2015-19 values, do not follow them. The fitted hold after an adverse study result is at its
240-month upper bound in five of nine regions, which means no hold within the bound is long enough to bring those regions' 60-month withdrawal shares
down to the data (MISO 0.74 against 0.62); it only delays when a withdrawal is recorded.

Study times out of sample. MISO's lengthening from about 21 to 45 months, between the 2010 and 2019 cohorts, falls within the fitted
cohorts. For the
2020 and 2021 cohorts the model's median is 45 months against 51 and 48. Medians are censored at December 2025, so
the share signed by then is the cleaner test, and it misses: MISO's 2021 cohort is 62% signed in the model against
36% in the data, and ERCOT's 2020-23 cohorts 94%, 89%, 70% and 52% against 67%, 53%, 44% and 32%. The pooled fit
fits PJM poorly: 99% of its 2020 cohort signs in the model against 3% in the data, though only six PJM requests
from 2020 have an agreement date at all.

What follows for the result. The model underpredicts recent solar and storage additions, holds recent withdrawal
rates at their 2015-19 levels, and signs agreements faster than the 2020s queues did. The first makes current-law
additions too low; the other two work in opposite directions on how many requests reach a decision. The Sec.2106
effect is a difference from the same current-law run, which removes errors in the level but not errors in how
completion responds to cost and waiting, and section 4.3 shows that the regional result rests on fitted values that
are corners. The headline also comes from the variant that validates worse (0.51 against 0.42 by region). I use it
because the simpler model cannot represent Sec.2106; the simpler model's +8.0 GW for the permitting and court
provisions is the better-validated part of the result. The uncertainty intervals include none of this.

## 7. Comparison with published estimates

| study | model | bill text | headline | how interconnection is treated |
|---|---|---|---|---|
| This brief | queue model with operator and developer rules, plus permitting and courts | Senate-passed (19 Nov) | 6.7 GW new capacity by Nov 2041 if no RTO changes, 37.0 if all do (21.9 central); renewables and storage 5.9 to 27.8 GW; 0.0 GW by 2028 | Sec.2106 only in FERC-jurisdictional RTOs; whether each changes its process, and how strictly it screens, are assumptions |
| Rhodium Group (2 Nov 2026) | RHG-NEMS, capacity expansion | as introduced | 17 to 249 GW more clean capacity through 2040 across its high-, mid- and low-emissions scenarios (technology costs, fuel prices); mid case 56 GW | "we reduce barriers in the existing interconnection process" |
| Resources for the Future (Rennert and Bergman, 29 Oct 2026) | ReEDS, capacity expansion | as introduced | about 60 GW more clean capacity in 2028; transmission about 30% above baseline in 2041 | baseline interconnection limits removed in the policy cases; results reported as robust to that representation |
| SEIA (10 Nov 2026) | not retrieved | not stated | 167 GW more solar, 2028-35 | not retrieved |

Comparing the closest available quantities, this model's gain in clean capacity (new renewables and storage) by
November 2041 is 5.9 GW if no RTO changes its process and 27.8 GW if all do (16.9 GW in the central case), against
Rhodium's 17 to 249 GW through 2040. Rhodium's range spans technology costs and fuel prices and holds the bill's implementation fixed, so the overlap at its low end says little. Against RFF's figure for 2028, this model's gain by 2028 is
zero. The difference has five sources, and from the published material they cannot be separated.

1. Transmission. Rhodium projects 1.9 to 2.6 TW-miles of new interregional transmission a year under the bill, against 0.9 to 1.9
   in its baseline and 0.7 in 2015-24, and RFF's transmission is about 30% above baseline by 2041. Both let new lines
   carry new generation. This model makes transmission already in the queue faster and adds Sec.2109 hosting room,
   but does not plan new lines in response to the bill (Sec.2103 is not modelled). This is a limit of this model.
2. Permit certainty. RFF writes that "In the near term, the primary drivers are provisions intended to increase
   permitting certainty and consistency across administrations and provisions intended to speed the interconnection
   of new generation." I disagree on the second driver by 2028, given the statute's clock (point 4). In the simpler model here, Sec.1401 adds 0.3 to 0.7 GW of renewables.
   The difference is in the assumed baseline: RFF's current law includes executive actions that impede wind, which
   its policy cases remove; this model's current law has a residual risk of federal halts that Sec.1401 reduces.
   Rhodium did not model the permit-certainty provisions. It calls its results conservative because it also left out
   the geothermal, advanced-transmission-technology and VPP provisions; Sec.2109 alone adds about 4 GW here.
3. Interconnection. All three studies set the extent of interconnection relief by assumption: RFF removes its
   baseline limits, Rhodium reduces barriers by a chosen amount, and this model assumes which RTOs change their
   process and how strictly they screen. RFF reports that its results are robust to its interconnection
   representation, with the timing of the build-out shifting. Here, the interconnection assumptions are the largest source of uncertainty.
4. Scope and timing. The Senate-passed Sec.2106 reaches only RTOs/ISOs; both studies used the introduced text,
   which already excluded ERCOT but also covered the Southeast and most of the non-ISO West. Those two regions account for
   34% of current-law new capacity here (323 of 954 GW). The statute's own clock (rule in 18 months, filings two years from enactment)
   makes a large interconnection effect by 2028 unlikely, whatever the model.
5. Quantity. Rhodium and RFF run capacity-expansion models in which demand is met with and without the bill, so their
   figures are net changes in an installed fleet, with other capacity and retirements adjusting. This model counts
   gross additions that reach operation, with nothing displaced; gas rises too, by 5.0 GW in the central case.

Neither published study estimates the NEPA and court provisions separately, so they neither confirm nor contradict
the small effect found for them here. The Clean Air Task Force (12 Nov 2026) argues that Sec.1401's
national-security exception, and the absence of a bar on agencies seeking voluntary remand of issued
authorizations, leave near-term risk to permitted projects. That points the same way as the residual halt risk
assumed here, though the model's residual rests on a different exception, 1401(b)(1)(F) (action "taken pursuant to any
applicable law or regulation").

SEIA's 167 GW of additional solar between 2028 and 2035 compares with this model's gain of 10.8 GW in all
technologies by 2035 and 9.0 GW of solar by November 2041 (central case). SEIA's method page could not be retrieved, so the comparison stops at the figure.

## 8. Limits

The largest limit is that the Sec.2106 effect rests on three assumptions with no data behind them: whether each RTO's
process changes, what the single decision point removes (the current-law re-study round, section 4.5), and how the
non-refundable security and withdrawal penalties screen entry. The entry screen was also respecified after the first
results were seen (section 2). Reading the result as a range across those assumptions is safer than reading the
central number. MISO carries about three quarters of the Sec.2106 effect, and its gain depends on its fitted shortfall
of study capacity persisting to 2041.

The model plans no transmission. Sec.2103 (new interregional planning with cost allocation) is, in my reading, the
bill's main route to new lines, and both published studies credit the bill with more transmission. Upgrade
costs here rise with capacity signed and fall only as transmission already in the queue is finished and with Sec.2109's added hosting room, so the model
understates what the bill does if Sec.2103 works as intended.

Several fitted values are corners. Five developer value scales sit at the lower bound of their range, PJM's
completion runs through zero-cost draws that the data do not show (section 6), ERCOT storage
does not fit its completion rate, and the hold after an adverse study result is at its 240-month upper bound in five
regions. The NEPA EIS probabilities were refitted with the agents on, which ties the permitting side to the queue
side of the calibration. The backcast fails out of sample on withdrawal timing and on the share of requests signed
(section 6), and the uncertainty intervals do not include these errors.

Developers respond to upgrade costs, published waits and their region's projected shortfall, but not to prices,
tax credits or offtake contracts, so the model says nothing about how the bill interacts with federal tax credits or
power prices. Demand is NERC's 2025 forecast and does not respond to the bill;
Sec.2107(b) on data-center supply is outside the model. On-peak shares of wind, solar and batteries start at
NERC's national values and fall halfway to PJM's 2041/42 ELCC class ratings by 2041 (outside PJM, whose installed
margin already reflects falling accreditation); they do not respond to how much of each is built.

Requests already in the queue when the rule takes effect keep the current process, because the new s.228 has no
transition clause; if FERC moved them into the reformed process, the effect would come sooner. The rule month (three
years after enactment, range two to four) is an assumption.

Court parameters come from cases filed 2001-22, before *Seven County Infrastructure Coalition v. Eagle County*
(2025), in which the Supreme Court told lower courts to defer to agencies on the scope of NEPA review. The central
case assumes no change since. If challengers' NEPA remedies fall by 30-50% and suits by up to 40%, the court
provisions are worth 0.2 to 0.5 GW instead of 0.9 GW (`results/sim2_litigation.md`). Sec.1110(d) codifies part of
that holding, so part of what is credited to the bill here may already be current law.

The model's West region is treated as outside Sec.2106, but SPP's RTO expansion into the Western Interconnection
began operating in April 2026, so Sec.2106 would reach those utilities if SPP changes its process. The West's gain is
understated by that much.

The model does not estimate prices, emissions, customer bills or reliability events. The shortfall below NERC's
reference margin levels is a planning benchmark.

## 9. Reproducibility

```bash
pip install -r requirements.txt
```

```bash
python run.py --all --runs 100
```

```bash
python run.py --uncertainty 400
```

```bash
python run.py --decomposition --runs 100
```

```bash
python run.py --brief-figures
```

```bash
python -m pytest -q
```

`--all` recalibrates, runs the 2010-25 backcast and all seven simulations, and writes `results/*.md|json` and
`figures/`; `--decomposition` writes `results/sec2106_decomposition.md|json`, the breakdown of Sec.2106 in
sections 4.3 to 4.5. Runs are seeded, so the same commands reproduce the committed results. Every parameter is tagged in
`baaja/params.py` as data (with source) or assumption (with range). Raw downloads are not committed; extractors in
`data/` rebuild the JSON summaries from them, and `data/SOURCES.md` lists where each file comes from.

## References

Clean Air Task Force (2026, 12 November). Even after the manager's amendment, BAAJA's permitting certainty provisions
may not prevent near-term actions to stop clean energy projects.
https://www.catf.us/2026/11/even-after-managers-amendment-baajas-permitting-certainty-provisions-may-not-prevent-near-term-actions-stop-clean-energy-projects/

Federal Energy Regulatory Commission (2023, 28 July). Improvements to Generator Interconnection Procedures and
Agreements, Order No. 2023. 184 FERC ¶ 61,054.

Grimm, V., Revilla, E., Berger, U., Jeltsch, F., Mooij, W.M., Railsback, S.F., Thulke, H.-H., Weiner, J.,
Wiegand, T. and DeAngelis, D.L. (2005). Pattern-oriented modeling of agent-based complex systems: lessons from
ecology. *Science* 310(5750): 987-991. https://doi.org/10.1126/science.1116681

Grimm, V., Railsback, S.F., Vincenot, C.E., Berger, U., Gallagher, C., DeAngelis, D.L., Edmonds, B., Ge, J.,
Giske, J., Groeneveld, J., Johnston, A.S.A., Milles, A., Nabe-Nielsen, J., Polhill, J.G., Radchuk, V.,
Rohwäder, M.-S., Stillman, R.A., Thiele, J.C. and Ayllón, D. (2020). The ODD protocol for describing agent-based and
other simulation models: a second update to improve clarity, replication, and structural realism. *Journal of
Artificial Societies and Social Simulation* 23(2): 7. https://doi.org/10.18564/jasss.4259

Johnston, S., Liu, Y. and Yang, C. (2023, revised November 2026). An empirical analysis of the interconnection
queue. NBER Working Paper 31946. https://doi.org/10.3386/w31946

King, B., Bower, G., Case, R., Kolus, H., Larsen, J., Pastorek, N. and Wiens, M. (2026, 2 November). Estimating
the US energy system impacts of the Bipartisan American Affordability and Jobs Act. Rhodium Group.
https://rhg.com/research/baaja-us-energy-system-impacts/

North American Electric Reliability Corporation (2026). *2025 Long-Term Reliability Assessment* (January 2026,
errata February 2026). Atlanta: NERC.
https://www.nerc.com/pa/RAPA/ra/Reliability%20Assessments%20DL/NERC_LTRA_2025.pdf

PJM Interconnection (2026, 30 October). *2026 PJM Effective Load Carrying Capability and Reserve Requirement Study
(ELCC/RRS)*; and preliminary ELCC class ratings for delivery years 2028/29-2041/42.
https://www.pjm.com/planning/resource-adequacy-planning/effective-load-carrying-capability

Rand, J., Cheyette, A., Gorman, W., Wiser, R., Seel, J., Kahrl, F., Talley, C. and Zhang, S. (2026, May).
*Interconnection Queue Dataset and Summarized Data Files, through 2025.* Berkeley, CA: Lawrence Berkeley National
Laboratory, with Interconnection.fyi. https://emp.lbl.gov/queues

Rennert, K. and Bergman, A. (2026, 29 October). Projected effects of the Bipartisan American Affordability and Jobs
Act on the power sector. Resources for the Future issue brief.
https://www.rff.org/publications/issue-briefs/projected-effects-of-the-bipartisan-american-affordability-and-jobs-act-on-the-power-sector/

Saltelli, A., Ratto, M., Andres, T., Campolongo, F., Cariboni, J., Gatelli, D., Saisana, M. and Tarantola, S.
(2008). *Global Sensitivity Analysis: The Primer.* Chichester: Wiley. https://doi.org/10.1002/9780470725184

SEIA statement of 10 November 2026, as reported by Ludt, B. (2026, 10 November), Senate advances federal energy
permitting bill, *Solar Power World*,
https://www.solarpowerworldonline.com/2026/11/senate-advances-federal-energy-permitting-bill/ ; Willis, B. (2026,
10 November), US permitting bill moves forward as opposition grows, *PV Tech*,
https://www.pv-tech.org/us-permitting-bill-moves-ahead-environment-opposition-grows/ ; and Bhambhani, A. (2026,
20 November), US BAAJA permitting bill could unlock 167 GW of solar, *TaiyangNews*,
https://taiyangnews.info/markets/us-baaja-permitting-bill-could-unlock-167-gw-solar

U.S. Senate (2026). Amendment No. 6883 to H.R. 2347 (floor copy KAT26804 V62), as passed 19 November 2026; and
engrossed Senate amendment, BILLS-119hr2347eas, GovInfo.
https://www.govinfo.gov/content/pkg/BILLS-119hr2347eas/html/BILLS-119hr2347eas.htm

Windrum, P., Fagiolo, G. and Moneta, A. (2007). Empirical validation of agent-based models: alternatives and
prospects. *Journal of Artificial Societies and Social Simulation* 10(2): 8. https://www.jasss.org/10/2/8.html
