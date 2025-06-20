
# 🧠 INFO8985 Flask Monolith – Observability with OpenTelemetry + SigNoz

This project demonstrates full observability (logging, tracing, and metrics) for a Python Flask monolithic application using **OpenTelemetry** and **SigNoz**.

> ✅ Built and tested in GitHub Codespaces  
> ✅ Real-time visibility using SigNoz  
> ✅ Includes error tracking and custom metrics

---

## 📌 Technologies Used

| Tool               | Purpose                                  |
|--------------------|-------------------------------------------|
| Flask              | Python web framework                     |
| OpenTelemetry SDK  | Instrumentation (logs, traces, metrics)  |
| SigNoz             | Observability backend (view everything)  |
| Docker Compose     | For running SigNoz locally               |

---

## 🎯 Project Goals

- ✅ Add OpenTelemetry to an existing Flask monolith  
- ✅ Send traces, metrics, and logs to SigNoz  
- ✅ Capture and display exceptions  
- ✅ Create meaningful dashboards in SigNoz

---

## 🧰 Setup Instructions

### 1. Clone This Repo

```bash
git clone https://github.com/jpremchander/info8985_monolith_analysis.git
cd info8985_monolith_analysis
```

### 2. Install Python Dependencies

```bash
pip install flask opentelemetry-sdk \
    opentelemetry-exporter-otlp \
    opentelemetry-instrumentation-flask
```

### 3. Clone SigNoz as Submodule

```bash
git submodule update --init --recursive
cd signoz/deploy/docker
docker-compose up -d
```

🧭 SigNoz UI: [http://localhost:8080](http://localhost:8080)

> Wait ~2 minutes for containers to become healthy.

---

## 🚀 Run the Flask App

In the root folder:

```bash
python app.py
```

✅ Flask will start on: `http://localhost:5000`

---

## 🔎 Available Endpoints

| Method | Endpoint             | Description                                |
|--------|----------------------|--------------------------------------------|
| GET    | `/rolldice`          | Roll a 6-sided dice                        |
| GET    | `/rolldice?player=Me`| Attach player name to log/trace            |
| GET    | `/rolldice?sides=0`  | Triggers an exception (for testing errors) |

---

## 📊 Observability Features in SigNoz

## Dashboard

![alt text](Dashboard.png)


## Service

![alt text](service-visible.png)


### 🟣 Traces

- Span: `roll`
- Attributes: `roll.value`, `player`
- Visible in **Traces tab → info8985-flask-app**

📷 

![alt text](roll-spantrace-attributes.png)


![alt text](roll-spantrace-attributes-2.png)


### 🟢 Metrics

- Custom counter: `dice.rolls`
- Label: `roll.value`
- Viewable via dashboard panel

📷 

![alt text](metrics.png)

### 🔵 Logs

- Collected using OpenTelemetry’s logger
- Level: `INFO`, `WARNING`, `ERROR`
- Search: `"rolling the dice"` or `"Error occurred"`

📷

![alt text](logs.png)

### 🔴 Exceptions

- Tracked using `record_exception` and span status
- Viewable as red spans in the **Traces** tab
- Used in computing **Error Rate %**

📷 

![alt text](error-signals.png)

![alt text](errors-percentage.png)

---

## 📈 Example Dashboard Panels

| Panel Type | Metric Source | Description                  |
|------------|---------------|------------------------------|
| Time Series| `dice.rolls`  | Count of rolls per value     |
| % Number   | Traces        | Error Rate (`status.code`)   |
| Bar Chart  | Logs          | Top players rolling          |
| Apdex Score| Traces        | End-user satisfaction        |



---

## 🧑‍💻 Author

- Name: *Premchander J*
- Student ID: *9015480*
- Course: INFO8985 – Database Automation - Inclass Task 3

---

## 🧼 Cleanup

To stop all containers:

```bash
cd signoz/deploy/docker
docker-compose down
```

---


