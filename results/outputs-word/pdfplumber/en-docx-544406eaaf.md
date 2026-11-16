Valuing the Unvalued: A Bibliometric Mapping of
Venture Capital, Private Equity, and Early-Stage
Venture Valuation Research
Alfath Ilmi Effendy Atthariq Arsyan Wahyudi Danang Prihandoko
Business Management Department, Management Department Business Management Department,
BBS Undergraduate Program BBS Undergraduate Program BBS Undergraduate Program
Bina Nusantara University Bina Nusantara University Bina Nusantara University
Bekasi, Indonesia Bekasi, Indonesia Bekasi, Indonesia
Alfath.effendy@binus.ac.id atthariq.wahyudi@binus.ac.id dprihandoko@binus.ac.id
Abstract— Early-stage ventures are difficult to value derived from observed VC transactions [3], and models that
because they lack stable revenues, financial histories, and reconcile entry valuations with exit multiples [6].
reliable market benchmarks, which makes venture valuation
a central concern in venture capital (VC), private equity (PE), Valuation in practice is not purely numerical. Investors
and entrepreneurial finance research. This study maps recent interpret signals from ventures, and their perceptions of those
scholarship on these topics through a bibliometric keyword signals differ across early financing stages [7]. VC investors,
co-occurrence analysis. Bibliographic records were retrieved for example, tend to treat innovation as central to their
from Scopus and screened by publication year (2021–2026), investment criteria and to rely on qualitative indicators,
language (English), and document type (journal article), whereas PE investors view it as one component among
which resulted in 150 articles. Author keywords were broader financial considerations [8]. At the same time, the
analyzed in VOSviewer using full counting and a minimum financing environment has widened. Recent studies address
occurrence threshold of three. The resulting network equity and lending crowdfunding [9], [10], the sources of
comprises 23 keywords in nine clusters. Venture capital and finance used by technology start-ups over their life cycle [11],
private equity occupy the central positions and connect the effects of exogenous crises on entrepreneurial finance
clusters on entrepreneurship and innovation, entrepreneurial [12], and the role of environmental, social, and governance
finance and ESG, crowdfunding and machine learning, and (ESG) and impact considerations in VC and PE investment
initial public offerings. The overlay visualization shows that [13], [14], [15]. Machine-learning models have also been
investment decision-making, sustainable finance, and fintech proposed to support start-up selection and exit prediction
are among the more recent topics, whereas emerging markets, [16]. Early-stage venture valuation thus sits at the intersection
performance measurement, crowdfunding, and impact of financial models, investor judgment, and a growing set of
investing appeared earlier. Valuation enters the network only financing channels.
through the keyword fair value, even though more than ten
valuation-related keywords appear in the dataset, which
Several bibliometric reviews have mapped parts of this
suggests that valuation research is fragmented in authors’
field. Cumming et al. [2] and Kumar et al. [1] analyzed VC
keyword choices. The study contributes a current, Scopus-
and PE research using Web of Science, Capizzi et al. [17]
based map of VC and PE research and indicates where
reviewed the journal Venture Capital, and Silva Júnior et al.
valuation needs clearer conceptual labeling.
[18] traced the evolution of start-up investments in a Scopus
corpus of 1,984 articles. Among the bibliometric reviews
Keywords—Venture Capital, Private Equity,
identified in our dataset, none analyzes recent Scopus-
Entrepreneurial Finance, Bibliometric Analysis, VOSviewer
indexed journal articles through a keyword co-occurrence
I. INTRODUCTION map that centers on early-stage venture valuation and
entrepreneurial finance. It therefore remains unclear which
topics currently anchor the field, how they relate to one
Venture capital (VC) and private equity (PE) play a
another, and which have emerged most recently.
pivotal role in nurturing newly established and growth-
oriented firms [1], and both fields have grown into a
heterogeneous set of research themes [2]. In early-stage This study addresses that gap through a keyword co-
financing, however, assigning a value to the venture is occurrence analysis of journal articles indexed in Scopus
difficult. The valuation of start-up firms is challenging yet between 2021 and 2026. It is guided by three research
highly relevant to entrepreneurs and financiers alike [3], and questions. RQ1: What are the most prominent author
high failure rates, long payback periods, and information keywords and thematic clusters in recent VC and PE
asymmetries are associated with conservative pricing and research? RQ2: How are valuation and entrepreneurial
valuation discounts [4]. The literature therefore draws on finance positioned within the keyword network? RQ3: Which
several approaches, including the venture capitalist method topics have emerged most recently? The study contributes a
and discounted cash flow analysis [5], fair-value multiples current, Scopus-based map of the field and a replicable
procedure for search, screening, and keyword analysis. The
XXX-X-XXXX-XXXX-X/XX/$XX.00 ©20XX IEEE

remainder of this paper reviews the related literature, start-ups choose sources of finance over their life cycle, and
describes the research method, presents and discusses the Kraemer-Eis et al. [12] examine the effect of the Russian war
results, and concludes. against Ukraine, treated as an unexpected exogenous crisis,
on entrepreneurial finance in Europe.
Sustainability and data-driven methods form two further
II. LITERATURE REVIEW strands. Drobetz et al. [13] find that PE and VC backing
increases the externally validated ESG scores of small and
A. Venture Capital and Private Equity as Entrepreneurial
medium-sized enterprises, Lange and Banadaki [14]
Finance
interview VC investors about the drivers, strategies, and
Cumming et al. [2] describe VC and PE as fields rooted in barriers of ESG consideration, and Barber et al. [15] show that
financing research on capital budgeting and initial public investors accept lower returns in dual-objective impact VC
offerings (IPOs). In their review, foundational VC themes funds. Ross et al. [16] develop a machine-learning model that
include adoption and financing processes, the roles of VC in predicts start-up exit outcomes with out-of-sample accuracy
business, governance, and syndication, whereas PE research of 80–89%.
emphasizes style drift into VC, buyouts and privatization, and
D. Bibliometric Analysis and Research Gap
valuation and performance. The boundary between the two is
increasingly porous. Cumming and Dai [19] show that non- Bibliometric analysis quantifies publication patterns and
VC private equity funds invest in entrepreneurial firms, prefer reveals the intellectual structure of a field. In the VC and PE
expansion and late-stage ventures, and are associated with domain, Cumming et al. [2] mapped geographical focus,
larger investments and higher valuations. For this reason, VC methodological choices, and themes using Web of Science
and PE are treated in this study as related but distinct concepts records. Kumar et al. [1] visualized two decades of PE and
and are not merged in the keyword analysis. Silva Júnior et VC articles and found that VC research is more frequent than
al. [18] further show that research on start-up investment PE research. Capizzi et al. [17] analyzed 385 documents
moved from VC and bootstrapping in the 1990s to angel published in the journal Venture Capital between 1999 and
investment, corporate venture capital, and innovation in the 2021 and highlighted themes such as crowdfunding,
following decade, and more recently to crowdfunding, PE, government venture capital, and market failure. Silva Júnior
accelerators, and data-driven technologies. et al. [18] combined VOSviewer and SciMAT to examine
1,984 Scopus articles on start-up investment.
B. Early-Stage Venture Valuation
These reviews differ in database, scope, and period.
Valuation approaches in the literature range from classical Among those identified in our dataset, none analyzes Scopus-
to market-based and hybrid. Peswani [5] uses a teaching case indexed journal articles from 2021 to 2026 through a keyword
to show how the venture capitalist approach and the co-occurrence map that centers on early-stage venture
discounted cash flow method are applied to a start-up, and valuation and entrepreneurial finance. This gap motivates the
how external and internal factors complicate the exercise. present study.
Barg et al. [3] reverse-engineer fair-value multiples by
comparing firm value at financing with firm value at exit, and III. RESEARCH METHOD
report that multiples are higher when more experienced
A. Research Design
investors are involved and when exit occurs through an IPO
rather than a merger or acquisition, and lower in later-stage This study uses bibliometric analysis, combining
rounds and larger investment consortia. Kang and Ryu [6] performance description with science mapping, to examine
propose a model that integrates growth dynamics and exit research on VC and PE with attention to early-stage venture
multiples to resolve inconsistencies between present valuation and entrepreneurial finance. Keyword co-
valuations and terminal values, with particular relevance for occurrence analysis was selected because it reveals the
VC and PE. thematic structure of a field from the terms that authors use to
Other studies examine what shapes value in practice. describe their own work. The analysis was carried out in
Nazir and Tbaishat [20] apply causal-impact methods to VOSviewer.
7,481 early-stage technology start-ups in the United Arab
B. Data Source and Search Strategy
Emirates to assess how funding relates to market valuation.
Bibliographic data were retrieved from Scopus, a curated
Giakoumelou et al. [4], drawing on contingency, innovation,
database that provides structured records including titles,
and signaling theories, examine the “patent premium” that PE
abstracts, author keywords, and citation information. The
investors pay for Italian start-ups in the growth and expansion
search was conducted on 13 October 2026 in the title,
stages. Information outside financial statements also matters:
abstract, and keyword fields using the following query:
Zheng et al. [7] find that angel investors extract and combine
“private equity and venture capital”.
different signals when reaching a financing decision, and Aas
et al. [8] show that VC, PE, and equity fund investors evaluate C. Screening Procedure
innovation capabilities differently.
The initial search returned 1,042 documents. Three filters
C. Financing Channels, Sustainability, and Data-Driven were then applied in sequence. Restricting the publication
Investing period to 2021–2026 reduced the set to 341 documents,
limiting the language to English left 329, and restricting the
Entrepreneurial finance has expanded beyond traditional
document type to journal articles left 150. These 150 articles
VC. Fricke et al. [9] study accredited crowdfunding under the
constitute the final dataset. Table I summarizes the procedure.
U.S. JOBS Act and find no support for a lemons market, while
Porro et al. [10] use machine learning to predict investor Table I. Article Selection Process

| Step | Filter Applied | Records |
|---|---|---|

dynamics in equity and lending crowdfunding campaigns in
Italy. Singh and Hillemane [11] analyze how technology


| 1 | Initial Scopus Search | 1,042 |
|---|---|---|
| 2 | Publication Year 2021-2026 | 341 |
| 3 | Language: English | 329 |
| 4 | Document Type: Journal Article | 150 |

No thesaurus file was applied, so keywords were analyzed
as recorded by the authors. VOSviewer treats keywords that
differ only in letter case as identical, but spelling variants,
abbreviations, and singular and plural forms remain separate
items (for example, “ipo” and “initial public offerings”). This
choice keeps the authors’ original terminology, but it also
means that some themes are split across several nodes, as
discussed in Section IV-D.
E. Visualization
D. Data Analysis Three VOSviewer visualizations were produced. In the
The selected records were exported from Scopus in CSV network visualization, nodes represent keywords, node size
format and analyzed in VOSviewer. A co-occurrence analysis reflects the number of occurrences, links represent co-
was performed on author keywords using the full counting occurrence, and colors indicate clusters. The overlay
method, in which every keyword of a record receives full visualization colors each keyword by the average publication
weight in each co-occurrence link. Of the exported records, year of the articles in which it appears, which makes the
124 contained author keywords, yielding 473 distinct relative recency of topics visible. The density visualization
keywords. Because most keywords appear in only one article, highlights the areas where keywords and links are
the minimum number of occurrences of a keyword was set to concentrated.
three, and 23 keywords met this threshold.
IV. RESULTS AND DISCUSSION
A. Keyword Co-occurrence Network
Fig. 1. Network visualization of keyword co-occurrence.

| esg | 4 | 2023.75 | Red |
|---|---|---|---|
| fintech | 4 | 2024.00 | Yellow |
| machine learning | 4 | 2023.50 | Purple |
| sustainable finance | 4 | 2024.25 | Red |
| corporate governance | 3 | 2023.33 | Green |
| crowdfunding | 3 | 2022.67 | Purple |
| emerging markets | 3 | 2021.33 | Blue |
| fair value | 3 | 2023.00 | Green |
| fundraising | 3 | 2023.67 | Cyan |
| impact investing | 3 | 2022.67 | Orange |
| initial public offerings | 3 | 2023.33 | Brown |
| investment decision- making | 3 | 2024.67 | Red |
| investments | 3 | 2024.67 | Cyan |
| performance | 3 | 2023.33 | Red |

Fig. 1 shows the network of the 23 author keywords that
met the threshold. The keywords form nine clusters,
distinguished by color in the figure. Table II lists each
keyword with its number of occurrences, its average
publication year, and its cluster.
Table II. Keywords Meeting the Minimum Occurrence Threshold of Three

| Keyword | Occurrences | Avg. year | Cluster |
|---|---|---|---|
| private equity | 65 | 2023.23 | Blue |
| venture capital | 60 | 2023.43 | Yellow |
| entrepreneurial finance | 8 | 2023.62 | Red |
| entrepreneurship | 7 | 2023.43 | Green |
| innovation | 6 | 2023.67 | Green |
| ipo | 6 | 2023.50 | Pink |
| g24 | 5 | 2025.40 | Red |



| performance measurement* | 3 | 2021.00 | Blue |
|---|---|---|---|
| start-ups | 3 | 2023.67 | Green |

(investment banking, venture capital, brokerage, and ratings)
rather than a topic, so it is not interpreted substantively. The
green cluster (entrepreneurship, innovation, start-ups,
Venture capital and private equity are by far the largest corporate governance, and fair value) represents the
nodes, with 60 and 65 occurrences, and they appear together entrepreneurial side of the field, and fair value is the only
in 48 of the 124 articles that report author keywords. Both are valuation-related keyword in it. The blue cluster links private
linked to most of the other keywords in the network, which equity to emerging markets and performance measurement,
confirms them as the core concepts of the dataset. and the yellow cluster links venture capital to fintech. The
The red cluster is the largest, with six keywords: cyan cluster (investments and fundraising) concerns the
entrepreneurial finance, ESG, sustainable finance, investment raising and deployment of capital, and the purple cluster
decision-making, performance, and g24. It connects the (crowdfunding and machine learning) concerns alternative
financing of entrepreneurial firms with sustainability financing channels and data-driven methods. Three single-
considerations and investment decisions. The keyword g24 is keyword clusters correspond to impact investing, ipo, and
a Journal of Economic Literature (JEL) classification code initial public offerings.
B. Overlay Visualization
Fig. 2. Overlay visualization of keywords by average publication year.
Fig. 2 colors the keywords by their average publication 2022.67) and fair value (2023.00). The most recent topics are
year. Venture capital and private equity are centered around fintech (2024.00), sustainable finance (2024.25), and
2023, which indicates that they are present throughout the investment decision-making and investments (both 2024.67).
period. Among the earlier topics are performance The keyword g24 has the highest average year (2025.40), but
measurement (2021.00) and emerging markets (2021.33), as a classification code it does not represent a topic.
followed by crowdfunding and impact investing (both

C. Density Visualization
Fig. 3. Density visualization of keyword occurrences.
Fig. 3 shows that the densest area is formed by venture flow, and exit multiples, most of which appear once. By
capital and private equity, which reflects both their frequency comparison, the word valuation appears in the title or abstract
and their many links. Areas of moderate density appear of 21 of the records. This gap shows that author keywords
around the green cluster (entrepreneurship, innovation, start- underrepresent valuation research and spread it across many
ups, and fair value), around entrepreneurial finance, ESG, and low-frequency terms.
investment decision-making, and around crowdfunding, Regarding RQ3, the most recent topics are investment
machine learning, ipo, and fintech. Keywords such as decision-making, investments, sustainable finance, and
emerging markets, performance measurement, impact fintech, whereas performance measurement, emerging
investing, and initial public offerings lie in low-density areas, markets, crowdfunding, and impact investing are associated
which is consistent with their lower frequencies and fewer with earlier years. This pattern suggests a shift from
links. performance and market-context topics toward investment
decisions and sustainability, which matches the growing
D. Discussion
attention to ESG in VC and PE [13], [14]. Because each of
Regarding RQ1, the keyword structure shows that VC and these keywords rests on three or four articles, the average
PE are the core of recent research, followed by years are indicative rather than conclusive.
entrepreneurial finance (8 occurrences), entrepreneurship (7), Several limitations should be noted. First, only 23
IPO (6), and innovation (6). The presence of nine clusters keywords reach the threshold, and 26 of the records have no
indicates a diverse field, with links to IPOs and exits [2], author keywords, so the map reflects authors’ keyword
crowdfunding and data-driven methods [17], [18], and ESG choices rather than the full content of the articles. Second,
and impact investing [13], [14], [15]. This diversity is because no thesaurus was applied, equivalent terms remain
consistent with the heterogeneous themes reported in earlier split across nodes; for example, ipo (6 occurrences) and initial
reviews [2], [18]. public offerings (3) are shown separately, and the
Regarding RQ2, entrepreneurial finance is the third most classification code g24 is retained as a node. Third, the
frequent keyword, and it co-occurs with venture capital in 6 clusters are based on a small number of articles per keyword
articles and with private equity in 5. Its cluster also contains and should be read as thematic tendencies. Future studies
ESG, sustainable finance, and investment decision-making, could combine author keywords with titles and abstracts,
which suggests that research on financing entrepreneurial apply a keyword-cleaning procedure, or analyze a larger
firms is increasingly tied to sustainability and investment corpus to capture valuation research more completely.
decisions [8], [13], [14]. Valuation, in contrast, appears only
through fair value, which occurs three times and sits in the V. CONCLUSION
cluster with start-ups, innovation, and entrepreneurship, in This study examined recent research on venture capital
line with studies that value start-ups through transaction-
(VC), private equity (PE), and early-stage venture valuation
based multiples and exit-consistent models [3], [6]. The through a bibliometric keyword co-occurrence analysis of
keyword valuation itself occurs only twice, and the dataset
150 Scopus-indexed journal articles published between 2021
contains more than ten valuation-related keywords, such as and 2026. The results show that venture capital and private
start-up valuation, post-money valuation, discounted cash
equity are the central themes in the research network,

connecting various topics, including entrepreneurial finance, model and exit multiples,” Finance Research Letters, vol.
entrepreneurship, innovation, crowdfunding, and sustainable 79, p. 107182, 2025, doi: 10.1016/j.frl.2025.107182.
finance. [7] L. J. Zheng, T. Bai, and A. R. Cross, “Signaling
The findings also indicate that entrepreneurial finance is Information Management in Entrepreneurial Firms’
closely associated with ESG, sustainable finance, and Financing Acquisition: An Integrated Signaling and
investment decision-making. However, valuation research Screening Perspective,” Journal of Global Information
Management, vol. 29, no. 6, p. 90, 2021, doi:
remains fragmented, as the keyword “valuation” appears
10.4018/JGIM.287590.
only twice, while “fair value” is the only valuation-related
[8] T. H. Aas, M. Rossfjord, and K. Østlie, “Evaluating
keyword that meets the minimum occurrence threshold. This
innovation in equity investment decisions: Insights from
suggests that valuation-related research is not fully
venture capital, private equity and equity fund
represented by the keywords used by authors, despite its
perspectives,” International Journal of Innovation
importance in early-stage investment decisions.
Management, vol. 29, no. 09n10, p. 2540014, 2025, doi:
Furthermore, investment decision-making, sustainable
10.1142/S1363919625400146.
finance, and fintech emerge as relatively recent research
[9] E. Fricke, S. Fung, and M. S. Goktan, “Is “accredited
topics, reflecting the evolving priorities in venture capital crowdfunding” a lemons market? Evidence from 506(c)
and private equity research. filings,” Journal of Small Business Management, vol. 59,
Despite these findings, the study has several limitations. no. 2, pp. 312–336, 2021, doi:
The analysis is based on a single database, includes only 150 10.1080/00472778.2020.1849715.
journal articles, and relies on author keywords without [10] R. Porro, T. Ercole, G. Pipitò, G. Vessio, and C. Loglisci,
applying a keyword-cleaning procedure. Future research “Pathways to success: a machine learning approach to
could incorporate additional databases, analyze titles and predicting investor dynamics in equity and lending
abstracts, and standardize related valuation terms to provide crowdfunding campaigns,” Journal of Intelligent
a more comprehensive understanding of early-stage venture Information Systems, vol. 63, no. 1, pp. 135–159, 2025,
valuation. Overall, this study provides a current overview of doi: 10.1007/s10844-024-00883-8.
[11] S. Singh and B. S. Mungila Hillemane, “Sources of
the research landscape and highlights the need for clearer
finance for tech startups over its lifecycle: what
conceptual classification to strengthen the understanding of
determines their approach of sources and its success?,”
valuation in early-stage ventures.
International Journal of Emerging Markets, vol. 18, no.
ACKNOWLEDGMENTS & CONTRIBUTORSHIP STATEMENT 8, pp. 1766–1787, 2023, doi: 10.1108/IJOEM-06-2020-
0705.
This research was supported by Bina Nusantara [12] H. Kraemer-Eis, J. Block, A. Botsari, F. Lang, S.
University, Indonesia. The authors acknowledge the use of Lorenzen, and W. Diegel, “Entrepreneurial finance in
Scopus bibliographic data and VOSviewer software to Europe and the Russian war against Ukraine,” Journal of
support the bibliometric analysis and visualization of the Technology Transfer, vol. 49, no. 6, pp. 2273–2305, 2024,
study. Alfath Ilmi Effendy and Atthariq Arsyan Wahyudi doi: 10.1007/s10961-024-10067-9.
contributed to data collection, data analysis, data processing, [13] W. Drobetz, S. El Ghoul, O. Guedhami, J. P. Hackmann,
and manuscript preparation. Danang Prihandoko served as the and P. P. Momtaz, “Entrepreneurial finance and
research supervisor. The authors declare that they have no sustainability: Do institutional investors impact the ESG
conflicts of interest related to this work. performance of SMEs?,” Journal of Business Venturing
Insights, vol. 22, p. e00498, 2024, doi:
REFERENCES 10.1016/j.jbvi.2024.e00498.
[14] E. M. Lange and N. G. Banadaki, “ESG consideration in
[1] R. Kumar, M. Firoz, and P. Kumar, “Renaissance of
venture capital: drivers, strategies and barriers,” Studies
alternate finance: Bibliometric visualization of private
in Economics and Finance, vol. 41, no. 3, pp. 724–739,
equity and venture capital,” Journal of Wealth
2024, doi: 10.1108/SEF-06-2023-0380.
Management, vol. 24, no. 2, pp. 114–128, 2021, doi:
[15] B. M. Barber, A. Morse, and A. Yasuda, “Impact
10.3905/JWM.2021.1.142.
investing,” Journal of Financial Economics, vol. 139, no.
[2] D. Cumming, S. Kumar, W. M. Lim, and N. Pandey,
1, pp. 162–185, 2021, doi: 10.1016/j.jfineco.2020.07.008.
“Mapping the venture capital and private equity research:
[16] G. Ross, S. Das, D. Sciro, and H. Raza, “CapitalVX: A
a bibliometric review and future research agenda,” Small
machine learning model for startup selection and exit
Business Economics, vol. 61, no. 1, pp. 173–221, 2023,
prediction,” Journal of Finance and Data Science, vol. 7,
doi: 10.1007/s11187-022-00684-9.
pp. 94–114, 2021, doi: 10.1016/j.jfds.2021.04.001.
[3] J. A. Barg, W. Drobetz, and P. P. Momtaz, “Valuing start-
[17] V. Capizzi, A. Paltrinieri, D. Pattnaik, and S. Kumar,
up firms: A reverse-engineering approach for fair-value
“Retrospective overview of the journal venture capital
multiples from venture capital transactions,” Finance
using bibliometric approach,” Venture Capital, vol. 24,
Research Letters, vol. 43, p. 102008, 2021, doi:
no. 1, pp. 1–23, 2022, doi:
10.1016/j.frl.2021.102008.
10.1080/13691066.2022.2051769.
[4] A. Giakoumelou, A. Salvi, O. Kvasova, and I.
[18] C. R. Silva Júnior, Á. L. Neuenfeldt Júnior, J. Siluk, V.
Rizomyliotis, “The start-up's roadmap to private equity
Gerhardt, and C. Michelin, “Evolution of start-up
financing: substituting discounts with a premium
investments: an overview and future research directions,”
in valuation for growth,” International Journal of
International Journal of Business Innovation and
Entrepreneurial Behavior & Research, vol. 31, no. 2–3,
Research, vol. 37, no. 2, pp. 246–272, 2025, doi:
pp. 479–497, 2025, doi: 10.1108/IJEBR-02-2022-0197.
10.1504/IJBIR.2025.146987.
[5] S. Peswani, “A venture capitalist’s endeavor: valuing a
[19] D. Cumming and N. Dai, “Shadow capital in venture
start-up for investment,” Emerald Emerging Markets
financing: Selection, valuation, and exit dynamic,”
Case Studies, vol. 15, no. 4, pp. 1–13, 2025, doi:
Journal of Empirical Finance, vol. 78, p. 101514, 2024,
10.1108/EEMCS-11-2024-0490.
doi: 10.1016/j.jempfin.2024.101514.
[6] H.-G. Kang and D. Ryu, “A complementary valuation
[20] A. Nazir and D. Tbaishat, “The impact of funding on

market valuation in technology start-up firms: Implication Technology, Market, and Complexity, vol. 9, no. 2, p.
for open innovation,” Journal of Open Innovation: 100028, 2023, doi: 10.1016/j.joitmc.2023.100028.
