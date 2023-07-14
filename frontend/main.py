import streamlit as st
import requests

def get():
	base_url = 'https://scoring-service-tq7rapbbua-uc.a.run.app/v1/hello'
	resp = requests.get(base_url)
	return resp.json()


variable = {
            "ingreso": 0,
            "antiguedad_laboral_meses": 0,
            "trabajos_ultimos_5": 0,
            "edad": 0,
            "crecimiento_ingreso": 0
            }

def post():
	base_url = f'https://scoring-service-tq7rapbbua-uc.a.run.app/v1/prediction'
	resp = requests.post(base_url, json=variable)
	return resp.json()
	

def main():
	st.title("Credit Scoring App")
	income = st.number_input('ingreso')
	seniority_employment_months = st.number_input('antiguedad_laboral_meses')
	last_5_jobs = st.number_input('trabajos_ultimos_5')
	age = st.number_input('edad')
	income_growth = st.number_input('crecimiento_ingreso')
	variable["ingreso"] = income
	variable["antiguedad_laboral_meses"] = seniority_employment_months
	variable["trabajos_ultimos_5"] = last_5_jobs
	variable["edad"] = age
	variable["crecimiento_ingreso"] = income_growth
	if st.button("Try"):
		results = post()
		st.write(results)



if __name__ == '__main__':
	main()