import pytest
from src.prompts.auditor_prompt import generate_audit_prompt, AUDITOR_SYSTEM_PROMPT
from src.prompts.fixer_prompt import generate_fixer_prompt, FIXER_SYSTEM_PROMPT
from src.prompts.judge_prompt import generate_judge_prompt, JUDGE_SYSTEM_PROMPT


class TestAuditorPrompt:
    """Tests pour le prompt de l'Auditor"""
    
    def test_auditor_prompt_contains_instructions(self):
        """Vérifie que le prompt contient les instructions clés"""
        assert "analyze" in AUDITOR_SYSTEM_PROMPT.lower() or "analyse" in AUDITOR_SYSTEM_PROMPT.lower()
        assert "json" in AUDITOR_SYSTEM_PROMPT.lower()
        assert "bug" in AUDITOR_SYSTEM_PROMPT.lower()
    
    def test_auditor_prompt_generation(self):
        """Vérifie que la génération du prompt fonctionne"""
        code = "def test(): pass"
        prompt = generate_audit_prompt(code)
        
        assert code in prompt
        assert len(prompt) > 100  # Le prompt doit être substantiel
    
    def test_auditor_prompt_has_output_format(self):
        """Vérifie que le format de sortie est spécifié"""
        assert "output" in AUDITOR_SYSTEM_PROMPT.lower()
        assert "{" in AUDITOR_SYSTEM_PROMPT  # Présence d'exemple JSON


class TestFixerPrompt:
    """Tests pour le prompt du Fixer"""
    
    def test_fixer_prompt_contains_instructions(self):
        """Vérifie que le prompt contient les instructions clés"""
        assert "fix" in FIXER_SYSTEM_PROMPT.lower() or "correct" in FIXER_SYSTEM_PROMPT.lower()
        assert "code" in FIXER_SYSTEM_PROMPT.lower()
    
    def test_fixer_prompt_generation(self):
        """Vérifie que la génération du prompt fonctionne"""
        code = "def buggy(): return 1/0"
        audit = '{"issues": [{"type": "BUG", "description": "Division by zero"}]}'
        
        prompt = generate_fixer_prompt(code, audit)
        
        assert code in prompt
        assert audit in prompt
        assert len(prompt) > 100
    
    def test_fixer_prompt_warns_against_truncation(self):
        """Vérifie que le prompt interdit les placeholders"""
        assert "do not" in FIXER_SYSTEM_PROMPT.lower() or "don't" in FIXER_SYSTEM_PROMPT.lower()
        # Recherche de mots-clés liés à la complétude du code
        full_code_keywords = ["full", "complete", "entire", "complet"]
        assert any(keyword in FIXER_SYSTEM_PROMPT.lower() for keyword in full_code_keywords)


class TestJudgePrompt:
    """Tests pour le prompt du Judge (s'il utilise un LLM)"""
    
    def test_judge_prompt_contains_test_instructions(self):
        """Vérifie que le prompt contient les instructions de test"""
        assert "test" in JUDGE_SYSTEM_PROMPT.lower()
        assert "pytest" in JUDGE_SYSTEM_PROMPT.lower()
    
    def test_judge_prompt_generation(self):
        """Vérifie que la génération du prompt fonctionne"""
        code = "def add(a, b): return a + b"
        filename = "math.py"
        
        prompt = generate_judge_prompt(code, filename)
        
        assert code in prompt
        assert "math" in prompt  # Le nom du fichier (sans .py) doit apparaître
        assert len(prompt) > 50


class TestPromptConsistency:
    """Tests de cohérence entre les prompts"""
    
    def test_all_prompts_use_markdown_blocks(self):
          """Vérifie que tous les prompts mentionnent le format markdown"""
         # Le Fixer et le Judge doivent demander du code en markdown
          assert "```" in FIXER_SYSTEM_PROMPT or "markdown" in FIXER_SYSTEM_PROMPT.lower()
    # Judge : on vérifie juste qu'il demande un "code block"
    assert "code block" in JUDGE_SYSTEM_PROMPT.lower() or "```" in JUDGE_SYSTEM_PROMPT or "markdown" in JUDGE_SYSTEM_PROMPT.lower()
    
    def test_prompts_are_not_empty(self):
        """Vérifie qu'aucun prompt n'est vide"""
        assert len(AUDITOR_SYSTEM_PROMPT) > 50
        assert len(FIXER_SYSTEM_PROMPT) > 50
        assert len(JUDGE_SYSTEM_PROMPT) > 50
    
    def test_prompts_specify_role(self):
        """Vérifie que chaque prompt définit un rôle clair"""
        assert "auditor" in AUDITOR_SYSTEM_PROMPT.lower() or "analyze" in AUDITOR_SYSTEM_PROMPT.lower()
        assert "fixer" in FIXER_SYSTEM_PROMPT.lower() or "refactor" in FIXER_SYSTEM_PROMPT.lower()
        assert "judge" in JUDGE_SYSTEM_PROMPT.lower() or "test" in JUDGE_SYSTEM_PROMPT.lower()


class TestPromptSecurity:
    """Tests de sécurité des prompts"""
    
    def test_no_dangerous_instructions(self):
        """Vérifie qu'aucun prompt ne contient d'instructions dangereuses"""
        dangerous_keywords = ["os.system", "subprocess", "eval(", "exec(", "rm -rf"]
        
        all_prompts = [AUDITOR_SYSTEM_PROMPT, FIXER_SYSTEM_PROMPT, JUDGE_SYSTEM_PROMPT]
        
        for prompt in all_prompts:
            for keyword in dangerous_keywords:
                assert keyword not in prompt, f"Prompt contient '{keyword}' - risque de sécurité!"
    
    def test_prompts_limit_scope(self):
        """Vérifie que les prompts limitent le scope des agents"""
        # L'Auditor ne doit PAS fixer
        assert "do not fix" in AUDITOR_SYSTEM_PROMPT.lower() or "don't fix" in AUDITOR_SYSTEM_PROMPT.lower()


@pytest.mark.integration
class TestPromptIntegration:
    """Tests d'intégration des prompts avec le LLM"""
    
    def test_auditor_prompt_with_real_code(self):
        """Test avec du vrai code buggé"""
        buggy_code = """
def divide(a, b):
    return a / b

result = divide(10, 0)
"""
        prompt = generate_audit_prompt(buggy_code)
        
        # Le prompt doit inclure le code
        assert "divide" in prompt
        assert "10, 0" in prompt
    
    def test_fixer_prompt_with_audit_result(self):
        """Test avec un résultat d'audit réel"""
        code = "def f(): return 1/0"
        audit = """
{
    "criticality": "HIGH",
    "issues": [
        {
            "line": 1,
            "type": "BUG",
            "description": "Division by zero",
            "suggestion": "Add zero check"
        }
    ]
}
"""
        prompt = generate_fixer_prompt(code, audit)
        
        assert "Division by zero" in prompt
        assert "1/0" in prompt