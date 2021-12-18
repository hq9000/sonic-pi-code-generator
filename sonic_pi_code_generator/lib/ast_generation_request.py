class ASTGenerationRequest:
    def __init__(self, complexity: float, reverb_amount: float):
        self._complexity: float = complexity
        self._reverb_amount: float = reverb_amount
