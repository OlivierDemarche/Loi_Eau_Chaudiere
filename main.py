import matplotlib.pyplot as plt
import numpy as np

# -------------------------------------------------------------
# ------------ PARAMETRES CHAUDIERE ET LOI D'EAU --------------
# -------------------------------------------------------------
PUISSANCE_NOM = 63.5
PUISSANCE_MIN = 12.2
T_EXT_BASE = -9
T_EXT_NON_CHAUFFAGE = 19
T_EAU_MIN_CHAUDIERE = 24
T_EAU_MAX_CHAUDIERE = 60
POINT_PIVOT_T_EXT = 20
POINT_PIVOT_T_MIN = 20

# Génération des valeurs X (température extérieure)
X = np.arange(T_EXT_BASE, T_EXT_NON_CHAUFFAGE + 1, 1)

# -------------------------------------------------------------
# ------------------ PARAMETRES POUR ANALYSE ------------------
# -------------------------------------------------------------
'''ENTRER ICI LA TEMPERATURE EXTERIEUR POUR CALCULER LA TEMPERATURE DE DEPART ET LA PUISSANCE ESTIMEE'''
temperature_exterieur = 30


# -------------------------------------------------------------
# -------------------------- FONCTIONS ------------------------
# -------------------------------------------------------------


# Calculs des paramètres de la loi d'eau (pente et deplacement) : relation entre température extérieur et température de départ
def loi_eau_t_depart_text():
    pente_temp_eau = (T_EAU_MAX_CHAUDIERE - T_EAU_MIN_CHAUDIERE) / (T_EXT_BASE - T_EXT_NON_CHAUFFAGE)
    depla_parallele = T_EAU_MIN_CHAUDIERE - (
                POINT_PIVOT_T_MIN + ((POINT_PIVOT_T_EXT - T_EXT_NON_CHAUFFAGE) * -pente_temp_eau))
    # Calcul de l'ordonnée à l'origine (b) en utilisant l'équation de droite (Y = mX + b)
    ordonnee_origine = T_EAU_MIN_CHAUDIERE - pente_temp_eau * T_EXT_NON_CHAUFFAGE
    # Calcul des valeurs Y (température de l'eau) en utilisant l'équation de droite (Température d'eau)
    y_temp_eau = pente_temp_eau * X + ordonnee_origine  # équation a)
    return -pente_temp_eau, depla_parallele, ordonnee_origine, y_temp_eau


# Calculs des paramètres de la loi d'eau (pente et ordonnée à l'origine) : relation entre température extérieur et puissance
# Hypothèse de linéarité dans l'évolution de la puissance pour l'estimation
def loi_eau_t_ext_puissance():
    pente_p = (PUISSANCE_NOM - PUISSANCE_MIN) / (T_EXT_BASE - T_EXT_NON_CHAUFFAGE)
    # Calcul de l'ordonnée à l'origine (b) en utilisant l'équation de droite (Y = mX + b)
    b_puissance = PUISSANCE_MIN - pente_p * T_EXT_NON_CHAUFFAGE
    # Calcul des valeurs Y (puissance) en utilisant l'équation de droite (Puissance)
    y = pente_p * X + b_puissance  # équation b)
    return pente_p, b_puissance, y


def tracer_graphique(y_temp_eau, P):  # Créer une figure 3D
    fig = plt.figure(figsize=(14, 7), dpi=100)
    ax = fig.add_subplot(111, projection='3d')
    # Tracer le graphique 3D
    ax.plot(X, y_temp_eau, P, label='Évolution de la puissance avec la température de l\'eau', color="crimson")

    ax.set_xlabel('Température extérieure (°C)')
    ax.set_ylabel('Température de l\'eau (°C)')
    ax.set_zlabel('Puissance')
    ax.invert_xaxis()
    ax.set_title('Évolution de la puissance et de la température de l\'eau en fonction de la température extérieure')
    plt.tight_layout()
    fig.savefig("figures/3D_Chaudiere")

    fig2 = plt.figure(2, figsize=(14, 7), dpi=100)
    plt.plot(X, y_temp_eau, label='Relation linéaire', color="crimson")
    plt.xlabel('Température extérieure (°C)')
    plt.gca().invert_xaxis()
    plt.ylabel('Température de l\'eau (°C)')
    plt.title('Relation entre température extérieure et température de départ de l\'eau')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.xticks(np.arange(T_EXT_BASE, T_EXT_NON_CHAUFFAGE + 1, 1))
    plt.yticks(np.arange(20, T_EAU_MAX_CHAUDIERE + 1, 5))
    fig2.savefig("figures/Relation_Text_Tdépart")

    fig3 = plt.figure(3, figsize=(14, 7), dpi=100)
    plt.plot(X, P, label='Relation linéaire', color="crimson")
    plt.xlabel('Température extérieure (°C)')
    plt.gca().invert_xaxis()
    plt.ylabel('Puissance [kW]')
    plt.title('Relation entre température extérieure et Puissance')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.xticks(np.arange(T_EXT_BASE, T_EXT_NON_CHAUFFAGE + 1, 1))
    plt.yticks(np.arange(10, 65 + 1, 5))
    fig3.savefig("figures/Relation_Text_Puissance")

    fig4 = plt.figure(4, figsize=(14, 7), dpi=100)
    plt.plot(y_temp_eau, P, label='Relation linéaire', color="crimson")
    plt.xlabel('Température de départ (°C)')
    plt.ylabel('Puissance [kW]')
    plt.title('Relation entre température de départ et Puissance')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.xticks(np.arange(20, T_EAU_MAX_CHAUDIERE + 1, 5))
    plt.yticks(np.arange(10, 65 + 1, 5))
    fig4.savefig("figures/Relation_Tdepart_Puissance")


def calculer_puissance(pente_p, ordonnee_temp, pente_temp, ordonnee_p, temperature_depart_eau):
    puissance_calculee = pente_p * ((
                                                -ordonnee_temp + temperature_depart_eau) / -pente_temp) + ordonnee_p  # trouvée à partir d'une résolution du système d'équation a) et b)
    return puissance_calculee


def calculer_t_depart(pente_temp, ordonnee_temp, temperature_ext):
    temp_depart = -pente_temp * temperature_ext + ordonnee_temp
    if temp_depart > T_EAU_MAX_CHAUDIERE:
        result = T_EAU_MAX_CHAUDIERE
    elif temp_depart < T_EAU_MIN_CHAUDIERE:
        result = T_EAU_MIN_CHAUDIERE
    else:
        result = temp_depart
    return result


# -------------------------- MAIN ------------------------------
if __name__ == "__main__":
    pente_t, deplacement_para_t, ordonnee_t, equation = loi_eau_t_depart_text()
    pente_puissance, ordonnee_puissance, equation_puissance = loi_eau_t_ext_puissance()
    temperature_depart_calculee = calculer_t_depart(temperature_ext=temperature_exterieur,
                                                    pente_temp=pente_t,
                                                    ordonnee_temp=ordonnee_t)
    puissance_fct_t_depart = calculer_puissance(temperature_depart_eau=temperature_depart_calculee,
                                                pente_p=pente_puissance,
                                                pente_temp=pente_t,
                                                ordonnee_temp=ordonnee_t,
                                                ordonnee_p=ordonnee_puissance)
    print("--------------------------------------------------------------")
    print("Température de départ calculée à l'aide de la loi d'eau : \n")
    print(f"Température extérieure [°C] : {temperature_exterieur} ")
    print(f"Température de départ [°C] : {temperature_depart_calculee} ")
    print("--------------------------------------------------------------")
    print(f"Puissance estimée de fonctionnement à {temperature_exterieur} °C : \n")
    print(f"Puissance nominale de la chaudière [kW] : {PUISSANCE_NOM} ")
    print(f"Puissance de fonctionnement de la chaudière [kW] : {puissance_fct_t_depart} ")
