-- A consulta agrupa os dados de compras por cliente para gerar as métricas:
-- recencia_em_dias: Dias desde a última compra (quanto menor, melhor).
-- frequencia: Número total de compras.
-- valor_total: Soma total do valor gasto pelo cliente.

SELECT
    "Cliente",
    CURRENT_DATE - MAX("Data") AS recencia_em_dias,
    COUNT(*) AS frequencia,
    SUM("Valor") AS valor_total
FROM
    compras
GROUP BY
    "Cliente"