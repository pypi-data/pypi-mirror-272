import ezkl

class ZKProof:
    def __init__(self):
        self.ezkl = ezkl.EZKL()

    def generate_proof(self, statement, witness):
        proof = self.ezkl.generate_proof(statement, witness)
        return proof

    def verify_proof(self, proof, statement):
        verified = self.ezkl.verify_proof(proof, statement)
        return verified
