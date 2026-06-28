def fusion(gauche, droite):
    """Fusionne deux listes triées en une seule liste triée."""
    resultat = []
    i, j = 0, 0
    
    # On compare les elements des deux listes
    while i < len(gauche) and j < len(droite):
        if gauche[i] <= droite[j]:
            resultat.append(gauche[i])
            i += 1
        else:
            resultat.append(droite[j])
            j += 1
            
    # On ajoute les elements restants (s'il y en a)
    for k in range(i, len(gauche)):
        resultat.append(gauche[k])

    for k in range(j, len(droite)):
        resultat.append(droite[k])

    return resultat

def tri_fusion(liste):
    """Trie une liste en utilisant le paradigme Diviser pour Regner."""
    # Cas de base : une liste de taille 0 ou 1 est deja triee
    if len(liste) <= 1:
        return liste
    
    # DIVISER : On coupe la liste en deux
    milieu = len(liste) // 2

    # On construit la sous-liste gauche 
    gauche = []
    for k in range(0, milieu):
        gauche.append(liste[k])
        
    # On construit la sous-liste droite
    droite = []
    for k in range(milieu, len(liste)):
        droite.append(liste[k])
    
    # REGNER : Appels recursifs
    gauche_triee = tri_fusion(gauche)
    droite_triee = tri_fusion(droite)
    
    # COMBINER : On fusionne les resultats
    return fusion(gauche_triee, droite_triee)


# ==========================================
# PARTIE TESTS
# ==========================================

if __name__ == "__main__":
    liste_test = [38, 27, 43, 3, 9, 82, 10]
    print(f"Liste originale : {liste_test}")
    
    liste_triee = tri_fusion(liste_test)
    print(f"Liste triée     : {liste_triee}")
    
    # Vérification robuste (Assertions)
    assert tri_fusion([]) == []
    assert tri_fusion([5]) == [5]
    assert tri_fusion([1, 2, 3, 4]) == [1, 2, 3, 4] # Déjà triée
    assert tri_fusion([4, 3, 2, 1]) == [1, 2, 3, 4] # Triée à l'envers
    
    print("Tous les tests sont passés avec succès !")