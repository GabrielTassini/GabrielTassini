from fastapi import FastAPI, HTTPException, Query
from datetime import datetime, timedelta

app = FastAPI()

def convert_to_date(date_string):
    try:
        return datetime.strptime(date_string, '%d/%m/%Y')
    except ValueError:
        raise ValueError("O formato da data fornecida está incorreto. Use (dd/mm/yyyy).")

def calculate_days_percentage(num, den):
    return (num / den) * 100 if den != 0 else 0

def calculate_without_decay(admission_date, resignation_date, cutoff_date, distribution_date):
    admission_date = convert_to_date(admission_date)
    resignation_date = convert_to_date(resignation_date)
    cutoff_date = convert_to_date(cutoff_date)
    distribution_date = convert_to_date(distribution_date)

    total_worked_days = (resignation_date - admission_date).days + 1
    decadence_date = distribution_date - timedelta(days=5 * 365.25)

    if decadence_date < admission_date:
        decadence_days = 0
        non_decadence_days = total_worked_days
        seller_days = (cutoff_date - admission_date).days + 1 if cutoff_date >= admission_date else 0
        buyer_days = (resignation_date - cutoff_date).days if cutoff_date <= resignation_date else 0
    else:
        decadence_days = (decadence_date - admission_date).days + 1
        non_decadence_days = total_worked_days - decadence_days
        seller_days = (cutoff_date - decadence_date).days + 1 if cutoff_date >= decadence_date else 0
        buyer_days = (resignation_date - cutoff_date).days if cutoff_date <= resignation_date else 0

    decadence_percent = calculate_days_percentage(decadence_days, total_worked_days)
    seller_percent = calculate_days_percentage(seller_days, non_decadence_days)
    buyer_percent = calculate_days_percentage(buyer_days, non_decadence_days)

    return {
        "total_worked_days": total_worked_days,
        "decadence_days": decadence_days,
        "seller_days": seller_days,
        "buyer_days": buyer_days,
        "decadence_percent": decadence_percent,
        "seller_percent": seller_percent,
        "buyer_percent": buyer_percent
    }

def calculate_with_decay(admission_date, resignation_date, cutoff_date, distribution_date):
    data_admissao = convert_to_date(admission_date)
    data_demissao = convert_to_date(resignation_date)
    data_distribuicao = convert_to_date(distribution_date)
    data_corte = convert_to_date(cutoff_date)

    data_decadencia = data_distribuicao - timedelta(days=5 * 365)

    periodo_total = (data_demissao - data_admissao).days
    periodo_com_decadencia = (data_decadencia - data_admissao).days
    percentual_periodo_com_decadencia = (periodo_com_decadencia / periodo_total) * 100

    periodo_vendedores = (data_corte - data_decadencia).days
    periodo_compradores = (data_demissao - data_corte).days

    responsabilidade_vendedores = (periodo_vendedores / (periodo_vendedores + periodo_compradores)) * 100
    responsabilidade_compradores = (periodo_compradores / (periodo_vendedores + periodo_compradores)) * 100

    return {
        "total_worked_days": periodo_total,
        "decadence_days": periodo_com_decadencia,
        "seller_days": periodo_vendedores,
        "buyer_days": periodo_compradores,
        "decadence_percent": percentual_periodo_com_decadencia,
        "seller_percent": responsabilidade_vendedores,
        "buyer_percent": responsabilidade_compradores
    }

def calculate_dates(admission_date, resignation_date, cutoff_date, distribution_date):
    total_days = (convert_to_date(resignation_date) - convert_to_date(admission_date)).days

    if total_days > 5 * 365:
        return calculate_with_decay(admission_date, resignation_date, cutoff_date, distribution_date)
    else:
        return calculate_without_decay(admission_date, resignation_date, cutoff_date, distribution_date)

@app.get("/hello")
def hello():
    return "Hello"

@app.get("/calculadora")
def calculadora(
    admission_date: str = Query(..., description="Data de admissão no formato dd/mm/yyyy"),
    resignation_date: str = Query(..., description="Data de demissão no formato dd/mm/yyyy"),
    cutoff_date: str = Query(..., description="Data de corte no formato dd/mm/yyyy"),
    distribution_date: str = Query(..., description="Data de distribuição no formato dd/mm/yyyy")
):
    try:
        results = calculate_dates(admission_date, resignation_date, cutoff_date, distribution_date)
        return results
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
