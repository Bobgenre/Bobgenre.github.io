def rotation_image(matrice):
    """
    Fonction principale pour tourner une image (matrice) carrée de 90° 
    dans le sens horaire.
    Précondition : La taille de la matrice doit être une puissance de 2.
    """
    pass

def rotation_recursive(matrice, x, y, taille):
    """
    Fonction récursive appliquant le paradigme Diviser pour Régner.
    x, y : coordonnées du coin en haut à gauche du sous-quadrant actuel.
    taille : la taille (côté) du sous-quadrant à traiter.
    """
    # 1. CAS DE BASE : Un pixel seul (1x1) est déjà tourné.
    
    
    # 2. DIVISER : On calcule la taille des 4 sous-quadrants
    
    
    # 3. RÉGNER : On tourne récursivement les 4 quadrants sur eux-mêmes
    
    
    # 4. COMBINER : Permutation circulaire des 4 quadrants
    pass


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