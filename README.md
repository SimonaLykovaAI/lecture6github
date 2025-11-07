# lecture6github
example on using github

## Paveikslėlio aprašymo Streamlit programa

Šiame repozitorijoje yra paprasta Streamlit aplikacija, kuri naudoja Ollama modelį `gemma:4b` paveikslėlių aprašymui.

Kaip paleisti lokaliai:

1. Įdiekite priklausomybes:

```bash
python -m pip install -r requirements.txt
```

2. Paleiskite Ollama serverį (jei dar neveikia):

```bash
ollama serve
```

3. Paleiskite Streamlit aplikaciją:

```bash
streamlit run app.py
```

Pastaba: įsitikinkite, kad modelis `gemma:4b` yra iškeltas arba pasiekiamas jūsų Ollama instancijoje. Jei reikia, naudokite `ollama pull gemma:4b`.

