from src.sport import Sport


class Joueur:
    """Représente un joueur sportif, tous sports confondus.

    Parameters
    ----------
    nom : str
        Nom de famille ou nom complet du joueur.
    sport : str
        Nom du sport pratiqué.
    prenom : str, optional
        Prénom du joueur.
    pseudo : str, optional
        Pseudo en jeu, spécifique à l'e-sport.
    equipe : str, optional
        Nom de l'équipe ou du circuit (ex : "ATP").
    position : str, optional
        Poste ou rôle (ex : "Forward", "jungle").
    date_naissance : str, optional
        Date de naissance au format AAAA-MM-JJ.
    taille : float, optional
        Taille en centimètres.
    poids : float, optional
        Poids en kilogrammes.
    pays : str, optional
        Pays ou code pays du joueur.
    main : str, optional
        Main dominante, spécifique au tennis (ex : "R", "L").
    """

    def __init__(
        self,
        nom: str,
        sport: str,
        prenom: str | None = None,
        pseudo: str | None = None,
        equipe: str | None = None,
        position: str | None = None,
        date_naissance: str | None = None,
        taille: float | None = None,
        poids: float | None = None,
        pays: str | None = None,
        main: str | None = None,
        numero: int | None = None,
        lieu_naissance: str | None = None,
        equipes_historique: list | None = None,
    ):
        self.nom = nom
        self.sport = sport
        self.prenom = prenom
        self.pseudo = pseudo
        self.equipe = equipe
        self.position = position
        self.date_naissance = date_naissance
        self.taille = taille
        self.poids = poids
        self.pays = pays
        self.main = main
        self.numero = numero
        self.lieu_naissance = lieu_naissance
        self.equipes_historique = equipes_historique

    def __str__(self):
        parts = []
        if self.prenom:
            parts.append(f"{self.prenom} {self.nom}")
        elif self.pseudo:
            parts.append(f"{self.pseudo} ({self.nom})")
        else:
            parts.append(self.nom)

        if self.equipe:
            parts.append(f"| {self.equipe}")
        if self.pays:
            parts.append(f"| {self.pays}")
        if self.position:
            parts.append(f"| {self.position}")
        if self.taille:
            parts.append(f"| {self.taille} cm")
        if self.date_naissance:
            parts.append(f"| né(e) le {self.date_naissance}")

        return f"[{self.sport}] " + " ".join(parts)

    @staticmethod
    def run_menu(sport: Sport) -> None:
        """Affiche le menu interactif des joueurs pour un sport donné.

        Charge tous les joueurs une seule fois, puis boucle sur les requêtes
        jusqu'à ce que l'utilisateur choisisse de revenir.

        Parameters
        ----------
        sport : Sport
            Sport sélectionné par l'utilisateur.
        """
        from src.loader.JoueurLoader import JoueurLoader

        joueurs = JoueurLoader().load_all_joueurs(sport)
        print(f"  {len(joueurs)} joueurs chargés pour {sport.nom}.")

        while True:
            print("\n  ── Joueurs ─────────────────────────────────────")
            print("  1  Chercher un joueur par nom")
            if sport.nom in ("basketball", "LOL"):
                print("  2  Chercher les joueurs d'une équipe")
                print("  3  Chercher les joueurs par position")
            elif sport.nom == "volley":
                print("  2  Chercher les joueurs par pays")
                print("  3  Filtrer par genre  (Hommes / Femmes)")
            elif sport.nom == "tennis":
                print("  2  Chercher les joueurs par pays")
                print("  3  Filtrer par circuit  (ATP / WTA)")
            else:
                print("  2  Chercher les joueurs par pays")
            print("  4  Statistiques des joueurs")
            print("  0  Retour")

            choix = input("\n  Votre choix : ").strip()

            if choix == "0" or choix.lower() in ("retour", "q"):
                break
            elif choix == "1":
                Joueur._chercher_par_nom(joueurs)
            elif choix == "2":
                if sport.nom in ("basketball", "LOL"):
                    Joueur._chercher_par_equipe(joueurs)
                else:
                    Joueur._chercher_par_pays(joueurs)
            elif choix == "3":
                if sport.nom in ("basketball", "LOL"):
                    Joueur._chercher_par_position(joueurs)
                elif sport.nom == "volley":
                    genre = input("  Genre (Hommes / Femmes) : ").strip()
                    resultats = [
                        j
                        for j in joueurs
                        if j.equipe and genre.lower() in j.equipe.lower()
                    ]
                    Joueur._afficher(resultats)
                elif sport.nom == "tennis":
                    circuit = input("  Circuit (ATP / WTA) : ").strip().upper()
                    resultats = [j for j in joueurs if j.equipe == circuit]
                    Joueur._afficher(resultats)
                else:
                    print("  Option non disponible pour ce sport.")
            elif choix == "4":
                from src.loader.JoueurLoader import JoueurLoader

                JoueurLoader().afficher_stats(joueurs, sport)
            else:
                print("  Choix invalide.")

    @staticmethod
    def _chercher_par_nom(joueurs: list) -> None:
        nom = input("  Nom du joueur : ").strip()
        resultats = [
            j
            for j in joueurs
            if nom.lower() in j.nom.lower()
            or (j.prenom and nom.lower() in j.prenom.lower())
            or (j.pseudo and nom.lower() in j.pseudo.lower())
        ]
        print(f"\n  {len(resultats)} résultat(s) :\n")
        for j in resultats[:10]:
            Joueur._afficher_fiche_detail(j)
        if len(resultats) > 10:
            print(
                f"  ... ({len(resultats) - 10} résultats supplémentaires non affichés)"
            )

    @staticmethod
    def _afficher_fiche_detail(j: "Joueur") -> None:
        from datetime import date as _date

        sep = "  " + "─" * 46

        def _age(dob_str):
            try:
                dob = _date.fromisoformat(dob_str[:10])
                today = _date.today()
                return (
                    today.year
                    - dob.year
                    - ((today.month, today.day) < (dob.month, dob.day))
                )
            except Exception:
                return None

        def ligne(label, valeur):
            print(f"  {label:<18}: {valeur}")

        print(sep)
        if j.prenom:
            ligne("Joueur", f"{j.prenom} {j.nom}")
        elif j.pseudo:
            ligne("Pseudo", j.pseudo)
            ligne("Nom réel", j.nom)
        else:
            ligne("Joueur", j.nom)

        if j.position:
            ligne("Poste", j.position)
        if j.equipe:
            ligne("Équipe actuelle", j.equipe)
        if j.equipes_historique:
            ligne("Équipes", ", ".join(j.equipes_historique))
        if j.pays:
            ligne("Pays", j.pays)
        if j.lieu_naissance:
            ligne("Lieu de naissance", j.lieu_naissance)
        if j.date_naissance:
            age = _age(j.date_naissance)
            age_str = f"  ({age} ans)" if age else ""
            ligne("Naissance", f"{j.date_naissance}{age_str}")
        if j.taille:
            ligne("Taille", f"{j.taille:.0f} cm")
        if j.poids:
            ligne("Poids", f"{j.poids:.1f} kg")
        if j.main:
            labels = {"R": "Droitier(ère)", "L": "Gaucher(ère)", "U": "Ambidextre"}
            ligne("Main dominante", labels.get(j.main, j.main))
        if j.numero is not None:
            ligne("Numéro maillot", f"#{j.numero}")
        print(sep)

    @staticmethod
    def _chercher_par_equipe(joueurs: list) -> None:
        """Filtre et affiche les joueurs appartenant à une équipe saisie.

        Parameters
        ----------
        joueurs : list
            Liste de Joueur à filtrer.
        """
        equipe = input("  Nom de l'équipe : ").strip()
        resultats = [
            j for j in joueurs if j.equipe and equipe.lower() in j.equipe.lower()
        ]
        Joueur._afficher(resultats)

    @staticmethod
    def _chercher_par_position(joueurs: list) -> None:
        """Filtre et affiche les joueurs occupant une position saisie.

        Parameters
        ----------
        joueurs : list
            Liste de Joueur à filtrer.
        """
        position = input("  Position (ex: Forward, top, jungle...) : ").strip()
        resultats = [
            j for j in joueurs if j.position and position.lower() in j.position.lower()
        ]
        Joueur._afficher(resultats)

    @staticmethod
    def _chercher_par_pays(joueurs: list) -> None:
        """Filtre et affiche les joueurs originaires d'un pays saisi.

        Parameters
        ----------
        joueurs : list
            Liste de Joueur à filtrer.
        """
        pays = input("  Pays : ").strip()
        resultats = [j for j in joueurs if j.pays and pays.lower() in j.pays.lower()]
        Joueur._afficher(resultats)

    @staticmethod
    def _afficher(resultats: list, limite: int = 20) -> None:
        """Affiche une liste de joueurs avec une limite optionnelle.

        Parameters
        ----------
        resultats : list
            Liste de Joueur à afficher.
        limite : int, optional
            Nombre maximum de résultats affichés (par défaut 20).
        """
        print(f"\n  {len(resultats)} résultat(s) :\n")
        for j in resultats[:limite]:
            print(f"  {j}")
        if len(resultats) > limite:
            print(
                f"  ... ({len(resultats) - limite} résultats supplémentaires non affichés)"
            )
