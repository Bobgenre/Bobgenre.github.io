def rotation_image(matrice):
    """
    Fonction principale pour tourner une image (matrice) carrée de 90° 
    dans le sens horaire.
    Précondition : La taille de la matrice doit être une puissance de 2.
    """
    n = len(matrice)
    rotation_recursive(matrice, 0, 0, n)

def rotation_recursive(matrice, x, y, taille):
    """
    Fonction récursive appliquant le paradigme Diviser pour Régner.
    x, y : coordonnées du coin en haut à gauche du sous-quadrant actuel.
    taille : la taille (côté) du sous-quadrant à traiter.
    """
    # 1. CAS DE BASE : Un pixel seul (1x1) est déjà tourné.
    if taille <= 1:
        return
    
    # 2. DIVISER : On calcule la taille des 4 sous-quadrants
    k = taille // 2
    
    # 3. RÉGNER : On tourne récursivement les 4 quadrants sur eux-mêmes
    rotation_recursive(matrice, x, y, k)             # Quadrant Haut-Gauche
    rotation_recursive(matrice, x, y + k, k)         # Quadrant Haut-Droit
    rotation_recursive(matrice, x + k, y, k)         # Quadrant Bas-Gauche
    rotation_recursive(matrice, x + k, y + k, k)     # Quadrant Bas-Droit
    
    # 4. COMBINER : Permutation circulaire des 4 quadrants
    # On déplace les blocs entiers : Haut-Gauche -> Haut-Droit -> Bas-Droit -> Bas-Gauche -> Haut-Gauche
    for i in range(k):
        for j in range(k):
            # On sauvegarde le pixel du quadrant Haut-Gauche
            temp = matrice[x + i][y + j]
            
            # Le Haut-Gauche reçoit la valeur du Bas-Gauche
            matrice[x + i][y + j] = matrice[x + k + i][y + j]
            
            # Le Bas-Gauche reçoit la valeur du Bas-Droit
            matrice[x + k + i][y + j] = matrice[x + k + i][y + k + j]
            
            # Le Bas-Droit reçoit la valeur du Haut-Droit
            matrice[x + k + i][y + k + j] = matrice[x + i][y + k + j]
            
            # Le Haut-Droit reçoit l'ancienne valeur du Haut-Gauche (sauvegardée)
            matrice[x + i][y + k + j] = temp


# ==========================================
# PARTIE TESTS 
# ==========================================

def afficher_matrice(matrice):
    for ligne in matrice:
        print(" ".join(f"{val:2}" for val in ligne))
    print()

if __name__ == "__main__":
    # Test avec une image matricielle 4x4
    image_test = [
        ["A", "B", "C", "D"],
        ["E", "F", "G", "H"],
        ["I", "J", "K", "L"],
        ["M", "N", "O", "P"]
    ]
    
    afficher_matrice(image_test)
    
    # Appel de la fonction
    rotation_image(image_test)
    
    afficher_matrice(image_test)