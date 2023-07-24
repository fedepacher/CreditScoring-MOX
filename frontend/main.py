import streamlit as st
import streamlit.components.v1 as components
import requests


LIMIT_LOWER = '300'
LIMIT_A = '400'
LIMIT_B = '500'
LIMIT_C = '560'
LIMIT_D = '680'
LIMIT_E = '850'

Entities = ['0-Aguascalientes', '1-Baja California', '2-Baja California Sur',
			'3-Campeche', '4-Coahuila de Zaragoza', '5-Colima', '6-Chiapas', '7-Chihuahua',
			'8-Ciudad de México', '9-Durango', '10-Guanajuato', '11-Guerrero', '12-Hidalgo',
			'13-Jalisco', '14-México', '15-Michoacán de Ocampo', '16-Morelos', '17-Nayarit',
			'18-Nuevo León', '19-Oaxaca', '20-Puebla', '21-Querétaro', '22-Quintana Roo',
			'23-San Luis Potosí', '24-Sinaloa', '25-Sonora', '26-Tabasco', '27-Tamaulipas',
			'28-Tlaxcala', '29-Veracruz de Ignacio de la Llave', '30-Yucatán', '31-Zacatecas']

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
html_var = html_var.replace('LIMIT_D', LIMIT_D)


primaryColor = st.get_option("theme.primaryColor")
backgroundColor = st.get_option("theme.backgroundColor")
s = f"""
<style>
div.stButton > button:first-child {{ background: {primaryColor}; 
 height:2em; width:7em; color:{backgroundColor}}}
 div.stButton > button:hover {{
    background-color: #ffffff;
    color:#000000;
    }}
div.stButton > button:focus {{
    background-color: #262730;
    color:#60616D;
    }}
div[data-baseweb="select"] > div {{
    background-color: #91E4DB;
}}

<style>
"""
st.markdown(s, unsafe_allow_html=True)
components.html(
    """
		<script>
		const elements = window.parent.document.querySelectorAll('.stNumberInput div[data-baseweb="input"] > div')
		console.log(elements)
		const color = '#A29DF1'
		elements[0].style.backgroundColor = color
		elements[1].style.backgroundColor = color
		elements[2].style.backgroundColor = color
		elements[3].style.backgroundColor = color
		elements[4].style.backgroundColor = color
		elements[5].style.backgroundColor = color
		elements[6].style.backgroundColor = color
		elements[7].style.backgroundColor = color
		</script>
		""",
    height=0,
    width=0,
)


def main():
	left_col, cent_col,last_col = st.columns(3)
	with cent_col:
		st.image('./frontend/images/mox.jpg', use_column_width=True)
	st.markdown("<h1 style='text-align: center; color: grey;'>Income Scoring</h1>", 
	     		unsafe_allow_html=True)
	st.markdown("<hr class='my-4'>", unsafe_allow_html=True)

	left_col, right_col = st.columns(2)
	with left_col:
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
	with right_col:
		weekwage = st.number_input("Semanas Cotizadas", value=0, step=1)
		if not isinstance(weekwage, int) or weekwage < 0:
			st.error("Semanas Cotizadas invalido")
		age = st.number_input("Edad", value=18, step=1)
		if not isinstance(age, int) or age < 18 or age > 100:
			st.error("Edad invalida, debe ser mayor a 18 años")
		income_growth = st.number_input("Crecimiento de Ingreso", value=0.0, step=1.0)
		if not isinstance(income_growth, float) or (income == 0 and income_growth != 0):
			st.error("Crecimiento de Ingreso invalido o Ingreso igual a 0")
		lugar_actual = st.selectbox("Seleccione Entidad Federativa", Entities)
		lugar = Entities.index(lugar_actual)

	if income < 0 or seniority_employment_months < 0 or time_unemployed < 0 or last_5_jobs < 0 or \
	   weekwage < 0 or age < 18 or age > 100:
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
	variable["lugar_actual"] = lugar

	col1, col2, col3, col4, col5 = st.columns(5)
	with col3:
		consult_btn = st.button("Consultar", disabled=st.session_state.get("disabled", False))
	
	left_col, cent_col, right_col = st.columns(3)
	with cent_col:
		if consult_btn:
			results = post()
			st.markdown(f'<h2 style=\'text-align: center; color: grey;\'>Cluster: {results["cluster"]}</h2>', unsafe_allow_html=True)
			value = float(results["scoring"]) * (1/550) - (300/550)
			var = html_var.replace('value_arg', str(value))
			# st.write(var)
			components.html(var,
							width=400,
							height=400
							)


if __name__ == '__main__':
	main()