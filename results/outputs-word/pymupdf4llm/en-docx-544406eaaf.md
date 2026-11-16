# Valuing the Unvalued: A Bibliometric Mapping of Venture Capital, Private Equity, and Early-Stage Venture Valuation Research 

|Alfath Ilmi Effendy|Atthariq Arsyan Wahyudi|Danang Prihandoko|
|---|---|---|
|_Business Management Department,_|_Management Department_|_Business Management Department,_|
|_BBS  Undergraduate Program_|_BBS  Undergraduate Program_|_BBS  Undergraduate Program_|
|Bina Nusantara University|Bina Nusantara University|Bina Nusantara University|
|Bekasi, Indonesia|Bekasi, Indonesia|Bekasi, Indonesia|
|Alfath.effendy@binus.ac.id|atthariq.wahyudi@binus.ac.id|dprihandoko@binus.ac.id|



**_Abstract_ —** Early-stage ventures are difficult to value because they lack stable revenues, financial histories, and reliable market benchmarks, which makes venture valuation a central concern in venture capital (VC), private equity (PE), and entrepreneurial finance research. This study maps recent scholarship on these topics through a bibliometric keyword co-occurrence analysis. Bibliographic records were retrieved from Scopus and screened by publication year (2021–2026), language (English), and document type (journal article), which resulted in 150 articles. Author keywords were analyzed in VOSviewer using full counting and a minimum occurrence threshold of three. The resulting network comprises 23 keywords in nine clusters. Venture capital and private equity occupy the central positions and connect clusters on entrepreneurship and innovation, entrepreneurial finance and ESG, crowdfunding and machine learning, and initial public offerings. The overlay visualization shows that investment decision-making, sustainable finance, and fintech are among the more recent topics, whereas emerging markets, performance measurement, crowdfunding, and impact investing appeared earlier. Valuation enters the network only through the keyword fair value, even though more than ten valuation-related keywords appear in the dataset, which suggests that valuation research is fragmented in authors’ keyword choices. The study contributes a current, Scopusbased map of VC and PE research and indicates where valuation needs clearer conceptual labeling. 

**_Keywords—_** _Venture Capital, Private Equity, Entrepreneurial Finance, Bibliometric Analysis, VOSviewer_ 

## I. INTRODUCTION 

Venture capital (VC) and private equity (PE) play a pivotal role in nurturing newly established and growthoriented firms [1], and both fields have grown into a heterogeneous set of research themes [2]. In early-stage financing, however, assigning a value to the venture is difficult. The valuation of start-up firms is challenging yet highly relevant to entrepreneurs and financiers alike [3], and high failure rates, long payback periods, and information asymmetries are associated with conservative pricing and valuation discounts [4]. The literature therefore draws on several approaches, including the venture capitalist method and discounted cash flow analysis [5], fair-value multiples 

derived from observed VC transactions [3], and models that reconcile entry valuations with exit multiples [6]. 

Valuation in practice is not purely numerical. Investors interpret signals from ventures, and their perceptions of those signals differ across early financing stages [7]. VC investors, for example, tend to treat innovation as central to their investment criteria and to rely on qualitative indicators, whereas PE investors view it as one component among broader financial considerations [8]. At the same time, the financing environment has widened. Recent studies address equity and lending crowdfunding [9], [10], the sources of finance used by technology start-ups over their life cycle [11], the effects of exogenous crises on entrepreneurial finance [12], and the role of environmental, social, and governance (ESG) and impact considerations in VC and PE investment [13], [14], [15]. Machine-learning models have also been proposed to support start-up selection and exit prediction [16]. Early-stage venture valuation thus sits at the intersection of financial models, investor judgment, and a growing set of financing channels. 

Several bibliometric reviews have mapped parts of this field. Cumming et al. [2] and Kumar et al. [1] analyzed VC and PE research using Web of Science, Capizzi et al. [17] reviewed the journal Venture Capital, and Silva Júnior et al. [18] traced the evolution of start-up investments in a Scopus corpus of 1,984 articles. Among the bibliometric reviews identified in our dataset, none analyzes recent Scopusindexed journal articles through a keyword co-occurrence map that centers on early-stage venture valuation and entrepreneurial finance. It therefore remains unclear which topics currently anchor the field, how they relate to one another, and which have emerged most recently. 

This study addresses that gap through a keyword cooccurrence analysis of journal articles indexed in Scopus between 2021 and 2026. It is guided by three research questions. RQ1: What are the most prominent author keywords and thematic clusters in recent VC and PE research? RQ2: How are valuation and entrepreneurial finance positioned within the keyword network? RQ3: Which topics have emerged most recently? The study contributes a current, Scopus-based map of the field and a replicable procedure for search, screening, and keyword analysis. The 

XXX-X-XXXX-XXXX-X/XX/$XX.00 ©20XX IEEE 

remainder of this paper reviews the related literature, describes the research method, presents and discusses the results, and concludes. 

## II. LITERATURE REVIEW 

- _A. Venture Capital and Private Equity as Entrepreneurial Finance_ 

Cumming et al. [2] describe VC and PE as fields rooted in financing research on capital budgeting and initial public offerings (IPOs). In their review, foundational VC themes include adoption and financing processes, the roles of VC in business, governance, and syndication, whereas PE research emphasizes style drift into VC, buyouts and privatization, and valuation and performance. The boundary between the two is increasingly porous. Cumming and Dai [19] show that nonVC private equity funds invest in entrepreneurial firms, prefer expansion and late-stage ventures, and are associated with larger investments and higher valuations. For this reason, VC and PE are treated in this study as related but distinct concepts and are not merged in the keyword analysis. Silva Júnior et al. [18] further show that research on start-up investment moved from VC and bootstrapping in the 1990s to angel investment, corporate venture capital, and innovation in the following decade, and more recently to crowdfunding, PE, accelerators, and data-driven technologies. 

## _B. Early-Stage Venture Valuation_ 

Valuation approaches in the literature range from classical to market-based and hybrid. Peswani [5] uses a teaching case to show how the venture capitalist approach and the discounted cash flow method are applied to a start-up, and how external and internal factors complicate the exercise. Barg et al. [3] reverse-engineer fair-value multiples by comparing firm value at financing with firm value at exit, and report that multiples are higher when more experienced investors are involved and when exit occurs through an IPO rather than a merger or acquisition, and lower in later-stage rounds and larger investment consortia. Kang and Ryu [6] propose a model that integrates growth dynamics and exit multiples to resolve inconsistencies between present valuations and terminal values, with particular relevance for VC and PE. 

Other studies examine what shapes value in practice. Nazir and Tbaishat [20] apply causal-impact methods to 7,481 early-stage technology start-ups in the United Arab Emirates to assess how funding relates to market valuation. Giakoumelou et al. [4], drawing on contingency, innovation, and signaling theories, examine the “patent premium” that PE investors pay for Italian start-ups in the growth and expansion stages. Information outside financial statements also matters: Zheng et al. [7] find that angel investors extract and combine different signals when reaching a financing decision, and Aas et al. [8] show that VC, PE, and equity fund investors evaluate innovation capabilities differently. 

## _C. Financing Channels, Sustainability, and Data-Driven Investing_ 

Entrepreneurial finance has expanded beyond traditional VC. Fricke et al. [9] study accredited crowdfunding under the U.S. JOBS Act and find no support for a lemons market, while Porro et al. [10] use machine learning to predict investor dynamics in equity and lending crowdfunding campaigns in Italy. Singh and Hillemane [11] analyze how technology 

start-ups choose sources of finance over their life cycle, and Kraemer-Eis et al. [12] examine the effect of the Russian war against Ukraine, treated as an unexpected exogenous crisis, on entrepreneurial finance in Europe. 

Sustainability and data-driven methods form two further strands. Drobetz et al. [13] find that PE and VC backing increases the externally validated ESG scores of small and medium-sized enterprises, Lange and Banadaki [14] interview VC investors about the drivers, strategies, and barriers of ESG consideration, and Barber et al. [15] show that investors accept lower returns in dual-objective impact VC funds. Ross et al. [16] develop a machine-learning model that predicts start-up exit outcomes with out-of-sample accuracy of 80–89%. 

## _D. Bibliometric Analysis and Research Gap_ 

Bibliometric analysis quantifies publication patterns and reveals the intellectual structure of a field. In the VC and PE domain, Cumming et al. [2] mapped geographical focus, methodological choices, and themes using Web of Science records. Kumar et al. [1] visualized two decades of PE and VC articles and found that VC research is more frequent than PE research. Capizzi et al. [17] analyzed 385 documents published in the journal Venture Capital between 1999 and 2021 and highlighted themes such as crowdfunding, government venture capital, and market failure. Silva Júnior et al. [18] combined VOSviewer and SciMAT to examine 1,984 Scopus articles on start-up investment. 

These reviews differ in database, scope, and period. Among those identified in our dataset, none analyzes Scopusindexed journal articles from 2021 to 2026 through a keyword co-occurrence map that centers on early-stage venture valuation and entrepreneurial finance. This gap motivates the present study. 

## III. RESEARCH METHOD 

## _A. Research Design_ 

This study uses bibliometric analysis, combining performance description with science mapping, to examine research on VC and PE with attention to early-stage venture valuation and entrepreneurial finance. Keyword cooccurrence analysis was selected because it reveals the thematic structure of a field from the terms that authors use to describe their own work. The analysis was carried out in VOSviewer. 

## _B. Data Source and Search Strategy_ 

Bibliographic data were retrieved from Scopus, a curated database that provides structured records including titles, abstracts, author keywords, and citation information. The search was conducted on 13 October 2026 in the title, abstract, and keyword fields using the following query: “private equity and venture capital”. 

## _C. Screening Procedure_ 

The initial search returned 1,042 documents. Three filters were then applied in sequence. Restricting the publication period to 2021–2026 reduced the set to 341 documents, limiting the language to English left 329, and restricting the document type to journal articles left 150. These 150 articles constitute the final dataset. Table I summarizes the procedure. 

**Table I.** Article Selection Process 

|Step|Filter Applied<br>Records|
|---|---|



|1|Initial Scopus<br>Search|1,042|
|---|---|---|
|2|Publication Year<br>2021-2026|341|
|3|Language:<br>English|329|
|4|Document Type:<br>Journal Article|150|



No thesaurus file was applied, so keywords were analyzed as recorded by the authors. VOSviewer treats keywords that differ only in letter case as identical, but spelling variants, abbreviations, and singular and plural forms remain separate items (for example, “ipo” and “initial public offerings”). This choice keeps the authors’ original terminology, but it also means that some themes are split across several nodes, as discussed in Section IV-D. 

## _E. Visualization_ 

## _D. Data Analysis_ 

The selected records were exported from Scopus in CSV format and analyzed in VOSviewer. A co-occurrence analysis was performed on author keywords using the full counting method, in which every keyword of a record receives full weight in each co-occurrence link. Of the exported records, 124 contained author keywords, yielding 473 distinct keywords. Because most keywords appear in only one article, the minimum number of occurrences of a keyword was set to three, and 23 keywords met this threshold. 

Three VOSviewer visualizations were produced. In the network visualization, nodes represent keywords, node size reflects the number of occurrences, links represent cooccurrence, and colors indicate clusters. The overlay visualization colors each keyword by the average publication year of the articles in which it appears, which makes the relative recency of topics visible. The density visualization highlights the areas where keywords and links are concentrated. 

## IV. RESULTS AND DISCUSSION 

## _A. Keyword Co-occurrence Network_ 



**Fig. 1.** Network visualization of keyword co-occurrence. 

Fig. 1 shows the network of the 23 author keywords that met the threshold. The keywords form nine clusters, distinguished by color in the figure. Table II lists each keyword with its number of occurrences, its average publication year, and its cluster. 

**Table II.** Keywords Meeting the Minimum Occurrence Threshold of Three 

|**Keyword**|**Occurrences**|**Avg. year**|**Cluster**|
|---|---|---|---|
|private equity|65|2023.23|Blue|
|venture capital|60|2023.43|Yellow|
|entrepreneurial<br>finance|8|2023.62|Red|
|entrepreneurship|7|2023.43|Green|
|innovation|6|2023.67|Green|
|ipo|6|2023.50|Pink|
|g24|5|2025.40|Red|



|esg|4|2023.75|Red|
|---|---|---|---|
|fintech|4|2024.00|Yellow|
|machine learning|4|2023.50|Purple|
|sustainable finance|4|2024.25|Red|
|corporate governance|3|2023.33|Green|
|crowdfunding|3|2022.67|Purple|
|emergingmarkets|3|2021.33|Blue|
|fair value|3|2023.00|Green|
|fundraising|3|2023.67|Cyan|
|impact investing|3|2022.67|Orange|
|initial public offerings|3|2023.33|Brown|
|investment decision-<br>making|3|2024.67|Red|
|investments|3|2024.67|Cyan|
|performance|3|2023.33|Red|



|performance|3|2021.00|Blue|
|---|---|---|---|
|measurement*||||
|start-ups|3|2023.67|Green|



Venture capital and private equity are by far the largest nodes, with 60 and 65 occurrences, and they appear together in 48 of the 124 articles that report author keywords. Both are linked to most of the other keywords in the network, which confirms them as the core concepts of the dataset. 

The red cluster is the largest, with six keywords: entrepreneurial finance, ESG, sustainable finance, investment decision-making, performance, and g24. It connects the financing of entrepreneurial firms with sustainability considerations and investment decisions. The keyword g24 is a Journal of Economic Literature (JEL) classification code 

(investment banking, venture capital, brokerage, and ratings) rather than a topic, so it is not interpreted substantively. The green cluster (entrepreneurship, innovation, start-ups, corporate governance, and fair value) represents the entrepreneurial side of the field, and fair value is the only valuation-related keyword in it. The blue cluster links private equity to emerging markets and performance measurement, and the yellow cluster links venture capital to fintech. The cyan cluster (investments and fundraising) concerns the raising and deployment of capital, and the purple cluster (crowdfunding and machine learning) concerns alternative financing channels and data-driven methods. Three singlekeyword clusters correspond to impact investing, ipo, and initial public offerings. 

_B. Overlay Visualization_ 



**Fig. 2.** Overlay visualization of keywords by average publication year. 

Fig. 2 colors the keywords by their average publication year. Venture capital and private equity are centered around 2023, which indicates that they are present throughout the period. Among the earlier topics are performance measurement (2021.00) and emerging markets (2021.33), followed by crowdfunding and impact investing (both 

2022.67) and fair value (2023.00). The most recent topics are fintech (2024.00), sustainable finance (2024.25), and investment decision-making and investments (both 2024.67). The keyword g24 has the highest average year (2025.40), but as a classification code it does not represent a topic. 

## _C. Density Visualization_ 



**Fig. 3.** Density visualization of keyword occurrences. 

Fig. 3 shows that the densest area is formed by venture capital and private equity, which reflects both their frequency and their many links. Areas of moderate density appear around the green cluster (entrepreneurship, innovation, startups, and fair value), around entrepreneurial finance, ESG, and investment decision-making, and around crowdfunding, machine learning, ipo, and fintech. Keywords such as emerging markets, performance measurement, impact investing, and initial public offerings lie in low-density areas, which is consistent with their lower frequencies and fewer links. 

## _D. Discussion_ 

Regarding RQ1, the keyword structure shows that VC and PE are the core of recent research, followed by entrepreneurial finance (8 occurrences), entrepreneurship (7), IPO (6), and innovation (6). The presence of nine clusters indicates a diverse field, with links to IPOs and exits [2], crowdfunding and data-driven methods [17], [18], and ESG and impact investing [13], [14], [15]. This diversity is consistent with the heterogeneous themes reported in earlier reviews [2], [18]. 

Regarding RQ2, entrepreneurial finance is the third most frequent keyword, and it co-occurs with venture capital in 6 articles and with private equity in 5. Its cluster also contains ESG, sustainable finance, and investment decision-making, which suggests that research on financing entrepreneurial firms is increasingly tied to sustainability and investment decisions [8], [13], [14]. Valuation, in contrast, appears only through fair value, which occurs three times and sits in the cluster with start-ups, innovation, and entrepreneurship, in line with studies that value start-ups through transactionbased multiples and exit-consistent models [3], [6]. The keyword valuation itself occurs only twice, and the dataset contains more than ten valuation-related keywords, such as start-up valuation, post-money valuation, discounted cash 

flow, and exit multiples, most of which appear once. By comparison, the word valuation appears in the title or abstract of 21 of the records. This gap shows that author keywords underrepresent valuation research and spread it across many low-frequency terms. 

Regarding RQ3, the most recent topics are investment decision-making, investments, sustainable finance, and fintech, whereas performance measurement, emerging markets, crowdfunding, and impact investing are associated with earlier years. This pattern suggests a shift from performance and market-context topics toward investment decisions and sustainability, which matches the growing attention to ESG in VC and PE [13], [14]. Because each of these keywords rests on three or four articles, the average years are indicative rather than conclusive. 

Several limitations should be noted. First, only 23 keywords reach the threshold, and 26 of the records have no author keywords, so the map reflects authors’ keyword choices rather than the full content of the articles. Second, because no thesaurus was applied, equivalent terms remain split across nodes; for example, ipo (6 occurrences) and initial public offerings (3) are shown separately, and the classification code g24 is retained as a node. Third, the clusters are based on a small number of articles per keyword and should be read as thematic tendencies. Future studies could combine author keywords with titles and abstracts, apply a keyword-cleaning procedure, or analyze a larger corpus to capture valuation research more completely. 

## V. CONCLUSION 

This study examined recent research on venture capital (VC), private equity (PE), and early-stage venture valuation through a bibliometric keyword co-occurrence analysis of 150 Scopus-indexed journal articles published between 2021 and 2026. The results show that venture capital and private equity are the central themes in the research network, 

connecting various topics, including entrepreneurial finance, entrepreneurship, innovation, crowdfunding, and sustainable finance. 

The findings also indicate that entrepreneurial finance is closely associated with ESG, sustainable finance, and investment decision-making. However, valuation research remains fragmented, as the keyword “valuation” appears only twice, while “fair value” is the only valuation-related keyword that meets the minimum occurrence threshold. This suggests that valuation-related research is not fully represented by the keywords used by authors, despite its importance in early-stage investment decisions. Furthermore, investment decision-making, sustainable finance, and fintech emerge as relatively recent research topics, reflecting the evolving priorities in venture capital and private equity research. 

Despite these findings, the study has several limitations. The analysis is based on a single database, includes only 150 journal articles, and relies on author keywords without applying a keyword-cleaning procedure. Future research could incorporate additional databases, analyze titles and abstracts, and standardize related valuation terms to provide a more comprehensive understanding of early-stage venture valuation. Overall, this study provides a current overview of the research landscape and highlights the need for clearer conceptual classification to strengthen the understanding of valuation in early-stage ventures. 

## **ACKNOWLEDGMENTS & CONTRIBUTORSHIP STATEMENT** 

This research was supported by Bina Nusantara University, Indonesia. The authors acknowledge the use of Scopus bibliographic data and VOSviewer software to support the bibliometric analysis and visualization of the study. Alfath Ilmi Effendy and Atthariq Arsyan Wahyudi contributed to data collection, data analysis, data processing, and manuscript preparation. Danang Prihandoko served as the research supervisor. The authors declare that they have no conflicts of interest related to this work. 

## REFERENCES 

- [1] R. Kumar, M. Firoz, and P. Kumar, “Renaissance of alternate finance: Bibliometric visualization of private equity and venture capital,” _Journal of Wealth Management_ , vol. 24, no. 2, pp. 114–128, 2021, doi: 10.3905/JWM.2021.1.142. 

- [2] D. Cumming, S. Kumar, W. M. Lim, and N. Pandey, “Mapping the venture capital and private equity research: a bibliometric review and future research agenda,” _Small Business Economics_ , vol. 61, no. 1, pp. 173–221, 2023, doi: 10.1007/s11187-022-00684-9. 

- [3] J. A. Barg, W. Drobetz, and P. P. Momtaz, “Valuing startup firms: A reverse-engineering approach for fair-value multiples from venture capital transactions,” _Finance Research Letters_ , vol. 43, p. 102008, 2021, doi: 10.1016/j.frl.2021.102008. 

- [4] A. Giakoumelou, A. Salvi, O. Kvasova, and I. Rizomyliotis, “The start-up's roadmap to private equity financing: substituting discounts with a premium in valuation for growth,” _International Journal of Entrepreneurial Behavior & Research_ , vol. 31, no. 2–3, pp. 479–497, 2025, doi: 10.1108/IJEBR-02-2022-0197. 

- [5] S. Peswani, “A venture capitalist’s endeavor: valuing a start-up for investment,” _Emerald Emerging Markets Case Studies_ , vol. 15, no. 4, pp. 1–13, 2025, doi: 10.1108/EEMCS-11-2024-0490. 

- [6] H.-G. Kang and D. Ryu, “A complementary valuation 

model and exit multiples,” _Finance Research Letters_ , vol. 79, p. 107182, 2025, doi: 10.1016/j.frl.2025.107182. 

- [7] L. J. Zheng, T. Bai, and A. R. Cross, “Signaling Information Management in Entrepreneurial Firms’ Financing Acquisition: An Integrated Signaling and Screening Perspective,” _Journal of Global Information Management_ , vol. 29, no. 6, p. 90, 2021, doi: 10.4018/JGIM.287590. 

- [8] T. H. Aas, M. Rossfjord, and K. Østlie, “Evaluating innovation in equity investment decisions: Insights from venture capital, private equity and equity fund perspectives,” _International Journal of Innovation Management_ , vol. 29, no. 09n10, p. 2540014, 2025, doi: 10.1142/S1363919625400146. 

- [9] E. Fricke, S. Fung, and M. S. Goktan, “Is “accredited crowdfunding” a lemons market? Evidence from 506(c) filings,” _Journal of Small Business Management_ , vol. 59, no. 2, pp. 312–336, 2021, doi: 10.1080/00472778.2020.1849715. 

- [10] R. Porro, T. Ercole, G. Pipitò, G. Vessio, and C. Loglisci, “Pathways to success: a machine learning approach to predicting investor dynamics in equity and lending crowdfunding campaigns,” _Journal of Intelligent Information Systems_ , vol. 63, no. 1, pp. 135–159, 2025, doi: 10.1007/s10844-024-00883-8. 

- [11] S. Singh and B. S. Mungila Hillemane, “Sources of finance for tech startups over its lifecycle: what determines their approach of sources and its success?,” _International Journal of Emerging Markets_ , vol. 18, no. 8, pp. 1766–1787, 2023, doi: 10.1108/IJOEM-06-20200705. 

- [12] H. Kraemer-Eis, J. Block, A. Botsari, F. Lang, S. Lorenzen, and W. Diegel, “Entrepreneurial finance in Europe and the Russian war against Ukraine,” _Journal of Technology Transfer_ , vol. 49, no. 6, pp. 2273–2305, 2024, doi: 10.1007/s10961-024-10067-9. 

- [13] W. Drobetz, S. El Ghoul, O. Guedhami, J. P. Hackmann, and P. P. Momtaz, “Entrepreneurial finance and sustainability: Do institutional investors impact the ESG performance of SMEs?,” _Journal of Business Venturing Insights_ , vol. 22, p. e00498, 2024, doi: 10.1016/j.jbvi.2024.e00498. 

- [14] E. M. Lange and N. G. Banadaki, “ESG consideration in venture capital: drivers, strategies and barriers,” _Studies in Economics and Finance_ , vol. 41, no. 3, pp. 724–739, 2024, doi: 10.1108/SEF-06-2023-0380. 

- [15] B. M. Barber, A. Morse, and A. Yasuda, “Impact investing,” _Journal of Financial Economics_ , vol. 139, no. 1, pp. 162–185, 2021, doi: 10.1016/j.jfineco.2020.07.008. 

- [16] G. Ross, S. Das, D. Sciro, and H. Raza, “CapitalVX: A machine learning model for startup selection and exit prediction,” _Journal of Finance and Data Science_ , vol. 7, pp. 94–114, 2021, doi: 10.1016/j.jfds.2021.04.001. 

- [17] V. Capizzi, A. Paltrinieri, D. Pattnaik, and S. Kumar, “Retrospective overview of the journal venture capital using bibliometric approach,” _Venture Capital_ , vol. 24, no. 1, pp. 1–23, 2022, doi: 10.1080/13691066.2022.2051769. 

- [18] C. R. Silva Júnior, Á. L. Neuenfeldt Júnior, J. Siluk, V. Gerhardt, and C. Michelin, “Evolution of start-up investments: an overview and future research directions,” _International Journal of Business Innovation and Research_ , vol. 37, no. 2, pp. 246–272, 2025, doi: 10.1504/IJBIR.2025.146987. 

- [19] D. Cumming and N. Dai, “Shadow capital in venture financing: Selection, valuation, and exit dynamic,” _Journal of Empirical Finance_ , vol. 78, p. 101514, 2024, doi: 10.1016/j.jempfin.2024.101514. 

- [20] A. Nazir and D. Tbaishat, “The impact of funding on 

market valuation in technology start-up firms: Implication _Technology, Market, and Complexity_ , vol. 9, no. 2, p. for open innovation,” _Journal of Open Innovation:_ 100028, 2023, doi: 10.1016/j.joitmc.2023.100028. 

