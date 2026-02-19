# tp-igl-refactoring-swarm

Projet de TP (IGL = *Introduction au Génie Logiciel*) : une **“swarm” d’agents** qui tente de **corriger / refactoriser automatiquement** un fichier Python en bouclant sur :

1. **Auditor** : analyse statique (Pylint) + plan de correction via LLM
2. **Fixer** : applique les corrections (LLM) et met à jour le code
3. **Judge** : génère des tests Pytest (LLM), exécute Pytest et décide PASS/FAIL

Le workflow est orchestré avec **LangGraph** et les interactions sont journalisées dans `logs/experiment_data.json`.

---

## Pré-requis

- Python **3.10** ou **3.11**
- Une clé API Google Gemini (variable `GOOGLE_API_KEY`)

> Remarque : le projet est actuellement configuré pour **Gemini** via `langchain-google-genai`.

---

## Installation

```bash
python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

---

## Configuration (.env)

Créer un fichier `.env` à la racine :

```bash
GOOGLE_API_KEY=...votre_cle...
```

Le chargement se fait via `python-dotenv` (voir `src/llm.py`).

### Sanity check

```bash
python check_setup.py
```

---

## Exécution

Le point d’entrée est `main.py`. Il attend un dossier contenant du code Python “buggy”.
Le script prend le **premier** fichier `*.py` du dossier qui **n’est pas** un fichier de test (exclut les `test_*.py`).

Exemple avec le dataset fourni :

```bash
python main.py --target_dir src/test_dataset
```

À la fin :

- si succès : le fichier cible a été **réécrit sur disque**
- quoi qu’il arrive : des traces sont écrites dans `logs/experiment_data.json`

---

## Comment ça marche (résumé)

- **Sandbox (nécessaire / configurable)** : les opérations “tool” (Pylint / Pytest) s’exécutent sur des fichiers écrits dans un dossier de travail isolé géré par `src/tools.py`.
  - Par défaut : `./sandbox` (auto-créé si absent).
  - Pour choisir l’emplacement : définir `SWARM_SANDBOX_DIR` (ex: `SWARM_SANDBOX_DIR=/tmp/my_sandbox`).
  - Couche de sécurité anti path traversal : accès limité au dossier sandbox choisi.
- **Boucle LangGraph** : `main.py` construit un graphe `Auditor → Fixer → Judge`.
  - Si les tests échouent, on reboucle sur **Fixer**.
  - Stop si succès ou si `iterations >= 10`.

---

## Logs (données “scientifiques”)

Les agents enregistrent leurs prompts/réponses et sorties d’outils via `src/utils/logger.py` dans :

- `logs/experiment_data.json`

Chaque entrée contient notamment : timestamp, agent, modèle, action, détails (`input_prompt`, `output_response`), statut.

---

## Tests du projet

Les tests du projet (pas ceux générés par le Judge) sont dans `tests/`.

```bash
pytest
```

---

## Structure du dépôt

- `main.py` : orchestration LangGraph (swarm)
- `src/llm.py` : configuration du LLM (Gemini) + chargement `.env`
- `src/state.py` : état partagé entre agents (`SwarmState`)
- `src/agents/` : `auditor.py`, `fixer.py`, `judge.py`
- `src/prompts/` : prompts système pour chaque agent
- `src/tools.py` : outils (Pylint, Pytest, IO) confinés au dossier sandbox (configurable)
- `src/test_dataset/` : exemples de cas “buggy” (données de TP)
- `logs/` : journalisation des expériences
- `sandbox/` : zone d’exécution par défaut (requise) pour les outils et les tests générés (peut être remplacée via `SWARM_SANDBOX_DIR`)

---

## Dépannage

- **`GOOGLE_API_KEY missing in .env`** : ajouter `GOOGLE_API_KEY` dans `.env` (racine du projet).
- **Quota / erreurs Gemini** : `main.py` applique un throttling (pause de 5s entre appels) pour réduire les crashes sur free tier.
- **Pylint/Pytest timeout** : les tools utilisent un `timeout=30` secondes (voir `src/tools.py`).

---

## Changer de modèle

Le modèle est défini dans `src/llm.py` (actuellement `models/gemini-2.5-flash`).
Vous pouvez modifier `model=...` et/ou la configuration LangChain selon vos besoins.

