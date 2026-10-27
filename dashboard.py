import streamlit as st
import json
import pandas as pd
import os
import time

st.set_page_config(page_title="Supervision Helpdesk IT", layout="wide")

st.title("⚡ Dashboard de Supervision Dynamique - Agent Helpdesk IT")
st.caption("🔄 Actualisation automatique en temps réel des métriques et logs")

LOG_FILE = "executions_log.json"

if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r") as f:
        try:
            logs = json.load(f)
        except:
            logs = []
    
    if logs:
        df = pd.DataFrame(logs)
        
        # 1. KPIs Globaux
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Tickets Traités", len(df))
        col2.metric("Taux de Résolution", f"{(df['status'] == 'SUCCESS').mean() * 100:.1f}%")
        col3.metric("Latence Moyenne", f"{df['duration_ms'].mean():.0f} ms")
        col4.metric("Coût Total LLM", f"${df['cost_usd'].sum():.4f}")
        
        st.divider()
        
        # 2. Graphiques Temporel & Métier
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("📈 Évolution de la Latence (ms)")
            st.line_chart(df[['duration_ms']])
        with c2:
            st.subheader("📊 Répartition par Catégorie")
            st.bar_chart(df['category'].value_counts())
            
        st.divider()
        
        # 3. Table des Traces (Correlation ID)
        st.subheader("📋 Traces en Direct (Correlation ID)")
        st.dataframe(
            df[['correlation_id', 'timestamp', 'status', 'category', 'priority', 'duration_ms', 'tokens_used']].iloc[::-1],
            use_container_width=True
        )
        
        # 4. Documentation des 3 Alertes
        st.subheader("🔔 Documentation des 3 Alertes de Supervision")
        st.markdown("""
        * ⚠️ **Alerte Latence (SLA)** : Déclenchée si `duration_ms > 1500 ms`
        * 🚨 **Alerte Taux d'Échec** : Déclenchée si `status == 'FAILURE'`
        * 💰 **Alerte Consommation Tokens** : Déclenchée si `tokens_used > 2000`
        """)
    else:
        st.warning("Fichier de logs vide. Lancez une exécution.")
else:
    st.info("Aucun log détecté. Lancez les tests ou l'agent.")

# Rafraîchissement automatique du dashboard toutes les 3 secondes
time.sleep(3)
st.rerun()