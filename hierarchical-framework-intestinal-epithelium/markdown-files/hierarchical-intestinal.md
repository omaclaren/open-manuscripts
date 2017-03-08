<!--
 HTML comment block.
 
 -->

---
header-includes:
- \usepackage{unicode-math}
- \usepackage{fncylab}
- \usepackage[right]{lineno}

title: "A hierarchical Bayesian framework for understanding the spatiotemporal dynamics of the intestinal epithelium"
abstract: 
author: O.J. Maclaren$^1$*, A. Parker$^2$, C. Pin$^2$, S.R. Carding$^{2,3}$, A.J.M. Watson$^{2,3}$, A.G. Fletcher$^{4,5}$, H.M. Byrne$^6$ and P.K. Maini$^6$
bibliography: "../bibtex-files/crypt-villus-refs.bib"
csl: "../csl/springer-vancouver.csl"

---

**1 Department of Engineering Science, University of Auckland, Auckland, New Zealand**\

**2 Gut Health and Food Safety Research Programme, Institute of Food Research, Norwich, United Kingdom**\

**3 Norwich Medical School, University of East Anglia, Norwich, United Kingdom**\

**4 School of Mathematics and Statistics, University of Sheffield, Sheffield, United Kingdom**\

**5 Bateson Centre, University of Sheffield, Sheffield, United Kingdom**\

**6 Wolfson Centre for Mathematical Biology, Mathematical Institute, University of Oxford, Oxford, United Kingdom**\

\***oliver.maclaren@auckland.ac.nz**

#Abstract
Our work addresses two key challenges, one biological and one methodological. First, we aim to understand how proliferation and cellular migration rates in the intestinal epithelium are related under healthy, damaged (Ara-C treated) and recovering conditions, and how these relations can be used to identify mechanisms of repair and regeneration. We analyse new data, presented in more detail in a companion paper, in which BrdU/IdU cell-labelling experiments were performed under these respective conditions. Second, in considering how to more rigorously process these data and interpret them using mathematical models, we develop a probabilistic, hierarchical framework. This framework provides a best-practice approach for systematically modelling and understanding the uncertainties that can otherwise undermine drawing reliable conclusions - uncertainties in experimental measurement and treatment, difficult-to-compare mathematical models of underlying mechanisms, and unknown or unobserved parameters. Both discrete and continuous mechanistic models are considered and related via hierarchical conditional probability assumptions. This allows the incorporation of features of both continuum tissue models and discrete cellular models. We perform model checks on both in-sample and out-of-sample datasets and use these checks to illustrate how to test possible model improvements and assess the robustness of our conclusions. This allows us to consider - and ultimately decide against - the need to retain finite-cell-size effects to explain a small misfit appearing in one set of long-time, out-of-sample predictions. Our approach leads us to conclude, for the present set of experiments, that a primarily proliferation-driven model is adequate for predictions over most time-scales. We describe each stage of our framework in detail, and hope that the present work may also serve as a guide for other applications of the hierarchical approach to problems in computational and systems biology more generally.

#Author Summary
The intestinal epithelium serves as an important model system for studying the dynamics and regulation of multicellular populations. It is characterised by rapid rates of self-renewal and repair; failure of the regulation of these processes is thought to explain, in part, why many tumours occur in the intestinal and similar epithelial tissues. These features have led to a large amount of work on estimating rate parameters in the intestine. There still remain, however, large gaps between the raw data collected, the experimental interpretation of these data, and speculative mechanistic models for underlying processes. In our view hierarchical statistical modelling provides an ideal, but currently underutilised, method to begin to bridge these gaps. This approach makes essential use of the distinction between 'measurement', 'process' and 'parameter' models, giving an explicit framework for combining experimental data and mechanistic modelling in the presence of multiple sources of uncertainty. As we illustrate, the hierarchical approach also provides a suitable framework for addressing other methodological questions of broader interest in systems biology: how to systematically relate discrete and continuous mechanistic models; how to formally interpret and visualise statistical evidence; and how to express causal assumptions in terms of conditional independence.

\linenumbers

# Introduction
## Motivation 
<!--
Primary motivation/context.
 -->
The intestinal epithelium provides crucial barrier, transport and homeostatic functions. These requirements lead it to undergo constant repair and regeneration, and dysfunctions can result in pathologies such as tumorigenesis [@Wright1984-kw; @Radtke2005-dh; @Reuss2010-fn; @Van_der_Flier2009-hw; @Turner2009-ei; @Marchiando2010-th; @Barker2014-xu]. While much work has been carried out on estimating the rate parameters in the intestine and other epithelia [@Wright1984-kw; @Kaur1986-xq; @Kaur1986-je; @Tsubouchi1983-tk], attempts to interpret these experimental data using mechanistic modelling remain inconclusive (see e.g. [@Dunn2013-tg; @Meineke2001-xi; @Loeffler1986-ej; @Loeffler1988-zb]). A key issue in drawing reliable conclusions is the lack of consistent and reproducible frameworks for comparing models representing conjectured biological mechanisms, both to each other and to experimental data. 

<!---
 Connecting the results of experiments to mechanistic understanding of biological processes remains challenging, however. 
 -->
This challenge goes in both directions: using experimental data (taken to be 'true') to parameterise and test mathematical or computational formalisations of mechanistic theories, and using these models (taken to be 'true') to predict, interpret and question experimental results. Both experimental measurements and mathematical models are subject to uncertainty, and we hence need systematic ways of quantifying these uncertainties and attributing them to the appropriate sources. Furthermore, establishing a common framework for analysing experimental results, formulating mechanistic models and generating new predictions has many potential advantages for enabling interdisciplinary teams to communicate in a common language and efficiently discover and follow promising directions as and when they arise.

<!--
 More specific methodological context.
 -->
## Approach
We address the above issues by developing a best-practice hierarchical Bayesian framework for combining measurements, models and inference procedures, and applying it to a tractable set of experiments targeting mechanisms of repair and regeneration in the intestinal epithelium. These experiments were performed ourselves and are presented in more detail in [@Parker2016-jf]. The aim of these experiments was to identify how proliferation rates, tissue growth and cellular migration rates are related under healthy, damaged (Ara-C treated) and recovering conditions, and how these relations can be used to identify mechanisms of repair and regeneration.

A notable feature of the Bayesian approach to probabilistic modelling is that all sources of uncertainty are represented via probability distributions, regardless of the source of uncertainty (e.g. physical or epistemic) [@Bernardo2009-uw; @Gelman2013-id; @Tarantola2005-sv]. We will adopt this perspective here, and thus we consider both observations and parameters to be random variables. Within a modelling or theoretical context, uncertainty may be associated with (at least): parameters within a mechanistic model of a biological or physical process, the mechanistic model of the process itself and the measurements of the underlying process. This leads, initially, to postulating a full joint probability distribution for observable, unobservable/unobserved variables, parameters and data.

Another key feature of the Bayesian perspective, of particular interest here, is that it provides a natural way of decomposing such full joint models in a *hierarchical* manner, e.g. by separating out processes occurring on different scales and at different analysis stages. A given set of hierarchical assumptions corresponds to assuming a factorisation of the full joint distribution mentioned above, and gives a more interpretable and tractable starting point. 

Our overall factorisation follows that described in [@Berliner1996-xr; @Tarantola2005-sv; @Cressie2011-sw; @Wikle2015-jq]. This comprises: a 'measurement model', which defines the observable (sample) features to be considered reproducible and to what precision they are reproducible (the measurement scale); an underlying 'process' model, which captures the key mechanistic hypotheses of spatiotemporal evolution, and a prior parameter model which defines a broad class of *a priori* acceptable possible parameter values. 

This hierarchical approach is being increasingly adopted - especially in areas such as environmental and geophysical science [@Berliner2003-yl; @Wikle2003-je], ecological modelling [@Cressie2009-wy; @Ogle2009-cb], as well as in Bayesian statistical modelling and inverse problems more generally [@Berliner1996-xr; @Tarantola2005-sv; @Cressie2011-sw; @Wikle2015-jq; see also @Gelman2013-id; @Blei2014-dh]. In our view, however, many of the advantages of hierarchical Bayesian modelling remain under-appreciated and it offers many opportunities for formulating more unified frameworks for model-data and model-model comparison. Furthermore, we note that a similar hierarchical approach has recently received significant development in the context of the non-Bayesian 'extended-likelihood' statistical modelling framework [@Pawitan2001-xm; @Pawitan2016-cz; @Lee2006-mr]. Thus, in our view, many of the benefits of the present approach can be attributed to its hierarchical aspect in particular ([@Cressie2011-sw] also emphasises this point). 

As illustration of some of the modelling benefits of the hierarchical approach, we show how both discrete and continuous process models can be derived and related using the hierarchical perspective. We discuss the connection of conditional/hierarchical modelling to the causal modelling literature (see [@Dawid2002-ry; @Dawid2010-ab; @Dawid2010-yg] for reviews) and illustrate the distinct roles of (Bayesian) predictive distributions vs. parameter distributions for model checking and the assessment of evidence, respectively (see [@Box1976-he; @Box1980-ch; @Evans2015-kg; @Gelman2013-wc; @Gelman2013-id] for discussion of these distinctions).

<!--
 Approach
 -->

## Conclusions
Our hierarchical Bayesian framework incorporates measurement, process and parameter models and facilitates separate checking of these components. This checking indicates, in the present application to the spatiotemporal dynamics of the intestinal epithelium, that much of the observed measurement variability is adequately captured by a simple measurement model. Similarly we find that a relatively simple process model can account for the main spatiotemporal dynamics of interest; however, model checking also identifies a minor misfit in the process model appearing over long time-scales. This motivates possible model improvements: we consider the inclusion of additional finite-cell-size effects in the process model, derived from a discrete process model and a subsequent continuum approximation formulated in terms of conditional probability. This only gives a slightly better qualitative fit to experimental data, however. We instead find that the dominant sources of the long-time misfits are probably due to some other factors - most likely relatively slow, time-varying proliferation rates (e.g. due to circadian rhythms). In summary, a primarily proliferation-driven model appears adequate for predictions over moderate time-scales. 


<!--
 Concluding comments
 ## Conclusions
 -->
# Materials and methods I: Experimental treatments and data processing
## Homeostasis mouse model
To obtain estimates of intestinal epithelial proliferation and migration rates under normal, homeostatic conditions in healthy mice, we used standard methods of proliferative cell labelling and tracing [@Wright1984-kw; @Kaur1986-xq; @Kaur1986-je; @Tsubouchi1983-tk; @Kozar2013-mr; @Vermeulen2013-ew; @Lopez-Garcia2010-bv] (see also [@Parker2016-jf] for full details). Actively proliferating cells in the intestinal crypts were labelled by single injection of the thymine analogue 5-bromo-2-deoxyuridine (BrdU) and labelled cells detected by immunostaining of intestinal sections collected from different individuals over time.  Migration of labelled cells traced from the base of crypts to villus tips was monitored over the course of 96 hours (5760 min). At least 30 strips were analysed per mouse. The figures presented in [@Parker2016-jf] show that strips were independent and obtained from one-cell thick sections. All strips in which the base of the crypt and the tip of the villus were clearly observed were considered. All sides of the crypt that were visible and connected to entire villi were analysed. There was no arbitrary selection of strips. A typical image from those analysed in [@Parker2016-jf] is also reproduced in the Supplementary information.

## Blocked-proliferation mouse model
To assess the effects of proliferation inhibition on crypt/villus migration, migrating and proliferating epithelial cells were monitored by double labelling with two thymine analogues (BrdU and IdU), administered sequentially a number of hours apart and subsequently distinguished by specific immunostaining in longitudinal sections of small intestine.  Following initial IdU labelling of proliferating cells at t= -17h (-1020 min, relative to Ara-C treatment), mice were then treated with cytosine arabinoside (Ara-C) at 250 mg/kg body weight, a dose reported to inhibit proliferation without causing major crypt cell atrophy (see [@Parker2016-jf] and references therein for full details). Tissues were collected over 24 hours, with BrdU administered one hour prior to collection to check for residual proliferation.  Successful inhibition of proliferation following treatment with Ara-C was confirmed by an absence of BrdU (S-phase) and phospho-Histone H3 (pH3) staining (M-phase) in longitudinal sections of small intestine (again, see [@Parker2016-jf] for full details).

## Recovering-proliferation mouse model
The above Ara-C treatment effect was observed to last for at least 10h (600 min). Cell proliferation resumed to near normal levels in samples obtained 18h (1080 min) post-Ara-C treatment. We hence considered samples collected at least 10h post-Ara-C treatment as corresponding to 'recovering-proliferation' conditions. 

## Data processing: reference grid and key observable features
To connect experimental measurements to the models discussed below we specified a reference grid and defined the key features of the data relative to this grid. These key features established an ideal 'underlying population' from which samples were considered to be drawn. This also allowed us to construct our hierarchical model in a 'top-down' (data-to-parameter) manner, starting from a measurement model.

![The (a) intestinal epithelium, (b) individual measurements as strips of cells and (c) collection of strips, where 'C' and 'V' indicated 'crypt' and 'villus' respectively.](../figures/figures_to_include/intestine-measurement.pdf){#fig:intestine-measurement}

With reference to Fig @fig:intestine-measurement, we considered the data to consist of a collection of one-dimensional 'strips' of cells. These strips ran from the base of the crypt to the tip of the villus, along the so-called 'crypt-villus' axis. This corresponds to how strips were collected experimentally, but does not account for possible biases due to 'angled' sampling [@Meineke2001-na; @Potten1988-tq]. Each measurement was given a spatial cell location index $i$ and a time label $t$. The location index was measured in number of cells along the crypt-villus axis, starting from the crypt base, and hence defined a discrete one-dimensional grid. The two labels $i$ and $t$ were also combined into a single index parameter $s := (i,t)$ when notationally convenient, which then defined a two-dimensional grid of space-time points. A 'typical' reference crypt-villus unit was characterised by the two vectors $(\mathbf{L},\mathbf{n})$, where $\mathbf{L}$ is the vector of labelled fractions at each grid point and $\mathbf{n}$ is the vector of number of samples at each grid point. This defines a useful reduction of the system from two spatial dimensions to one. 

We assumed that each strip was independent of the others as, in general, strips are taken from different crypt-villus units and/or animals after 'identical preparation'. Thus we did not ever directly possess, for example, measurements of a particular crypt with dimensions given in terms of a certain number of strips. We note, however, that in general the dynamics of strips in a given crypt may be affected by those in the same crypt. We did not consider this additional complexity in the present work, and so this complication should be kept in mind when interpreting the results. 

# Materials and methods II: Mathematical framework
Our hierarchical probability model was constructed on the basis of conditional probability assumptions. These allowed us to factor out a measurement model, a mechanistic model and a parameter model. 

## Overall hierarchical structure 
Our overall model structure consisted of a full joint distribution, conditioned on a given experimental treatment $E$ and known sample size vector $\mathbf{n}$, decomposed according to

$$p(\mathbf{y},\mathbf{L},\mathbf{k}|\mathbf{n},E) = p(\mathbf{y}|\mathbf{L},\mathbf{n})p(\mathbf{L}|\mathbf{k})p(\mathbf{k}|E).$$ {#eq:decomp}

where $\mathbf{k}$ are the cellular proliferation rates (these are discussed more fully in the Process models and Parameter model sections below). This hierarchical factorisation corresponds to the assumption of conditional independence between the various levels, i.e. $p(\mathbf{y}|\mathbf{L},\mathbf{k},\mathbf{n},E) = p(\mathbf{y}|\mathbf{L},\mathbf{n})$, $p(\mathbf{L}|\mathbf{k},\mathbf{n},E) = p(\mathbf{L}|\mathbf{k})$ and $p(\mathbf{k}|\mathbf{n},E) = p(\mathbf{k}|E)$. The first term, $p(\mathbf{y}|\mathbf{L},\mathbf{n})$ is the *measurement model*; the second term $p(\mathbf{L}|\mathbf{k})$ is the underlying *process model*, and the last term $p(\mathbf{k}|E)$ is a *prior parameter model*. These are discussed in more detail below.

 Notably, a 'causal' (structural invariance) assumption [@Pearl2009-qh; @Pearl2009-jp; @Dawid1979-gu; @Dawid2002-ry; @Dawid2010-ab; @Dawid2010-yg; @Woodward2003-oz; @Woodward1997-dk; @Spirtes2000-zd] is made by assuming that the experimental treatment condition affects the process parameter $\mathbf{k}$ but not the structure of the measurement or process models. In general, we suppressed, in our notation, the explicit conditioning on sample size $\mathbf{n}$, since it was taken to be fixed and known, as well as the conditioning on $E$ (keeping in mind that it only affects $\mathbf{k}$).

The assumptions underlying the above factorisation could be checked to some extent. This relied on a distinction between working 'within' the model - e.g. parameter estimation assuming the model and factorisation is valid - and working 'outside' the model, e.g. checking the validity of the model structural assumptions themselves [@Gelman2013-wc; @Gelman2013-id; @Evans2015-kg]. This distinction is made in the Results section.

Implicit in the model derivations, discussed below, we used a *deterministic expression of conservation of probability* for the process model, as is typical for such equations [@Van_Kampen1992-ik]. It sufficed for the presentation here to simply replace all functional dependencies on the process variable above with a dependence on the process parameters [@Tarantola2005-sv].

## Bayesian framework for predictions and incorporating information from observations  
The overall model of the previous section defined our initial 'generative' probabilistic model, prior to explicitly incorporating the information from our experimental data. This enabled samples to be drawn from both prior predictive and prior parameter models, in the usual way (see e.g. [@Gelman2013-id; @Maclaren2015-be] and the Computational methods section below). In particular, the prior predictive distribution was used in its usual form

$$\mathbf{y} \sim p(\mathbf{y}) = \int p(\mathbf{y}|f(\mathbf{k}))p(\mathbf{k})d\mathbf{k}$$ {#eq:prior-predictive}

which incorporates the aforementioned deterministic link between a given sample of process parameters and the output process variable, $\mathbf{L}=f(\mathbf{k})$. Note that here $\sim$ denotes 'distributed as', or more relevantly, 'samples drawn according to'.

To incorporate new data $\mathbf{y_0}$ we updated the parameters of the model, hence passing to a 'posterior predictive' model [@Gelman2013-id] 

$$\mathbf{y} | \mathbf{y_0} \sim p(\mathbf{y}|\mathbf{y_0}) = \int p(\mathbf{y}|f(\mathbf{k}))p(\mathbf{k}|\mathbf{y_0})d\mathbf{k}$$ {#eq:posterior-predictive}

where we used the conditional probability closure assumption $p(\mathbf{y}|f(\mathbf{k}),\mathbf{y_0}) = p(\mathbf{y}|f(\mathbf{k}))$. This closure assumption can be interpreted as maintaining our same mechanistic model despite new observations. This also connects well with current theories of causality as based on ideas of structural invariance [@Pearl2009-qh; @Pearl2009-jp; @Dawid1979-gu; @Dawid2002-ry; @Dawid2010-ab; @Dawid2010-yg; @Woodward2003-oz; @Woodward1997-dk; @Spirtes2000-zd].

The logical flow of the updating process we used is depicted in Fig @fig:update-process. This depicts the 'forward' predictive processes as arising from sequences of draws going from 'lower-level' to 'higher-level' distributions (though this does not correspond directly to the implementation - see Computational methods for specifics). Distributions were updated in the 'reverse' manner by conditioning at the highest level and propagating the implications of this back down the hierarchy. 

![Illustration of the Bayesian predictive and parameter inference processes. Following the arrows (1) to (2) we move from a prior parameter model (left, black) to associated predictive distribution (right, black) via the process and measurement models. Following the arrows (3) to (4) we condition on observed data to obtain a posterior parameter model (left, blue) and associated predictive distribution (right, blue). Our structural assumptions mean that the information gained is represented in updates of the parameter model while the process and measurement models maintain the same form. Modified from [@Maclaren2015-be], which was based on [@iglesias2014-uq].](../figures/figures_to_include/update-process.pdf){#fig:update-process}


## Measurement model 
The measurement model $p(\mathbf{y}|\mathbf{L},\mathbf{n})$ component was taken to be a binomial distribution $\mathcal{B}$ of the form

\begin{align}p(\mathbf{y}|\mathbf{L},\mathbf{n}) = \underset{s=0}{\overset{S-1}{\Pi}}\mathcal{B}(n_s,L_s).\end{align}

This related our 'raw' observable $\mathbf{y}$, the vector of counts of labelled cells at each grid point, to 'ideal characteristics' of comparison $(\mathbf{L},\mathbf{n})$,

This was developed as follows. Firstly we assumed that all observations at a given grid point $s$ were exchangeable (see [@Bernardo2009-uw; @Gelman2013-id] for a formal definition and further discussion) conditional on $(\mathbf{L},\mathbf{n})$. Such exchangeability conditions imply the existence of Bayesian probability models and correspond, in essence, to statistical reduction/symmetry assumptions [@Bernardo2009-uw; @Gelman2013-id]. We then adopted a slight strengthening [@Bernardo2009-uw; @Gelman2013-id] of the general exchangeability assumption - which only leads to a pure existence theorem - to an assumption of conditional independence. This assumes that if the true parameters are known at each location then observations can be made independently at those locations. 

This latter strengthening assumption is worth noting because it is related to the issue, discussed in the section on experimental methods above, of taking each strip to be independent and the corresponding reduction from two spatial dimensions to one spatial dimension. As such it represents a simplifying approximation and should be kept in mind when interpreting the subsequent results.

We also took the measurement component to be independent of $E$ - i.e. treatment was assumed to affect the underlying *process parameters* only (this is discussed in more detail in 'Overall hierarchical structure' above, and corresponds to a 'causal' assumption).
 
### Likelihood and normal approximation
The above defined our measurement component $p(\mathbf{y}|\mathbf{L},\mathbf{n})$ of the full sampling model for the probability of a set of observed labelled cells $\mathbf{y}$ in samples of sizes $\mathbf{n}$ given the vector of modelled underlying labelled fractions $\mathbf{L}$. This then defined a likelihood function $\mathcal{L}$ for this measurement model, which is proportional to the probability given by the sampling model evaluated for the observed data and considered as a function of $\mathbf{L}$, i.e.

$$\mathcal{L}(\mathbf{L};\mathbf{y},\mathbf{n}) = \underset{s=0}{\overset{S-1}{\Pi}}
L_s^{y_s}(1-L_s)^{n_s-y_s} \propto p(\mathbf{y}|\mathbf{L},\mathbf{n}) = \underset{s=0}{\overset{S-1}{\Pi}}\mathcal{B}(n_s,L_s).$$ {#eq:likel-binom}

We also used, for interpreting model misfit, the fact that for each $s$, if $n_s$ is sufficiently large and $L_s$ is not too close to 0 or 1 (e.g. $n_sL_s$ and $n_s(1-L_s) > 5$ is typical), then the binomial distribution $\mathcal{B}(n_s,L_s)$ can be replaced by the normal approximation $\mathcal{N}(n_sL_s,n_sL_s(1-L_s))$. In this case, denoting the set of all measured labelled fractions through the (useful, but slightly non-standard) notation $\mathbf{y}/\mathbf{n} := (y_1/n_1,...,y_S/n_S)$, 

$$\mathcal{L}(\mathbf{L};\mathbf{n},\frac{\mathbf{y}}{\mathbf{n}}) = p(\frac{\mathbf{y}}{\mathbf{n}}|\mathbf{L},\mathbf{n}) =
\underset{s=0}{\overset{S-1}{\Pi}} \frac{1}{\sigma_s
\sqrt{2\pi}}\exp{(-\frac{(\frac{y_s}{n_s}-L_s)^2}{2\sigma_s^2})}$$ {#eq:likel-norma}

where the standard deviations are given by $\sigma_s = \sqrt{\frac{L_s(1-L_s)}{n_s}}$. This normal approximation formulation was not used in the model fitting but provided a useful guide for checking model misfit based on residuals.

## Process models
Our process model was developed in a number of stages and considered at different levels of resolution. Firstly, we considered a discrete probabilistic model at the level of our measurement grid defined above. Then we considered two different continuous approximations to this - one excluding explicit cell-scale effects and one including explicit cell-scale effects.

### Discrete, measurement-grid-level process model 
Our basic 'process' model described the evolution of the (population) 'measurement' probability (labelled fraction) at the scale of the measurement grid. This was derived as follows.

With reference to Fig @fig:intestine-measurement, we considered a collection of one-dimensional 'strips' of cells. We used $l_i \in \{0,1\}$ as an indicator variable denoting the occupancy status of site $i$ of a given strip. The full state of this strip was given by the vector $\mathbf{l} = (l_0,l_1,...l_{S-1})$. 

We then sought a description of the probabilistic dynamics in terms of a discrete-time Markov chain for the probability distribution of the full state $p(\mathbf{l},t)$ following standard arguments [@Van_Kampen1992-ik; @Wilkinson2011-wh].

We began from an explicit joint distribution for the full state and then reduced it to description in terms of the set of 'single-site' probability distributions $p(l_i,t)$ for each site $i$. This derivation was aided by adopting an explicit notation: the probabilities of occupancy and vacancy at site $i$ at time $t$ were denoted by $p(l_i(t)=1)$ and $p(l_i(t)=0)$ respectively. Since $p(l_i(t)=1)+ p(l_i(t)=0) = 1$ we only needed to consider the probability of occupancy to fully characterise the distribution $p(l_i(t))$.

The equation of evolution for this probability was derived by considering conservation of probability in terms of probability fluxes in and out, giving, to first order in $\Delta t$

\begin{align}p(l_i(t+\Delta t)=1) &- p(l_i(t)=1) = \nonumber \\ &\Delta t\sum_{j=0}^{i-1}k_j\left[p(l_{i-1}(t)=1,l_{i}(t)=0)-p(l_{i-1}(t)=0,l_{i}(t)=1)\right]. \end{align}

The first term on the right gave a net 'influx of occupancy probability' due to a single division event somewhere at site $j < i$, each division event having a probability given by $k_j\Delta t$. This flux meant the value of the state variable $l_i(t) = 0$ could be replaced, at the next time step, by the value of $l_{i-1}(t) = 1$. The second term similarly represented a net 'outflux of occupancy probability' due to a division event somewhere at site $j < i$.

Since  $l_i(t)=0$ and $l_i(t)=1$ partitioned the event space of $l_i(t)$, we could use

$$p(l_{i-1}(t) = 1,l_i(t)=0) = p(l_{i-1}(t)=1) - p(l_{i-1}(t) = 1,l_i(t)=1)$$ {#eq:identities-one}
 
and similarly, since $l_{i-1}(t)=0$ and $l_{i-1}(t)=1$ partitioned the event space of $l_{i-1}(t)$, we had

$$p(l_{i-1}(t) = 0,l_i(t)=1) = p(l_{i}(t)=1) - p(l_{i-1}(t) = 1,l_i(t)=1). $$ {#eq:identities-two}

This led to the simplification in terms of only single-site probability distributions

$$p(l_i(t+\Delta t)=1) - p(l_i(t)=1) = \Delta t\sum_{j=0}^{i-1}k_j\left[p(l_{i-1}(t)=1)-p(l_i(t)=1)\right]. $$ {#eq:label-master-discrete-cons}

### Underlying continuous model - zeroth-order approximation
To aid model interpretation and model cross comparisons we introduced a smooth parameter field of underlying labelled fractions $L(x,t)$, defined over a continuous space-time domain. This gave a further idealisation of the 'underlying population' from which we envisaged the strips were sampled. This smoothness assumption, while not strictly necessary, meant some model properties could be interpreted in terms of local derivatives; it also reduced arbitrary dependence on discrete grid features, aiding future comparisons with off-lattice and/or continuum models (see [@Maclaren2015-be] for a review of various model types).

To derive the continuous approximation we first defined the position $x$ as a continuous coordinate passing through the discrete cell indices. For example $x = 0$ denoted the coordinate of the cell labelled '0' (base of the crypt), while $x = 0.5$ was the location halfway between the cell labelled '0' and that labelled 1'. Sample locations consisting of space-time pairs were denoted by $s = (x_s,t_s)$. Then, for sample locations $(i,t)$ corresponding to cell indices and arbitrary times, we matched the discrete model and continuous model using

$$p(l_i(t)=1|L(i,t)) = L(i,t)$$ {#eq:pop-param}

i.e. $L(i,t)$ served as the parameter for a single measurement modelled as a Bernoulli trial at that sample location (as in the above Measurement model section).

Next, the discrete dynamics of $p(l_i(t)=1)$ were 'transferred' to the continuous $L(x,t)$ dynamics. In particular, since $L(x,t)$ was taken to be a smooth function, we made the correspondence

\begin{align}p(l_{i-1}(t)=1|L(i-1,t)) &= L(i-1,t) \nonumber \\ &\equiv \nonumber\\ p(l_{i-1}(t)=1|L(i,t),L_x(i,t),...,\Delta x) &= L(i,t)-\Delta x \frac{\partial L(i,t)}{\partial x}+\frac{\Delta x^2}{2} \frac{\partial^2 L(i,t)}{\partial x^2} - ...\end{align} 

where $\Delta x = i-(i-1) = 1$ was the normalised cell length and we also conditioned on knowledge of the spatial derivatives at $i$, $L_x(i,t) = \frac{\partial L(i,t)}{\partial x}$ etc. The continuous spatial field effectively interpolated between - i.e. *internal* to - points of the discrete grid, making use of local derivative information. Substituting the above Taylor series, and similar expressions, into the discrete Markov equation @eq:label-master-discrete-cons led to 

$$\frac{\partial L(i,t)}{\partial t} + v(i)\frac{\partial L(i,t)}{\partial x} = \frac{1}{2}\left(\Delta x v(i) \frac{\partial^2 L(i,t)}{\partial x^2} - \Delta t \frac{\partial^2 L(i,t)}{\partial t^2}\right) + ...$$ {#eq:model-pde-ts}

where, for completeness, we also retained higher order terms in $\Delta t$ for the continuous model. We similarly assumed the existence of smooth functions $k(x,t)$ and $v(x,t)$ that satisfied the discrete relations

$$v(i,t) = \sum_{j=0}^{i-1} k_j \Delta x = \int_0^{i} k(x,t) dx + v(0). $$ {#eq:model-veloc-ts}

Furthermore, we assumed $k(x,t) = k(x)$, $v(x,t) = v(x)$ and $v(0) = 0$ in what follows. This assumption is discussed further in the Results section. 

We obtained 'closure' for the continuous model by keeping only the lowest order terms in both time and space, and further asserting that the equation structure obtained held *for all continuous $x$* and not just discrete $i$ (this could also be motivated by an assumption of grid translation invariance). This gave the advection equation

$$\frac{\partial L(x,t)}{\partial t} + v(x)\frac{\partial L(x,t)}{\partial x} = 0$$ {#eq:model-pde}

with

$$v(x) = \int_0^{x} k(x') dx'.$$ {#eq:model-veloc}

When we incorporated cell death, with discrete rates $d_i$, this led to the same equations with $k$ replaced by $k-d$, where $d(x,t)$ was defined similarly to $k(x,t)$. Hence we interpreted $k$ in the above as the net cell production rate (which hence could be negative).

The above partial differential equation has an interpretation as the advection of a tracer in an incompressible fluid field with a source, and is sometimes referred to in this context as the 'colour equation' [@LeVeque2002-eq].  

### Underlying continuous model - higher-order spatial effects
Our 'zeroth-order' continuous approximation above was obtained by neglecting all higher-order terms in $\Delta x$. We conceived of this as a process of 'continualisation' - the reverse process of discretising a continuous equation to obtain a numerical scheme (see e.g. [@Askes2005-cd] and [@LeVeque2002-eq] Section 8.6 for similar ideas). We thus expected that a better continuum approximation could be obtained by retaining higher-order spatial derivatives and hence finite-cell-size effects. 

As described below, retaining the higher-order spatial derivative naturally gave rise to a Fokker-Planck equation containing a diffusion term [@Van_Kampen1992-ik]. Equations of this (and similar) form have been derived before, also based on continuous approximations to discrete master equations (e.g. [@Baker2010-ne; @Hywood2013-zf; while @Fozard2010-hd; @Murray2009-zg] also contain similar ideas; [@Maclaren2015-be] gives additional references). 

<!---

--->

To derive this higher-order approximation we reconsidered the expansion in @eq:model-pde-ts. We again neglected all terms of order $\Delta t$, but here retained the next order spatial derivative leading to

$$\frac{\partial L(x,t)}{\partial t} + v(x)\frac{\partial L(x,t)}{\partial x} = D(x)\frac{\partial^2 L(x,t)}{\partial x^2}$$ {#eq:model-pde-higher-two}

where $D(x) = (1/2)\Delta x v(x)$.

Retaining the second spatial derivative hence amounted to accounting for spatial effects due to finite cell sizes. We first evaluated our original 'zeroth-order' (advection) model against our data, but also examined the extent to which higher-order spatial terms such as those considered above could account for any misfits. 

## Parameter model
Since we adopted a Bayesian perspective in this work we required a parameter prior model to express additional modelling assumptions ([@Gelman2013-id] provides an applied account of the role of priors in Bayesian inference, while [@Gelman2013-wc] presents a more philosophical perspective).
 
Candidate proliferation profiles, varying with cell locations, were represented as realisations from a prior given in terms of a discretised random field (a random vector) $\mathbf{k}$ of length $m=5$, modelled as a multivariate Gaussian $\mathcal{N}(\symbf{\mu},\mathbf{C})$ with joint distribution

$$p(\mathbf{k}) = \frac{1}{(2\pi)^m\sqrt{\mbox{det}(\mathbf{C})}}\exp(-(\mathbf{k}-\symbf{\mu})^T\mathbf{C}^{-1}(\mathbf{k}-\symbf{\mu})/2)$$ {#eq:prior}

characterised by its mean vector $\symbf{\mu}$ and covariance matrix $\mathbf{C}$. This parameter prior constrained the variability of the spatially varying parameter field *a priori* to help avoid unphysical solutions.  

The covariance matrix was first decomposed into a standard deviation matrix given by the outer (tensor) product of the standard deviation vector for each variable, $\mathbf{S} = \symbf{\sigma}\symbf{\sigma}^T$, and correlation matrix $\mathbf{R}$. These multiply element-wise to give $C_{ij} = S_{ij}R_{ij}$ (no summation). We then adopted the common, equivalent, representation $\mathbf{C} = \mathbf{D}\mathbf{R}\mathbf{D}$ where $\mathbf{D}$ is a diagonal matrix with diagonal entries $D_{ii} = \sigma_i$. 

This decomposition of the covariance matrix into separate parts was adopted because it we felt it presented a clearer picture of how the smoothness and magnitude of variations are controlled via off-diagonal and diagonal terms, respectively, in addition to the mean response. We also varied these prior assumptions to explore the solution dependence on parameter variability (and, as discussed below, our code is made available for further sensitivity tests).

We took the correlation matrix $\mathbf{R}$ to have the squared-exponential (Gaussian) correlation function $k(i,j) = \exp(\frac{(i-j)^2}{2l_c^2})$, where $l_c$ is a parameter controlling the characteristic length-scale of the correlations in terms of number of indices of $\mathbf{k}$. This characteristic length scale gives the number of $\mathbf{k}$ indices over which the correlation function decays to $1/e$. This allowed us to control the 'smoothness' of the realisations from the $\mathbf{k}$ prior, in the sense that as $l_c$ is increased the values $\mathbf{k}_i$ and $\mathbf{k}_j$ tend to be more similar.

The matrix $\mathbf{R}$ was generated by evaluating this correlation function at discrete locations along the crypt-villus axis. This discretisation was chosen to be coarser than the measurement grid and gave a variation somewhat similar to compartment-style regions of proliferation activity. This corresponded to assuming that the cell-type and associated proliferation rates varied on a coarser scale than individual cells, and was thus somewhat similar to a compartment-style assumption [@Johnston2007-pq; @Carulli2014-bd], though the resulting proliferation rate function is defined for all values of the finer, individual-cell scale $x$.  The parameter $l_c$ could also be interpreted as a 'parameter correlation length' for the proliferation rates, a measure of the number of parameters - or number of 'compartments' - over which the correlations decay. We considered correlation lengths of 1-2 parameters.

We found it most informative to visualise realisations of the whole function from the resulting prior rather than simply give the individual parameters/matrices separately ([@Tarantola2005-sv] discusses this visualisation approach to priors in more detail). These are hence discussed and displayed in more detail in the Results section below.

## Computational methods 
### Implementation of MCMC sampling and Bayesian updating
To implement the updating from prior to posterior parameter distributions, given measurements, we used Monte Carlo Markov Chain (MCMC) sampling (see [@Robert2013-gx] for a comprehensive reference). In particular, we used the (open source) Python package *emcee* (http://dan.iel.fm/emcee/) which implements an 'affine-invariant ensemble sampler' MCMC algorithm and has been applied in particular to astrophysics problems (see [@Foreman-Mackey2013-mb] for details). Given samples from the resulting prior and posterior parameter distributions, respectively, prior and posterior predictive distributions were obtained by forward simulation of the process model described below. We note that each candidate proliferation rate vector $\mathbf{k}$ is connected to the measurements $\mathbf{y}$ via the latent vector $\mathbf{L}$; since this step is deterministic, however, no additional sampling steps were required for the process model component.

### Differential equations
For the results in all sections other than the final results section in which we include higher-order spatial effects, we solved the differential equation model using the *PyCLAW* [@Ketcheson2012-od; @Pyclaw2014-py] Python interface to the *CLAWPACK* [@Clawpack2014-cs] set of solvers for hyperbolic PDEs. We adapted a Riemann solver for the colour equation available from the Riemann solver repository (https://github.com/clawpack/riemann). For testing the inclusion of higher-order spatial effects (thus changing the class of our equations from hyperbolic to parabolic) we used the Python finite-volume solver *FiPy* [@Guyer2009-sq].

### Data and source code availability
Our code is available in the form of a Jupyter Notebook (http://ipython.org/notebook.html) in the Supplementary Information. To run these we used the Anaconda distribution of Python (https://store.continuum.io/cshop/anaconda) which is a (free) distribution bundling a number of scientific Python tools. Any additional Python packages and instructions which may be required are listed at the beginning of our Jupyter Notebook.

## Interpretation of statistical evidence
We have described above how mechanistic or causal assumptions relate to assumptions of structural invariance under different scenarios. In order to interpret the results that follow, however, we also required an interpretation of the 'statistical evidence' that a set of measurements provided about parameter values within a fixed model structure. This proved a surprisingly controversial topic and we encountered continuing debate about fundamental principles and definitions of statistical evidence [@Royall1997-ai; @Mayo2014-pz; @Evans2014-gn; @Evans2015-kg; @Taper2016-la]. 

Following our conditional modelling approach, we decided to adopt the simple - yet quite generally applicable - principle of evidence based on conditional probability: if we observe $b$ and $p(a|b) > p(a)$ then we have evidence for $a$. A 'gold-standard' theory of statistical evidence starting from this premise has been developed and defended recently by Evans in a series of papers (summarised in [@Evans2015-kg]). Besides simplicity, a nice feature of this approach, that we used below, is that it can be applied both to prior and posterior predictive distribution comparisons such as $p(\mathbf{y}|\mathbf{y_0}) \overset{?}{>} p(\mathbf{y})$, as well as to prior and posterior parameter distribution comparisons such as $p(\mathbf{k}|\mathbf{y_0}) \overset{?}{>} p(\mathbf{k})$. This approach is not without criticism, however (again, see [@Royall1997-ai; @Mayo2014-pz; @Evans2014-gn; @Evans2015-kg; @Taper2016-la] for an entry point to the ongoing debates).

Another notable feature of the interpretation of statistical evidence that we adopted below is that we emphasised the visual comparison of various prior and posterior distributions, rather than adopting arbitrary numerical standards ([@Tarantola2005-sv] advocates a similar 'movie strategy' for the interpretation of statistical evidence and inference procedures, [@Gelman2004-bk; @Gelman2013-id; @Gelman2013-wc; @Davies2014-dz] similarly emphasise the benefits of graphical visualisation methods in statistics). 

# Results
## Parameter inference under homeostatic (healthy) conditions
Fig @fig:BrdU-prior-to-posterior-prolif-vel illustrates the process of updating from realisations of the prior distributions of the proliferation and velocity fields to realisations of their posterior (post-data) distributions. The left-hand side of the figure shows simulations from the prior distribution for proliferation field (top) and realisations from the induced distribution for the velocity field (bottom), respectively. The right-hand side shows the corresponding simulations after the prior parameter distribution has been updated to a posterior parameter distribution. The prior-to-posterior parameter estimation was carried out using the MCMC sampling approach described above with $t = 120$ min (2 h) as an initial condition and $t = 360$ min (6 h) and $600$ min (10 h) as given data. The initial condition for the underlying labelled fraction was determined by fitting a smoothing spline to the data. The prior distribution for the proliferation field shown in Fig @fig:BrdU-prior-to-posterior-prolif-vel incorporated a weak mean trend in net proliferation rates, rising from the crypt base to the mid-crypt before falling exponentially to zero over the last few parameter regions post-crypt end, and a parameter correlation length of 1. These assumptions can be relaxed/varied with little effect, though typically a non-zero parameter correlation length and a shut-off in proliferation after the crypt end produce more stable (well-identified) estimates. As mentioned, the code is available for use and so these assumptions are able to be varied by future researchers. Additional visualisations of the parameter inferences are also provided in the Supplementary information.

![Simulated realisations from the prior (left) and posterior (right) distributions for proliferation profiles (top) and velocities (bottom). After data are obtained the posterior distributions are much more tightly-constrained, and are picking out biologically plausible results (see main text).](../figures/figures_to_include/BrdU-prior-to-posterior-prolif-vel.pdf){#fig:BrdU-prior-to-posterior-prolif-vel}

## Parameter inference for blocked proliferation conditions 
Fig @fig:AraC-prior-to-posterior-prolif-vel is the same as Fig @fig:BrdU-prior-to-posterior-prolif-vel described in the previous section, but this time under treatment by Ara-C. The previous results from the baseline case are shown in grey, while the new results under Ara-C treatment are shown in blue. Here 1140 min (19 h post IdU labelling, 2 h post Ara-C treatment) was used as the initial condition and 1500 min (25 h post IdU labelling, 8 h post Ara-C treatment) used for fitting. The intermediate time 1260 min (21 h post IdU labelling, 4 h post Ara-C treatment) and later time 1620 min (27 h post IdU labelling, 10 h post Ara-C treatment) were used as out-of-sample comparisons (see later).

![Simulated realisations from the prior (left) and posterior (right) distributions for proliferation profiles (top) and velocities (bottom) under Ara-C treatment (blue) as compared to no treatment (grey). The velocities are reduced to near zero, as are the proliferation rates, though the latter are noisier.](../figures/figures_to_include/AraC-prior-to-posterior-prolif-vel-legend.pdf){#fig:AraC-prior-to-posterior-prolif-vel}

As can be seen, there is a clear inhibition of proliferation and an even clearer effect on the migration (growth) velocity. The underlying parameter results are clearly more variable than those in the baseline case. This may indicate, for example, greater parameter underdetermination and/or inconsistency of the model. This is not surprising as we expect all the proliferation parameters to be reduced to similar (low) values and hence the parameters become less distinguishable.

To add additional stability to the results we can attempt to reduce underdetermination in the parameters by increasing the parameter correlation length and inducing an effectively more 'lumped' representation of the parameter field (since values tend to stick together more). Doing this removed the more extreme negative net proliferation in the posterior profile, however it still allowed for small amounts of negative net proliferation/velocity (the available Jupyter notebook can be used to explore various prior assumptions). 

Again, the need to introduce more stability is likely due to some combination of the limitations of resolution, a consequence of trying to fit the data too closely, or an indication of model inadequacies. In particular, under inhibited-proliferation conditions the effective number of parameters would be expected to be reduced. When fitting the full model, with largely independent parameters for each region, it is to be expected that some additional regularisation would be required for greater stability.  

## Parameter inference for recovering proliferation conditions
Ara-C is metabolised between 10-12 h post-treatment. The two times considered here, 1620 min and 2520 min, correspond to 10 h and 25 h post Ara-C treatment, respectively, i.e to the end of the effect and after the resumption of proliferation. Hence, to check for the recovery of proliferation, we fitted the model using 1620 min as the initial condition and 2520 min as the final time. 

Fig @fig:AraC-recovery-prior-to-posterior-prolif-vel is the same as Fig @fig:BrdU-prior-to-posterior-prolif-vel and Fig @fig:AraC-prior-to-posterior-prolif-vel described in the previous sections, but this time after/during recovering from treatment by Ara-C. The previous results from the baseline case are shown in grey, while the new results following recovery from Ara-C treatment are shown in blue. Here 1620 min (27 h post IdU labelling, 10 h post Ara-C treatment) was used as the initial condition and 2520 min (42 h post IdU labelling, 25 h post Ara-C treatment) used for fitting. We did not make additional out-of-sample comparisons in this case, though in-sample posterior predictive checks were still carried out (see later).

Here the proliferation and velocity profiles indicate that proliferation has resumed, as expected. The rates of proliferation appear to be lower than under fully healthy conditions, however, perhaps due to incomplete recovery (the initial condition being right at the beginning of the recovery period). The timing of the recovery of proliferation and the well-identified proliferation and velocity profiles inferred give no indication that any other mechanism is required to account for these data, however.

![Simulated realisations from the prior (left) and posterior (right) distributions for proliferation profiles (top) and velocities (bottom) after recovery from Ara-C treatment (blue) as compared to no treatment (grey). The velocities and proliferation rates show a clear recovery towards healthy conditions, though not to the full level.](../figures/figures_to_include/AraC-recovery-prior-to-posterior-prolif-vel-legend.pdf){#fig:AraC-recovery-prior-to-posterior-prolif-vel}

## Predictive checks under homeostatic (healthy) conditions
Fig @fig:BrdU-prior-to-posterior-label illustrates simulations from the predictive distributions corresponding to the prior and posterior parameter distributions of Fig @fig:BrdU-prior-to-posterior-prolif-vel. This enables a first self-consistency check - i.e. can the model re-simulate data similar to the data to which it was fitted [@Gelman2004-bk; @Gelman2013-id]. If this is the case then we can (provisionally) trust the parameter estimates in the previous figure; if this was not the case then the parameter estimates would be unreliable, no matter how well-determined they seem. Here the model appears to adequately replicate the data used for fitting.

![Simulated realisations from prior (top) and posterior (bottom) predictive distributions (grey) for label data at fitted times (120 min, 360 min and 600 min i.e. 2 h, 6 h and 10 h). Actual data are indicated by black lines. Again the posterior distributions are much more constrained than the prior distributions, representing the gain in information from collecting (and fitting to) experimental data. The first profile in each panel is held as a constant initial condition in this example.](../figures/figures_to_include/BrdU-prior-to-posterior-label-legend.pdf){#fig:BrdU-prior-to-posterior-label}

Fig @fig:BrdU-future-realisations-1080-min and Fig @fig:BrdU-posterior-characteristics illustrate two additional ways of visualising replicated datasets. The former visualises the label profile along the crypt-villus axis at the future unfitted/out-of-sample time 1080 min (18 h), while the latter visualises both fitted (120 min/2 h, 360 min/6 h and 600 min/10 h) and unfitted/out-of-sample (1080 min/18 h) predictions plotted in the characteristic plane $(t,x)$ in which the slopes along lines of constant colour should be inversely proportional to the migration velocities at that point, due to the (hyperbolic) nature of our 'colour' equation (see e.g. [@LeVeque2002-eq]). We have interpolated between the dotted grid lines. These figures, in combination with Fig @fig:BrdU-prior-to-posterior-label above, indicate that the model is capable of reliably reproducing the data to which it was fitted, as well as predicting key features of unfitted datasets such as the rate of movement of the front. On the other hand, there is clearly a greater misfit with the predicted rather than fitted data. In order to locate the possible source of misfit we considered various model residuals and error terms - see 'Locating model misfit' below.

![Simulated realisations from prior (left) and posterior (right) predictive distributions (grey) for label data at the unfitted (out-of-sample) time 1080 min (18 h). Actual data are indicated by black lines. The model appears to give reasonable predictions capturing the main effects, but there is also clearly some misfit to be explored further.](../figures/figures_to_include/BrdU-future-realisations-1080-min-legend.pdf){#fig:BrdU-future-realisations-1080-min}

![Actual (smoothed) data (left, black box) and one replication based on the model (right; plotting the latent/measurement-error-free process) as visualised in the characteristic plane. This has been discretised and interpolated between the dotted lines to facilitate fair but coarse-grained comparisons. The model structure implies that there should be lines of constant colour tracing out curves with slopes inversely proportional to the migration velocities at that point. The model again captures a number of these key qualitative features, but also fits less well for the out-of-sample (above the horizontal gap at 600 min/10 h) data. There is little variability in the latent model process and so only one replication is shown.](../figures/figures_to_include/BrdU-posterior-characteristics.pdf){#fig:BrdU-posterior-characteristics}

## Predictive checks under blocked proliferation conditions
Here 1140 min (19 h; post IdU labelling) was used as the initial condition and 1500 min (25 h) used for fitting. 1260 min (21 h) and 1620 min (27 h) were used as out-of-sample (non-fitted) comparisons. Fig @fig:AraC-posterior-label-all is analogous to Fig @fig:BrdU-prior-to-posterior-label in the healthy case. In general all of the features up to 1620 min (27 h) in Fig @fig:AraC-posterior-label-all, and for both fitted and predicted times, appear to be reasonably well captured. The fit at 1620 min is generally good, but perhaps worse than the other cases. This could be due to both errors in longer-time predictions and to the beginning of proliferation recovery. We explore both longer-time misfits and recovering proliferation conditions in what follows.

![Simulated realisations from posterior predictive distributions (grey) for label data at 1140 min (initial condition), 1500 min (fitted time) and at two out-of-sample/unfitted times (1260 and 1620 min). The posterior distributions appear to adequately capture the actual label data (black).](../figures/figures_to_include/AraC-posterior-label-all-legend.pdf){#fig:AraC-posterior-label-all}

## Predictive checks under recovering proliferation conditions
As discussed above, Ara-C is metabolised between 10-12 h post-treatment. The two times considered here, 1620 min and 2520 min, correspond to 10 h and 25 h post Ara-C treatment, respectively, i.e to the end of the effect and after the resumption of proliferation. 

Again, as expected, the label has resumed movement in concert with the resumption in proliferation. The model appears to fit reasonably well.


![Simulated realisations from posterior predictive distributions (grey) for label data at 1620 min (initial condition) and 2520 min (fitted). These indicate that proliferation has resumed, consistent with the time taken to metabolise Ara-C - see the main text for more detail.](../figures/figures_to_include/AraC-recovery-prior-to-posterior-label-legend.pdf){#fig:AraC-recovery-posterior-label-all}


## Locating model misfit
While the zeroth-order model behaves essentially as desired under experimental perturbation, and is likely capturing the essential features of interest, we observed some some minor model misfit. We used posterior predictive checks to unpick the contributions of the various model parts and determine the source(s) of misfit. This in turn motivated potential model improvements. These checks were carried out under baseline (healthy) conditions as we were more confident of the experimental effects under this scenario, but they can equally be carried out for the other datasets. Note, however, that time-varying effects are not expected to be as relevant under conditions of inhibited proliferation.

Fig @fig:BrdU-posterior-residuals shows the following checks: measurement error as determined by subtracting a smoothed spline from the observed data (dark line) and comparing these to the results obtained by subtracting the process model from the simulated data (panels 1-4, moving left-to-right and top-to-bottom, showing fitted - 120 min/2 h, 360 min/6 h and 600 min/10 h - and unfitted/out-of-sample - 1080 min/18 h - times). This presentation follows the noise-checking approach in [@Aguilar2015-um], as well as the general recommendations given in [@Gelman2004-bk; @Gelman2013-id]. Reliable interpretation of these as 'true' measurement residuals depends on the validity of the normal approximation @eq:likel-norma since these expressions are not directly interpretable in terms of the discrete binomial model (see e.g. [@Gelman2004-bk; @Gelman2013-id]). These are also visualised in terms of the corresponding cumulative distributions in the middle panel (panel 5, following as above). Panels 6-9 show the differences between the underlying process model and the smoothed spline fitted to the data. As can be seen, the measurement model appears approximately valid at all times, while the process model appears to have non-zero error for the 1080 min sample. We consider this in more detail next.

![Model and data residual components. Panels 1-4, moving left-to-right and top-to-bottom, shows measurement error as determined by subtracting a smoothed spline from the observed data (dark line) and comparing this to the results obtained by subtracting the process model for fitted - 120, 360 and 600 mins - and unfitted/out-of-sample - 1080 min - times from the realised data (grey). These measurement error distributions are also visualised in terms of the corresponding cumulative distributions in the middle panel (panel 5, following as above. Black - actual data, grey - model simulations). Panels 6-9 show the differences between realisations of the underlying process model and the smoothed spline fitted to the data. As can be seen across panels, the measurement model appears approximately valid at all times, while the process model appears to have non-zero error for the 1080 min sample. This observation is discussed in the text.](../figures/figures_to_include/BrdU-posterior-residuals-legend.pdf){#fig:BrdU-posterior-residuals}

## Possible model improvement and robustness - higher-order spatial effects
As discussed in the process model section above, the presence of cellular structure in the epithelial tissue means that higher-order spatial effects could be present. One way of deciding whether these are important is to consider the extent to which these may account for the minor misfit identified above, as opposed to other factors such as time-varying proliferation rates. To do this we considered both uniform percentage reductions of the original parameter estimates (approximating time-varying rates) and the inclusion of higher-order spatial terms. 

Fig @fig:BrdU-comparison-diffusion-correction gives an idea of the qualitative differences induced by including the higher-order spatial terms and those that could be induced by time-varying proliferation rates. This figure is based on the (healthy) 1080 min (18 h) data in which we found some indication of a process model error. 

 We see that while the higher-order model appears to give a slightly better qualitative fit to the data, both the higher-order and lower-order models require similar reductions of the parameter values to quantitatively improve the fit to our out-of-sample data. The reduced parameter values shown in Fig @fig:BrdU-comparison-diffusion-correction correspond to a reduction of 20\%, which was chosen visually as a reduction accounting for the bulk of the misfit.

Thus the key (yet relatively small) difference between the model and out-of-sample data is likely due to an effect other than finite-cell sizes; in this case it is likely due to time-variation in parameter values due to circadian rhythms (we have assumed steady-state parameter values). Other potential factors include label dilution or an unmodelled mixing phenomenon in the full two-dimensional case. We note however that these effects are small and appear to be important primarily for predicting much further ahead in time than the fitted data and the steady-state parameter assumption is likely valid for reasonable time intervals. This means that the more easily interpretable original model may be sufficient for many purposes.

![Comparison of the modified process model which includes higher-order spatial terms (blue) to the original model (grey, dashed), both at lowered proliferation rates (decreased 20\%), which is required for a better fit to the data. The original model at the original fitted proliferation rates is also shown (grey, solid). Although the model with higher-order spatial terms gives a better qualitative fit to the data for the same proliferation rates, it is clear that the dominant cause of misfit is better attributed to (time) varying proliferation rates (in the context of the present set of models).](../figures/figures_to_include/BrdU-comparison-diffusion-correction-legend.pdf){#fig:BrdU-comparison-diffusion-correction}

# Discussion 
Understanding the complicated dynamics of the intestinal epithelium requires an interdisciplinary approach involving experimental measurements, mathematical and computational modelling, and statistical quantification of uncertainties. While a diverse range of mathematical models have been constructed for epithelial cell and tissue dynamics (reviewed in [@Johnston2007-pq; @Carulli2014-bd; @Kershaw2013-jb; @De_Matteis2013-zo; @Fletcher2015-yc]), from compartment models to individual-based models to continuum models, we lack consistent and reproducible frameworks for comparing models representing conjectured biological mechanisms both to each other and to experimental data (for an overview, see our review [@Maclaren2015-be]). These shortcomings may explain why questions such as the connection between proliferation and migration and its variation under experimental perturbations remain open, despite much investigation [@Kaur1986-xq; @Kaur1986-je; @Tsubouchi1983-tk; @Loeffler1986-ej; @Loeffler1988-zb; @Meineke2001-xi; @Dunn2013-tg].

The aim of the present work was to acknowledge and confront these difficulties explicitly, and to present some initial constructive steps in establishing such a framework. To do this we carried out new experiments (described more fully in a companion paper [@Parker2016-jf]) aimed at determining how proliferation rates, tissue growth and cellular migration rates are related in the intestinal epithelium under healthy, damaged (Ara-C treated) and recovering conditions. We performed BrdU/IdU cell-labelling experiments under these respective conditions. In considering how to best process these data and interpret them using mathematical models, we then developed a probabilistic, hierarchical (conditional) framework. 

Our hierarchical framework provides a best-practice approach for systematically modelling and understanding the uncertainties that could lead to unreliable mechanistic conclusions - uncertainties in experimental measurement and treatment, difficult-to-compare mathematical models of underlying mechanisms, and unknown or unobserved parameters. Our approach was influenced by recognising the benefits that the hierarchical Bayesian approach has demonstrated in applications across a number of different disciplines (e.g. in environmental and geophysical science as in [@Berliner2003-yl; @Wikle2003-je]; ecological modelling as in [@Cressie2009-wy; @Ogle2009-cb]; and in Bayesian statistical modelling and inverse problems more generally as in [@Berliner1996-xr; @Tarantola2005-sv; @Cressie2011-sw; @Wikle2015-jq; @Gelman2013-id; @Blei2014-dh]). We also note that a hierarchical approach can have significant benefits outside the Bayesian framework (see for example the 'extended likelihood' approach described in [@Pawitan2001-xm; @Pawitan2016-cz; @Lee2006-mr]).

The hierarchical approach has advantages not only in terms of providing a framework for combining disparate sources of uncertainty, but also as a framework for facilitating modelling derivations and relating discrete and continuous models. Though the resulting measurement, process and parameter models can or have all been derived by other means, as far as we are aware this particular perspective has not been systematically utilised in the same manner as considered here - at the very least it appears uncommon within the mathematical/systems/computational biology communities. Furthermore, in the main text we noted the connections of our conditional, probabilistic approach for relating discrete and continuous models to similar procedures in the numerical analysis literature. This raises exciting connections to the developing field of probabilistic numerical methods and computing [@Hennig2015-im].

We also note the connection between the choice of a measurement model as required here (and/or process model error, and following e.g. [@Berliner1996-xr; @Berliner2003-yl; @Wikle2015-jq; @Cressie2011-sw; @Mosegaard2002-lx; @Tarantola2005-sv]), and the development of approximate sampling and parameter fitting procedures, which are particularly useful for analytically difficult models. A key concern of the latter is the appropriate choice of summary statistics for constructing a 'synthetic likelihood' [@Wood2010-hp] or similarly-modified posterior target for Approximate Bayesian Computation (ABC) [@Marin2012-fd; @Wilkinson2013-rs; @Ratmann2009-de].  This choice determines (implicitly or explicitly) in which ways a given model or set of models can be considered an 'adequate' representation of the data, which features are considered to be reproducible and what the associated 'noise' structure should be ([@Davies2014-dz] presents an alternative approach to characterising data features and model adequacy). These issues are crucial in deciding how to model the complexity of epithelial cell and tissue dynamics. 

An important next step, as described above, would be to bring more process model types into this framework and to evaluate and compare them under carefully modelled experimental conditions. Extensions incorporating other mechanical and/or cellular-level information (e.g. [@Dunn2013-tg; @Meineke2001-xi]) into process models would provide a natural next step. Importantly, due to the separation between measurement and process model components, these more complex process models could be incorporated into our present framework simply by replacing our process model component with a new model, while retaining the same measurement model. Of course additional parameters would require additional prior assumptions, and if additional data features were of interest then these would need to be incorporated into a modified measurement model. The benefit of a hierarchical framework is that it offers an explicit guide as to where such modifications should be incorporated. 

We also agree with the view expressed by [@Gelman2013-id] that the cycle, adopted here, of model construction, parameter estimation, (graphical) model checking and model expansion is typically more informative than 'model selection' as traditionally understood - especially when this latter activity is based on Bayes factors or other assignments of single numerical quantities to complex models. We generally advocate understanding and comparing models in terms of predictive checks and identifying which features particular models capture well and which they miss. That is, we do not believe that there is much to gain from choosing one model as 'best' - rather that we should understand in which respects our models are 'useful' [@Box1976-he; @Box1980-ch]. Part of our goal here was to encourage more researchers to think in these terms and point out that the hierarchical approach has the potential to facilitate such analyses for a range of different model types. 

As a final methodological point, by making our code and data available, as well as leveraging already-available open-source scientific Python software, we open up our work to other researchers to build on.

In summary, the main results established using the above framework were 

- An adequate description of intestinal epithelial dynamics is achievable using a model based on purely proliferation-driven growth
- This model is consistent with healthy, proliferation-inhibited (Ara-C treated) and recovering conditions
- The measurement and process model errors can be reasonably distinguished and checked separately 
- This checking indicates that much of the natural variability is directly attributable to the collection process and this process can be modelled in a simple manner
- Possible model errors can also be identified and proposed explanations incorporated and tested within our framework, and thus the proper interpretation of experimental procedures is aided by using an explicit mathematical model and its predictive simulations
- Including finite-cell-size effects gives a slightly better qualitative fit to experimental data, but the dominant sources of the long-time misfits are likely due to some other factor such as (relatively slowly) time-varying proliferation rates (e.g. due to circadian rhythms) or label dilution.


# Acknowledgements 
This work was funded by the BBSRC-UK, project numbers BB/K018256/1, BB/K017578/1, BB/K017144/1 and BB/J004529/1 and the EPSRC-UK, project number EP/I017909/1.

\nolinenumbers

# References

