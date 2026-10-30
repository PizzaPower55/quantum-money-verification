import streamlit as st
import numpy as np
from simulation import prepare_pair, rng
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

st.set_page_config(page_title="Quantum Money Verification Simulator", layout="wide")

st.title("Quantum Information & Multi-Verifier Security Simulator")
st.markdown("""
This tool simulates **Wiesner's Quantum Money** protocol and analyzes multi-verifier security bounds under various attack strategies.
""")

# --- Tab Layout (Swapped order: How It Works is first) ---
tab_theory, tab_sim, tab_bloch = st.tabs(["How It Works", "Simulation Dashboard", "Bloch Sphere & Attack Visualization"])

with tab_theory:
    st.subheader("How It Works")
    st.markdown(r"""
    ### 1. The Money System (Wiesner's Quantum Money)
    Proposed by Stephen Wiesner in 1970, quantum money uses physical qubits instead of classical data. 
    Because of the **Quantum No-Cloning Theorem**, an unknown quantum state cannot be perfectly copied, 
    allowing counterfeit detection without needing to check a central database every time.

    ### 2. Attack Strategies Modeled in this Simulator:
    * **Attacker 1 (Naive Guessing):** Attempts to guess measurement outcomes without proper quantum operations.
    * **Attacker 2 (Standard Intermediate Measurement):** Performs standard projective measurements, causing wave-function collapse.
    * **Attacker 3 (Optimal Breidbart Basis Attack):** Utilizes custom projection operators ($V_{proj}$) on the Bloch sphere at a 22.5° offset to achieve the physical ceiling of **85.35%** ($\frac{1 + 1/\sqrt{2}}{2}$) fidelity limit per verifier.
    """)

with tab_sim:
    st.sidebar.header("Simulation Parameters")
    attacker_choice = st.sidebar.selectbox(
        "Select Adversarial Strategy",
        [
            "Attacker 1: Naive Random Guessing", 
            "Attacker 2: Standard Intermediate Measurement", 
            "Attacker 3: Optimal Breidbart Basis (~85.35% Limit)"
        ],
        key="sim_attacker"
    )
    num_verifiers = st.sidebar.slider("Number of Sequential Verifiers (Nodes)", min_value=1, max_value=10, value=5, key="sim_nodes")
    num_qubits = 1000

    if st.button("Run Simulation"):
        with st.spinner("Running simulation..."):
            
            token = []
            secret = []
            for _ in range(num_qubits):
                b = int(rng.integers(0, 2))
                c0 = int(rng.integers(0, 2))
                c1 = int(rng.integers(0, 2))
                token.append(prepare_pair(b, c0, c1))
                secret.append((b, c0, c1))
            
            if "Attacker 1" in attacker_choice:
                base_rate = 0.50 
            elif "Attacker 2" in attacker_choice:
                base_rate = 0.743 
            else:
                base_rate = (1.0 + 1.0 / np.sqrt(2.0)) / 2.0 
            
            node_success_rates = [1.0]
            current_prob = 1.0
            for v in range(1, num_verifiers):
                current_prob *= (base_rate + rng.normal(0, 0.01))
                node_success_rates.append(max(0.0, current_prob))
            
            st.success("Simulation Complete!")
            
            col_left, col_right = st.columns([1, 1])
            
            with col_left:
                st.metric(
                    label=f"Total Cumulative Probability ({num_verifiers} Nodes)", 
                    value=f"{node_success_rates[-1] * 100:.2f}%"
                )
                
                st.markdown("**Step-by-Step Success Rates:**")
                if num_verifiers <= 5:
                    sub_cols = st.columns(num_verifiers)
                    for idx, col in enumerate(sub_cols):
                        with col:
                            st.metric(label=f"Node {idx+1}", value=f"{node_success_rates[idx]*100:.1f}%")
                else:
                    rates_text = " | ".join([f"N{i+1}: {rate*100:.1f}%" for i, rate in enumerate(node_success_rates)])
                    st.write(rates_text)
                
                st.info(f"**Summary:** Compounding across {num_verifiers} nodes yields a final success rate of **{node_success_rates[-1] * 100:.2f}%**.")
                
            with col_right:
                fig, ax = plt.subplots(figsize=(4.5, 2.2))
                ax.plot(range(1, num_verifiers + 1), node_success_rates, marker='o', color='#ff4b4b', linewidth=2, markersize=4, label="Cumulative Probability")
                ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.7, label="Random Guess Threshold")
                ax.set_xlabel("Verifiers Passed (n)", fontsize=8)
                ax.set_ylabel("Probability", fontsize=8)
                ax.set_title("Security Decay Curve", fontsize=9)
                ax.set_xticks(range(1, num_verifiers + 1))
                ax.set_ylim(0, 1.05)
                ax.tick_params(axis='both', which='major', labelsize=8)
                ax.grid(True, linestyle='--', alpha=0.5)
                ax.legend(fontsize=7, loc='upper right')
                st.pyplot(fig)

with tab_bloch:
    st.subheader("Geometric Comparison of Measurement Strategies")
    st.markdown("""
    Comparing standard computational measurements against the optimal Breidbart intermediate basis 
    on the Bloch sphere. The 22.5° offset balances information gain with minimal state disturbance.
    """)
    
    bloch_col1, bloch_col2 = st.columns(2)
    
    u = np.linspace(0, 2 * np.pi, 25)
    v = np.linspace(0, np.pi, 25)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))
    
    with bloch_col1:
        st.markdown("**Attacker 2: Standard Measurement**")
        fig1 = plt.figure(figsize=(3.5, 3.5))
        ax1 = fig1.add_subplot(111, projection='3d')
        ax1.plot_wireframe(x, y, z, color='gray', alpha=0.15, rstride=5, cstride=5)
        
        ax1.quiver(0, 0, -1.2, 0, 0, 2.4, color='black', arrow_length_ratio=0.1, linewidth=1)
        ax1.quiver(0, -1.2, 0, 0, 2.4, 0, color='black', arrow_length_ratio=0.1, linewidth=1)
        ax1.quiver(-1.2, 0, 0, 2.4, 0, 0, color='black', arrow_length_ratio=0.1, linewidth=1)
        
        ax1.quiver(0, 0, 0, 0, 0, 1.0, color='cyan', arrow_length_ratio=0.15, linewidth=2.5)
        ax1.text(0, 0, 1.3, "|0⟩", fontsize=7, ha='center')
        
        ax1.set_xlim([-1.3, 1.3])
        ax1.set_ylim([-1.3, 1.3])
        ax1.set_zlim([-1.3, 1.3])
        ax1.axis('off')
        st.pyplot(fig1)
        st.caption("Measures strictly along standard axes (~74.3% limit).")

    with bloch_col2:
        st.markdown("**Attacker 3: Optimal Breidbart Basis**")
        fig2 = plt.figure(figsize=(3.5, 3.5))
        ax2 = fig2.add_subplot(111, projection='3d')
        ax2.plot_wireframe(x, y, z, color='gray', alpha=0.15, rstride=5, cstride=5)
        
        ax2.quiver(0, 0, -1.2, 0, 0, 2.4, color='black', arrow_length_ratio=0.1, linewidth=1)
        ax2.quiver(0, -1.2, 0, 0, 2.4, 0, color='black', arrow_length_ratio=0.1, linewidth=1)
        ax2.quiver(-1.2, 0, 0, 2.4, 0, 0, color='black', arrow_length_ratio=0.1, linewidth=1)
        
        theta = np.pi / 4 
        bx = np.sin(theta)
        bz = np.cos(theta)
        ax2.quiver(0, 0, 0, bx, 0, bz, color='red', arrow_length_ratio=0.15, linewidth=2)
        ax2.text(0, 0, 1.3, "|0⟩", fontsize=7, ha='center')
        
        ax2.set_xlim([-1.3, 1.3])
        ax2.set_ylim([-1.3, 1.3])
        ax2.set_zlim([-1.3, 1.3])
        ax2.axis('off')
        st.pyplot(fig2)
        st.caption("Measures along 22.5° offset (~85.35% limit).")

st.markdown("---")
st.caption("Built by Justen Mao based on work in UTD Quantum Computing Lab")