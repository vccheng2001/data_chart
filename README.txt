1. Sort subjects by disease code (ICD9 Code) after getting diagnose_icd table
2. Filter out by
    1. Patients with reasonable data size
    2. Completeness of vitals measurements

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

  -- Systolic/diastolic

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
