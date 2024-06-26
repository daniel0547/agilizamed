from flask import jsonify, Blueprint, request
import openai
import os
from openai import OpenAI
from app.settings import app

api = Blueprint('api', __name__, template_folder='templates', static_folder='../static')

@api.route('/build-patient', methods=['POST'])
def get_token():
    data = request.json
    patient =  data["patient"]
    prompt = build_prompt(patient["pain_level"], patient["diseases"], patient["sintomns"])
    response = send_prompt(prompt)
    patient["speciality"], patient["time"] = response.content.split(";")
    return jsonify(patient)

@api.route('/order-queue', methods=['POST'])
def order_queue():
    data = request.json
    queue = data["queue"]
    new_patient = data["new_patient"]
    response = order_queue_prompt(queue, new_patient)
    return jsonify(position=response.content)

def describe_pacient(pacient):
    return f"O paciente tem {pacient['pain_level']} de dor, {pacient['diseases']} e descreveu os seguintes sintomas: {pacient['sintomns']} e vai ser atendido por um médico de {pacient['speciality']} por {pacient['time']}"

def order_queue_prompt(queue, new_element):
    client = OpenAI(api_key=app.config['OPEN_AI_API_KEY'])
    prompt = f"Novo paciente:\n{describe_pacient(new_element)}\nFila de espera:\n"
    for i, pacient in enumerate(queue):
        prompt += f"\n{i+1} - {describe_pacient(pacient)}"
    print(prompt)
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Você é um assistente hospitalar que define a ordem de atendimento de pacientes em uma fila de espera baseado na urgencia que cada paciente deve ser atendido de acordo com suas condições, sendo possivel que pacientes com condições mais urgentes sejam atendidos primeiro que pacientes que já estão na fila. Você deve responder em uma unica expressão qual a posição o paciente deve assumir na fila de espera considerando que a posição 1 é a próxima a ser atendida. sem o ponto final seguido da justificativa. Exemplo: '1'."},
        {"role": "user", "content": prompt}
    ]
    )
    return completion.choices[0].message

def send_prompt(prompt):
    client = OpenAI(api_key=app.config['OPEN_AI_API_KEY'])

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Você é um assistente hospitalar que define qual especialidade médica uma pessoa precisa baseado nos sintomas, nível de dor e doenças pré existentes que ela descreve. Você deve responder em uma unica expressão qual especialidade médica é a mais adequada para o caso sem o ponto final. Exemplo: 'Cardiologia'. E depois informar quanto tempo levará a consulta no formato HH:mm. Os campos da resposta devem estar separados por um ponto e virgula e não deve haver espaços entre os campos. Exemplo: 'Cardiologia;00:30'"},
        {"role": "user", "content": prompt}
    ]
    )
    return completion.choices[0].message

def build_prompt(pain_level, diseases, prompt):
    return f"O paciente tem {pain_level} de dor, {diseases} e descreveu os seguintes sintomas: {prompt}"