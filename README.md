<p align=center><img src=_src/assets/mox.jpg><p>

# <h1 align=center> **Credit Scoring System with Machine Learning** </h1>

# Introduction

This is a project for a Mexican Fintech that want to implement a credit scoring system using machine learning techniques. 

# About MOX

MOX is a startup focused on OpenData in order to automate and streamline the pre-qualification, 
origination and collection processes for financial entities in Mexico. One of MOX's solutions 
consists of a platform that allows viewing data on income/employment/pensions of credit applicants 
in real time.


# Project Overview

The main objective of the project is to provide clients with a useful tool to qualify profiles and 
evaluate the repayment ability of applicants for all types of personal loans and credits. The income 
score will be built using individual information from the profile, as well as external data 
(demographic data, national surveys/household surveys, among other datasets) that refer to your 
environment. This combination of information will allow obtaining a clearer and more precise image 
of the financial situation of each person. To give customers a better understanding of each 
profile's ability to pay, alternate credit scores are used. Customers will be able to issue credit 
in an informed and data-driven manner by using the score as a quantitative indicator.<br>
<br>
The main advantage of the income score built in this project lies in the combination of individual 
profile information and external data referring to its environment. By considering factors such as 
income, job seniority, number of jobs in recent years, age, state/province, income growth, 
education, type and behavior of the industry, and social status of the population, a more complete 
and comprehensive perspective is obtained. accurate profile of the applicant. Some of these 
variables are obtained directly from the MOX datasets such as the specific variables of the profile, 
the other variables about their environment will be obtained from public databases, open government 
data and surveys.<br>
<br>
The deliverable of the project is to create a score that gathers the different data around the 
requested profile and immediately offers a balanced metric for easy classification of the profile.

## New Dataframe

<details>
  <summary>Variables:</summary>


| Variable | Reference | Specific variable | Basis Download | Comments | | 
| --- | --- | --- | --- | --- | --- |
|  Income | Economic income of the applicant. | Net_Income [BASE MOX, Main] | MOX-BASED | |
|  Labor Seniority | Years of work experience in the current job. | Date_add_current_entry [BASE MOX, Main] | MOX-BASED | |
|  Number of Jobs | Number of jobs per year in the last 5 years, used as a proxy for job stability.Var = n/5 (where n= Number of Jobs in the last 5 years) [BASE MOX, Main] | VARIABLE TO CREATE: [BASE MOX, Main] | CREATE VARIABLE - MOX BASE | |
|  Age | Applicant's age. | birth_date [BASE MOX, Main] | MOX-BASED | |
|  Income growth | Factor that represents the percentage growth of the applicant's income in the last 3 years | VARIABLE TO CREATE: [BASE MOX, Main] | MOX-BASED | |
|  Education | Educational level of the applicant. 1=Undergraduate, 0=Non-Undergraduate | Dummy(1;0)| With CURP MOX - [Buho](https://www.buholegal.com/consultasep/) | PENDING VARIABLE - Variable will be available in BASE MOX shortly. |
|  Current location | State (Region) of Mexico in which you reside. | status [MOX BASE, Address Table] | MOX-BASED With the registered company name | |
|  Industry | Growth of the industry sector in the region. The variable "Current place" is used to determine the base to use. | BASE DENUE, (according to “Current Place”) | [DENUE Historical Data](https://www.inegi.org.mx/app/descarga/?ti=6) | PROBLEM: Link Company Name (Name) with Industry |
|  General economic growth of the region | General economic growth of the region where the applicant resides. | Economic_activities_by_federative_entity_PERCENTUAL VARIATION (IMAIEF) [INEGI]| INEGI> Indicators by State>Economy> (IMAIEF) Economic_Activities_by:entidad_federativa_PERCENTUAL VARIATION [link](https://www.inegi.org.mx/app/estatal/?ag=07000019#grafica) | Take the total value of the state to which it belongs, not by sector. |
|  Liquidity | Only monetary income that an average person has in the corresponding State. | Table 6.1, ENIGH-TABLED | ENIGH>Ns_ef_Tabulados>Table 6.1 [link](https://www.inegi.org.mx/programas/enigh/nc/2020/#Tabulados) | Monetary: Income in currency Non-Monetary: Transactions in kind or self-consumption. |
|  Income Decile | Auxiliary Variable for Var "Cost of Life". Depending on the State (Var. “Current Place”) and the Work Income (Var. Income), it is established to which decile the household belongs. | Table 3.5, ENIGH-TABLED | ENIGH***>Ns_ef_Tabulados>Table 3.5 [link](https://www.inegi.org.mx/programas/enigh/nc/2020/#Tabulados) | Auxiliary Variable. Do not include directly. |
|  Cost of Living | Average cost of living in the place where the applicant is established corresponding to the income level decile belonging to. | Table 4.2A, ENIGH-TABLED | ENIGH>Ns_ef_Tabulados>Table 4.2A [link](https://www.inegi.org.mx/programas/enigh/nc/2020/#Tabulados) | Variable determined by: Var”Current Place” (State) and Var”Income” (Decile to which the household belongs) |
|  Expenditures and loans | We lend to third parties depending on the Var ”Current Place” | Table 5.1, ENIGH-TABLED | ENIGH***>Ns_ef_Tabulados>Table 6.1>Financial Expenditures [link](https://www.inegi.org.mx/programas/enigh/nc/2020/#Tabulados) | Use the variable at criteria |

* INEGI: The "National Institute of Statistics and Geography" is a public and autonomous body that captures and disseminates information on territory, resources, population and economy.

* DENUE: The "National Statistical Directory of Economic Units" is an INEGI tool for consulting location, contact and economic activity data for businesses in Mexico.

* ENIGH: The “National Income and Expenditure Survey” is a data tool collected by INEGI to provide a statistical overview of the income and expenditure behavior of individuals and households in Mexico.

* CURP: National identification number equivalent to the DNI in Mexico.


</details>