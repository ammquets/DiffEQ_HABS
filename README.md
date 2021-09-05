This repository has been archived. It is now read-only.

# Modeling Pseudo-nitzschia Blooms and Toxicity
Hallie Arno and Andrea Quets

15 March 2020

College of the Atlantic

Differential Equations

## Code Attribution
file                              | owner
----------------------------------|--------------
2d_diffusion_chakrabordy_2020.py  | hallie00 
CHATTOPADHYAY_eq1.py              | ammquets 
LotkaVolterraNutrients.py         | hallie00
chakrabordy2008(2).py             | hallie00
exponential_growth_preliminary.py | ammquets
strong_predation_preliminary.py   | ammquets
tox.py                            | ammquets

chakrabordy2008(2).py and tox.py were the primary models used in the final version of the project.

## Background information and conclusions copied from our report
### Abstract
Harmful algae blooms (HABs) are dangerous to humans when consumed through a shellfish vector and have implications for aquatic ecosystems. Management efforts rely on effective prediction of HAB dynamics, including population size and the toxins they produce. We used simulated Pseudo-nitzschia using Euler’s method programs to predict these respective dynamics based on nutrient levels, ratios of silicate to nitrate, and initial phytoplankton and zooplankton population sizes. Our models reflect previous research showing that HAB frequency and size depends heavily on nutrient inflow and zooplankton predation, and that the toxin levels produced depend on reaching a minimum nitrate to silicate threshold. While we recognize that there are many interrelated factors that could influence blooms and were not able to model all of them, our results seem consistent with what we expected based on previous research and knowledge on the subject. 

### Introduction
Algae blooms are naturally occurring phenomenon in aquatic ecosystems. They are caused by an influx of nutrients and usually increased levels of irradiance. In the Gulf of Maine (GoM), at the end of winter and the beginning of spring, light and nutrients become more available due to winter mixing and increased springtime runoff, which leads to increased nutrient availability. This leads to primary productivity, which serves as a base to the food web: zooplankton feed on phytoplankton and larger organisms feed on zooplankton. Abnormal nutrient inputs can cause algal blooms, and when this triggers blooms of harmful or toxin producing algae, bloom dynamics must be monitored closely to limit the impact on human health and livelihoods. 

There are three primary harmful algae threats which currently exist in the GoM.  Alexandrium fundyense is a dinoflagellate which has previously been the primary harmful algae species of concern in the GoM. Alexandrium produces the neurotoxin saxitoxin which causes paralytic shellfish poisoning in humans. A second threat in the GoM is an alga called Dinophysis. Dinophysis produces a toxin called okadaic acid which causes diathetic shellfish poisoning in humans. Since about 2013 a new threat has emerged in the GoM: Pseudo-nitzschia spp (Fernandes, 2013). There are 52 species of Pseudo-nitzschia, 26 of which produce domoic acid (Bates, 2018). Domoic acid causes amnesiac shellfish poisoning. If a wayward person were to ingest too much of either saxitoxin or domoic acid, it could result in death, unless the individual is proactive about seeking hospitalization. This paper will focus on Pseudo-nitzschia because currently Pseudo-nitzschia is of the greatest concern currently in the GoM. 

Toxin is passed to humans through a shellfish vector, such as clams or mussels. It is not possible to get sick just from ingesting some sea water, even if the Pseudo-nitzschia density was high; a shellfish vector is required to concentrates the toxin. Shellfish operate by siphoning water over their ctenidia which then collect the toxic plankton inside of their visceral mass.

Because of these human health concerns, shellfish beds are often closed during bloom season. For species that accumulate toxins quickly, such as mussels, there is a broad-reaching closure as soon as a certain threshold of Pseudo-nitzschia cells are detected in the water (Maine Department of Marine Resources, 2020). While it is better to overestimate the length of the bloom and the areas affected than underestimate, closures are controversial and economically detrimental to the local shellfish harvesters and economy. Managers are beginning to use models to more accurately predict when, where, and how long blooms will be to reopen flats as soon as they are safe and close them right before they become dangerous (Chattopadhyay et al., 2004). This keeps the public most safe and has the minimum effect on the livelihood of shellfish harvesters. 

Some HABs are more predictable than others. For example, Alexandrium almost always blooms in early May in the GoM, so there is a short precautionary annual closure (Maine Department of Marine Resources). Other species, such as Pseudo-nitzschia, do not appear to exhibit a predictable annual pattern in either population or toxin production. There are many factors that can influence both of these, such as nutrient levels and ratios, irradiance, temperature, and ecological factors.  

There are several factors which go into toxin production in Pseudo-nitzschia. It is unclear exactly what evolutionary advantage the toxin may present for the species. One hypothesis is that the domoic acid binds trace nutrients such as iron and copper (Rue & Bruland, 2001). This hypothesis is supported by the fact that domoic acid levels tend to increase under nutrient imitating conditions. Domoic acid levels are also increased with the presence of grazers. This suggests that the toxin is also used as a defense mechanism (Chakraborty & Chattopadhyay, 2008). 

Bates et al (1991) found that there were at least three factors which influenced Pseudo-nitzschia ability to produce toxin. These factors included cessation of cell division, nitrate availability, and presence of light (Bates, 1991). Cessation of cell division and nitrate availability can be summarized by tracking the nitrate:silicate ratio (Bates, 1991). When silicate begins to limit cell division, but nitrate is still available, then domoic acid can be produced (Bates, 1991). Domoic acid can also be produced during growth if the N:Si ratio is greater than 8 (Bates, 1991). 

An important factor for the length and severity of HABs is grazing from zooplankton (Chattopadhyay, 2002). Grazers a control on the size and timing of the bloom by eating the phytoplankton and further limiting their population in different ways than nutrient depletion alone would. 

Most of the factors that affect HAB dynamics reciprocally influence each other. For example, nutrients affect both the number of cells as well as the amount of toxin produced. Phytoplankton then take up these nutrients, which leads to a limiting factor on their population as well as a change in the toxin production. Toxin production lowers zooplankton grazing, which increases phytoplankton population size. (Bates, 1991, Chattopadhyay, 2002; Chakraborty and Chattopadhyay, 2008.)

The two most basic factors used to predict HABs are the population (number of cells in the water) and toxin production (per cell). However, most of the factors that affect these two things reciprocally influence each other. For example, nutrients affect both the number of cells as well as the amount of toxin produced. Phytoplankton then take up these nutrients, which leads to a limiting factor on their population as well as a change in the toxin production.

### Conclusion

These models could be applied to predict how long a bloom will last if the managers knew factors such as the number of zooplankton and the nutrient inflow, which could be obtained from field surveys. The toxicity model is useful for determining toxin output based on nutrients. In a bloom scenario, resource managers could test parameters then use these models to estimate the length of the bloom (using the population model) and the amount of toxins produced (using the toxicity model). Together, these could give useful insight into the dynamics and severity of the bloom. 

While the population model takes into account a changing amount of rainfall over the course of the year which will affect the nutrient influx, neither of the models take into account the increased growth of phytoplankton when there is increased sunlight (summer). The toxin model could be adjusted for compatibility with changes in irradiance by altering the toxin input function. There are further seasonal dynamics that could be explored, such as the effect of increased temperature on stratification, which would mean fewer nutrients in the photic zone. 

The models also do not take into account competition for nutrients from other species. While the population model assumes that there is other food available for zooplankton aside from Pseudo-nitzschia, it does not take into account nutrient depletion from another population of plankton. There are some instances where non-harmful species will outcompete harmful species for nutrients, which would terminate the HAB more quickly. 

An opportunity for future work on this project could involve adding an equation for shellfish toxin uptake and flush times to determine how long shellfish take to become safe for consumption after a bloom. 

Integrating the toxicity and population models would involve a reconciliation of units. When both models are using the same units, the phytoplankton differential equation in the toxicity model can be replaced with the system of differential equations from the population model. Assessing the behavior of the models compared to historical data would be integral, since these models both carry their own assumptions and amounts of error, and the combination of them may magnify that error. To protect against this, it would be necessary to test against real data. 

### Citations
Bates, S. S., Freitas, A. D., Milley, J. E., Pocklington, R., Quilliam, M. A., Smith, J. C., & 
	Worms, J. (1991). Controls on domoic acid production by the diatom Nitzschia pungens f. 
	multiseries in culture: nutrients and irradiance. Canadian Journal of Fisheries and 	
	Aquatic Sciences, 48(7), 1136-1144.
Bates, S. S., Hubbard, K. A., Lundholm, N., Montresor, M., & Leaw, C. P. (2018). Pseudo-	
	nitzschia, Nitzschia, and domoic acid: new research since 2011. Harmful Algae, 79, 3-43.
Chakraborty, S., & Chattopadhyay, J. (2008). Nutrient-phytoplankton-zooplankton 
	dynamics in the presence of additional food source—A mathematical study. Journal of 
	Biological Systems, 16(04), 547-564.
Chattopadhyay, J., Sarkar, R. R., & El Abdllaoui, A. (2002). A delay differential equation model 
	on harmful algal blooms in the presence of toxic substances. Mathematical Medicine and 
	Biology: A Journal of the IMA, 19(2), 137-161.
Chattopadhyay, J., Sarkar, R. R., & Pal, S. (2004). Mathematical modelling of harmful algal 
	blooms supported by experimental findings. Ecological Complexity, 1(3), 225-235.
Fernandes, L. F., Richlen, M. L., Kulis, D., Erdner, D. L., Bates, S. S., Ehrman, J., ... & Anderson, D. M. (2009, November). The taxonomy and biodiversity of the diatom Pseudo-nitzschia H. Peragallo in the Gulf of Maine: characterizing an emerging threat in the region. In Fifth Symposium on Harmful Algae in the US, Ocean Shores, WA (p. 40). Olson, M. B., Lessard, E. J., Cochlan, L., & Trainer, V. L. (2008). Intrinsic growth and microzooplankton grazing on toxigenic Pseudo‐nitzschia spp. diatoms from the coastal northeast Pacific. Limnology and Oceanography, 53(4), 1352-1368.
Red Tide (Paralytic Shellfish Poisoning): Maine DMR Bureau of Public Health—Shellfish 
	Sanitation and Management. (2020). Retrieved March 15, 2020.
Rue, E., & Bruland, K. (2001). Domoic acid binds iron and copper: a possible role for the toxin 
	produced by the marine diatom Pseudo-nitzschia. Marine Chemistry, 76(1-2), 127-134.
