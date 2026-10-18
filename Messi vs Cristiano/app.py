import json
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parent / "data_limpia"
JUG = ["Ronaldo", "Messi"]
NOMBRE = {"Ronaldo": "Cristiano Ronaldo", "Messi": "Lionel Messi"}

PALETA = {
    "Ronaldo": "#c8323d",
    "Messi": "#1f6fd1",
    "tinta": "#1e2624",
    "tinta_2": "#5b6662",
    "papel": "#f6f8f7",
    "regla": "#d9dedc",
    "grid": "rgba(30, 38, 36, 0.06)",
    "cancha": "#2e6b4f",
}
BANDA = {"Ronaldo": "rgba(200, 50, 61, 0.14)", "Messi": "rgba(31, 111, 209, 0.14)"}

MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]


def mes_txt(f):
    f = pd.Timestamp(f)
    return f"{MESES[f.month - 1]} {f.year}"


st.set_page_config(page_title="La carrera a los 1000 goles", layout="wide")

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Barlow:wght@400;500;600&display=swap');

#MainMenu, footer, header, [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] {{
    visibility: hidden; height: 0;
}}
.stApp {{ background: {PALETA["papel"]}; }}
html, body, .stApp, .stMarkdown, label, p {{ font-family: 'Barlow', sans-serif; color: {PALETA["tinta"]}; }}
.block-container {{ padding-top: 2.2rem; padding-bottom: 3rem; max-width: 1280px; }}

h1.titulo {{
    font-family: 'Barlow Condensed', sans-serif; font-weight: 700; font-size: 2.9rem;
    line-height: 1.02; letter-spacing: -0.01em; margin: 0 0 .4rem 0; color: {PALETA["tinta"]};
}}
p.bajada {{ font-size: 1.05rem; color: {PALETA["tinta_2"]}; max-width: 70ch; margin: 0 0 1.6rem 0; }}

.marcador {{
    display: grid; grid-template-columns: 1fr 1fr; border-top: 3px solid {PALETA["tinta"]};
    border-bottom: 1px solid {PALETA["regla"]}; margin-bottom: 1.4rem;
}}
.lado {{ padding: 1.1rem 1.6rem 1.3rem 0; }}
.lado + .lado {{ border-left: 1px solid {PALETA["regla"]}; padding-left: 1.6rem; }}
.lado .nombre {{ font-weight: 600; font-size: 1.05rem; display: flex; align-items: center; gap: .5rem; }}
.lado .nombre i {{ width: 12px; height: 12px; border-radius: 2px; display: inline-block; }}
.lado .cifra {{ font-family: 'Barlow Condensed', sans-serif; font-weight: 600; line-height: .9; margin: .35rem 0 .2rem 0; }}
.lado .cifra b {{ font-size: 5.6rem; font-weight: 700; }}
.lado .cifra span {{ font-size: 1.6rem; color: {PALETA["tinta_2"]}; margin-left: .35rem; }}
.lado .barra {{ height: 6px; background: {PALETA["regla"]}; border-radius: 3px; margin: .6rem 0 1rem 0; overflow: hidden; }}
.lado .barra div {{ height: 100%; border-radius: 3px; }}
.lado dl {{ display: grid; grid-template-columns: repeat(3, auto); gap: .2rem 2rem; margin: 0; justify-content: start; }}
.lado dt {{ font-size: .85rem; color: {PALETA["tinta_2"]}; }}
.lado dd {{ margin: 0; white-space: nowrap; font-family: 'Barlow Condensed', sans-serif; font-size: 1.55rem; font-weight: 600; }}
.eficiencia {{ display: grid; grid-template-columns: repeat(2, minmax(0, 11rem)); gap: .75rem; margin-top: .9rem; }}
.ficha {{ border: 1px solid {PALETA["regla"]}; border-radius: 4px; padding: .5rem .8rem .55rem; background: rgba(255, 255, 255, .55); }}
.ficha span {{ display: block; font-size: .8rem; color: {PALETA["tinta_2"]}; }}
.ficha b {{ font-family: 'Barlow Condensed', sans-serif; font-size: 1.2rem; font-weight: 600; }}
p.contexto {{ font-size: .98rem; margin: -.4rem 0 1.2rem 0; max-width: 80ch; color: {PALETA["tinta"]}; }}
.veredicto {{ font-size: 1.1rem; margin: 0 0 1.8rem 0; max-width: 75ch; }}
.veredicto strong {{ font-weight: 600; }}

h3.seccion {{ font-family: 'Barlow Condensed', sans-serif; font-weight: 600; font-size: 1.55rem; margin: 1.6rem 0 .2rem 0; }}
p.nota {{ font-size: .92rem; color: {PALETA["tinta_2"]}; margin: 0 0 .6rem 0; max-width: 80ch; }}

@media (max-width: 760px) {{
    .marcador {{ grid-template-columns: 1fr; }}
    .lado + .lado {{ border-left: none; border-top: 1px solid {PALETA["regla"]}; padding-left: 0; }}
    .lado .cifra b {{ font-size: 4.2rem; }}
    h1.titulo {{ font-size: 2.2rem; }}
}}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def cargar():
    base = pd.read_csv(DATA / "modelo_base.csv", parse_dates=["mitad", "fin"])
    params = json.loads((DATA / "parametros_modelo.json").read_text(encoding="utf-8"))
    res_a = pd.read_csv(DATA / "resultados_modelo_a.csv", index_col="jugador")
    res_b = pd.read_csv(DATA / "resultados_modelo_b.csv", index_col="jugador")
    proy_b = pd.read_csv(DATA / "proyeccion_bayes.csv", parse_dates=["fecha"])
    lleg_b = pd.read_csv(DATA / "llegadas_bayes.csv", parse_dates=["Messi", "Ronaldo"])
    pj = pd.read_csv(DATA / "partidos.csv", index_col="jugador")
    return base, params, res_a, res_b, proy_b, lleg_b, pj


base, P, res_a, res_b, proy_b, lleg_b, pj = cargar()
pj["ratio"] = pj.goles / pj.partidos
CORTE = {j: pd.Timestamp(P["corte"][j]) for j in JUG}
CONTRATO = {j: pd.Timestamp(P["contrato"][j]) for j in JUG}


@st.cache_data
def modelo_a(hasta):
    rng = np.random.default_rng(11)
    proy, lleg = [], {}
    for j in JUG:
        lam = res_a.loc[j, "goles_por_año"]
        sem = pd.date_range(CORTE[j], hasta, freq="7D")[1:]
        t = ((sem - CORTE[j]).days / 365.25).values
        sims = P["total"][j] + rng.poisson(lam * t, size=(4000, len(t)))
        q = np.percentile(sims, [10, 50, 90], axis=0)
        proy.append(pd.DataFrame({"jugador": j, "fecha": sem, "p10": q[0], "p50": q[1], "p90": q[2]}))
        dias = rng.gamma(1000 - P["total"][j], 1 / lam, 20000) * 365.25
        lleg[j] = CORTE[j] + pd.to_timedelta(dias, unit="D")
    return pd.concat(proy), pd.DataFrame(lleg)


st.markdown('<h1 class="titulo">Messi o Cristiano Ronaldo: ¿quién llegará primero a los mil goles?</h1>', unsafe_allow_html=True)
st.markdown(
    f'<p class="bajada">Proyección estadística de la fecha en que cada jugador alcanzará los 1000 goles oficiales '
    f'(club y selección), a partir de su rendimiento reciente ajustado por edad y nivel de liga. '
    f'Datos hasta el {CORTE["Messi"]:%d/%m/%Y} (Messi) y el {CORTE["Ronaldo"]:%d/%m/%Y} (Ronaldo).</p>',
    unsafe_allow_html=True)

with st.container():
    c1, c2, c3, _ = st.columns([1.3, 1.1, 1.1, 1.5])
    modelo = c1.radio("Modelo", ["Bayesiano con edad", "Decaimiento temporal"], horizontal=True)
    hasta_anio = c2.select_slider("Proyectar hasta", options=[2027, 2028, 2029, 2030], value=2029)
    desde_anio = c3.select_slider("Historia desde", options=list(range(2008, 2025, 2)), value=2016)

hasta = pd.Timestamp(f"{hasta_anio}-12-31")

if modelo.startswith("Bayesiano"):
    proy = proy_b[proy_b.fecha <= hasta]
    lleg = lleg_b
else:
    proy, lleg = modelo_a(hasta)

lleg_r, lleg_m = lleg["Ronaldo"], lleg["Messi"]
p_cr7 = (lleg_r.notna() & (lleg_m.isna() | (lleg_r < lleg_m))).mean()
ventaja = (lleg_m - lleg_r).median().days / 30.44


def lado(j):
    tot = P["total"][j]
    f = lleg[j].dropna()
    p10, p50, p90 = f.quantile([.1, .5, .9])
    p_contrato = (lleg[j] < CONTRATO[j]).mean()
    return f"""<div class="lado">
<div class="nombre"><i style="background:{PALETA[j]}"></i>{NOMBRE[j]}</div>
<div class="cifra"><b>{tot}</b><span>de 1000</span></div>
<div class="barra"><div style="width:{tot / 10:.1f}%; background:{PALETA[j]}"></div></div>
<dl>
<dt>Goles que faltan</dt><dt>Fecha estimada</dt><dt>Antes del fin de contrato</dt>
<dd>{1000 - tot}</dd><dd>{mes_txt(p50)}</dd><dd>{p_contrato:.0%}</dd>
</dl>
<p class="nota" style="margin-top:.5rem">Rango probable (80%): {mes_txt(p10)} a {mes_txt(p90)}. Contrato vigente hasta {mes_txt(CONTRATO[j])}.</p>
<div class="eficiencia">
<div class="ficha"><span>Goles por partido</span><b>{pj.loc[j, "ratio"]:.2f}</b></div>
<div class="ficha"><span>Partidos jugados</span><b>{pj.loc[j, "partidos"]}</b></div>
</div>
</div>"""


st.markdown(f'<div class="marcador">{lado("Ronaldo")}{lado("Messi")}</div>', unsafe_allow_html=True)

mas, menos = pj.partidos.idxmax(), pj.partidos.idxmin()
dif = pj.loc[mas, "partidos"] - pj.loc[menos, "partidos"]
st.markdown(
    f'<p class="contexto">{NOMBRE[mas]} ha disputado <strong>{dif} partidos más</strong> que {NOMBRE[menos]} '
    f'({pj.loc[mas, "partidos"]} frente a {pj.loc[menos, "partidos"]}). Por partido, Messi promedia '
    f'{pj.loc["Messi", "ratio"]:.2f} goles y Ronaldo {pj.loc["Ronaldo", "ratio"]:.2f}. '
    f'Goles y partidos tomados del mismo corte ({pd.Timestamp(pj.corte.iloc[0]):%d/%m/%Y}).</p>',
    unsafe_allow_html=True)

lider = "Cristiano Ronaldo" if p_cr7 >= .5 else "Lionel Messi"
st.markdown(
    f'<p class="veredicto"><strong>{lider} llega primero en el {max(p_cr7, 1 - p_cr7):.0%} de las simulaciones</strong>, '
    f'con una ventaja mediana de {abs(ventaja):.0f} meses.</p>', unsafe_allow_html=True)


def estilo(fig, alto):
    fig.update_layout(
        height=alto, margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Barlow, sans-serif", size=13, color=PALETA["tinta"]),
        hoverlabel=dict(bgcolor="white", bordercolor=PALETA["regla"], font=dict(family="Barlow, sans-serif", color=PALETA["tinta"])),
        legend=dict(orientation="h", x=0, y=1.02, xanchor="left", yanchor="bottom", bgcolor="rgba(0,0,0,0)"),
        showlegend=True,
    )
    fig.update_xaxes(gridcolor=PALETA["grid"], zeroline=False, linecolor=PALETA["regla"], ticks="")
    fig.update_yaxes(gridcolor=PALETA["grid"], zeroline=False, showline=False, ticks="")
    return fig


SIN_BARRA = {"displayModeBar": False}

st.markdown('<h3 class="seccion">Goles acumulados y proyección</h3>', unsafe_allow_html=True)
st.markdown('<p class="nota">Línea continua: goles reales al cierre de cada año. Línea discontinua: mediana proyectada. '
            'Banda: 80% de los escenarios simulados.</p>', unsafe_allow_html=True)

fig = go.Figure()
for j in JUG:
    h = base[base.jugador == j].assign(acum=lambda d: d.goles.cumsum())
    h = h[h.anio >= desde_anio]
    p = proy[proy.jugador == j]
    col = PALETA[j]

    fig.add_trace(go.Scatter(x=pd.concat([p.fecha, p.fecha[::-1]]), y=pd.concat([p.p90, p.p10[::-1]]),
                             fill="toself", fillcolor=BANDA[j], line=dict(width=0), hoverinfo="skip", showlegend=False))
    fig.add_trace(go.Scatter(x=h.fin, y=h.acum, name=NOMBRE[j], mode="lines+markers",
                             line=dict(color=col, width=2.5), marker=dict(size=7, color=col, line=dict(color="white", width=2)),
                             hovertemplate="%{x|%d/%m/%Y}<br>%{y:.0f} goles<extra>" + j + "</extra>"))
    fig.add_trace(go.Scatter(x=p.fecha, y=p.p50, mode="lines", line=dict(color=col, width=2, dash="dash"), showlegend=False,
                             customdata=np.stack([p.p10, p.p90], axis=1),
                             hovertemplate="%{x|%b %Y}<br>Mediana %{y:.0f} goles<br>80%: %{customdata[0]:.0f} a %{customdata[1]:.0f}<extra>" + j + "</extra>"))

    med = lleg[j].dropna().median()
    if med <= hasta:
        fig.add_trace(go.Scatter(x=[med], y=[1000], mode="markers", showlegend=False, hoverinfo="skip",
                                 marker=dict(size=12, color=col, line=dict(color="white", width=2.5))))
        fig.add_annotation(x=med, y=1000, text=f"{j}: {mes_txt(med)}", showarrow=False,
                           yshift=18 if j == "Ronaldo" else -18, xanchor="right" if j == "Ronaldo" else "left",
                           font=dict(size=13, color=PALETA["tinta"]))

fig.add_hline(y=1000, line=dict(color=PALETA["tinta_2"], width=1, dash="dot"))
y_min = min(base[base.jugador == j].goles.cumsum()[base[base.jugador == j].anio >= desde_anio].min() for j in JUG)
fig.update_yaxes(range=[y_min - 30, 1080], title=None)
fig.update_xaxes(range=[pd.Timestamp(f"{desde_anio}-06-01"), hasta])
st.plotly_chart(estilo(fig, 460), config=SIN_BARRA)

izq, der = st.columns([1.15, 1], gap="large")

with izq:
    st.markdown('<h3 class="seccion">Cuándo llega cada uno</h3>', unsafe_allow_html=True)
    st.markdown('<p class="nota">Distribución mensual de la fecha en que cada escenario simulado alcanza el gol 1000. '
                'Las líneas punteadas marcan el fin de cada contrato.</p>', unsafe_allow_html=True)
    fig2 = go.Figure()
    for j in JUG:
        fig2.add_trace(go.Histogram(x=lleg[j].dropna(), name=NOMBRE[j], marker_color=PALETA[j], opacity=0.8,
                                    xbins=dict(size="M1"), histnorm="percent",
                                    hovertemplate="%{x|%b %Y}<br>%{y:.0f}% de los escenarios<extra>" + j + "</extra>"))
        fig2.add_shape(type="line", x0=CONTRATO[j], x1=CONTRATO[j], y0=0, y1=1, yref="paper",
                       line=dict(color=PALETA[j], width=1.5, dash="dot"))
        fig2.add_annotation(x=CONTRATO[j], y=1, yref="paper", text=f"fin contrato {j}", showarrow=False,
                            xanchor="left", xshift=4, yanchor="top", font=dict(size=11, color=PALETA["tinta_2"]))
    fig2.update_layout(barmode="overlay", bargap=0.08)
    fig2.update_yaxes(ticksuffix="%")
    st.plotly_chart(estilo(fig2, 330), config=SIN_BARRA)

with der:
    st.markdown('<h3 class="seccion">Comparación de modelos</h3>', unsafe_allow_html=True)
    st.markdown('<p class="nota">El modelo bayesiano añade la caída por edad y la incertidumbre sobre el ritmo real; '
                'por eso sus rangos son más amplios.</p>', unsafe_allow_html=True)
    lleg_a = modelo_a(hasta)[1]
    filas = []
    for nombre_m, l in [("Decaimiento temporal", lleg_a), ("Bayesiano con edad", lleg_b)]:
        for j in JUG:
            f = l[j].dropna()
            filas.append({
                "Jugador": j, "Modelo": nombre_m,
                "Fecha estimada": mes_txt(f.median()),
                "Rango 80%": f"{mes_txt(f.quantile(.1))} a {mes_txt(f.quantile(.9))}",
                "Antes del contrato": f"{(l[j] < CONTRATO[j]).mean():.0%}",
            })
    tabla = pd.DataFrame(filas)
    st.dataframe(tabla, hide_index=True)

st.markdown('<h3 class="seccion">Datos de entrada del modelo</h3>', unsafe_allow_html=True)
st.markdown(f'<p class="nota">Goles por año calendario. Los goles ajustados equivalen a goles en una liga top europea; '
            f'el peso combina la etapa de carrera y un decaimiento exponencial con vida media de {P["H"] * 12:.0f} meses '
            f'(calibrada por backtest).</p>', unsafe_allow_html=True)

tab = base.assign(Peso=base.w / base.groupby("jugador").w.transform("sum") * 100)
tab = tab[tab.anio >= desde_anio]
tab = tab.rename(columns={"jugador": "Jugador", "anio": "Año", "goles": "Goles", "goles_aj": "Goles ajustados",
                          "coef_mix": "Coef. liga", "edad": "Edad", "etapa": "Etapa"})
tab["Coef. liga"] = tab["Coef. liga"] * 100
tab = tab.pivot(index="Año", columns="Jugador", values=["Goles", "Goles ajustados", "Coef. liga", "Peso"])
tab.columns = [f"{a} {b}" for a, b in tab.columns]
tab = tab.reset_index().sort_values("Año", ascending=False)

st.dataframe(
    tab, hide_index=True,
    column_config={c: st.column_config.NumberColumn(c, format="%.0f%%" if c.startswith(("Coef", "Peso")) else "%.0f")
                   for c in tab.columns if c != "Año"} | {"Año": st.column_config.NumberColumn("Año", format="%d")},
)

st.markdown(f'<p class="nota" style="margin-top:1.4rem">Fuentes: messivsronaldo.football (resúmenes por año y totales), '
            f'registro gol a gol de Messi y dataset de goles de club de Cristiano Ronaldo (Kaggle). '
            f'Coeficientes de liga inspirados en el Opta Power Rankings.</p>', unsafe_allow_html=True)

