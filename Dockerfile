FROM python:3.10.11-slim-buster

WORKDIR /app

COPY api/requirements.txt .

RUN pip install -U pip && pip install -r requirements.txt

COPY api/ ./api

COPY model/model_reg.pkl ./model/model_reg.pkl

COPY model/model_clf.pkl ./model/model_clf.pkl

COPY model/model_scaler.pkl ./model/model_scaler.pkl

COPY initializer.sh .

RUN chmod +x initializer.sh

EXPOSE 8000

ENTRYPOINT [ "./initializer.sh" ]