import random
import time

import streamlit as st

from generator import IdoGeikoGenerator, Step, format_step, rotate_cycle


st.set_page_config(page_title="IDO GEIKO - Kyokushin", layout="centered")

st.title("IDO GEIKO CIRCULAR - KYOKUSHIN")

level = st.slider("Número de técnicas por paso (1-5)", 1, 5, 3)

use_custom_seed = st.checkbox("Usar seed personalizada")
seed = None

if use_custom_seed:
    seed = int(st.number_input("Seed", min_value=0, value=12345, step=1))
else:
    seed = int(time.time() * 1000) + random.randint(0, 10000)

if st.button("Generar"):
    generator = IdoGeikoGenerator(seed)

    st.caption(f"Seed: {seed}")
    st.divider()

    starting_position, base_cycle = generator.generate_cycle(level)

    st.subheader("Posición inicial")
    st.write(f"**{starting_position}**")
    st.divider()

    for start in range(1, 5):
        st.subheader(f"Empezando desde paso {start}")
        rotated = rotate_cycle(
            [Step(s.number, s.stance, s.combo.copy()) for s in base_cycle],
            start,
        )
        for step in rotated:
            st.write(format_step(step))
        st.divider()
