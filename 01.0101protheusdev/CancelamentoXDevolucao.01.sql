SELECT 
    'P |01|01' 
        AS BK_EMPRESA
    ,CASE 
        WHEN SLX.LX_FILIAL IS NULL 
        THEN 'P |01||' 
        ELSE 'P |01|01'+ CAST(SLX.LX_FILIAL AS CHAR (4) ) 
        END 
        AS BK_FILIAL
    ,'P |01|SA6010|'+COALESCE(NULLIF(RTRIM( COALESCE(SA6.A6_FILIAL,' ') )+'|'+RTRIM( COALESCE(SLX.LX_OPERADO,' ') ),' '),'|') 
        AS BK_OPERADOR
    , SLX.LX_DTMOVTO 
        AS DATA
    , SLX.LX_CUPOM
        AS NUMERO_DOCUMENTO
    , SLX.LX_SERIE
        AS SERIE_DOCUMENTO
    , SLX.LX_ITEM
        AS NUMERO_ITEM 
    , SLX.LX_VALOR
        AS VALOR_ITEM 
    ,'P |01|SB1010|'+COALESCE(NULLIF(RTRIM( COALESCE(SB1.B1_FILIAL,' ') )+'|'+RTRIM( COALESCE(SLX.LX_PRODUTO,' ') ),' '),'|') 
        AS BK_PRODUTO
    , SLX.LX_QTDE
        AS QUANTIDADE_ITEM 
    , SLX.LX_TPCANC
        AS TIPO_CANCELAMENTO
    , SLX.LX_SITUA
        AS STATUS_DOCUMENTO 
    , SLX.LX_SDOC
        AS SERIE_ORCAMENTO 
    , SLX.LX_NUMORC 
        AS NUMERO_ORCAMENTO
    ,'P |01|SA3010|'+COALESCE(NULLIF(RTRIM( COALESCE(SB1.B1_FILIAL,' ') )+'|'+RTRIM( COALESCE(SL1.L1_VEND,' ') ),' '),'|') 
        AS BK_VENDEDOR
    ,SL1.L1_EMISNF
        AS DATA_EMISSAO


FROM SLX010 SLX
    LEFT JOIN SA6010 SA6 
        ON SA6.A6_FILIAL = SLX.LX_FILIAL
        AND SA6.A6_COD = SLX.LX_OPERADO 
        AND SA6.D_E_L_E_T_ = ' '
    LEFT JOIN SB1010 SB1 
        ON SB1.B1_FILIAL = SUBSTRING(SLX.LX_FILIAL , 1 , 2) 
        AND SB1.B1_COD = SLX.LX_PRODUTO
        AND SB1.D_E_L_E_T_ = ' ' 
    LEFT JOIN SL1010 SL1
        ON SL1.L1_FILIAL = SLX.LX_FILIAL
        AND SL1.L1_DOC = SLX.LX_CUPOM
        AND SL1.L1_SERIE = SLX.LX_SERIE
        AND SL1.D_E_L_E_T_ = ' '

WHERE 
    SLX.LX_DTMOVTO BETWEEN <<START_DATE>> AND <<FINAL_DATE>> 
    AND SLX.D_E_L_E_T_ = ' '