import subprocess
import sys
import json
from pathlib import Path
import time


def print_section(title: str):
    """Affiche une section formatée"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def check_structure():
    """Vérifie que la structure du projet est complète"""
    print_section("1. VÉRIFICATION DE LA STRUCTURE")
    
    required_files = [
        "main.py",
        ".env",
        "src/state.py",
        "src/llm.py",
        "src/agents/auditor.py",
        "src/agents/fixer.py",
        "src/agents/judge.py",
        "src/utils/logger.py",
        "src/utils/validate_logs.py",
    ]
    
    required_dirs = [
        "logs",
        "test_dataset",
        "tests",
    ]
    
    all_good = True
    
    # Vérifier les fichiers
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} MANQUANT")
            all_good = False
    
    # Vérifier les dossiers
    for directory in required_dirs:
        if Path(directory).exists():
            print(f"✅ {directory}/")
        else:
            print(f"❌ {directory}/ MANQUANT")
            all_good = False
    
    # Créer logs et sandbox s'ils n'existent pas
    Path("logs").mkdir(exist_ok=True)
    Path("sandbox").mkdir(exist_ok=True)
    
    return all_good


def check_test_dataset():
    """Vérifie que test_dataset contient des cas de test"""
    print_section("2. VÉRIFICATION DE VOTRE JEU DE DONNÉES")
    
   # Chercher test_dataset dans src/ si pas trouvé à la racine
test_dataset = Path("test_dataset")
if not test_dataset.exists():
    test_dataset = Path("src/test_dataset")
    # Chercher les cas de test
    cases = sorted([d for d in test_dataset.iterdir() if d.is_dir() and d.name.startswith("case_")])
    
    # Alternative : chercher des fichiers .py directement dans test_dataset/
    py_files_root = list(test_dataset.glob("*.py"))
    
    if cases:
        print(f"✅ {len(cases)} cas de test trouvés (structure case_*/) :")
        for case in cases:
            py_files = list(case.glob("*.py"))
            if py_files:
                print(f"   - {case.name}/")
                for py_file in py_files:
                    print(f"     └─ {py_file.name}")
            else:
                print(f"   ⚠️  {case.name}/ est vide")
        return True
    elif py_files_root:
        print(f"✅ {len(py_files_root)} fichiers Python trouvés directement dans test_dataset/ :")
        for py_file in py_files_root:
            print(f"   - {py_file.name}")
        return True
    else:
        print("⚠️  Aucun cas de test ou fichier Python trouvé dans test_dataset/")
        print("   Structure attendue :")
        print("   - test_dataset/case_1/*.py")
        print("   OU")
        print("   - test_dataset/*.py")
        return False


def run_unit_tests():
    """Lance les tests unitaires avec pytest"""
    print_section("3. TESTS UNITAIRES (pytest)")
    
    # Vérifier que pytest est installé
    try:
        result = subprocess.run(
            ["pytest", "--version"],
            capture_output=True,
            text=True
        )
        print(f"✅ pytest installé : {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ pytest n'est pas installé. Installez-le avec : pip install pytest")
        return False
    
    # Lancer les tests
    print("\nLancement des tests...")
    result = subprocess.run(
        ["pytest", "tests/", "-v", "--tb=short", "--maxfail=5"],
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    if result.returncode == 0:
        print("✅ Tous les tests unitaires passent")
        return True
    elif result.returncode == 5:
        print("⚠️  Aucun test trouvé dans tests/")
        return True
    else:
        print(f"⚠️  Certains tests ont échoué (exit code: {result.returncode})")
        return False


def test_on_dataset(test_path: Path, test_name: str):
    """Teste le système sur un cas ou fichier spécifique"""
    print(f"\n   Testing {test_name}...")
    
    try:
        result = subprocess.run(
            [sys.executable, "main.py", "--target_dir", str(test_path)],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print(f"   ✅ {test_name} - SUCCESS")
            return True
        else:
            print(f"   ❌ {test_name} - FAILED (exit code {result.returncode})")
            if result.stderr:
                print(f"      Error: {result.stderr[:200]}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"   ⏱️  {test_name} - TIMEOUT (>60s)")
        return False
    except Exception as e:
        print(f"   ❌ {test_name} - ERROR: {e}")
        return False


def run_integration_tests():
    """Lance le système sur tous les cas de votre test_dataset"""
    print_section("4. TESTS D'INTÉGRATION (votre test_dataset)")
    
    test_dataset = Path("test_dataset")
    if not test_dataset.exists():
        print("❌ test_dataset/ introuvable")
        return False
    
    # Chercher les cas de test (case_*/)
    cases = sorted([d for d in test_dataset.iterdir() if d.is_dir() and d.name.startswith("case_")])
    
    # Alternative : fichiers .py directement dans test_dataset/
    py_files_root = [f for f in test_dataset.glob("*.py") if not f.name.startswith("test_")]
    
    results = []
    
    if cases:
        print(f"📁 Mode : Dossiers case_*/ ({len(cases)} trouvés)")
        for case in cases:
            success = test_on_dataset(case, case.name)
            results.append((case.name, success))
            time.sleep(2)  # Délai entre les tests
    elif py_files_root:
        print(f"📄 Mode : Fichiers Python dans test_dataset/ ({len(py_files_root)} trouvés)")
        for py_file in py_files_root:
            success = test_on_dataset(test_dataset, f"test_dataset/{py_file.name}")
            results.append((py_file.name, success))
            time.sleep(2)
    else:
        print("❌ Aucun cas de test trouvé")
        return False
    
    # Résumé
    success_count = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\n📊 RÉSULTATS : {success_count}/{total} réussis ({success_count*100//total if total else 0}%)")
    
    return success_count > 0


def validate_logs():
    """Valide le format et le contenu des logs"""
    print_section("5. VALIDATION DES LOGS")
    
    log_file = Path("logs/experiment_data.json")
    
    if not log_file.exists():
        print("❌ Fichier logs/experiment_data.json introuvable")
        print("   Le système n'a peut-être pas encore été exécuté.")
        return False
    
    if log_file.stat().st_size == 0:
        print("❌ Le fichier de logs est vide")
        return False
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            print("❌ Le fichier de logs n'est pas une liste JSON")
            return False
        
        if len(data) == 0:
            print("⚠️  Le fichier de logs est vide (aucune action enregistrée)")
            return False
        
        print(f"✅ {len(data)} entrées de logs trouvées")
        
        # Validation stricte
        required_fields = ["agent", "model", "action", "details", "status", "timestamp"]
        required_details = ["input_prompt", "output_response"]
        
        errors = []
        warnings = []
        
        for i, entry in enumerate(data, 1):
            # Vérifier les champs obligatoires (accepter "agent" ou "agent_name")
            for field in required_fields:
                if field == "agent":
                    if "agent" not in entry and "agent_name" not in entry:
                        errors.append(f"Entrée {i} : champ 'agent' ou 'agent_name' manquant")
                elif field not in entry:
                    errors.append(f"Entrée {i} : champ '{field}' manquant")
            
            # Vérifier les details
            details = entry.get("details")
            if isinstance(details, dict):
                for detail in required_details:
                    if detail not in details:
                        warnings.append(f"Entrée {i} : '{detail}' manquant dans details")
                    elif not details[detail] or details[detail] == "":
                        warnings.append(f"Entrée {i} : '{detail}' est vide")
            else:
                errors.append(f"Entrée {i} : 'details' invalide ou manquant")
        
        if errors:
            print(f"\n❌ {len(errors)} ERREURS CRITIQUES :")
            for error in errors[:10]:  # Limiter l'affichage
                print(f"   - {error}")
            if len(errors) > 10:
                print(f"   ... et {len(errors)-10} autres erreurs")
            return False
        
        if warnings:
            print(f"\n⚠️  {len(warnings)} AVERTISSEMENTS :")
            for warning in warnings[:10]:
                print(f"   - {warning}")
            if len(warnings) > 10:
                print(f"   ... et {len(warnings)-10} autres avertissements")
        
        # Statistiques
        success_count = sum(1 for e in data if e.get("status") == "SUCCESS")
        failure_count = sum(1 for e in data if e.get("status") == "FAILURE")
        
        print(f"\n📊 STATISTIQUES :")
        print(f"   - Total d'entrées : {len(data)}")
        print(f"   - Succès : {success_count}")
        print(f"   - Échecs : {failure_count}")
        
        agents = set(e.get("agent") or e.get("agent_name", "Unknown") for e in data)
        print(f"   - Agents actifs : {', '.join(sorted(agents))}")
        
        # Vérifier que les prompts sont présents
        prompts_present = sum(1 for e in data if e.get("details", {}).get("input_prompt"))
        print(f"   - Entrées avec prompts : {prompts_present}/{len(data)}")
        
        if prompts_present == 0:
            print("   ⚠️  AUCUN prompt trouvé ! Vérifiez que log_experiment() est appelé correctement.")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Le fichier de logs contient du JSON invalide : {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur lors de la validation : {e}")
        return False


def main():
    """Point d'entrée principal"""
    print("\n" + "🔬" * 35)
    print("  VALIDATION COMPLÈTE - THE REFACTORING SWARM")
    print("  (Utilise VOTRE test_dataset existant)")
    print("🔬" * 35)
    
    results = {
        "structure": check_structure(),
        "test_dataset": check_test_dataset(),
        "unit_tests": run_unit_tests(),
        "integration": run_integration_tests(),
        "logs": validate_logs(),
    }
    
    # Résumé final
    print_section("RÉSUMÉ FINAL")
    
    for check, passed in results.items():
        status = "✅" if passed else "❌"
        print(f"{status} {check.upper().replace('_', ' ')}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 70)
    if all_passed:
        print("🏆 TOUS LES TESTS SONT PASSÉS ! Votre système est prêt.")
        print("\n📝 Prochaines étapes :")
        print("   1. Documentez vos résultats dans un README")
        print("   2. Committez régulièrement (1 commit/jour minimum)")
        print("   3. Vérifiez que logs/experiment_data.json est complet")
        return 0
    else:
        print("⚠️  CERTAINS TESTS ONT ÉCHOUÉ. Corrigez les erreurs ci-dessus.")
        print("\n💡 Conseils :")
        if not results["structure"]:
            print("   - Vérifiez que tous les fichiers requis existent")
        if not results["test_dataset"]:
            print("   - Assurez-vous que test_dataset/ contient des fichiers .py")
        if not results["unit_tests"]:
            print("   - Corrigez les erreurs dans les tests pytest")
        if not results["integration"]:
            print("   - Vérifiez que main.py fonctionne correctement")
        if not results["logs"]:
            print("   - Assurez-vous que log_experiment() est appelé avec tous les paramètres")
        return 1


if __name__ == "__main__":
    sys.exit(main())
