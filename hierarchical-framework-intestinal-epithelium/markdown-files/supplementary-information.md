---
header-includes:
bibliography: "../bibtex-files/crypt-villus-refs.bib"
csl: "../csl/springer-vancouver.csl"

---

#Supplementary information

## Availability
All manuscript, code and data files can be found at the following github page: 

<span style="color:blue">[https://github.com/omaclaren/open-manuscripts/tree/master/hierarchical-framework-intestinal-epithelium](https://github.com/omaclaren/open-manuscripts/tree/master/hierarchical-framework-intestinal-epithelium)</span>

## Supplementary visualisations of posterior distributions
In Fig @fig:BrdU-corner, Fig @fig:AraC-active-corner and Fig @fig:AraC-passive-corner, respectively, we present alternative visualisations of the posterior distributions for proliferation rates under healthy, Ara-C-treated and recovering conditions. These are alternative visualisations of the data presented in Figs 3-5 in the main manuscript. These plots were produced using the package ‘corner.py’ described in [@Foreman-Mackey2016-cj].

![Posterior for proliferation rates under baseline, healthy conditions. The upper diagonal represents the marginal distributions for each proliferation rate when averaging over all other profileration rates. The plots below the diagonal show bivariate marginal distributions illustrating pairwise associations after averaging over all other profileration rates. These visualisations are a way of understanding the full joint posterior distribution which is five-dimensional in full generality.](../figures/figures_to_include/mcmc-proliferation-rates-processed-BrdU-passive.pdf){#fig:BrdU-corner}

![Posterior for proliferation rates under Ara-C treatment. The upper diagonal represents the marginal distributions for each proliferation rate when averaging over all other profileration rates. The plots below the diagonal show bivariate marginal distributions illustrating pairwise associations after averaging over all other profileration rates. These visualisations are a way of understanding the full joint posterior distribution which is five-dimensional in full generality.](../figures/figures_to_include/mcmc-proliferation-rates-processed-AraC-active.pdf){#fig:AraC-active-corner}

![Posterior for proliferation rates when recovering from Ara-C treatment. The upper diagonal represents the marginal distributions for each proliferation rate when averaging over all other profileration rates. The plots below the diagonal show bivariate marginal distributions illustrating pairwise associations after averaging over all other profileration rates. These visualisations are a way of understanding the full joint posterior distribution which is five-dimensional in full generality.](../figures/figures_to_include/mcmc-proliferation-rates-processed-AraC-passive.pdf){#fig:AraC-passive-corner}

## Typical sample from intestinal epithelium
The companion paper [@Parker2016-jf] contains full details of the experimental procedures. In Fig @fig:section below we reproduce, for reference, a typical section obtained from an intestinal in these experiments. 

![Typical section obtained during the experimental procedures described in the main manuscript and more fully in the companion paper [@Parker2016-jf].](../figures/figures_to_include/041_10h_Ring_1_20x.tif){#fig:section}

