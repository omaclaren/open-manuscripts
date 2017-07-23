---
header-includes:
- \usepackage[labelformat=empty]{caption}

bibliography: "../bibtex-files/crypt-villus-refs.bib"
csl: "../csl/springer-vancouver.csl"

---

#Supplementary information

## Availability
All manuscript, code and data files can be found at the following github page: 

<span style="color:blue">[https://github.com/omaclaren/open-manuscripts/tree/master/hierarchical-framework-intestinal-epithelium](https://github.com/omaclaren/open-manuscripts/tree/master/hierarchical-framework-intestinal-epithelium)</span>

## Derivation of 'zeroth-order' continuous model
To derive the continuous approximation we first defined the position $x$ as a continuous coordinate passing through the discrete cell indices. For example $x = 0$ denoted the coordinate of the cell labelled '0' (base of the crypt), while $x = 0.5$ was the location halfway between the cell labelled '0' and that labelled 1'. Sample locations consisting of space-time pairs were denoted by $s = (x_s,t_s)$. Then, for sample locations $(i,t)$ corresponding to cell indices and arbitrary times, we matched the discrete model and continuous model using

$$p(l_i(t)=1|L(i,t)) = L(i,t)$$ {#eq:pop-param}

i.e. $L(i,t)$ served as the parameter for a single measurement modelled as a Bernoulli trial at that sample location (as in the above Measurement model section).

Next, the discrete dynamics of $p(l_i(t)=1)$ were 'transferred' to the continuous $L(x,t)$ dynamics. In particular, since $L(x,t)$ was taken to be a smooth function, we made the correspondence

\begin{align}p(l_{i-1}(t)=1|L(i-1,t)) &= L(i-1,t) \nonumber \\ &\equiv \nonumber\\ p(l_{i-1}(t)=1|L(i,t),L_x(i,t),...,\Delta x) &= L(i,t)-\Delta x \frac{\partial L(i,t)}{\partial x}+\frac{\Delta x^2}{2} \frac{\partial^2 L(i,t)}{\partial x^2} - ...\end{align} 

where $\Delta x = i-(i-1) = 1$ was the normalised cell length and we also conditioned on knowledge of the spatial derivatives at $i$, $L_x(i,t) = \frac{\partial L(i,t)}{\partial x}$ etc. The continuous spatial field effectively interpolated between - i.e. *internal* to - points of the discrete grid, making use of local derivative information. Substituting the above Taylor series, and similar expressions, into the discrete Markov equation led to 

$$\frac{\partial L(i,t)}{\partial t} + v(i)\frac{\partial L(i,t)}{\partial x} = \frac{1}{2}\left(\Delta x v(i) \frac{\partial^2 L(i,t)}{\partial x^2} - \Delta t \frac{\partial^2 L(i,t)}{\partial t^2}\right) + ...$$ {#eq:model-pde-ts}

where, for completeness, we also retained higher order terms in $\Delta t$ for the continuous model. We similarly assumed the existence of smooth functions $k(x,t)$ and $v(x,t)$ that satisfied the discrete relations

$$v(i,t) = \sum_{j=0}^{i-1} k_j \Delta x = \int_0^{i} k(x,t) dx + v(0). $$ {#eq:model-veloc-ts}

Furthermore, we assumed $k(x,t) = k(x)$, $v(x,t) = v(x)$ and $v(0) = 0$ in what follows. This assumption is discussed further in the Results section. 

We obtained 'closure' for the continuous model by keeping only the lowest order terms in both time and space, and further asserting that the equation structure obtained held *for all continuous $x$* and not just discrete $i$ (this could also be motivated by an assumption of grid translation invariance). This leads to the advection equation

$$\frac{\partial L(x,t)}{\partial t} + v(x)\frac{\partial L(x,t)}{\partial x} = 0$$ {#eq:model-pde}

with

$$v(x) = \int_0^{x} k(x') dx'.$$

When we incorporated cell death, with discrete rates $d_i$, this led to the same equations with $k$ replaced by $k-d$, where $d(x,t)$ was defined similarly to $k(x,t)$. Hence we interpreted $k$ in the above as the net cell production rate (which hence could be negative).

## Supplementary visualisations of posterior distributions
In Fig A, Fig B and Fig C, respectively, we present alternative visualisations of the posterior distributions for proliferation rates under healthy, Ara-C-treated and recovering conditions. These are alternative visualisations of the data presented in Figs 3-5 in the main manuscript. These plots were produced using the package ‘corner.py’ described in [@Foreman-Mackey2016-cj].

![\textbf{Fig A. Posterior for proliferation rates under baseline, healthy conditions.} The upper diagonal represents the marginal distributions for each proliferation rate when averaging over all other profileration rates. The plots below the diagonal show bivariate marginal distributions illustrating pairwise associations after averaging over all other profileration rates. These visualisations are a way of understanding the full joint posterior distribution which is five-dimensional in full generality.](../figures/figures_to_include/S1_Fig_A.pdf)

![\textbf{Fig B. Posterior for proliferation rates under Ara-C treatment.} The upper diagonal represents the marginal distributions for each proliferation rate when averaging over all other profileration rates. The plots below the diagonal show bivariate marginal distributions illustrating pairwise associations after averaging over all other profileration rates. These visualisations are a way of understanding the full joint posterior distribution which is five-dimensional in full generality.](../figures/figures_to_include/S1_Fig_B.pdf)

![\textbf{Fig C. Posterior for proliferation rates when recovering from Ara-C treatment.} The upper diagonal represents the marginal distributions for each proliferation rate when averaging over all other profileration rates. The plots below the diagonal show bivariate marginal distributions illustrating pairwise associations after averaging over all other profileration rates. These visualisations are a way of understanding the full joint posterior distribution which is five-dimensional in full generality.](../figures/figures_to_include/S1_Fig_C.pdf)

## Typical sample from intestinal epithelium
The companion paper [@Parker2016-jf] contains full details of the experimental procedures. In Fig D below we reproduce, for reference, a typical section obtained from an intestinal in these experiments. 

![\textbf{Fig D. Typical section obtained during the experimental procedures described in the main manuscript}. These are also detailed more fully in the companion paper [@Parker2016-jf].](../figures/figures_to_include/S1_Fig_D.tif)

## Interpretation of statistical evidence
We have described above how mechanistic or causal assumptions relate to assumptions of structural invariance under different scenarios. In order to interpret the results that follow, however, we also required an interpretation of the 'statistical evidence' that a set of measurements provided about parameter values within a fixed model structure. This proved a surprisingly controversial topic and we encountered continuing debate about fundamental principles and definitions of statistical evidence [@Royall1997-ai; @Mayo2014-pz; @Evans2014-gn; @Evans2015-kg; @Taper2016-la]. 

Following our conditional modelling approach, we decided to adopt the simple - yet quite generally applicable - principle of evidence based on conditional probability: if we observe $b$ and $p(a|b) > p(a)$ then we have evidence for $a$. A 'gold-standard' theory of statistical evidence starting from this premise has been developed and defended recently by Evans in a series of papers (summarised in [@Evans2015-kg]). Besides simplicity, a nice feature of this approach, that we used below, is that it can be applied both to prior and posterior predictive distribution comparisons such as $p(\mathbf{y}|\mathbf{y_0}) \overset{?}{>} p(\mathbf{y})$, as well as to prior and posterior parameter distribution comparisons such as $p(\mathbf{k}|\mathbf{y_0}) \overset{?}{>} p(\mathbf{k})$. This approach is not without criticism, however (again, see [@Royall1997-ai; @Mayo2014-pz; @Evans2014-gn; @Evans2015-kg; @Taper2016-la] for an entry point to the ongoing debates).

Another notable feature of the interpretation of statistical evidence that we adopted below is that we emphasised the visual comparison of various prior and posterior distributions, rather than adopting arbitrary numerical standards ([@Tarantola2005-sv] advocates a similar 'movie strategy' for the interpretation of statistical evidence and inference procedures, [@Gelman2004-bk; @Gelman2013-id; @Gelman2013-wc; @Davies2014-dz] similarly emphasise the benefits of graphical visualisation methods in statistics). 
