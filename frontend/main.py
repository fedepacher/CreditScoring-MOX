import streamlit as st
import streamlit.components.v1 as components
import requests


LIMIT_LOWER = '300'
LIMIT_A = '400'
LIMIT_B = '500'
LIMIT_C = '600'
LIMIT_D = '750'

Entities = ['Aguascalientes', 'Baja California', 'Baja California Sur',
			'Campeche', 'Coahuila de Zaragoza', 'Colima', 'Chiapas', 'Chihuahua',
			'Ciudad de México', 'Durango', 'Guanajuato', 'Guerrero', 'Hidalgo',
			'Jalisco', 'México', 'Michoacán de Ocampo', 'Morelos', 'Nayarit',
			'Nuevo León', 'Oaxaca', 'Puebla', 'Querétaro', 'Quintana Roo',
			'San Luis Potosí', 'Sinaloa', 'Sonora', 'Tabasco', 'Tamaulipas',
			'Tlaxcala', 'Veracruz de Ignacio de la Llave', 'Yucatán', 'Zacatecas']

variable = {
            "ingreso": 45000,
			"antiguedad_laboral_meses": 50,
			"tiempo_desempleado": 0,
			"trabajos_ultimos_5": 1,
			"semanasCotizadas": 1000,
			"edad": 32,
			"crecimiento_ingreso": 265.38,
			"lugar_actual": "Aguascalientes"
            }


def post():
	base_url = f'https://scoring-service-tq7rapbbua-uc.a.run.app/v1/prediction'
	resp = requests.post(base_url, json=variable)
	return resp.json()
	

def btn_disable(state):
    st.session_state['disabled'] = state


with open('./frontend/code/gauge.html', 'r', encoding='utf-8') as file:
	html_var = file.read()
html_var = html_var.replace('LIMIT_LOWER', LIMIT_LOWER)
html_var = html_var.replace('LIMIT_A', LIMIT_A)
html_var = html_var.replace('LIMIT_B', LIMIT_B)
html_var = html_var.replace('LIMIT_C', LIMIT_C)

def main():
	left_col, cent_col,last_col = st.columns(3)
	with cent_col:
		st.image('./frontend/images/mox.jpg', use_column_width=True)
	st.markdown("<h1 style='text-align: center; color: grey;'>Credit Scoring</h1>", 
	     		unsafe_allow_html=True)
	st.markdown("<hr class='my-4'>", unsafe_allow_html=True)

	income = st.number_input("Ingreso", value=0.0, step=1.0)
	if not isinstance(income, float) or income < 0:
		st.error("Ingreso invalido")
	seniority_employment_months = st.number_input("Antigüedad Laboral (meses)", value=0, step=1)
	if not isinstance(seniority_employment_months, int) or seniority_employment_months < 0:
		st.error("Antigüedad Laboral (meses) invalido")
	time_unemployed = st.number_input("Tiempo Desempleado (meses)", value=0, step=1)
	if not isinstance(time_unemployed, int) or time_unemployed < 0:
		st.error("Tiempo Desempleado (meses) invalido")
	last_5_jobs = st.number_input("Trabajos Últimos 5 años", value=0, step=1)
	if not isinstance(last_5_jobs, int) or last_5_jobs < 0:
		st.error("Trabajos Últimos 5 años invalido")
	weekwage = st.number_input("Semanas Cotizadas", value=0, step=1)
	if not isinstance(weekwage, int) or weekwage < 0:
		st.error("Semanas Cotizadas invalido")
	age = st.number_input("Edad", value=18, step=1)
	if not isinstance(age, int) or age < 18 or age > 100:
		st.error("Edad invalida, debe ser mayor a 18 años")
	income_growth = st.number_input("Crecimiento de Ingreso", value=0.0, step=1.0)
	if not isinstance(income_growth, float) or income_growth < 0 or (income_growth > 0 and income == 0):
		st.error("Crecimiento de Ingreso invalido o Ingreso igual a 0")
	lugar_actual = st.selectbox("Seleccione Entidad Federativa", Entities)

	if income < 0 or seniority_employment_months < 0 or time_unemployed < 0 or last_5_jobs < 0 or \
	   weekwage < 0 or age < 18 or age > 100 or income_growth < 0:
		btn_disable(True)
	else:
		btn_disable(False)

	variable["ingreso"] = float(income)
	variable["antiguedad_laboral_meses"] = int(seniority_employment_months)
	variable["tiempo_desempleado"] = int(time_unemployed)
	variable["trabajos_ultimos_5"] = int(last_5_jobs)
	variable["semanasCotizadas"] = int(weekwage)
	variable["edad"] = int(age)
	variable["crecimiento_ingreso"] = float(income_growth)
	variable["lugar_actual"] = str(lugar_actual)

	col1, col2, col3, col4, col5 = st.columns(5)
	with col3:
		consult_btn = st.button("Consultar", disabled=st.session_state.get("disabled", False))
	col1, col2, col3 = st.columns(3)
	with col2:
		if consult_btn:
			results = post()
			st.markdown(f'<h2 style=\'text-align: center; color: grey;\'>Cluster: {results["cluster"]}</h2>', unsafe_allow_html=True)
			value = float(results["scoring"]) * (1/450) - (300/450)
			var = html_var.replace('value_arg', str(value))
			# st.write(var)
			components.html(var,
							width=400,
							height=400
							)


if __name__ == '__main__':
	main()