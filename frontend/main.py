import streamlit as st
import requests

def get():
	base_url = 'https://scoring-service-tq7rapbbua-uc.a.run.app/v1/hello'
	resp = requests.get(base_url)
	return resp.json()


variable = {
            "ingreso": 45000,
			"antiguedad_laboral_meses": 50,
			"tiempo_desempleado": 0,
			"trabajos_ultimos_5": 1,
			"semanasCotizadas": 1000,
			"edad": 32,
			"crecimiento_ingreso": 265.38,
			"crecimiento_gral": 0,
			"ENIGH": 9
            }

def post():
	base_url = f'https://scoring-service-tq7rapbbua-uc.a.run.app/v1/prediction'
	resp = requests.post(base_url, json=variable)
	return resp.json()
	

def main():
	st.title("Credit Scoring App")
	income = st.number_input('ingreso')
	seniority_employment_months = st.number_input('antiguedad_laboral_meses')
	time_unemployed = st.number_input('tiempo_desempleado')
	last_5_jobs = st.number_input('trabajos_ultimos_5')
	weekwage = st.number_input('semanasCotizadas')
	age = st.number_input('edad')
	income_growth = st.number_input('crecimiento_ingreso')
	gral_growth = st.number_input('crecimiento_gral')
	enigh = st.number_input('enigh')
	variable["ingreso"] = income
	variable["antiguedad_laboral_meses"] = seniority_employment_months
	variable["tiempo_desempleado"] = time_unemployed
	variable["trabajos_ultimos_5"] = last_5_jobs
	variable["semanasCotizadas"] = weekwage
	variable["edad"] = age
	variable["crecimiento_ingreso"] = income_growth
	variable["crecimiento_gral"] = gral_growth
	variable["ENIGH"] = enigh
	if st.button("Try"):
		results = post()
		st.write(results)



if __name__ == '__main__':
	main()