url = "https://infoms.saude.gov.br/extensions/SEIDIGI_DEMAS_VACINACAO_CALENDARIO_NACIONAL_COBERTURA_RESIDENCIA/SEIDIGI_DEMAS_VACINACAO_CALENDARIO_NACIONAL_COBERTURA_RESIDENCIA.html"
fltDivLoad = "//div[@id = 'body_load']"
fltBtnData = "//button[@id = 'aba2-tab']"
fltSelYear = "//select[@class = 'dropdownsel lui-select']/option[text() = '{year}']"
fltBtnConf = "//button[@title = 'Confirmar seleção']"
fltTagYear = "//div[@id = 'tagselections']/span[@id = 'Ano']"
fltTagUf = "//div[@id = 'tagselections']/span[@id = 'UF Residência']"
fltTagDim = "//div[@id = 'tagselections']/span[@id = 'Dimensao']"
fltTagMeas = "//div[@id = 'tagselections']/span[@id = 'Medida']"
fltTabData = "//div[@id = 'QVSelection-02']"
fltScrNum = ("scr:return document.querySelector("
             "\"span[title = 'Numerador']\")"
             )
fltScrDen = ("scr:return document.querySelector("
             "\"span[title = 'Denominador']\")"
             )
fltLnkExport = "//a[@id = 'exportar-dados-QV1-10']"
fltTxtUpdate = "//*[contains(text(), 'Atualização do painel')]"
dic_filters = {
    "year": {"tag": {"val": fltTagYear, "flt": "{year}"},
             "flt": {"val": fltSelYear}},
    "num": {"tag": {"val": fltTagMeas, "flt": "Numerador"},
            "flt": {"val": fltScrNum}},
    "den": {
        "tag": {"val": fltTagMeas, "flt": "Denominador"},
        "flt": {"val": fltScrDen}}
}