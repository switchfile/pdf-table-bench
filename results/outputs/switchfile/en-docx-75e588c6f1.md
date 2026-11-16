<!-- page 1 -->

# Text S2 Supporting figures tables and inspection sensitivity

Supplement to Risk-Calibrated Position Acceptance of Robot-Placed Lines through Mission- Aware Kriging

Ramadan Mazrekaj

This file contains supporting content relocated from the manuscript to meet the submission length limit. It complements the existing Text S1 and Data S1 and does not replace either file. All results and data are retained as reported in the source manuscript. Figures S17–S21 and Tables S19–S22 continue the numbering used in Text S1.

Table S19. Capabilities of related approaches and of this study for the acceptance of robotplaced geometric work

| Approach (representative work) | Explicit knowledge representation | Measuremen t uncertainty | Spatial correlation | Machine log fused with checks | Calibrate d decision risk | Robot mechanisms |
| --- | --- | --- | --- | --- | --- | --- |
| Rule-based | Yes | – | – | – | – | – |
| compliance |  |  |  |  |  |  |
| checking |  |  |  |  |  |  |
| (Eastman et |  |  |  |  |  |  |
| al. 2009; Zhong |  |  |  |  |  |  |
| et al. 2012) |  |  |  |  |  |  |
| Semantic | Yes | – | – | – | – | – |

and SHACL

checking (Soman

et al. 2020;

Hagedorn et

al. 2023)

<!-- page 2 -->

| Approach<br>(representative<br>work) | Explicit<br>knowledge<br>representation | Measuremen<br>t uncertainty | Spatial<br>correlation | Machine<br>log fused<br>with checks | Calibrate<br>d decision risk | Robot<br>mechanisms |
| --- | --- | --- | --- | --- | --- | --- |
| Scan-versus-<br>design<br>dimensional<br>control (Bosché<br>2010; Kim et<br>al. 2015) | Partial | Partial | – | – | – | – |
| Intelligent<br>compaction<br>specifications<br>(FHWA 2017) | – | Partial | Partial | Partial | – | – |
| Acceptance<br>sampling and<br>conformity (ISO<br>2022; JCGM<br>2012) | – | Yes | – | – | Yes | – |
| Kriging-<br>based excursion<br>estimation (Bect<br>et al. 2012;<br>Chevalier et<br>al. 2014) | – | Yes | Yes | – | Partial | – |
| Robot<br>accuracy<br>evaluations<br>(Brosque and<br>Fischer 2022b;<br>Mazrekaj 2026) | – | Partial | – | – | – | Partial |
| This study | Yes | Yes | Yes | Yes | Yes | Yes |

<!-- page 3 -->

Note: – = not addressed in the cited representative works, which does not mean that an approach could not be extended. Coverage of capabilities does not by itself demonstrate methodological novelty; the contribution of the mission covariance is tested by the paired kernel ablation in the Results.

![Image 1]()

Fig. S17. Robot Acceptance Knowledge (RAK) ontology and its alignment with PROV-O, SOSA, and QUDT.

<!-- page 4 -->

![Image 2]()

Fig. S18. Computational pipeline of the acceptance engine and its knowledge graph.

![Image 3]()

Fig. S19. Operating envelope from the closed-loop model: (a) violating 15-m windows by speed, tool lever, and route geometry; and (b) position risk against speed.

![Image 4]()

Fig. S20. Probability of acceptance against the true nonconforming fraction on (a) a straight route, (b) a 15-m radius, and (c) the closed loop with a 0.5-m lever.

<!-- page 5 -->

![Image 5]()

Fig. S21. Closed-loop simulation of a differential-drive marking robot: (a) distributions of the logged residual, positioning error, and true deviation; and (b) their correlation structure.

Table S20. Consumer and producer risks (CR/PR) of acceptance rules under misspecification and non-Gaussian errors ( mm; interior lots of 50 runs of 10 km per scenario)

Variables, 20 Log + 3,

Scenario points constant offset Log + 3, kriging Log + 5, kriging

| Baseline, model correct | 0.08/0.17 | 0.20/0.13 | 0.19/0.08 | 0.15/0.06 |
| --- | --- | --- | --- | --- |
| Assumed = 50 m (true 100 m) | 0.09/0.17 | 0.12/0.23 | 0.13/0.14 | 0.10/0.10 |
| Assumed = 200 m (true 100 m) | 0.09/0.17 | 0.26/0.08 | 0.27/0.05 | 0.22/0.04 |
| True = 30 m (assumed 100 m) | 0.11/0.26 | 0.52/0.11 | 0.50/0.07 | 0.46/0.04 |
| Assumed = 6 mm (true 8 mm) | 0.08/0.17 | 0.28/0.08 | 0.29/0.04 | 0.25/0.03 |
| Heavy-tailed residual () | 0.09/0.17 | 0.20/0.12 | 0.19/0.08 | 0.13/0.06 |
| RTK float episodes, flagged | 0.08/0.16 | 0.19/0.16 | 0.17/0.10 | 0.15/0.08 |
| RTK float | 0.09/0.17 | 0.24/0.13 | 0.24/0.08 | 0.19/0.07 |

<!-- page 6 -->

Variables, 20 Log + 3,

Scenario points constant offset Log + 3, kriging Log + 5, kriging

episodes, not flagged

| Baseline of second runa | 0.09/0.18 | 0.21/0.13 | 0.19/0.09 | 0.16/0.06 |
| --- | --- | --- | --- | --- |
| Random-walk drift, reset every kma | 0.04/0.21 | 0.11/0.16 | 0.10/0.13 | 0.08/0.09 |
| Multipath regimes, 20% of routea | 0.05/0.18 | 0.22/0.14 | 0.18/0.10 | 0.14/0.07 |
| Smooth (second- order) positioning errora | 0.09/0.19 | 0.32/0.12 | 0.28/0.07 | 0.19/0.05 |
| Log time offset 0.1 s a | 0.08/0.16 | 0.20/0.14 | 0.20/0.10 | 0.16/0.07 |
| Log time offset 0.3 s a | 0.08/0.16 | 0.22/0.16 | 0.20/0.11 | 0.16/0.08 |
| Spray-fan smoothing, 0.3 ma | 0.10/0.17 | 0.20/0.14 | 0.20/0.09 | 0.15/0.08 |

Note:aScenarios outside the Gauss–Markov family and log imperfections, from a simulation run (50 runs of 10 km); fixed default thresholds throughout; the first and last

separate lot of each run are excluded.

## Inspection spacing and measurement noise

In this realization, the three accepted violating lots are explained by measurement noise rather than by the sampling interval (Table S15). Windows of 15 m lie entirely within a lot, 850 at the 0.1-m grid and 170 at the 0.5-m spacing. The noiseless violating fractions of the three lots were 5.1–6.2% at 0.1 m and 5.3–5.9% at 0.5 m, both above the 5% limit, whereas the noisy offsets gave 2.9–3.5%; small exceedances can be cancelled by 1-mm errors. The miss count is, however, not a stable property of the procedure (Table S17): with another realization of the 1- mm noise, 7 of the 91 violating lots were accepted; with a noiseless survey at 0.5 m, 12 were accepted, because the 0.5-m spacing misses short exceedances that define a violation at 0.1 m; and survey errors of 2 and 3 mm reduced the misses to 1 and 0 but rejected 832 and 2,554 conforming lots. Measurement noise inflates window ranges and thus trades missed violations for false rejections, so a verification rule must define the alignment requirement at the spacing and precision of the inspection it uses. Over the 3,955 position-accepted lots, coarsening from 0.1 to 0.5 m changed the classification of 13 lots, whereas the measurement noise changed 124 (121 from conforming to violating, which explains most of the 107 conforming lots rejected by the survey). The screen sent 3,337 of the 3,955 position-accepted lots to the survey and reduced the number of simulated survey offsets by only 16% compared with surveying every lot; this is a count of simulated measurements, not a measured saving of time or cost. That no violating lot remained unsurveyed at mm is an observation in this simulation, not a general guarantee for lots that are accepted without a survey.

<!-- page 7 -->

Table S21. Risks of acceptance rules for 100-m lots ( mm, mm, zero bias; 9,800 interior lots of 100 runs, of which 2,432 nonconforming)

| Rule | lot New points per | Consumer risk | Producer risk | PR@CR10 |
| --- | --- | --- | --- | --- |
| Attribute, all | 5 | 0.447 | 0.097 | 0.449 |
| points within tolerance |  |  |  |  |
| Attribute, all | 20 | 0.049 | 0.325 | 0.239 |

points within tolerance

<!-- page 8 -->

| Rule | lot New points per | Consumer risk | Producer risk | PR@CR10 |
| --- | --- | --- | --- | --- |
| Variables, | 20 | 0.079 | 0.162 | 0.135 |
| estimated |  |  |  |  |
| Log + checks, | 3 | 0.015 | 0.695 | – |
| guard band |  |  |  |  |
| Log + checks, | 3 | 0.187 | 0.132 | 0.246 |
| constant offset |  |  |  |  |
| Log + checks, | 3 | 0.176 | 0.078 | 0.138 |
| kriging |  |  |  |  |
| Log + checks, | 5 | 0.145 | 0.064 | 0.097 |

kriging

Note: PR@CR10 = producer risk at a matched consumer risk of 10%. For the kriging rules the checks of the two neighboring lots also enter each decision ( measurements). Run-clustered standard errors are at most 0.011 for consumer risk, 0.006 for producer risk, and 0.016 for PR@CR10.

Table S22. Complete alignment procedure on 4,900 interior lots of an improved robot (50 independent closed-loop runs of 10 km, first and last lot of each run excluded; 119 lots violating the alignment target, 91 of them accepted on position, 3,955 lots accepted on position)

Violating lots finally

accepted

|  | A: |  |  | [binomial | Conformi | Survey |
| --- | --- | --- | --- | --- | --- | --- |
| Margin | accepted on | B: | Violating | reference | ng lots | offsets (% of |
| (mm) | screen | surveyed | lots left in A | interval] | rejected | all) |
| 0 | 3,858 | 97 | 75 | 75 | 11 | 19,400 |

(82.4%) [73.0,

<!-- page 9 -->

Violating

lots finally accepted

|  | A: |  |  | [binomial | Conformi | Survey |
| --- | --- | --- | --- | --- | --- | --- |
| Margin | accepted on | B: | Violating | reference | ng lots | offsets (% of |
| (mm) | screen | surveyed | lots left in A | interval] | rejected | all) |
|  |  |  |  | 89.6] |  | (2%) |
| 2 | 3,442 | 513 | 57 | 59 | 31 | 102,600 |
|  |  |  |  | (64.8%) [54.1, |  | (13%) |
|  |  |  |  | 74.6] |  |  |
| 4 | 2,244 | 1,711 | 19 | 22 | 76 | 342,200 |
|  |  |  |  | (24.2%) [15.8, |  | (43%) |
|  |  |  |  | 34.3] |  |  |
| 6 | 618 | 3,337 | 0 | 3 (3.3%) | 107 | 667,400 |
|  |  |  |  | [0.7, 9.3] |  | (84%) |
| 8 | 31 | 3,924 | 0 | 3 (3.3%) | 110 | 784,800 |
|  |  |  |  | [0.7, 9.3] |  | (99%) |

Note: Outcome B lots are decided by a synthetic dense offset survey (offsets to the design alignment every 0.5 m, independent error of 1 mm standard deviation); percentages refer to the 91 violating lots accepted on position; the binomial reference interval assumes independent lots; surveying all position-accepted lots needs 791,000 offsets.

## Additional detailed results and validation design

The following passages retain details condensed in the final manuscript. Figure and table numbers in these passages refer to the final main manuscript and its supplements.

The research questions concern computable and traceable acceptance (RQ1), clausedependent error budgets and mission effects (RQ2), and risk-calibrated fusion of logs and checks with a separate alignment decision (RQ3).

<!-- page 10 -->

The central contribution is a mission-aware, traceable procedure for statistical position acceptance of robot-placed lines that fuses the dense log with sparse independent checks. It rests on a mission-dependent covariance used for kriging, analytical error budgets for position and window-range clauses, plans calibrated with a distribution-free bound and evaluated on independent lots, and a knowledge model constrained by the Shapes Constraint Language (SHACL) and aligned with the PROV-O, SOSA, and QUDT ontologies. Ordinary kriging, SHACL, and distribution-free calibration are established methods; the contribution lies in their integration and in the mission covariance, whose value is tested by a paired ablation. Fig. 1 summarizes the framework.

On 196,000 interior lots (20 cells of 100 runs of 10 km; Table S21 shows the cell mm, zero bias; Table S14 maps all samples), five-point attribute checks, which resemble current spot checks, accepted 44.7% of nonconforming lots at mm. Compared at a matched consumer risk of 10%, kriging with three new checks per lot had a producer risk indistinguishable from that of a 20-point variables survey (0.138 against 0.135) and 0.097 with five checks; standard errors from a bootstrap over whole runs were 0.008–0.009 (Table S21). With thresholds calibrated on 4,000 independent lots and tested on 4,000 others in five scenarios, the realized consumer risks were 3.3–6.7% (Table 2, Fig. 5). Five new checks per lot with the log had a lower producer risk than the 20-point survey in four scenarios, for example 16.2% against 24.8% on a straight route and 21.1% against 36.4% in the exact closed loop with a 0.5-m lever. On the 15-m radius, the paired difference over 2,780 conforming lots was −0.5 percentage points (95% interval −2.5 to 1.5), so no significant difference was detected, which does not establish equivalence. The additional contribution of the geometry-aware covariance was isolated by a paired ablation with identical measurements, three new checks per lot, and separately calibrated thresholds, in which only the kernel differed: a stationary straight-route kernel against the geometry-aware kernel of Eq. (5). At closely matched consumer risks (differences of at most 0.5 percentage points), the producer risk fell from 44.1% to 40.6% on the 50-m radius (paired difference 3.5 percentage points, 95% interval 2.6–4.5) and from 75.3% to 55.0% on the 15-m radius (20.3, 95% interval 18.4–22.2); on straight routes the two kernels coincide and the risks were identical. Under the tested curvedroute scenarios, the ablation thus isolates the additional reduction in producer risk attributable to the geometry-aware covariance, which grows with curvature; it does not by itself explain every difference between the integrated method and other methods.

<!-- page 11 -->

Selection and evaluation of plans used independent three-lot replicates in which only the central lot is counted, with separate selection lots (4,800 per candidate ) and evaluation lots (4,800), so that the conditions of Proposition 4 hold (Table 3, Fig. 6a). Without a margin, the evaluated consumer risks of the selected plans were 0.082–0.117, and for the floor-layout specification the target was exceeded (0.117, 95% interval 0.095–0.143). With thresholds selected under a DKW margin shared by the four candidate plans, the evaluated consumer risks were 0.019–0.072, all upper confidence limits below 0.10, at the price of producer risks of 0.126–0.286; for the analyzed parameters and the strict-alignment variant no candidate met the producer-risk target of 0.15 with the margin, and the engine flagged them as infeasible. In 12 end-to-end replicates, and were identified by maximum likelihood from ten 500-m control-line passes, a plan was synthesized with the lower bound of , and it was applied to 1,960 new interior lots with a random bias. With a correct Gauss–Markov model, the realized consumer risk was 0.028–0.077 (median 0.040); with a smooth second-order truth analyzed with the first-order model, it exceeded the target in 5 of 12 replicates (maximum 0.124). The covariance family, not only its parameters, must be identified.

<!-- page 12 -->

In all alignment results, as in the discrimination study, the first and last lot of each run are excluded, because with a single kriging neighbor they would need their own calibration. The margin was selected on the 490 interior lots of a development run (five closed-loop runs of 10 km, seed 2027) by a stated rule, the smallest margin that leaves at most one of the 12 development violations unflagged, which gave mm (Table S16). All margins were evaluated on the 4,900 interior lots of 50 further independent runs with separate seeds (38 and 380), not used for the selection. Of these, 119 lots violated the alignment target and 91 passed the position test (Table S22, Fig. 6b). Without a margin, the screen left 75 of the 91 in outcome A. With mm, all 91 were flagged, and the complete procedure accepted 3 of 91 (3.3%). The binomial reference interval assuming independent lots is 0.7–9.3%. The lots are, however, clustered in 41 runs; as sensitivity analyses, a design-effect adjustment (design effect 1.00, estimated from only three events) leaves it unchanged, and a percentile bootstrap over whole runs (2,000 replicates of the pooled ratio) gives 0.0–8.1%. Three misses observed in 91 relevant lots do not provide a sufficient basis to claim a miss rate below 10% with 95% confidence.

What a field campaign must supply is site-specific input, and the method places field data where they are most informative. The covariance family, the failure mode of Table S20, was selected correctly by likelihood from control-line passes in all 60 replicates for each family, already with five passes of 500 m (lower 95% bound 0.94; Table S18), and ten passes bound within 73–132 m. Demonstrating the consumer risk directly on field lots is, by contrast, impractical: showing a risk below 0.10 with 95% confidence and 80% power when the true risk is 0.05 needs about 180 independent nonconforming lots, roughly 700 lots at the nonconforming share of the simulations. As in acceptance sampling by variables, the risk is therefore calibrated on the identified model, and the field check is a predictive check of that model: about 125 heldout survey points detect a drop of the 95% prediction-interval coverage to 90%.

<!-- page 13 -->
