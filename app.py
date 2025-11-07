import streamlit as st
from ollama import chat
from PIL import Image
import io


st.set_page_config(page_title="Paveikslėlio aprašymas", page_icon="🖼️", layout="centered")

st.title("Paveikslėlio aprašymas — gemma:4b + Ollama")
st.write("Įkelkite paveikslėlį, o modelis apibūdins jo turinį.")

with st.sidebar:
    st.header("Nustatymai")
    model = st.text_input("Modelis", value="gemma:4b")
    temperature = st.slider("Kūrybiškumas (temperature)", 0.0, 1.0, 0.0, 0.05)
    max_tokens = st.number_input("Max predict (num_predict)", min_value=16, max_value=2048, value=256, step=16)
    st.markdown("---")
    st.write("Pastaba: įsitikinkite, kad Ollama serveris veikia (`ollama serve`) ir modelis yra paruoštas.")


uploaded_file = st.file_uploader("Pasirinkite paveikslėlį", type=["png", "jpg", "jpeg", "webp", "bmp"])

default_prompt = (
    "Apibūdink trumpai, kas matoma šiame paveikslėlyje. Pateik 2-4 sakinius, įtraukti pagrindinius objektus, veiksmą ir aplinką."
)

prompt = st.text_area("Klausimas modeliui", value=default_prompt, height=120)

if uploaded_file is not None:
    # Read bytes for both display and model
    image_bytes = uploaded_file.read()

    try:
        image = Image.open(io.BytesIO(image_bytes))
        st.image(image, caption="Įkeltas paveikslėlis", use_column_width=True)
    except Exception:
        st.write("Negalima atidaryti paveikslėlio per PIL, bet bandysiu siųsti žalius baitus į modelį.")

    if st.button("Apibūdinti paveikslėlį"):
        with st.spinner("Kreipiamasi į modelį..."):
            try:
                messages = [
                    {
                        "role": "user",
                        "content": prompt,
                        "images": [image_bytes],
                    }
                ]

                response = chat(
                    model=model,
                    messages=messages,
                    options={"temperature": float(temperature), "num_predict": int(max_tokens)},
                )

                # Response object shapes vary; try common accessors
                text = None
                if hasattr(response, "message") and getattr(response.message, "content", None):
                    text = response.message.content
                elif getattr(response, "response", None):
                    text = response.response
                else:
                    # Fallback to string representation
                    text = str(response)

                st.markdown("### Modelio atsakymas")
                st.write(text)

            except Exception as e:
                st.error("Įvyko klaida kreipiantis į Ollama:")
                st.exception(e)
                st.info("Patikrinkite, ar Ollama serveris veikia (`ollama serve`) ir ar modelis yra iškeltas (pull/pullable).")

else:
    st.info("Įkelkite paveikslėlį, kad pradėtumėte.")
