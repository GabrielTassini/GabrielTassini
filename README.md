
Refinamento PDF
Mathpix
Marker

marker_single ./data/douglas_bersch_sample.pdf OUTPUT --batch_multiplier 2 --langs Portuguese

uvicorn app:app --reload


#
- Docker Registry
> Guardar imagens dos seus sistemas

1. Criar imagem docker do seu código

`docker build -t gabriel-img .` 
`docker tag gabriel-img simonaggio.azurecr.io/gabriel-img` 
`docker login -u simonaggio -p U6m4OUkc8Q8PgJDkADgQX2byphXf1J4AF/wsLj144P+ACRBJ0qpa simonaggio.azurecr.io`
`docker push simonaggio.azurecr.io/gabriel-img`

> Docker é uma ferramenta para virtualização

2. Enviar ela para o container registry do Azure
> 

3. Criar o serviço a partir da imagem

