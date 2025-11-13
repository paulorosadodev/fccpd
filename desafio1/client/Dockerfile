# Dockerfile para o cliente que faz requisições HTTP
FROM alpine:3.19

# Instala curl e bash
RUN apk add --no-cache curl bash python3

# Define o diretório de trabalho
WORKDIR /app

# Copia o script de requisições
COPY request.sh .

# Torna o script executável
RUN chmod +x request.sh

# Comando para executar o script
CMD ["./request.sh"]

