This is a sorting algorithm to determine the most useful subject files for patient data visualization of vitals.

In order to generate a complete, informative ADDS chart and graphically display trends in vital signs,
patient data needs to be have all the vital signs measurements, but also be measured continuously and
evenly over time.

100,000 patient CHART_EVENTS files from the MIMIC Critical Care Database were scored out of 100 and
ranked from most to least informative. Out of these files, around 24,300 scored at at least 75/100.

The overall score used to determine the rankings is the average of the two following scores:
    1. Continuity (C) score: continuity of measurements over a duration of 3 days
    2. Vitals (V) score: Completeness of vitals measurements

Rankings are listed in detailed_rankings.txt.


--------------------------------------------------------------------------------------------------------------
Detailed Information on Scoring
---------------------------------------------------------------------------------------------------------------
************************** 1. CONTINUITY OF MEASUREMENTS OVER TIME  ***************************************

 For each patient, we also measure the continuity of patient observations in order to determine whether
it would generate an informative, complete visualization of data when graphed.

For each patient file, the timestamps of each observation made are sorted in chronological order.
A Kolmogorov–Smirnov test (ks-test) is then performed on the timestamps to compare the empirical
distribution function from the patient sample with a reference uniform distribution over three days
(from minute 0 to minute 4320). Since the average ICU stay is ~2 days, we believe that 3 days is a good duration
to test continuity.

The resulting D-statistic from the ks-test (Kolmogorov's D statistic) is a number between 0 and 1 which tells us how
different the sample data is from a reference uniform distribution. Thus, a D-statistic close to 0 signifies
ideal continuity of data, while a D-statistic closer to 100 signifies complete lack of continuity.

The Continuity (C) score is (1 - <d-statistic score>) * 100, resulting in a percentage between 0 and 100.


******************************  2. COMPLETENESS OF VITALS  ****************************************************

Since medical professionals monitor patient deterioration by analyzing trends in vital signs, it is crucial
for patient files to have continuous measurements of all 5 vitals: respiratory rate, heart rate, SP02, temperature,
and blood pressure.

The number of vitals measured corresponds to the vitals (V) score linearly as follows:
0 vitals out of 5 - 0%
1 vital  out of 5 - 20%
2 vitals out of 5 - 40%
3 vitals out of 5 - 60%
4 vitals out of 5 - 80%
5 vitals out of 5 - 100%

The ITEMID codes corresponding to each vital are listed below (both CareVue and MetaVision ITEMIDs are considered):
 -- TEMPERATURE
	  223762, -- "Temperature Celsius"
	  676,	-- "Temperature C"
	  223761, -- "Temperature Fahrenheit"
	  678 --	"Temperature F"

-- RESPIRATORY RATE
	  618,--	Respiratory Rate
	  615,--	Resp Rate (Total)
	  220210,--	Respiratory Rate
	  224690, --	Respiratory Rate (Total)

-- HEART RATE
	  211, --"Heart Rate"
	  220045, --"Heart Rate"

-- BLOOD PRESSURE
	  51, --	Arterial BP [Systolic]
	  442, --	Manual BP [Systolic]
	  455, --	NBP [Systolic]
	  6701, --	Arterial BP #2 [Systolic]
	  220179, --	Non Invasive Blood Pressure systolic
	  220050, --	Arterial Blood Pressure systolic

	  8368, --	Arterial BP [Diastolic]
	  8440, --	Manual BP [Diastolic]
	  8441, --	NBP [Diastolic]
	  8555, --	Arterial BP #2 [Diastolic]
	  220180, --	Non Invasive Blood Pressure diastolic
	  220051, --	Arterial Blood Pressure diastolic

-- SPO2, peripheral
      646
      220277


