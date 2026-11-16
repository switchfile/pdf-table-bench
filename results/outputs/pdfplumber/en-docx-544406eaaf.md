Valuing the Unvalued: A Bibliometric Mapping of
Venture Capital, Private Equity, and Early-Stage
Venture Valuation Research
Alfath Ilmi Effendy Atthariq Arsyan Wahyudi Danang Prihandoko
Business Management Department, Management Department Business Management Department,
BBS Undergraduate Program BBS Undergraduate Program BBS Undergraduate Program
Bina Nusantara University Bina Nusantara University Bina Nusantara University
Bekasi, Indonesia Bekasi, Indonesia Bekasi, Indonesia
Alfath.effendy@binus.ac.id atthariq.wahyudi@binus.ac.id dprihandoko@binus.ac.id
Abstract— Early-stage ventures are difficult to value signals differ across early financing stages [7]. VC investors,
because they lack stable revenues, financial histories, and for example, tend to treat innovation as central to their
reliable market benchmarks, which makes venture valuation a investment criteria and to rely on qualitative indicators,
central concern in venture capital (VC), private equity (PE), whereas PE investors view it as one component among
and entrepreneurial finance research. This study maps recent broader financial considerations [8]. At the same time, the
scholarship on these topics through a bibliometric keyword financing environment has widened. Recent studies address
co-occurrence analysis. Bibliographic records were retrieved equity and lending crowdfunding [9], [10], the sources of
from Scopus and screened by publication year (2021–2026), finance used by technology start-ups over their life cycle [11],
language (English), and document type (journal article), the effects of exogenous crises on entrepreneurial finance
which resulted in 150 articles. Author keywords were [12], and the role of environmental, social, and governance
analyzed in VOSviewer using full counting and a minimum (ESG) and impact considerations in VC and PE investment
occurrence threshold of three. The resulting network [13], [14], [15]. Machine-learning models have also been
comprises 23 keywords in nine clusters. Venture capital and proposed to support start-up selection and exit prediction
private equity occupy the central positions and connect [16]. Early-stage venture valuation thus sits at the intersection
clusters on entrepreneurship and innovation, entrepreneurial of financial models, investor judgment, and a growing set of
finance and ESG, crowdfunding and machine learning, and financing channels.
initial public offerings. The overlay visualization shows that Several bibliometric reviews have mapped parts of this
investment decision-making, sustainable finance, and fintech field. Cumming et al. [2] and Kumar et al. [1] analyzed VC
are among the more recent topics, whereas emerging markets, and PE research using Web of Science, Capizzi et al. [17]
performance measurement, crowdfunding, and impact reviewed the journal Venture Capital, and Silva Júnior et al.
investing appeared earlier. Valuation enters the network only [18] traced the evolution of start-up investments in a Scopus
through the keyword fair value, even though more than ten corpus of 1,984 articles. Among the bibliometric reviews
valuation-related keywords appear in the dataset, which identified in our dataset, none analyzes recent Scopus-
suggests that valuation research is fragmented in authors’ indexed journal articles through a keyword co-occurrence
keyword choices. The study contributes a current, Scopus- map that centers on early-stage venture valuation and
based map of VC and PE research and indicates where entrepreneurial finance. It therefore remains unclear which
valuation needs clearer conceptual labeling. topics currently anchor the field, how they relate to one
another, and which have emerged most recently.
Keywords—Venture Capital, Private Equity,
This study addresses that gap through a keyword co-
Entrepreneurial Finance, Bibliometric Analysis, VOSviewer
occurrence analysis of journal articles indexed in Scopus
I. INTRODUCTION between 2021 and 2026. It is guided by three research
questions. RQ1: What are the most prominent author
Venture capital (VC) and private equity (PE) play a
keywords and thematic clusters in recent VC and PE
pivotal role in nurturing newly established and growth-
research? RQ2: How are valuation and entrepreneurial
oriented firms [1], and both fields have grown into a
finance positioned within the keyword network? RQ3: Which
heterogeneous set of research themes [2]. In early-stage
topics have emerged most recently? The study contributes a
financing, however, assigning a value to the venture is
current, Scopus-based map of the field and a replicable
difficult. The valuation of start-up firms is challenging yet
procedure for search, screening, and keyword analysis. The
highly relevant to entrepreneurs and financiers alike [3], and
remainder of this paper reviews the related literature,
high failure rates, long payback periods, and information
describes the research method, presents and discusses the
asymmetries are associated with conservative pricing and
results, and concludes.
valuation discounts [4]. The literature therefore draws on
several approaches, including the venture capitalist method
and discounted cash flow analysis [5], fair-value multiples II. LITERATURE REVIEW
derived from observed VC transactions [3], and models that
A. Venture Capital and Private Equity as Entrepreneurial
reconcile entry valuations with exit multiples [6].
Finance
Valuation in practice is not purely numerical. Investors
Cumming et al. [2] describe VC and PE as fields rooted in
interpret signals from ventures, and their perceptions of those
financing research on capital budgeting and initial public
XXX-X-XXXX-XXXX-X/XX/$XX.00 ©20XX IEEE

offerings (IPOs). In their review, foundational VC themes predicts start-up exit outcomes with out-of-sample accuracy
include adoption and financing processes, the roles of VC in of 80–89%.
business, governance, and syndication, whereas PE research
D. Bibliometric Analysis and Research Gap
emphasizes style drift into VC, buyouts and privatization, and
valuation and performance. The boundary between the two is Bibliometric analysis quantifies publication patterns and
increasingly porous. Cumming and Dai [19] show that non- reveals the intellectual structure of a field. In the VC and PE
VC private equity funds invest in entrepreneurial firms, prefer domain, Cumming et al. [2] mapped geographical focus,
expansion and late-stage ventures, and are associated with methodological choices, and themes using Web of Science
larger investments and higher valuations. For this reason, VC records. Kumar et al. [1] visualized two decades of PE and VC
and PE are treated in this study as related but distinct concepts articles and found that VC research is more frequent than PE
and are not merged in the keyword analysis. Silva Júnior et al. research. Capizzi et al. [17] analyzed 385 documents
[18] further show that research on start-up investment moved published in the journal Venture Capital between 1999 and
from VC and bootstrapping in the 1990s to angel investment, 2021 and highlighted themes such as crowdfunding,
corporate venture capital, and innovation in the following government venture capital, and market failure. Silva Júnior
decade, and more recently to crowdfunding, PE, accelerators, et al. [18] combined VOSviewer and SciMAT to examine
and data-driven technologies. 1,984 Scopus articles on start-up investment.
These reviews differ in database, scope, and period.
B. Early-Stage Venture Valuation Among those identified in our dataset, none analyzes Scopus-
Valuation approaches in the literature range from classical indexed journal articles from 2021 to 2026 through a keyword
to market-based and hybrid. Peswani [5] uses a teaching case co-occurrence map that centers on early-stage venture
to show how the venture capitalist approach and the valuation and entrepreneurial finance. This gap motivates the
discounted cash flow method are applied to a start-up, and present study.
how external and internal factors complicate the exercise.
Barg et al. [3] reverse-engineer fair-value multiples by III. RESEARCH METHOD
comparing firm value at financing with firm value at exit, and
A. Research Design
report that multiples are higher when more experienced
This study uses bibliometric analysis, combining
investors are involved and when exit occurs through an IPO
performance description with science mapping, to examine
rather than a merger or acquisition, and lower in later-stage
research on VC and PE with attention to early-stage venture
rounds and larger investment consortia. Kang and Ryu [6]
valuation and entrepreneurial finance. Keyword co-
propose a model that integrates growth dynamics and exit
occurrence analysis was selected because it reveals the
multiples to resolve inconsistencies between present
thematic structure of a field from the terms that authors use to
valuations and terminal values, with particular relevance for
describe their own work. The analysis was carried out in
VC and PE.
VOSviewer.
Other studies examine what shapes value in practice.
Nazir and Tbaishat [20] apply causal-impact methods to 7,481 B. Data Source and Search Strategy
early-stage technology start-ups in the United Arab Emirates
Bibliographic data were retrieved from Scopus, a curated
to assess how funding relates to market valuation.
database that provides structured records including titles,
Giakoumelou et al. [4], drawing on contingency, innovation,
abstracts, author keywords, and citation information. The
and signaling theories, examine the “patent premium” that PE
search was conducted on 13 October 2026 in the title, abstract,
investors pay for Italian start-ups in the growth and expansion
and keyword fields using the following query: “private equity
stages. Information outside financial statements also matters:
and venture capital”.
Zheng et al. [7] find that angel investors extract and combine
different signals when reaching a financing decision, and Aas C. Screening Procedure
et al. [8] show that VC, PE, and equity fund investors evaluate
The initial search returned 1,042 documents. Three filters
innovation capabilities differently.
were then applied in sequence. Restricting the publication
C. Financing Channels, Sustainability, and Data-Driven period to 2021–2026 reduced the set to 341 documents,
limiting the language to English left 329, and restricting the
Investing
document type to journal articles left 150. These 150 articles
Entrepreneurial finance has expanded beyond traditional
constitute the final dataset. Table I summarizes the procedure.
VC. Fricke et al. [9] study accredited crowdfunding under the
U.S. JOBS Act and find no support for a lemons market, while Table I. Article Selection Process

| Step | Filter Applied | Records |
|---|---|---|
| 1 | Initial Scopus Search | 1,042 |
| 2 | Publication Year 2021-2026 | 341 |
| 3 | Language: English | 329 |
| 4 | Document Type: Journal Article | 150 |

Porro et al. [10] use machine learning to predict investor
dynamics in equity and lending crowdfunding campaigns in
Italy. Singh and Hillemane [11] analyze how technology start-
ups choose sources of finance over their life cycle, and
Kraemer-Eis et al. [12] examine the effect of the Russian war
against Ukraine, treated as an unexpected exogenous crisis, on
entrepreneurial finance in Europe.
Sustainability and data-driven methods form two further
strands. Drobetz et al. [13] find that PE and VC backing
increases the externally validated ESG scores of small and
medium-sized enterprises, Lange and Banadaki [14]
D. Data Analysis
interview VC investors about the drivers, strategies, and
barriers of ESG consideration, and Barber et al. [15] show that The selected records were exported from Scopus in CSV
investors accept lower returns in dual-objective impact VC format and analyzed in VOSviewer. A co-occurrence analysis
funds. Ross et al. [16] develop a machine-learning model that was performed on author keywords using the full counting
method, in which every keyword of a record receives full

weight in each co-occurrence link. Of the exported records, means that some themes are split across several nodes, as
124 contained author keywords, yielding 473 distinct discussed in Section IV-D.
keywords. Because most keywords appear in only one article,
E. Visualization
the minimum number of occurrences of a keyword was set to
three, and 23 keywords met this threshold. Three VOSviewer visualizations were produced. In the
No thesaurus file was applied, so keywords were analyzed network visualization, nodes represent keywords, node size
as recorded by the authors. VOSviewer treats keywords that reflects the number of occurrences, links represent co-
differ only in letter case as identical, but spelling variants, occurrence, and colors indicate clusters. The overlay
abbreviations, and singular and plural forms remain separate visualization colors each keyword by the average publication
items (for example, “ipo” and “initial public offerings”). This year of the articles in which it appears, which makes the
choice keeps the authors’ original terminology, but it also relative recency of topics visible. The density visualization
highlights the areas where keywords and links are
concentrated.
IV. RESULTS AND DISCUSSION
A. Keyword Co-occurrence Network
Fig. 1. Network visualization of keyword co-occurrence.

| investment decision- making | 3 | 2024.67 | Red |
|---|---|---|---|
| investments | 3 | 2024.67 | Cyan |
| performance | 3 | 2023.33 | Red |
| performance measurement* | 3 | 2021.00 | Blue |
| start-ups | 3 | 2023.67 | Green |

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
| esg | 4 | 2023.75 | Red |
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

Venture capital and private equity are by far the largest
nodes, with 60 and 65 occurrences, and they appear together
in 48 of the 124 articles that report author keywords. Both are
linked to most of the other keywords in the network, which
confirms them as the core concepts of the dataset.
The red cluster is the largest, with six keywords:
entrepreneurial finance, ESG, sustainable finance, investment
decision-making, performance, and g24. It connects the
financing of entrepreneurial firms with sustainability
considerations and investment decisions. The keyword g24 is
a Journal of Economic Literature (JEL) classification code
(investment banking, venture capital, brokerage, and ratings)
rather than a topic, so it is not interpreted substantively. The
green cluster (entrepreneurship, innovation, start-ups,
corporate governance, and fair value) represents the
entrepreneurial side of the field, and fair value is the only
valuation-related keyword in it. The blue cluster links private

equity to emerging markets and performance measurement, (crowdfunding and machine learning) concerns alternative
and the yellow cluster links venture capital to fintech. The financing channels and data-driven methods. Three single-
cyan cluster (investments and fundraising) concerns the keyword clusters correspond to impact investing, ipo, and
raising and deployment of capital, and the purple cluster initial public offerings.
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

Fig. 3 shows that the densest area is formed by venture through a bibliometric keyword co-occurrence analysis of
capital and private equity, which reflects both their frequency 150 Scopus-indexed journal articles published between 2021
and their many links. Areas of moderate density appear and 2026. The results show that venture capital and private
around the green cluster (entrepreneurship, innovation, start- equity are the central themes in the research network,
ups, and fair value), around entrepreneurial finance, ESG, and connecting various topics, including entrepreneurial finance,
investment decision-making, and around crowdfunding, entrepreneurship, innovation, crowdfunding, and sustainable
machine learning, ipo, and fintech. Keywords such as finance.
emerging markets, performance measurement, impact The findings also indicate that entrepreneurial finance is
investing, and initial public offerings lie in low-density areas, closely associated with ESG, sustainable finance, and
which is consistent with their lower frequencies and fewer investment decision-making. However, valuation research
links. remains fragmented, as the keyword “valuation” appears
only twice, while “fair value” is the only valuation-related
D. Discussion
keyword that meets the minimum occurrence threshold. This
Regarding RQ1, the keyword structure shows that VC and suggests that valuation-related research is not fully
PE are the core of recent research, followed by entrepreneurial represented by the keywords used by authors, despite its
finance (8 occurrences), entrepreneurship (7), IPO (6), and importance in early-stage investment decisions.
innovation (6). The presence of nine clusters indicates a Furthermore, investment decision-making, sustainable
diverse field, with links to IPOs and exits [2], crowdfunding finance, and fintech emerge as relatively recent research
and data-driven methods [17], [18], and ESG and impact topics, reflecting the evolving priorities in venture capital and
investing [13], [14], [15]. This diversity is consistent with the private equity research.
heterogeneous themes reported in earlier reviews [2], [18]. Despite these findings, the study has several limitations.
Regarding RQ2, entrepreneurial finance is the third most The analysis is based on a single database, includes only 150
frequent keyword, and it co-occurs with venture capital in 6 journal articles, and relies on author keywords without
articles and with private equity in 5. Its cluster also contains applying a keyword-cleaning procedure. Future research
ESG, sustainable finance, and investment decision-making, could incorporate additional databases, analyze titles and
which suggests that research on financing entrepreneurial abstracts, and standardize related valuation terms to provide a
firms is increasingly tied to sustainability and investment more comprehensive understanding of early-stage venture
decisions [8], [13], [14]. Valuation, in contrast, appears only valuation. Overall, this study provides a current overview of
through fair value, which occurs three times and sits in the the research landscape and highlights the need for clearer
cluster with start-ups, innovation, and entrepreneurship, in conceptual classification to strengthen the understanding of
line with studies that value start-ups through transaction-based valuation in early-stage ventures.
multiples and exit-consistent models [3], [6]. The keyword
valuation itself occurs only twice, and the dataset contains ACKNOWLEDGMENTS & CONTRIBUTORSHIP STATEMENT
more than ten valuation-related keywords, such as start-up This research was supported by Bina Nusantara
valuation, post-money valuation, discounted cash flow, and University, Indonesia. The authors acknowledge the use of
exit multiples, most of which appear once. By comparison, the Scopus bibliographic data and VOSviewer software to
word valuation appears in the title or abstract of 21 of the support the bibliometric analysis and visualization of the
records. This gap shows that author keywords underrepresent study. Alfath Ilmi Effendy and Atthariq Arsyan Wahyudi
valuation research and spread it across many low-frequency contributed to data collection, data analysis, data processing,
terms. and manuscript preparation. Danang Prihandoko served as the
Regarding RQ3, the most recent topics are investment research supervisor. The authors declare that they have no
decision-making, investments, sustainable finance, and conflicts of interest related to this work.
fintech, whereas performance measurement, emerging
markets, crowdfunding, and impact investing are associated REFERENCES
with earlier years. This pattern suggests a shift from
[1] R. Kumar, M. Firoz, and P. Kumar, “Renaissance of
performance and market-context topics toward investment
alternate finance: Bibliometric visualization of private
decisions and sustainability, which matches the growing
equity and venture capital,” Journal of Wealth
attention to ESG in VC and PE [13], [14]. Because each of Management, vol. 24, no. 2, pp. 114–128, 2021, doi:
these keywords rests on three or four articles, the average 10.3905/JWM.2021.1.142.
years are indicative rather than conclusive. [2] D. Cumming, S. Kumar, W. M. Lim, and N. Pandey,
Several limitations should be noted. First, only 23 “Mapping the venture capital and private equity research:
keywords reach the threshold, and 26 of the records have no a bibliometric review and future research agenda,” Small
author keywords, so the map reflects authors’ keyword Business Economics, vol. 61, no. 1, pp. 173–221, 2023,
choices rather than the full content of the articles. Second, doi: 10.1007/s11187-022-00684-9.
because no thesaurus was applied, equivalent terms remain [3] J. A. Barg, W. Drobetz, and P. P. Momtaz, “Valuing start-
split across nodes; for example, ipo (6 occurrences) and initial up firms: A reverse-engineering approach for fair-value
public offerings (3) are shown separately, and the multiples from venture capital transactions,” Finance
Research Letters, vol. 43, p. 102008, 2021, doi:
classification code g24 is retained as a node. Third, the
10.1016/j.frl.2021.102008.
clusters are based on a small number of articles per keyword
[4] A. Giakoumelou, A. Salvi, O. Kvasova, and I.
and should be read as thematic tendencies. Future studies
Rizomyliotis, “The start-up's roadmap to private equity
could combine author keywords with titles and abstracts,
financing: substituting discounts with a premium
apply a keyword-cleaning procedure, or analyze a larger
in valuation for growth,” International Journal of
corpus to capture valuation research more completely.
Entrepreneurial Behavior & Research, vol. 31, no. 2–3,
pp. 479–497, 2025, doi: 10.1108/IJEBR-02-2022-0197.
V. CONCLUSION
[5] S. Peswani, “A venture capitalist’s endeavor: valuing a
This study examined recent research on venture capital start-up for investment,” Emerald Emerging Markets
(VC), private equity (PE), and early-stage venture valuation Case Studies, vol. 15, no. 4, pp. 1–13, 2025, doi:

10.1108/EEMCS-11-2024-0490. [13] W. Drobetz, S. El Ghoul, O. Guedhami, J. P. Hackmann,
[6] H.-G. Kang and D. Ryu, “A complementary valuation and P. P. Momtaz, “Entrepreneurial finance and
model and exit multiples,” Finance Research Letters, vol. sustainability: Do institutional investors impact the ESG
79, p. 107182, 2025, doi: 10.1016/j.frl.2025.107182. performance of SMEs?,” Journal of Business Venturing
[7] L. J. Zheng, T. Bai, and A. R. Cross, “Signaling Insights, vol. 22, p. e00498, 2024, doi:
Information Management in Entrepreneurial Firms’ 10.1016/j.jbvi.2024.e00498.
Financing Acquisition: An Integrated Signaling and [14] E. M. Lange and N. G. Banadaki, “ESG consideration in
Screening Perspective,” Journal of Global Information venture capital: drivers, strategies and barriers,” Studies
Management, vol. 29, no. 6, p. 90, 2021, doi: in Economics and Finance, vol. 41, no. 3, pp. 724–739,
10.4018/JGIM.287590. 2024, doi: 10.1108/SEF-06-2023-0380.
[8] T. H. Aas, M. Rossfjord, and K. Østlie, “Evaluating [15] B. M. Barber, A. Morse, and A. Yasuda, “Impact
innovation in equity investment decisions: Insights from investing,” Journal of Financial Economics, vol. 139, no.
venture capital, private equity and equity fund 1, pp. 162–185, 2021, doi: 10.1016/j.jfineco.2020.07.008.
perspectives,” International Journal of Innovation [16] G. Ross, S. Das, D. Sciro, and H. Raza, “CapitalVX: A
Management, vol. 29, no. 09n10, p. 2540014, 2025, doi: machine learning model for startup selection and exit
10.1142/S1363919625400146. prediction,” Journal of Finance and Data Science, vol. 7,
[9] E. Fricke, S. Fung, and M. S. Goktan, “Is “accredited pp. 94–114, 2021, doi: 10.1016/j.jfds.2021.04.001.
crowdfunding” a lemons market? Evidence from 506(c) [17] V. Capizzi, A. Paltrinieri, D. Pattnaik, and S. Kumar,
filings,” Journal of Small Business Management, vol. 59, “Retrospective overview of the journal venture capital
no. 2, pp. 312–336, 2021, doi: using bibliometric approach,” Venture Capital, vol. 24,
10.1080/00472778.2020.1849715. no. 1, pp. 1–23, 2022, doi:
[10] R. Porro, T. Ercole, G. Pipitò, G. Vessio, and C. Loglisci, 10.1080/13691066.2022.2051769.
“Pathways to success: a machine learning approach to [18] C. R. Silva Júnior, Á. L. Neuenfeldt Júnior, J. Siluk, V.
predicting investor dynamics in equity and lending Gerhardt, and C. Michelin, “Evolution of start-up
crowdfunding campaigns,” Journal of Intelligent investments: an overview and future research directions,”
Information Systems, vol. 63, no. 1, pp. 135–159, 2025, International Journal of Business Innovation and
doi: 10.1007/s10844-024-00883-8. Research, vol. 37, no. 2, pp. 246–272, 2025, doi:
[11] S. Singh and B. S. Mungila Hillemane, “Sources of 10.1504/IJBIR.2025.146987.
finance for tech startups over its lifecycle: what [19] D. Cumming and N. Dai, “Shadow capital in venture
determines their approach of sources and its success?,” financing: Selection, valuation, and exit dynamic,”
International Journal of Emerging Markets, vol. 18, no. 8, Journal of Empirical Finance, vol. 78, p. 101514, 2024,
pp. 1766–1787, 2023, doi: 10.1108/IJOEM-06-2020- doi: 10.1016/j.jempfin.2024.101514.
0705. [20] A. Nazir and D. Tbaishat, “The impact of funding on
[12] H. Kraemer-Eis, J. Block, A. Botsari, F. Lang, S. market valuation in technology start-up firms: Implication
Lorenzen, and W. Diegel, “Entrepreneurial finance in for open innovation,” Journal of Open Innovation:
Europe and the Russian war against Ukraine,” Journal of Technology, Market, and Complexity, vol. 9, no. 2, p.
Technology Transfer, vol. 49, no. 6, pp. 2273–2305, 2024, 100028, 2023, doi: 10.1016/j.joitmc.2023.100028.
doi: 10.1007/s10961-024-10067-9.
